"""
Quick verification script to check if quotes exist in HubSpot
"""

import os
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

try:
    # Get first 10 quotes
    response = hubspot.crm.quotes.basic_api.get_page(limit=10)
    
    print(f"\nTotal quotes found: {response.total if hasattr(response, 'total') else 'Unknown'}")
    print(f"\nShowing first {len(response.results)} quotes:\n")
    
    for quote in response.results:
        print(f"Quote ID: {quote.id}")
        print(f"  Title: {quote.properties.get('hs_title', 'No title')}")
        print(f"  Status: {quote.properties.get('hs_status', 'Unknown')}")
        print(f"  Created: {quote.properties.get('createdate', 'Unknown')}")
        print(f"  View: https://app.hubspot.com/contacts/quote/{quote.id}")
        print()
        
except Exception as e:
    print(f"Error fetching quotes: {e}")