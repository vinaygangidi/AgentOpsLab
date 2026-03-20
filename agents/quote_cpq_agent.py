"""
Complete Quote System Agent
Creates products, deals with line items, and optionally quotes
Includes full pricing, quantities, discounts, and totals
"""

import os
import time
from anthropic import Anthropic
from hubspot import HubSpot
from hubspot.crm.associations import BatchInputPublicAssociation, PublicAssociation
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

# Configuration
BATCH_SIZE = 100
RATE_LIMIT_DELAY = 0.5


def create_product(product_data):
    """
    Creates a product in HubSpot product library.
    
    Args:
        product_data (dict): Product information
        
    Returns:
        object: HubSpot product object or None if failed
    """
    
    print(f"\nCreating product: {product_data['name']}")
    
    properties = {
        "name": product_data['name'],
        "description": product_data.get('description', ''),
        "price": str(product_data.get('price', 0)),
        "hs_sku": product_data.get('sku', ''),
        "hs_cost_of_goods_sold": str(product_data.get('cost', 0))
    }
    
    try:
        api_response = hubspot.crm.products.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        print(f"  Product created: ID {api_response.id}")
        return api_response
    except Exception as e:
        # Product might already exist, try to find it
        print(f"  Product creation failed (might already exist): {e}")
        try:
            # Search for existing product by name
            search_response = hubspot.crm.products.search_api.do_search(
                public_object_search_request={
                    "filterGroups": [{
                        "filters": [{
                            "propertyName": "name",
                            "operator": "EQ",
                            "value": product_data['name']
                        }]
                    }],
                    "limit": 1
                }
            )
            if search_response.total > 0:
                existing = search_response.results[0]
                print(f"  Using existing product: ID {existing.id}")
                return existing
        except Exception as search_error:
            print(f"  Could not find existing product: {search_error}")
        
        return None


def create_deal_with_line_items(deal_data, line_items_data):
    """
    Creates a complete deal with products and pricing.
    
    Args:
        deal_data (dict): Deal information
        line_items_data (list): List of line items with products
        
    Returns:
        tuple: (deal_object, line_items_objects)
    """
    
    print(f"\n{'='*70}")
    print(f"Creating complete deal: {deal_data['dealname']}")
    print(f"{'='*70}")
    
    # Step 1: Create or get products
    print("\nStep 1: Managing products...")
    products = []
    for item in line_items_data:
        product = create_product(item['product'])
        if product:
            products.append({
                'product_id': product.id,
                'quantity': item.get('quantity', 1),
                'price': item.get('price', item['product'].get('price', 0)),
                'discount': item.get('discount', 0)
            })
    
    if not products:
        print("  Error: No products available for deal")
        return None, None
    
    # Step 2: Create the deal
    print("\nStep 2: Creating deal...")
    deal_properties = {
        "dealname": deal_data['dealname'],
        "dealstage": deal_data.get('dealstage', 'qualifiedtobuy'),
        "pipeline": deal_data.get('pipeline', 'default'),
        "closedate": deal_data.get('closedate', '')
    }
    
    try:
        deal_response = hubspot.crm.deals.basic_api.create(
            simple_public_object_input_for_create={"properties": deal_properties}
        )
        print(f"  Deal created: ID {deal_response.id}")
        deal_id = deal_response.id
    except Exception as e:
        print(f"  Error creating deal: {e}")
        return None, None
    
    # Step 3: Add line items to deal
    print("\nStep 3: Adding line items to deal...")
    created_line_items = []
    total_amount = 0
    
    for idx, item in enumerate(products):
        print(f"  Adding line item {idx+1}/{len(products)}...")
        
        # Calculate line item total
        price = float(item['price'])
        quantity = int(item['quantity'])
        discount = float(item.get('discount', 0))
        
        line_total = price * quantity
        if discount > 0:
            line_total = line_total * (1 - discount / 100)
        
        total_amount += line_total
        
        line_item_properties = {
            "quantity": str(quantity),
            "price": str(price),
            "amount": str(line_total),
            "hs_product_id": str(item['product_id'])
        }
        
        if discount > 0:
            line_item_properties["discount"] = str(discount)
        
        try:
            # Create line item
            line_item_response = hubspot.crm.line_items.basic_api.create(
                simple_public_object_input_for_create={"properties": line_item_properties}
            )
            
            # Associate line item with deal using correct API
            try:
                association = PublicAssociation(
                    _from={"id": str(line_item_response.id)},
                    to={"id": str(deal_id)},
                    type="line_item_to_deal"
                )
                
                hubspot.crm.associations.batch_api.create(
                    from_object_type="line_items",
                    to_object_type="deals",
                    batch_input_public_association=BatchInputPublicAssociation(inputs=[association])
                )
                
                created_line_items.append(line_item_response)
                print(f"    Line item added: ${line_total:.2f}")
                
            except Exception as assoc_error:
                print(f"    Warning: Line item created but association failed: {assoc_error}")
                created_line_items.append(line_item_response)
            
        except Exception as e:
            print(f"    Error adding line item: {e}")
    
    print(f"\n  Total deal amount: ${total_amount:.2f}")
    
    # Step 4: Update deal with total amount
    try:
        hubspot.crm.deals.basic_api.update(
            deal_id=deal_id,
            simple_public_object_input={"properties": {"amount": str(total_amount)}}
        )
        print(f"  Deal amount updated")
    except Exception as e:
        print(f"  Warning: Could not update deal amount: {e}")
    
    return deal_response, created_line_items


def enrich_deal_with_claude(deal_data, line_items_data):
    """
    Uses Claude to suggest deal improvements.
    
    Args:
        deal_data (dict): Deal information
        line_items_data (list): Line items
        
    Returns:
        dict: Enrichment suggestions
    """
    
    # Build product summary
    products_summary = []
    for item in line_items_data:
        product = item['product']
        qty = item.get('quantity', 1)
        price = item.get('price', product.get('price', 0))
        products_summary.append(f"{product['name']} x{qty} @ ${price}")
    
    products_text = ", ".join(products_summary)
    
    prompt = f"""You are a sales deal optimization agent. Review this deal:

Deal Name: {deal_data['dealname']}
Products: {products_text}

Tasks:
1. Suggest an appropriate close date (YYYY-MM-DD format, 30-60 days from March 20, 2026)
2. Suggest deal stage (choose ONE: appointmentscheduled, qualifiedtobuy, presentationscheduled, decisionmakerboughtin, contractsent)
3. Suggest win probability as percentage (NUMBER only, 0-100)
4. Provide brief recommendation (1-2 sentences)

Return ONLY in this format:
CLOSEDATE: YYYY-MM-DD
DEALSTAGE: [exact stage name]
PROBABILITY: [number]
RECOMMENDATION: [brief recommendation]
"""
    
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response = message.content[0].text
    
    # Parse response
    enriched = {}
    for line in response.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            enriched[key.strip()] = value.strip()
    
    return enriched


def create_complete_quote(deal_name, products_list, enrich=True):
    """
    Creates a complete, executable quote with products and pricing.
    
    Args:
        deal_name (str): Name of the deal/quote
        products_list (list): List of products with quantities
        enrich (bool): Whether to use Claude for recommendations
        
    Returns:
        dict: Created deal and line items
    """
    
    deal_data = {
        "dealname": deal_name,
        "dealstage": "qualifiedtobuy",
        "pipeline": "default"
    }
    
    # Enrich if requested
    if enrich:
        print("\nEnriching deal with Claude AI...")
        enriched = enrich_deal_with_claude(deal_data, products_list)
        
        if enriched.get('CLOSEDATE'):
            deal_data['closedate'] = enriched['CLOSEDATE']
        if enriched.get('DEALSTAGE'):
            deal_data['dealstage'] = enriched['DEALSTAGE']
        if enriched.get('RECOMMENDATION'):
            print(f"AI Recommendation: {enriched['RECOMMENDATION']}")
        
        print("Enrichment complete\n")
    
    # Create the deal with line items
    deal, line_items = create_deal_with_line_items(deal_data, products_list)
    
    if deal:
        print(f"\n{'='*70}")
        print("SUCCESS: Complete quote created!")
        print(f"{'='*70}")
        print(f"Deal ID: {deal.id}")
        print(f"View in HubSpot: https://app.hubspot.com/contacts/deal/{deal.id}")
        print(f"Total Line Items: {len(line_items)}")
        print(f"{'='*70}\n")
        
        return {
            'deal': deal,
            'line_items': line_items
        }
    else:
        print("\nFailed to create complete quote")
        return None


def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("COMPLETE QUOTE SYSTEM - WITH PRODUCTS AND PRICING")
    print("=" * 70 + "\n")
    
    # Example: Complete quote with multiple products
    deal_name = "Enterprise Software Package - Acme Corp Q1 2026"
    
    products_to_quote = [
        {
            'product': {
                'name': 'Enterprise Software License',
                'description': 'Annual enterprise software license',
                'price': 25000,
                'sku': 'ENT-SW-001',
                'cost': 5000
            },
            'quantity': 1,
            'price': 25000,
            'discount': 10  # 10% discount
        },
        {
            'product': {
                'name': 'Professional Services - Implementation',
                'description': 'Implementation and setup services',
                'price': 15000,
                'sku': 'PROF-SVC-001',
                'cost': 8000
            },
            'quantity': 1,
            'price': 15000,
            'discount': 0
        },
        {
            'product': {
                'name': 'Annual Support Contract',
                'description': '24/7 premium support',
                'price': 5000,
                'sku': 'SUPPORT-001',
                'cost': 1000
            },
            'quantity': 1,
            'price': 5000,
            'discount': 0
        }
    ]
    
    # Create the complete quote
    result = create_complete_quote(
        deal_name=deal_name,
        products_list=products_to_quote,
        enrich=True
    )
    
    if result:
        print("Quote is ready for execution!")
        print("Next steps:")
        print("1. Review in HubSpot")
        print("2. Send to customer")
        print("3. Convert to order when won")


if __name__ == "__main__":
    main()