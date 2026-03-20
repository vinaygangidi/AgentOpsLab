"""
Pipeline Orchestrator Agent
Coordinates multiple agents to create complete sales pipelines from email conversations
Uses: email_intelligence_agent + contact/company/deal/quote creation
"""

import os
import sys
from hubspot import HubSpot
from hubspot.crm.associations import BatchInputPublicAssociation, PublicAssociation
from dotenv import load_dotenv

# Import the email intelligence extraction function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from email_intelligence_agent import extract_intelligence_from_email

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))


def create_contact(contact_data):
    """Creates contact in HubSpot"""
    
    print(f"\n👤 Creating contact: {contact_data.get('firstname')} {contact_data.get('lastname')}")
    
    properties = {
        "firstname": contact_data.get('firstname', ''),
        "lastname": contact_data.get('lastname', ''),
        "email": contact_data.get('email', ''),
        "phone": contact_data.get('phone', ''),
        "jobtitle": contact_data.get('jobtitle', ''),
        "hs_lead_status": "NEW"
    }
    
    try:
        contact = hubspot.crm.contacts.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        print(f"   ✅ Contact created: ID {contact.id}")
        return contact
    except Exception as e:
        print(f"   ❌ Error creating contact: {e}")
        return None


def create_company(company_data):
    """Creates company in HubSpot"""
    
    print(f"\n🏢 Creating company: {company_data.get('name')}")
    
    properties = {
        "name": company_data.get('name', ''),
        "domain": company_data.get('domain', ''),
        "industry": company_data.get('industry', ''),
        "numberofemployees": str(company_data.get('numberofemployees', '')),
        "annualrevenue": str(company_data.get('annualrevenue', '')),
        "description": company_data.get('description', '')
    }
    
    try:
        company = hubspot.crm.companies.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        print(f"   ✅ Company created: ID {company.id}")
        return company
    except Exception as e:
        print(f"   ❌ Error creating company: {e}")
        return None


def create_deal(deal_data):
    """Creates deal in HubSpot"""
    
    print(f"\n💼 Creating deal: {deal_data.get('dealname')}")
    
    properties = {
        "dealname": deal_data.get('dealname', ''),
        "amount": str(deal_data.get('amount', '')),
        "closedate": deal_data.get('closedate', ''),
        "dealstage": deal_data.get('dealstage', 'qualifiedtobuy'),
        "pipeline": "default"
    }
    
    try:
        deal = hubspot.crm.deals.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        print(f"   ✅ Deal created: ID {deal.id}")
        print(f"   Amount: ${deal_data.get('amount', 0):,}")
        return deal
    except Exception as e:
        print(f"   ❌ Error creating deal: {e}")
        return None


def create_product(product_data):
    """Creates or retrieves product"""
    
    # Generate SKU if not provided
    if not product_data.get('sku'):
        product_data['sku'] = f"AUTO-{product_data.get('name', 'PRODUCT')[:10].upper().replace(' ', '-')}"
    
    properties = {
        "name": product_data.get('name', ''),
        "description": f"Product from email intelligence: {product_data.get('name')}",
        "price": str(product_data.get('price', 0)),
        "hs_sku": product_data['sku'],
        "hs_cost_of_goods_sold": str(product_data.get('price', 0) * 0.4)
    }
    
    try:
        product = hubspot.crm.products.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        return product
    except Exception as e:
        # Product might exist, search for it
        try:
            search_response = hubspot.crm.products.search_api.do_search(
                public_object_search_request={
                    "filterGroups": [{
                        "filters": [{
                            "propertyName": "name",
                            "operator": "EQ",
                            "value": product_data.get('name')
                        }]
                    }],
                    "limit": 1
                }
            )
            if search_response.total > 0:
                return search_response.results[0]
        except:
            pass
        return None


def create_quote_with_products(deal_id, products_data):
    """Creates line items and associates to deal"""
    
    print(f"\n📋 Creating quote with {len(products_data)} products...")
    
    created_products = []
    total_amount = 0
    
    for idx, product_data in enumerate(products_data):
        print(f"   Product {idx+1}: {product_data.get('name')}")
        
        # Create or get product
        product = create_product(product_data)
        if not product:
            print(f"      ⚠️ Skipped product")
            continue
        
        # Calculate line item total
        price = float(product_data.get('price', 0))
        quantity = int(product_data.get('quantity', 1))
        discount = float(product_data.get('discount', 0))
        
        line_total = price * quantity
        if discount > 0:
            line_total = line_total * (1 - discount / 100)
        
        total_amount += line_total
        
        # Create line item
        line_item_properties = {
            "quantity": str(quantity),
            "price": str(price),
            "amount": str(line_total),
            "hs_product_id": str(product.id)
        }
        
        if discount > 0:
            line_item_properties["discount"] = str(discount)
        
        try:
            line_item = hubspot.crm.line_items.basic_api.create(
                simple_public_object_input_for_create={"properties": line_item_properties}
            )
            
            # Associate line item with deal
            association = PublicAssociation(
                _from={"id": str(line_item.id)},
                to={"id": str(deal_id)},
                type="line_item_to_deal"
            )
            
            hubspot.crm.associations.batch_api.create(
                from_object_type="line_items",
                to_object_type="deals",
                batch_input_public_association=BatchInputPublicAssociation(inputs=[association])
            )
            
            created_products.append(line_item)
            print(f"      ✅ Added: ${line_total:,.2f}")
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    # Update deal amount
    try:
        hubspot.crm.deals.basic_api.update(
            deal_id=deal_id,
            simple_public_object_input={"properties": {"amount": str(total_amount)}}
        )
        print(f"\n   💰 Total Quote Value: ${total_amount:,.2f}")
    except Exception as e:
        print(f"   ⚠️ Could not update deal amount: {e}")
    
    return created_products, total_amount


def associate_records(contact_id, company_id, deal_id):
    """Associates contact, company, and deal"""
    
    print("\n🔗 Creating associations...")
    
    # Associate contact to company
    try:
        association = PublicAssociation(
            _from={"id": str(contact_id)},
            to={"id": str(company_id)},
            type="contact_to_company"
        )
        hubspot.crm.associations.batch_api.create(
            from_object_type="contacts",
            to_object_type="companies",
            batch_input_public_association=BatchInputPublicAssociation(inputs=[association])
        )
        print("   ✅ Contact → Company")
    except Exception as e:
        print(f"   ⚠️ Contact → Company: {e}")
    
    # Associate deal to contact
    try:
        association = PublicAssociation(
            _from={"id": str(deal_id)},
            to={"id": str(contact_id)},
            type="deal_to_contact"
        )
        hubspot.crm.associations.batch_api.create(
            from_object_type="deals",
            to_object_type="contacts",
            batch_input_public_association=BatchInputPublicAssociation(inputs=[association])
        )
        print("   ✅ Deal → Contact")
    except Exception as e:
        print(f"   ⚠️ Deal → Contact: {e}")
    
    # Associate deal to company
    try:
        association = PublicAssociation(
            _from={"id": str(deal_id)},
            to={"id": str(company_id)},
            type="deal_to_company"
        )
        hubspot.crm.associations.batch_api.create(
            from_object_type="deals",
            to_object_type="companies",
            batch_input_public_association=BatchInputPublicAssociation(inputs=[association])
        )
        print("   ✅ Deal → Company")
    except Exception as e:
        print(f"   ⚠️ Deal → Company: {e}")


def print_intelligence_report(intelligence, contact_id, company_id, deal_id):
    """Prints intelligence analysis report"""
    
    print("\n" + "="*70)
    print("INTELLIGENCE REPORT")
    print("="*70)
    
    print(f"\n📊 SENTIMENT: {intelligence.get('sentiment', 'Unknown').upper()}")
    print(f"🎯 CONFIDENCE: {intelligence.get('confidence', 'Unknown').upper()}")
    print(f"⚠️  RISK LEVEL: {intelligence.get('risk_level', 'Unknown').upper()}")
    
    if intelligence.get('key_concerns'):
        print(f"\n🚩 KEY CONCERNS:")
        for concern in intelligence['key_concerns']:
            print(f"   • {concern}")
    
    print(f"\n📝 NEXT STEPS:")
    print(f"   {intelligence.get('next_steps', 'None identified')}")
    
    print(f"\n🔗 HUBSPOT LINKS:")
    print(f"   Contact: https://app.hubspot.com/contacts/contact/{contact_id}")
    print(f"   Company: https://app.hubspot.com/contacts/company/{company_id}")
    print(f"   Deal: https://app.hubspot.com/contacts/deal/{deal_id}")
    
    print("\n" + "="*70)


def orchestrate_pipeline_from_email(email_filepath):
    """
    Complete pipeline orchestration: email → full CRM pipeline
    
    Args:
        email_filepath: Path to email conversation file
        
    Returns:
        dict: Created records (contact, company, deal, products, intelligence)
    """
    
    print("\n" + "="*70)
    print("PIPELINE ORCHESTRATOR - EMAIL TO CRM")
    print("="*70)
    
    # Step 1: Extract intelligence from email
    print("\n📧 STEP 1: Extracting intelligence from email...")
    intelligence = extract_intelligence_from_email(email_filepath)
    
    if not intelligence:
        print("❌ Failed to extract intelligence from email")
        return None
    
    print("\n" + "="*70)
    print("STEP 2: CREATING CRM PIPELINE")
    print("="*70)
    
    # Step 2: Create contact
    contact = create_contact(intelligence['contact'])
    if not contact:
        print("❌ Pipeline creation failed at contact")
        return None
    
    # Step 3: Create company
    company = create_company(intelligence['company'])
    if not company:
        print("❌ Pipeline creation failed at company")
        return None
    
    # Step 4: Create deal
    deal = create_deal(intelligence['deal'])
    if not deal:
        print("❌ Pipeline creation failed at deal")
        return None
    
    # Step 5: Create quote with products
    line_items = []
    total = 0
    if intelligence.get('products'):
        line_items, total = create_quote_with_products(deal.id, intelligence['products'])
    
    # Step 6: Associate all records
    associate_records(contact.id, company.id, deal.id)
    
    # Step 7: Print intelligence report
    print_intelligence_report(intelligence['intelligence'], contact.id, company.id, deal.id)
    
    print("\n✅ COMPLETE SALES PIPELINE CREATED FROM EMAIL CONVERSATION!\n")
    
    return {
        'contact': contact,
        'company': company,
        'deal': deal,
        'line_items': line_items,
        'total': total,
        'intelligence': intelligence['intelligence']
    }


def main():
    """Main execution"""
    
    # Example: Process enterprise software deal
    email_filepath = "data/email_conversations/enterprise_software_deal.txt"
    
    # Check if file exists
    if not os.path.exists(email_filepath):
        print(f"\n❌ File not found: {email_filepath}")
        print("Run: python utilities/email_synthesizer.py first to generate conversations\n")
        return
    
    # Orchestrate complete pipeline
    result = orchestrate_pipeline_from_email(email_filepath)
    
    if result:
        print("🎉 Pipeline orchestration complete!")
        print(f"   Contact ID: {result['contact'].id}")
        print(f"   Company ID: {result['company'].id}")
        print(f"   Deal ID: {result['deal'].id}")
        print(f"   Total Value: ${result['total']:,.2f}")


if __name__ == "__main__":
    main()