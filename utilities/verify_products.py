"""
Quick verification script to check products in HubSpot
"""

import os
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

try:
    # Get first 20 products
    response = hubspot.crm.products.basic_api.get_page(limit=20)
    
    print(f"\nTotal products found: {response.total if hasattr(response, 'total') else 'Unknown'}")
    print(f"\nShowing first {len(response.results)} products:\n")
    
    for product in response.results:
        print(f"Product ID: {product.id}")
        print(f"  Name: {product.properties.get('name', 'No name')}")
        print(f"  SKU: {product.properties.get('hs_sku', 'No SKU')}")
        print(f"  Price: ${product.properties.get('price', '0')}")
        print(f"  View: https://app.hubspot.com/products/{product.id}")
        print()
        
except Exception as e:
    print(f"Error fetching products: {e}")