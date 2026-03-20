"""
Email Intelligence Agent - EXTRACTION ONLY
Reads messy email conversations and extracts structured intelligence
Does NOT create any HubSpot records - use pipeline_orchestrator for that
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
    print(f"   Preview: {conversation[:200]}...\n")
    
    return conversation


def extract_intelligence(conversation):
    """
    Uses Claude to extract structured data from messy conversation.
    Returns JSON with contact, company, deal, products, and intelligence.
    DOES NOT CREATE ANYTHING - just extracts and returns data.
    """
    
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


def extract_intelligence_from_email(filepath):
    """
    Main function - reads email and extracts intelligence.
    Returns structured data, does NOT create any HubSpot records.
    
    Returns:
        dict: Extracted intelligence with contact, company, deal, products, intelligence
    """
    
    print("\n" + "="*70)
    print("EMAIL INTELLIGENCE EXTRACTION")
    print("="*70)
    
    # Read conversation
    conversation = read_email_conversation(filepath)
    
    # Extract intelligence
    intelligence = extract_intelligence(conversation)
    
    if intelligence:
        print("="*70)
        print("EXTRACTION COMPLETE")
        print("="*70)
        print("\nExtracted data ready for pipeline creation.")
        print("Use pipeline_orchestrator_agent.py to create CRM records.\n")
    
    return intelligence


def main():
    """Main execution - extracts intelligence from sample conversation"""
    
    # Example: Extract from one conversation
    filepath = "data/email_conversations/enterprise_software_deal.txt"
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"\n❌ File not found: {filepath}")
        print("Run: python utilities/email_synthesizer.py first to generate conversations\n")
        return
    
    # Extract intelligence (does not create anything)
    intelligence = extract_intelligence_from_email(filepath)
    
    if intelligence:
        # Display what was extracted
        print("\n📊 EXTRACTED INTELLIGENCE:")
        print(f"Contact: {intelligence['contact']['firstname']} {intelligence['contact']['lastname']}")
        print(f"Company: {intelligence['company']['name']}")
        print(f"Deal: ${intelligence['deal']['amount']} - {intelligence['deal']['dealstage']}")
        print(f"Products: {len(intelligence['products'])} items")
        print(f"Sentiment: {intelligence['intelligence']['sentiment']}")
        print(f"Confidence: {intelligence['intelligence']['confidence']}")
        print(f"\nTo create CRM records, run: python agents/pipeline_orchestrator_agent.py\n")


if __name__ == "__main__":
    main()