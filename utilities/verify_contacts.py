"""
Quick verification script to check contacts in HubSpot
"""

import os
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

try:
    # Get first 20 contacts
    response = hubspot.crm.contacts.basic_api.get_page(limit=20)
    
    print(f"\nTotal contacts found: {response.total if hasattr(response, 'total') else 'Unknown'}")
    print(f"\nShowing first {len(response.results)} contacts:\n")
    
    for contact in response.results:
        print(f"Contact ID: {contact.id}")
        print(f"  Name: {contact.properties.get('firstname', '')} {contact.properties.get('lastname', '')}")
        print(f"  Email: {contact.properties.get('email', 'No email')}")
        print(f"  Company: {contact.properties.get('company', 'No company')}")
        print(f"  View: https://app.hubspot.com/contacts/contact/{contact.id}")
        print()
        
except Exception as e:
    print(f"Error fetching contacts: {e}")