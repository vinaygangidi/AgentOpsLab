"""
Real HubSpot Contact Creator Agent
Creates actual contacts in HubSpot using Claude AI for data enrichment
"""

import os
from anthropic import Anthropic
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

# Sample contact data
MOCK_CONTACT = {
    "firstname": "Sarah",
    "lastname": "Johnson",
    "email": "sarah.johnson@techcorp.com",
    "phone": "5559876543",
    "company": "TechCorp Industries"
}


def enrich_contact_with_claude(contact_data):
    """
    Enriches contact data using Claude AI.
    
    Args:
        contact_data (dict): Basic contact information
        
    Returns:
        dict: Enriched data from Claude
    """
    
    print("Step 1: Enriching contact with Claude AI")
    
    prompt = f"""You are a contact enrichment agent. Review this contact:

First Name: {contact_data['firstname']}
Last Name: {contact_data['lastname']}
Email: {contact_data['email']}
Phone: {contact_data['phone']}
Company: {contact_data['company']}

Tasks:
1. Suggest a professional job title based on the name and company
2. Suggest the industry for this company
3. Format the phone number to (555) 987-6543
4. Validate the email format

Return ONLY in this exact format (no extra text):
JOB_TITLE: [title]
INDUSTRY: [industry]
FORMATTED_PHONE: [phone]
EMAIL_VALID: Yes/No
"""
    
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response = message.content[0].text
    print("Claude enrichment complete")
    print(response)
    
    # Parse Claude's response
    enriched = {}
    for line in response.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            enriched[key.strip()] = value.strip()
    
    return enriched


def create_hubspot_contact(contact_data, enriched_data):
    """
    Creates a contact in HubSpot CRM.
    
    Args:
        contact_data (dict): Original contact data
        enriched_data (dict): Enriched data from Claude
        
    Returns:
        object: HubSpot API response or None if failed
    """
    
    print("\nStep 2: Creating contact in HubSpot")
    
    # Prepare contact properties
    properties = {
        "firstname": contact_data['firstname'],
        "lastname": contact_data['lastname'],
        "email": contact_data['email'],
        "phone": enriched_data.get('FORMATTED_PHONE', contact_data['phone']),
        "company": contact_data['company'],
        "jobtitle": enriched_data.get('JOB_TITLE', 'Unknown'),
        "industry": enriched_data.get('INDUSTRY', 'Unknown')
    }
    
    # Create the contact
    simple_public_object_input = SimplePublicObjectInputForCreate(properties=properties)
    
    try:
        api_response = hubspot.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=simple_public_object_input
        )
        
        print("Contact created successfully in HubSpot")
        print(f"Contact ID: {api_response.id}")
        print(f"View in HubSpot: https://app.hubspot.com/contacts/contact/{api_response.id}")
        
        return api_response
        
    except Exception as e:
        print(f"Error creating contact: {e}")
        return None


def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("REAL HUBSPOT CONTACT CREATOR WITH CLAUDE AI")
    print("=" * 70 + "\n")
    
    # Step 1: Enrich with Claude
    enriched = enrich_contact_with_claude(MOCK_CONTACT)
    
    # Step 2: Create in HubSpot
    result = create_hubspot_contact(MOCK_CONTACT, enriched)
    
    if result:
        print("\n" + "=" * 70)
        print("SUCCESS: Contact created in your HubSpot account")
        print("=" * 70)
    else:
        print("\nFailed to create contact. Check the error above.")


if __name__ == "__main__":
    main()