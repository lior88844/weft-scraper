#!/usr/bin/env python3
"""
Weft MCP Server
Enables browsing and ordering from Weft stores via ChatGPT
"""

import os
import json
import math
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

PORT = int(os.getenv("PORT", "8080"))

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
STORES_DIR = PROJECT_ROOT / "stores"
DEFAULT_STORE = "nitzat-haduvdevan"
WIDGET_DIR = Path(__file__).parent / "web" / "dist"
WIDGET_MIME_TYPE = "text/html+skybridge"
PRODUCTS_WIDGET_URI = "ui://widget/products.html"
CART_WIDGET_URI = "ui://widget/cart.html"

# In-memory cart storage: {session_id: {product_key: {product, quantity}}}
user_carts = {}

# Initialize MCP server
mcp = FastMCP("Nitzat Haduvdevan Store", port=PORT, host="0.0.0.0", stateless_http=True)


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
    """Get list of available stores (restricted to Nitzat Haduvdevan)"""
    if not STORES_DIR.exists():
        return []
    
    store_path = STORES_DIR / DEFAULT_STORE / "data" / "products.json"
    if store_path.exists():
        return [DEFAULT_STORE]
    
    return []


def transform_product_to_mcp_format(product: Dict, index: int, store_name: str) -> Dict:
    """Transform Weft product format to MCP widget format"""
    # Create unique ID combining store name and index
    product_key = f"{store_name}:{index}"
    
    # Build full image URL from the official store website
    image_url = product.get('image', '')
    if image_url and not image_url.startswith('http'):
        # Remove leading slash if present
        image_url = image_url.lstrip('/')
        # Construct full URL to the site's CDN/domain
        image_url = f"https://www.nizat.com/{image_url}"
    
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
        ),
        types.Resource(
            name="Cart Widget",
            title="Cart Widget",
            uri=CART_WIDGET_URI,
            description="Interactive shopping cart with add/remove items",
            mimeType=WIDGET_MIME_TYPE,
            _meta={
                "openai/outputTemplate": CART_WIDGET_URI,
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
    
    elif uri == CART_WIDGET_URI:
        widget_path = WIDGET_DIR / "cart.html"
        
        if not widget_path.exists():
            logger.error(f"Cart widget not found at: {widget_path}")
            return types.ServerResult(
                types.ReadResourceResult(
                    contents=[],
                    _meta={"error": f"Widget not found: {widget_path}"}
                )
            )

        html_content = widget_path.read_text(encoding="utf-8")
        logger.info(f"Read cart widget HTML, length: {len(html_content)}")

        contents = [
            types.TextResourceContents(
                uri=CART_WIDGET_URI,
                mimeType=WIDGET_MIME_TYPE,
                text=html_content,
                _meta={
                    "openai/outputTemplate": CART_WIDGET_URI,
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
            description="List the available Weft store (Nitzat Haduvdevan)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="search_products",
            title="Search Products",
            description="""Search for Nitzat Haduvdevan products.
            
            You can search by:
            - Product name (Hebrew or English)
            - Category (e.g., 'דגנים', 'אגוזים', 'קטניות')
            - Use empty search to see all products""",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string", 
                        "description": "Search query to filter products. Empty string shows all products."
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional: filter by category"
                    },
                    "page": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Page number (1 = first page)"
                    },
                    "page_size": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 50,
                        "description": "How many products per page (default 12, max 50)"
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
            },
            _meta={
                "openai/outputTemplate": CART_WIDGET_URI,
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
        ),
        types.Tool(
            name="debug_session",
            title="Debug Session",
            description="Display session information and cart statistics (for debugging)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            },
            annotations={
                "destructiveHint": False,
                "openWorldHint": False,
                "readOnlyHint": True,
            }
        )
    ]


# Tool implementation functions
def list_stores_func() -> str:
    """List all available stores (single store deployment)"""
    stores = get_available_stores()
    
    if not stores:
        return "לא נמצאה חנות נתמכת. ודא שקיים קובץ data/products.json תחת stores/nitzat-haduvdevan."
    
    products = load_store_products(DEFAULT_STORE)
    count = len(products)
    return f"🏪 **חנויות זמינות:**\n• **Nitzat Haduvdevan**\n  מוצרים: {count}\n"


def search_products(
    search: str = "",
    store: str = None,
    category: str = None,
    page: int = 1,
    page_size: int = 12,
) -> types.CallToolResult:
    """Search for products in the Nitzat Haduvdevan store"""
    logger.info(
        "search_products called with search='%s', store='%s', category='%s', page=%s, page_size=%s",
        search,
        store,
        category,
        page,
        page_size,
    )
    
    try:
        all_products = []
        stores_to_search = get_available_stores()
        filters_meta = {
            "search": search or "",
            "category": category or "",
        }
        page_size = max(1, min(page_size or 12, 50))
        page = max(1, page or 1)

        if store and store != DEFAULT_STORE:
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text="ניתן לחפש רק בחנות Nitzat Haduvdevan בממשק זה."
                    )
                ],
                structuredContent={
                    "products": [],
                    "pagination": {
                        "currentPage": 1,
                        "totalPages": 1,
                        "pageSize": page_size,
                        "totalProducts": 0,
                        "hasNext": False,
                        "hasPrev": False,
                    },
                    "filters": filters_meta,
                }
            )
        
        if not stores_to_search:
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text="חנות Nitzat Haduvdevan אינה זמינה (חסר קובץ products.json)."
                    )
                ],
                structuredContent={
                    "products": [],
                    "pagination": {
                        "currentPage": 1,
                        "totalPages": 1,
                        "pageSize": page_size,
                        "totalProducts": 0,
                        "hasNext": False,
                        "hasPrev": False,
                    },
                    "filters": filters_meta,
                }
            )
        
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
                structuredContent={
                    "products": [],
                    "pagination": {
                        "currentPage": 1,
                        "totalPages": 1,
                        "pageSize": page_size,
                        "totalProducts": 0,
                        "hasNext": False,
                        "hasPrev": False,
                    },
                    "filters": filters_meta,
                }
            )
        
        total_products = len(all_products)
        total_pages = max(1, math.ceil(total_products / page_size))
        if page > total_pages:
            page = total_pages
        start = (page - 1) * page_size
        end = start + page_size
        page_products = all_products[start:end]

        # Format for text output (current page)
        text_result = []
        for product in page_products:
            text_result.append(
                f"• {product['name']}\n"
                f"  מחיר: {product['price_formatted']}\n"
                f"  קטגוריה: {product['category']}\n"
                f"  מזהה: {product['id']}"
            )
        
        logger.info(f"Returning {len(page_products)} products for page {page}/{total_pages} (total {total_products})")
        
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=(
                        f"נמצאו {total_products} מוצרים "
                        f"(עמוד {page} מתוך {total_pages}):\n\n" + "\n\n".join(text_result[:10])
                    )
                )
            ],
            structuredContent={
                "products": page_products,
                "pagination": {
                    "currentPage": page,
                    "totalPages": total_pages,
                    "pageSize": page_size,
                    "totalProducts": total_products,
                    "hasNext": page < total_pages,
                    "hasPrev": page > 1,
                },
                "filters": {
                    "search": search or "",
                    "category": category or "",
                },
            }
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
            structuredContent={
                "products": [],
                "pagination": {
                    "currentPage": 1,
                    "totalPages": 1,
                    "pageSize": page_size if 'page_size' in locals() else 12,
                    "totalProducts": 0,
                    "hasNext": False,
                    "hasPrev": False,
                },
                "filters": {"search": search or "", "category": category or ""},
                "error": str(e),
            }
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


async def view_cart(ctx: Context) -> types.CallToolResult:
    """View cart contents with visual widget"""
    session_id = ctx.session_id
    
    if session_id not in user_carts or not user_carts[session_id]:
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text="העגלה ריקה 🛒"
                )
            ],
            structuredContent={"items": [], "total": 0}
        )
    
    items = []
    total = 0
    text_result = ["🛒 **העגלה שלך:**\n"]
    
    for product_id, item in user_carts[session_id].items():
        product = item['product']
        quantity = item['quantity']
        store_name = item['store']
        price = float(product['price'])
        line_total = price * quantity
        total += line_total
        
        # Get product index from product_id (format: "store:index")
        index = int(product_id.split(':')[1])
        
        # Transform product to get proper image URL
        transformed = transform_product_to_mcp_format(product, index, store_name)
        
        # Add to items array for widget
        items.append({
            "id": product_id,
            "name": product['name'],
            "price": product['price'],
            "quantity": quantity,
            "image": transformed['image'],
            "line_total": line_total
        })
        
        # Build text fallback
        text_result.append(f"• {product['name']}")
        text_result.append(f"  כמות: {quantity}")
        text_result.append(f"  מחיר ליחידה: {price} ₪")
        text_result.append(f"  סה\"כ: {line_total:.2f} ₪")
        text_result.append(f"  מזהה: {product_id}\n")
    
    text_result.append(f"\n**סה\"כ לתשלום: {total:.2f} ₪**")
    
    return types.CallToolResult(
        content=[
            types.TextContent(
                type="text",
                text="\n".join(text_result)
            )
        ],
        structuredContent={"items": items, "total": total}
    )


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


async def debug_session(ctx: Context) -> str:
    """Debug session information and cart statistics"""
    session_id = ctx.session_id
    
    result = ["🔍 **Session Debug Information**\n"]
    result.append(f"**Current Session ID:** `{session_id}`\n")
    
    # Total sessions tracked
    total_sessions = len(user_carts)
    result.append(f"**Total Active Sessions:** {total_sessions}\n")
    
    # Current session cart
    if session_id in user_carts and user_carts[session_id]:
        items_count = len(user_carts[session_id])
        total = sum(
            float(item['product']['price']) * item['quantity']
            for item in user_carts[session_id].values()
        )
        result.append(f"**Items in Your Cart:** {items_count}")
        result.append(f"**Your Cart Total:** {total:.2f} ₪\n")
    else:
        result.append("**Your Cart:** Empty\n")
    
    # Other sessions (for debugging)
    if total_sessions > 1:
        result.append("**Other Active Sessions:**")
        for sid in user_carts:
            if sid != session_id and user_carts[sid]:
                items = len(user_carts[sid])
                result.append(f"  - Session `{sid[:8]}...`: {items} items")
        result.append("")
    
    result.append("ℹ️ *Each chat conversation should have a unique session ID.*")
    result.append("*If multiple chats share the same ID, they'll share a cart.*")
    
    return "\n".join(result)


# Tool call request handler
async def handle_call_tool(req: types.CallToolRequest) -> types.ServerResult:
    """Route tool calls to appropriate handlers"""
    tool_name = req.params.name
    arguments = req.params.arguments or {}
    
    logger.info(f"handle_call_tool called: {tool_name}")
    logger.info(f"Arguments: {arguments}")
    
    # Extract session_id - try multiple sources for better ChatGPT compatibility
    session_id = None
    
    # Debug: Log what we're receiving
    logger.info(f"Request params type: {type(req.params)}")
    logger.info(f"Request params _meta: {getattr(req.params, '_meta', 'NO _META ATTRIBUTE')}")
    if hasattr(req, '_meta'):
        logger.info(f"Request _meta: {req._meta}")
    
    # Try to get from request params metadata (ChatGPT should send this)
    if hasattr(req.params, '_meta') and req.params._meta:
        session_id = req.params._meta.get('sessionId') or req.params._meta.get('conversationId')
        if session_id:
            logger.info(f"Found session ID in params._meta: {session_id}")
    
    # Try to get from request metadata
    if not session_id and hasattr(req, '_meta') and req._meta:
        session_id = req._meta.get('sessionId') or req._meta.get('conversationId')
        if session_id:
            logger.info(f"Found session ID in req._meta: {session_id}")
    
    # Fallback: Use a default session (not ideal but better than crashing)
    if not session_id:
        session_id = "default"
        logger.warning(f"⚠️  No session ID provided by ChatGPT! All chats will share the same cart.")
        logger.warning(f"⚠️  Using fallback session ID: {session_id}")
    else:
        logger.info(f"✓ Using session ID: {session_id}")
    
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
            page = arguments.get("page", 1)
            page_size = arguments.get("page_size", 12)
            result = search_products(
                search=search,
                store=store,
                category=category,
                page=page,
                page_size=page_size,
            )
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
            return types.ServerResult(result)
        
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
        
        elif tool_name == "debug_session":
            from types import SimpleNamespace
            ctx = SimpleNamespace(session_id=session_id)
            result = await debug_session(ctx)
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


