#!/usr/bin/env python3
"""
Test script to verify Weft MCP Server setup
This can run even without fastmcp installed
"""

import sys
import json
from pathlib import Path

def test_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required for fastmcp")
        print("   Current version:", f"{version.major}.{version.minor}")
        print("   Please install Python 3.10 or higher")
        return False
    else:
        print("✓ Python version OK")
        return True

def test_project_structure():
    """Check if project structure is correct"""
    print("\nChecking project structure...")
    
    mcp_dir = Path(__file__).parent
    project_root = mcp_dir.parent
    
    required_files = {
        "server.py": mcp_dir / "server.py",
        "requirements.txt": mcp_dir / "requirements.txt",
        "products.html": mcp_dir / "web" / "dist" / "products.html",
        "stores directory": project_root / "stores",
    }
    
    all_ok = True
    for name, path in required_files.items():
        if path.exists():
            print(f"✓ {name}: {path}")
        else:
            print(f"❌ {name} not found: {path}")
            all_ok = False
    
    return all_ok

def test_store_data():
    """Check if store data is available"""
    print("\nChecking store data...")
    
    project_root = Path(__file__).parent.parent
    stores_dir = project_root / "stores"
    
    if not stores_dir.exists():
        print(f"❌ Stores directory not found: {stores_dir}")
        return False
    
    stores_found = 0
    for store_dir in stores_dir.iterdir():
        if not store_dir.is_dir():
            continue
            
        products_file = store_dir / "data" / "products.json"
        if products_file.exists():
            try:
                with open(products_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    product_count = len(data.get('products', []))
                    print(f"✓ {store_dir.name}: {product_count} products")
                    stores_found += 1
            except Exception as e:
                print(f"❌ Error reading {store_dir.name}: {e}")
        else:
            print(f"⚠️  {store_dir.name}: No products.json found")
    
    if stores_found == 0:
        print("❌ No valid stores found")
        return False
    
    print(f"\n✓ Found {stores_found} store(s) with data")
    return True

def test_dependencies():
    """Check if required Python packages are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        ('fastmcp', 'fastmcp'),
        ('httpx', 'httpx'),
        ('dotenv', 'python-dotenv')
    ]
    all_installed = True
    
    for import_name, display_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {display_name} installed")
        except ImportError:
            print(f"❌ {display_name} not installed")
            all_installed = False
    
    if not all_installed:
        print("\nTo install dependencies, run:")
        print("  pip3 install -r requirements.txt")
    
    return all_installed

def main():
    """Run all tests"""
    print("=" * 60)
    print("Weft MCP Server Setup Test")
    print("=" * 60)
    
    results = {
        "Python Version": test_python_version(),
        "Project Structure": test_project_structure(),
        "Store Data": test_store_data(),
        "Dependencies": test_dependencies()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! Ready to run server.")
        print("\nTo start the server:")
        print("  python3 server.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        
        if not results["Python Version"]:
            print("\n📝 Install Python 3.10+:")
            print("   macOS: brew install python@3.11")
            print("   Or download from: https://www.python.org/downloads/")
        
        if not results["Dependencies"]:
            print("\n📝 Install dependencies:")
            print("   pip3 install -r requirements.txt")
    
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

