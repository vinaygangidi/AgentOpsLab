"""
Email Intelligence Reader (Read-Only Mode)
Demonstrates AI extraction without creating HubSpot records
Shows what WOULD be created from email conversations
"""

import os
import json
import re
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def read_email_conversation(filepath):
    """Reads email conversation from file"""
    
    print(f"\n📧 Reading email conversation: {filepath}")
    
    with open(filepath, 'r') as f:
        conversation = f.read()
    
    print(f"   Length: {len(conversation)} characters")
    print(f"   Lines: {conversation.count(chr(10))} lines\n")
    
    return conversation


def extract_intelligence(conversation):
    """Uses Claude to extract structured data from messy conversation"""
    
    print("🤖 Analyzing conversation with Claude AI...")
    print("   Extracting: contacts, companies, deals, products, sentiment\n")
    
    prompt = f"""You are an expert sales intelligence analyst. Analyze this email conversation and extract structured information for CRM creation.

EMAIL CONVERSATION:
{conversation}

EXTRACT THE FOLLOWING INFORMATION:

1. PRIMARY CONTACT (the buyer/decision maker):
   - First name
   - Last name
   - Email
   - Phone (if mentioned)
   - Job title
   - Role/responsibilities

2. COMPANY INFORMATION:
   - Company name
   - Industry
   - Number of employees (estimate if not exact)
   - Annual revenue (estimate based on company size/context)
   - Website (construct likely domain if not mentioned)
   - Description (what they do)

3. DEAL INFORMATION:
   - Deal name (create descriptive name)
   - Deal amount (final negotiated price or best estimate)
   - Products/services being purchased (list each)
   - Close date (estimate based on urgency/timeline mentioned)
   - Deal stage (choose: appointmentscheduled, qualifiedtobuy, presentationscheduled, decisionmakerboughtin, contractsent)
   - Win probability (0-100)

4. PRODUCTS & QUANTITIES:
   For each product/service mentioned, provide:
   - Product name
   - Quantity
   - Unit price (if mentioned or estimated)
   - Discount percentage (if mentioned)

5. INTELLIGENCE ANALYSIS:
   - Overall sentiment (positive/neutral/negative)
   - Confidence level (high/medium/low) - how much information is available
   - Key concerns or objections mentioned
   - Next steps recommendation
   - Risk assessment

Return your analysis in this EXACT JSON format (no markdown, no extra text):

{{
  "contact": {{
    "firstname": "",
    "lastname": "",
    "email": "",
    "phone": "",
    "jobtitle": "",
    "notes": ""
  }},
  "company": {{
    "name": "",
    "domain": "",
    "industry": "",
    "numberofemployees": "",
    "annualrevenue": "",
    "description": ""
  }},
  "deal": {{
    "dealname": "",
    "amount": "",
    "closedate": "YYYY-MM-DD",
    "dealstage": "",
    "probability": ""
  }},
  "products": [
    {{
      "name": "",
      "quantity": 1,
      "price": 0,
      "discount": 0,
      "sku": ""
    }}
  ],
  "intelligence": {{
    "sentiment": "",
    "confidence": "",
    "key_concerns": [],
    "next_steps": "",
    "risk_level": ""
  }}
}}"""

    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text.strip()
    
    # Remove markdown code blocks if present
    response_text = re.sub(r'^```json\s*', '', response_text)
    response_text = re.sub(r'\s*```$', '', response_text)
    response_text = response_text.strip()
    
    try:
        data = json.loads(response_text)
        print("✅ Intelligence extraction complete\n")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        print(f"Response: {response_text}")
        return None


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
    print("   To create records, use: email_intelligence_agent.py")
    print("="*70 + "\n")


def process_email_conversation(filepath):
    """Main pipeline: reads email and extracts intelligence"""
    
    print("\n" + "="*70)
    print("EMAIL INTELLIGENCE READER (Read-Only Mode)")
    print("="*70)
    
    # Read conversation
    conversation = read_email_conversation(filepath)
    
    # Extract intelligence
    data = extract_intelligence(conversation)
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