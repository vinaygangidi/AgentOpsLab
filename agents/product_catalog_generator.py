"""
Product Catalog Generator
Creates a comprehensive product catalog in HubSpot
Generates 100+ products across different categories
"""

import os
import time
from hubspot import HubSpot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize HubSpot client
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

# Configuration
BATCH_SIZE = 100
RATE_LIMIT_DELAY = 0.5


def generate_product_catalog(count=100):
    """
    Generates a diverse product catalog.
    
    Args:
        count (int): Number of products to generate
        
    Returns:
        list: List of product dictionaries
    """
    
    print(f"Generating {count} products for catalog...")
    
    # Product categories with base prices
    categories = {
        "Software Licenses": {
            "products": ["Enterprise Suite", "Professional Edition", "Standard Version", 
                        "Starter Pack", "Developer License", "Team Edition"],
            "base_price": 10000,
            "price_variance": 5000
        },
        "Professional Services": {
            "products": ["Implementation", "Consulting", "Training", "Support", 
                        "Custom Development", "Integration Services"],
            "base_price": 15000,
            "price_variance": 10000
        },
        "Support Contracts": {
            "products": ["Premium Support", "Standard Support", "Basic Support", 
                        "24/7 Support", "Business Hours Support", "Enterprise Support"],
            "base_price": 5000,
            "price_variance": 3000
        },
        "Hardware": {
            "products": ["Server", "Workstation", "Laptop", "Desktop", 
                        "Network Equipment", "Storage Device"],
            "base_price": 2000,
            "price_variance": 1500
        },
        "Cloud Services": {
            "products": ["Hosting", "Storage", "Compute", "Database", 
                        "CDN Service", "Backup Service"],
            "base_price": 500,
            "price_variance": 400
        },
        "Subscription Services": {
            "products": ["Monthly Plan", "Annual Plan", "Quarterly Plan", 
                        "Enterprise Plan", "Team Plan", "Individual Plan"],
            "base_price": 1000,
            "price_variance": 800
        }
    }
    
    products = []
    product_num = 1
    
    # Generate products cycling through categories
    while len(products) < count:
        for category, details in categories.items():
            if len(products) >= count:
                break
            
            for product_name in details["products"]:
                if len(products) >= count:
                    break
                
                # Calculate price with variance
                base = details["base_price"]
                variance = details["price_variance"]
                price = base + (product_num % 10) * (variance / 10)
                cost = price * 0.4  # 40% cost
                
                # Create unique SKU
                category_code = ''.join([w[0].upper() for w in category.split()[:2]])
                sku = f"{category_code}-{product_num:04d}"
                
                product = {
                    "name": f"{product_name} - {category} #{product_num}",
                    "description": f"{product_name} from {category} category. Professional grade solution.",
                    "price": round(price, 2),
                    "sku": sku,
                    "cost": round(cost, 2)
                }
                
                products.append(product)
                product_num += 1
    
    print(f"Generated {len(products)} products successfully")
    return products


def create_products_in_batches(products, batch_size=BATCH_SIZE):
    """
    Creates products in HubSpot using batch API.
    
    Args:
        products (list): List of product dictionaries
        batch_size (int): Number of products per batch
        
    Returns:
        tuple: (created_count, failed_count)
    """
    
    total = len(products)
    created = 0
    failed = 0
    
    print(f"\nStarting bulk product creation: {total} products")
    print(f"Batch size: {batch_size} products per request")
    print("=" * 70)
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = products[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        print(f"\nBatch {batch_num}/{total_batches}: Processing {len(batch)} products")
        
        # Prepare batch input
        inputs = []
        for product in batch:
            properties = {
                "name": product['name'],
                "description": product['description'],
                "price": str(product['price']),
                "hs_sku": product['sku'],
                "hs_cost_of_goods_sold": str(product['cost'])
            }
            inputs.append({"properties": properties})
        
        batch_input = {"inputs": inputs}
        
        try:
            start_time = time.time()
            api_response = hubspot.crm.products.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create=batch_input
            )
            elapsed = time.time() - start_time
            
            batch_created = len(api_response.results)
            created += batch_created
            
            print(f"Batch {batch_num} complete: {batch_created} products created in {elapsed:.2f}s")
            
            progress = (created / total) * 100
            print(f"Progress: {created}/{total} ({progress:.1f}%)")
            
            if i + batch_size < total:
                print(f"Waiting {RATE_LIMIT_DELAY}s before next batch")
                time.sleep(RATE_LIMIT_DELAY)
            
        except Exception as e:
            failed += len(batch)
            print(f"Batch {batch_num} failed: {e}")
            print(f"Failed products: {len(batch)}")
    
    return created, failed


def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("PRODUCT CATALOG GENERATOR")
    print("=" * 70 + "\n")
    
    # Configuration
    TOTAL_PRODUCTS = 100  # Change this to create more or fewer products
    
    print(f"Creating {TOTAL_PRODUCTS} products across multiple categories")
    print("Categories: Software, Services, Support, Hardware, Cloud, Subscriptions\n")
    
    # Generate product catalog
    products = generate_product_catalog(TOTAL_PRODUCTS)
    
    # Create products in HubSpot
    created, failed = create_products_in_batches(products, batch_size=BATCH_SIZE)
    
    print("\n" + "=" * 70)
    print("PRODUCT CATALOG CREATION SUMMARY")
    print("=" * 70)
    print(f"Successfully created: {created} products")
    print(f"Failed: {failed} products")
    print(f"Success rate: {(created/(created+failed)*100) if (created+failed) > 0 else 0:.1f}%")
    print(f"\nView in HubSpot: https://app.hubspot.com/products-library")
    print("=" * 70)


if __name__ == "__main__":
    main()