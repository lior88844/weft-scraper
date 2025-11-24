#!/usr/bin/env python3
"""
Weft MCP Server
Enables browsing and ordering from Weft stores via ChatGPT
"""

import os
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP, Context
from mcp import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

PORT = int(os.getenv("PORT", "8547"))

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
STORES_DIR = PROJECT_ROOT / "stores"
WIDGET_DIR = Path(__file__).parent / "web" / "dist"
WIDGET_MIME_TYPE = "text/html+skybridge"
PRODUCTS_WIDGET_URI = "ui://widget/products.html"

# In-memory cart storage: {session_id: {product_key: {product, quantity}}}
user_carts = {}

# Initialize MCP server
mcp = FastMCP("Weft Store", port=PORT, host="0.0.0.0", stateless_http=True)


def load_store_products(store_name: str) -> List[Dict]:
    """Load products from a specific store's JSON file"""
    store_path = STORES_DIR / store_name / "data" / "products.json"
    
    if not store_path.exists():
        logger.error(f"Store data not found: {store_path}")
        return []
    
    try:
        with open(store_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('products', [])
    except Exception as e:
        logger.error(f"Error loading store data: {e}")
        return []


def get_available_stores() -> List[str]:
    """Get list of available stores"""
    if not STORES_DIR.exists():
        return []
    
    stores = []
    for store_dir in STORES_DIR.iterdir():
        if store_dir.is_dir() and (store_dir / "data" / "products.json").exists():
            stores.append(store_dir.name)
    
    return stores


def transform_product_to_mcp_format(product: Dict, index: int, store_name: str) -> Dict:
    """Transform Weft product format to MCP widget format"""
    # Create unique ID combining store name and index
    product_key = f"{store_name}:{index}"
    
    # Build full image URL (assuming relative to store directory)
    image_url = product.get('image', '')
    if image_url and not image_url.startswith('http'):
        # Construct path relative to GitHub Pages or local server
        image_url = f"stores/{store_name}/{image_url}"
    
    return {
        "id": product_key,
        "name": product.get('name', 'Unknown Product'),
        "price_formatted": f"{product.get('price', '0')} ₪",
        "image": image_url,
        "category": product.get('category', ''),
        "url": product.get('url', ''),
        "is_purchasable": True,
        "is_in_stock": True,
        "has_options": False,
        "product_type": "simple"
    }


# Register widget resources
@mcp._mcp_server.list_resources()
async def list_resources() -> List[types.Resource]:
    """List available widget resources"""
    return [
        types.Resource(
            name="Products Widget",
            title="Products Widget",
            uri=PRODUCTS_WIDGET_URI,
            description="Interactive product grid with images and prices",
            mimeType=WIDGET_MIME_TYPE,
            _meta={
                "openai/outputTemplate": PRODUCTS_WIDGET_URI,
                "openai/widgetAccessible": True,
                "openai/resultCanProduceWidget": True,
                "openai/widgetPrefersBorder": True,
                "openai/widgetDomain": "https://chatgpt.com",
            }
        )
    ]


async def handle_read_resource(req: types.ReadResourceRequest) -> types.ServerResult:
    """Read widget HTML content"""
    uri = str(req.params.uri)
    logger.info(f"handle_read_resource called for URI: {uri}")

    if uri == PRODUCTS_WIDGET_URI:
        widget_path = WIDGET_DIR / "products.html"
        
        if not widget_path.exists():
            logger.error(f"Widget not found at: {widget_path}")
            return types.ServerResult(
                types.ReadResourceResult(
                    contents=[],
                    _meta={"error": f"Widget not found: {widget_path}"}
                )
            )

        html_content = widget_path.read_text(encoding="utf-8")
        logger.info(f"Read widget HTML, length: {len(html_content)}")

        contents = [
            types.TextResourceContents(
                uri=PRODUCTS_WIDGET_URI,
                mimeType=WIDGET_MIME_TYPE,
                text=html_content,
                _meta={
                    "openai/outputTemplate": PRODUCTS_WIDGET_URI,
                    "openai/widgetAccessible": True,
                    "openai/resultCanProduceWidget": True,
                    "openai/widgetPrefersBorder": True,
                    "openai/widgetDomain": "https://chatgpt.com",
                }
            )
        ]

        return types.ServerResult(types.ReadResourceResult(contents=contents))
    else:
        return types.ServerResult(
            types.ReadResourceResult(
                contents=[],
                _meta={"error": f"Unknown resource URI: {uri}"}
            )
        )


# Tool definitions
@mcp._mcp_server.list_tools()
async def list_tools() -> List[types.Tool]:
    """List available tools with widget metadata"""
    return [
        types.Tool(
            name="list_stores",
            title="List Stores",
            description="List all available stores in Weft",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="search_products",
            title="Search Products",
            description="""Search for products across all stores or in a specific store.
            
            You can search by:
            - Product name (Hebrew or English)
            - Category (e.g., 'דגנים', 'אגוזים', 'קטניות')
            - Use empty search to see all products
            
            Optionally filter by store name (e.g., 'nitzat-haduvdevan')""",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string", 
                        "description": "Search query to filter products. Empty string shows all products."
                    },
                    "store": {
                        "type": "string",
                        "description": "Optional: specific store name to search in (e.g., 'nitzat-haduvdevan')"
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional: filter by category"
                    }
                },
                "required": ["search"]
            },
            _meta={
                "openai/outputTemplate": PRODUCTS_WIDGET_URI,
                "openai/widgetAccessible": True,
                "openai/resultCanProduceWidget": True,
            },
            annotations={
                "destructiveHint": False,
                "openWorldHint": False,
                "readOnlyHint": True,
            }
        ),
        types.Tool(
            name="add_to_cart",
            title="Add to Cart",
            description="Add a product to the shopping cart",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The product ID (format: 'store:index')"},
                    "quantity": {"type": "integer", "description": "Number of items", "default": 1}
                },
                "required": ["product_id"]
            }
        ),
        types.Tool(
            name="view_cart",
            title="View Cart",
            description="View current shopping cart contents",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="remove_from_cart",
            title="Remove from Cart",
            description="Remove a specific item from the shopping cart",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The product ID to remove"}
                },
                "required": ["product_id"]
            }
        ),
        types.Tool(
            name="clear_cart",
            title="Clear Cart",
            description="Clear all items from the cart",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


# Tool implementation functions
def list_stores_func() -> str:
    """List all available stores"""
    stores = get_available_stores()
    
    if not stores:
        return "לא נמצאו חנויות זמינות"
    
    result = ["🏪 **חנויות זמינות:**\n"]
    for store in stores:
        # Load product count
        products = load_store_products(store)
        count = len(products)
        
        # Format store name nicely
        display_name = store.replace('-', ' ').title()
        result.append(f"• **{display_name}**")
        result.append(f"  מוצרים: {count}\n")
    
    return "\n".join(result)


def search_products(search: str = "", store: str = None, category: str = None) -> types.CallToolResult:
    """Search for products in Weft stores"""
    logger.info(f"search_products called with search='{search}', store='{store}', category='{category}'")
    
    try:
        all_products = []
        stores_to_search = [store] if store else get_available_stores()
        
        for store_name in stores_to_search:
            products = load_store_products(store_name)
            
            for idx, product in enumerate(products):
                # Apply filters
                if search and search.lower() not in product.get('name', '').lower():
                    continue
                
                if category and category.lower() != product.get('category', '').lower():
                    continue
                
                # Transform and add
                transformed = transform_product_to_mcp_format(product, idx, store_name)
                all_products.append(transformed)
        
        if not all_products:
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text="לא נמצאו מוצרים התואמים לחיפוש"
                    )
                ],
                structuredContent={"products": []}
            )
        
        # Format for text output
        text_result = []
        for product in all_products:
            text_result.append(
                f"• {product['name']}\n"
                f"  מחיר: {product['price_formatted']}\n"
                f"  קטגוריה: {product['category']}\n"
                f"  מזהה: {product['id']}"
            )
        
        logger.info(f"Returning {len(all_products)} products")
        
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"נמצאו {len(all_products)} מוצרים:\n\n" + "\n\n".join(text_result[:10])
                )
            ],
            structuredContent={"products": all_products}
        )
    
    except Exception as e:
        logger.error(f"search_products failed: {str(e)}")
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"שגיאה בחיפוש מוצרים: {str(e)}"
                )
            ],
            structuredContent={"products": [], "error": str(e)}
        )


async def add_to_cart(ctx: Context, product_id: str, quantity: int = 1) -> str:
    """Add a product to cart"""
    session_id = ctx.session_id
    
    try:
        # Parse product_id (format: "store:index")
        if ':' not in product_id:
            return "❌ מזהה מוצר לא תקין. יש להשתמש במזהה שהתקבל מחיפוש המוצרים."
        
        store_name, index_str = product_id.split(':', 1)
        index = int(index_str)
        
        # Load product
        products = load_store_products(store_name)
        if index >= len(products):
            return "❌ מוצר לא נמצא"
        
        product = products[index]
        
        # Initialize cart if needed
        if session_id not in user_carts:
            user_carts[session_id] = {}
        
        # Add to cart
        if product_id in user_carts[session_id]:
            user_carts[session_id][product_id]['quantity'] += quantity
        else:
            user_carts[session_id][product_id] = {
                'product': product,
                'store': store_name,
                'quantity': quantity
            }
        
        # Calculate total
        total = sum(
            float(item['product']['price']) * item['quantity']
            for item in user_carts[session_id].values()
        )
        items_count = len(user_carts[session_id])
        
        return f"✓ המוצר נוסף לעגלה!\n\n{product['name']}\nכמות: {quantity}\n\nסה\"כ פריטים בעגלה: {items_count}\nסכום כולל: {total:.2f} ₪"
    
    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        return f"❌ שגיאה בהוספה לעגלה: {str(e)}"


async def view_cart(ctx: Context) -> str:
    """View cart contents"""
    session_id = ctx.session_id
    
    if session_id not in user_carts or not user_carts[session_id]:
        return "העגלה ריקה 🛒"
    
    result = ["🛒 **העגלה שלך:**\n"]
    total = 0
    
    for product_id, item in user_carts[session_id].items():
        product = item['product']
        quantity = item['quantity']
        price = float(product['price'])
        line_total = price * quantity
        total += line_total
        
        result.append(f"• {product['name']}")
        result.append(f"  כמות: {quantity}")
        result.append(f"  מחיר ליחידה: {price} ₪")
        result.append(f"  סה\"כ: {line_total:.2f} ₪")
        result.append(f"  מזהה: {product_id}\n")
    
    result.append(f"\n**סה\"כ לתשלום: {total:.2f} ₪**")
    
    return "\n".join(result)


async def remove_from_cart(ctx: Context, product_id: str) -> str:
    """Remove item from cart"""
    session_id = ctx.session_id
    
    if session_id not in user_carts or product_id not in user_carts[session_id]:
        return "❌ המוצר לא נמצא בעגלה"
    
    product_name = user_carts[session_id][product_id]['product']['name']
    del user_carts[session_id][product_id]
    
    if not user_carts[session_id]:
        return f"✓ {product_name} הוסר מהעגלה!\n\nהעגלה ריקה כעת."
    
    # Calculate new total
    total = sum(
        float(item['product']['price']) * item['quantity']
        for item in user_carts[session_id].values()
    )
    items_count = len(user_carts[session_id])
    
    return f"✓ {product_name} הוסר מהעגלה!\n\nסה\"כ פריטים: {items_count}\nסכום כולל: {total:.2f} ₪"


async def clear_cart(ctx: Context) -> str:
    """Clear entire cart"""
    session_id = ctx.session_id
    
    if session_id in user_carts:
        user_carts[session_id] = {}
    
    return "✓ העגלה נוקתה"


# Tool call request handler
async def handle_call_tool(req: types.CallToolRequest) -> types.ServerResult:
    """Route tool calls to appropriate handlers"""
    tool_name = req.params.name
    arguments = req.params.arguments or {}
    
    logger.info(f"handle_call_tool called: {tool_name}")
    logger.info(f"Arguments: {arguments}")
    
    # Extract session_id
    session_id = getattr(req.params, '_meta', {}).get('sessionId') or "default"
    logger.info(f"Session ID: {session_id}")
    
    try:
        if tool_name == "list_stores":
            result = list_stores_func()
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=result)]
                )
            )
        
        elif tool_name == "search_products":
            search = arguments.get("search", "")
            store = arguments.get("store")
            category = arguments.get("category")
            result = search_products(search=search, store=store, category=category)
            return types.ServerResult(result)
        
        elif tool_name == "add_to_cart":
            product_id = arguments.get("product_id")
            quantity = arguments.get("quantity", 1)
            
            from types import SimpleNamespace
            ctx = SimpleNamespace(session_id=session_id)
            result = await add_to_cart(ctx, product_id, quantity)
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=result)]
                )
            )
        
        elif tool_name == "view_cart":
            from types import SimpleNamespace
            ctx = SimpleNamespace(session_id=session_id)
            result = await view_cart(ctx)
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=result)]
                )
            )
        
        elif tool_name == "remove_from_cart":
            product_id = arguments.get("product_id")
            from types import SimpleNamespace
            ctx = SimpleNamespace(session_id=session_id)
            result = await remove_from_cart(ctx, product_id)
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=result)]
                )
            )
        
        elif tool_name == "clear_cart":
            from types import SimpleNamespace
            ctx = SimpleNamespace(session_id=session_id)
            result = await clear_cart(ctx)
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=result)]
                )
            )
        
        else:
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=f"Unknown tool: {tool_name}")],
                    isError=True
                )
            )
    
    except Exception as e:
        logger.error(f"Error in handle_call_tool: {e}", exc_info=True)
        return types.ServerResult(
            types.CallToolResult(
                content=[types.TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )
        )


# Register the request handlers
mcp._mcp_server.request_handlers[types.CallToolRequest] = handle_call_tool
mcp._mcp_server.request_handlers[types.ReadResourceRequest] = handle_read_resource


if __name__ == "__main__":
    print(f"Starting Weft MCP Server on port {PORT}")
    print(f"MCP endpoint: http://0.0.0.0:{PORT}/mcp")
    print(f"Loading stores from: {STORES_DIR}")
    
    # List available stores
    stores = get_available_stores()
    print(f"\nAvailable stores ({len(stores)}):")
    for store in stores:
        products = load_store_products(store)
        print(f"  - {store}: {len(products)} products")
    
    mcp.run(transport="http")


