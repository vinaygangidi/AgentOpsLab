"""
Quick verification script to check deals in HubSpot
"""

import os
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

try:
    # Get first 20 deals
    response = hubspot.crm.deals.basic_api.get_page(limit=20)
    
    print(f"\nTotal deals found: {response.total if hasattr(response, 'total') else 'Unknown'}")
    print(f"\nShowing first {len(response.results)} deals:\n")
    
    for deal in response.results:
        print(f"Deal ID: {deal.id}")
        print(f"  Name: {deal.properties.get('dealname', 'No name')}")
        print(f"  Amount: ${deal.properties.get('amount', '0')}")
        print(f"  Stage: {deal.properties.get('dealstage', 'Unknown')}")
        print(f"  View: https://app.hubspot.com/contacts/deal/{deal.id}")
        print()
        
except Exception as e:
    print(f"Error fetching deals: {e}")