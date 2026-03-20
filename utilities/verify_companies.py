"""
Quick verification script to check companies in HubSpot
"""

import os
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

try:
    # Get first 20 companies
    response = hubspot.crm.companies.basic_api.get_page(limit=20)
    
    print(f"\nTotal companies found: {response.total if hasattr(response, 'total') else 'Unknown'}")
    print(f"\nShowing first {len(response.results)} companies:\n")
    
    for company in response.results:
        print(f"Company ID: {company.id}")
        print(f"  Name: {company.properties.get('name', 'No name')}")
        print(f"  Domain: {company.properties.get('domain', 'No domain')}")
        print(f"  Industry: {company.properties.get('industry', 'Unknown')}")
        print(f"  View: https://app.hubspot.com/contacts/company/{company.id}")
        print()
        
except Exception as e:
    print(f"Error fetching companies: {e}")