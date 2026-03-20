"""
Email Intelligence Reader (Read-Only Mode)
Demonstrates AI extraction without creating HubSpot records
Shows what WOULD be created from email conversations
"""

import os
import sys

# Import the extraction function from the refactored agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from email_intelligence_agent import extract_intelligence_from_email


def display_extracted_data(data):
    """Displays all extracted data in formatted output"""
    
    print("\n" + "="*70)
    print("EXTRACTED INTELLIGENCE - WHAT WOULD BE CREATED")
    print("="*70)
    
    # Contact Information
    print("\n👤 CONTACT RECORD")
    print("-" * 70)
    contact = data['contact']
    print(f"Name:       {contact.get('firstname', '')} {contact.get('lastname', '')}")
    print(f"Email:      {contact.get('email', 'Not found')}")
    print(f"Phone:      {contact.get('phone', 'Not found')}")
    print(f"Job Title:  {contact.get('jobtitle', 'Not found')}")
    if contact.get('notes'):
        print(f"Notes:      {contact.get('notes', '')}")
    
    # Company Information
    print("\n🏢 COMPANY RECORD")
    print("-" * 70)
    company = data['company']
    print(f"Name:       {company.get('name', '')}")
    print(f"Domain:     {company.get('domain', 'Not found')}")
    print(f"Industry:   {company.get('industry', 'Not found')}")
    print(f"Employees:  {company.get('numberofemployees', 'Not found')}")
    print(f"Revenue:    ${company.get('annualrevenue', 'Not found')}")
    print(f"Description: {company.get('description', '')[:100]}...")
    
    # Deal Information
    print("\n💼 DEAL RECORD")
    print("-" * 70)
    deal = data['deal']
    print(f"Deal Name:     {deal.get('dealname', '')}")
    print(f"Amount:        ${float(deal.get('amount', 0)):,.2f}")
    print(f"Close Date:    {deal.get('closedate', 'Not set')}")
    print(f"Stage:         {deal.get('dealstage', 'Not set')}")
    print(f"Win Probability: {deal.get('probability', 'Not set')}%")
    
    # Products
    print("\n📦 PRODUCTS & LINE ITEMS")
    print("-" * 70)
    products = data.get('products', [])
    total_value = 0
    
    for idx, product in enumerate(products, 1):
        price = float(product.get('price', 0))
        quantity = int(product.get('quantity', 1))
        discount = float(product.get('discount', 0))
        
        line_total = price * quantity
        if discount > 0:
            line_total = line_total * (1 - discount / 100)
        
        total_value += line_total
        
        print(f"\nProduct {idx}: {product.get('name', 'Unknown')}")
        print(f"  Quantity:  {quantity}")
        print(f"  Unit Price: ${price:,.2f}")
        if discount > 0:
            print(f"  Discount:  {discount}%")
        print(f"  Line Total: ${line_total:,.2f}")
    
    print(f"\n{'─' * 70}")
    print(f"TOTAL QUOTE VALUE: ${total_value:,.2f}")
    print(f"{'─' * 70}")
    
    # Intelligence Report
    print("\n📊 INTELLIGENCE ANALYSIS")
    print("-" * 70)
    intel = data['intelligence']
    print(f"Sentiment:    {intel.get('sentiment', 'Unknown').upper()}")
    print(f"Confidence:   {intel.get('confidence', 'Unknown').upper()}")
    print(f"Risk Level:   {intel.get('risk_level', 'Unknown').upper()}")
    
    if intel.get('key_concerns'):
        print(f"\n🚩 Key Concerns:")
        for concern in intel['key_concerns']:
            print(f"   • {concern}")
    
    print(f"\n📝 Recommended Next Steps:")
    print(f"   {intel.get('next_steps', 'None identified')}")
    
    print("\n" + "="*70)
    print("EXTRACTION COMPLETE")
    print("="*70)
    print("\n💡 NOTE: This is READ-ONLY mode. No records were created in HubSpot.")
    print("   To create records, use: python agents/pipeline_orchestrator_agent.py")
    print("="*70 + "\n")


def process_email_conversation(filepath):
    """Main pipeline: reads email and extracts intelligence"""
    
    print("\n" + "="*70)
    print("EMAIL INTELLIGENCE READER (Read-Only Mode)")
    print("="*70)
    
    # Extract intelligence (does not create anything)
    data = extract_intelligence_from_email(filepath)
    
    if not data:
        print("❌ Failed to extract intelligence from conversation")
        return
    
    # Display extracted data
    display_extracted_data(data)


def main():
    """Main execution - processes all conversations"""
    
    conversations = [
        "data/email_conversations/enterprise_software_deal.txt",
        "data/email_conversations/hardware_services_deal.txt",
        "data/email_conversations/professional_services_deal.txt"
    ]
    
    for filepath in conversations:
        if os.path.exists(filepath):
            process_email_conversation(filepath)
            print("\n" + "▼" * 70 + "\n")
        else:
            print(f"\n⚠️  File not found: {filepath}")
            print("Run: python utilities/email_synthesizer.py to generate conversations\n")


if __name__ == "__main__":
    main()