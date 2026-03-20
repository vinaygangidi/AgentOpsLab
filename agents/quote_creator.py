"""
Flexible Quote Creator Agent
Creates quote records in HubSpot with Claude AI enrichment
Handles both single record creation and bulk operations
Note: HubSpot quotes have limited editable fields via API
"""

import os
import time
from anthropic import Anthropic
from hubspot import HubSpot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

# Configuration
BATCH_SIZE = 100
RATE_LIMIT_DELAY = 0.5

# Sample quote data for single creation
SINGLE_QUOTE = {
    "hs_title": "Enterprise Software License Quote - Q1 2026",
    "hs_expiration_date": "2026-04-30"
}


def generate_mock_quotes(count=10):
    """
    Generates mock quote data for bulk testing.
    
    Args:
        count (int): Number of quotes to generate
        
    Returns:
        list: List of quote dictionaries
    """
    
    print(f"Generating {count} mock quotes")
    
    products = ["Enterprise Software", "Professional Services", "Annual License", 
                "Consulting Package", "Support Contract", "Training Program"]
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    
    quotes = []
    for i in range(count):
        quarter = quarters[i % len(quarters)]
        quote = {
            "hs_title": f"{products[i % len(products)]} Quote - {quarter} 2026 #{i}",
            "hs_expiration_date": "2026-06-30"
        }
        quotes.append(quote)
    
    print(f"Generated {len(quotes)} quotes successfully")
    return quotes


def enrich_quote_with_claude(quote_data):
    """
    Enriches quote data using Claude AI.
    Note: Most enrichment fields are not available in HubSpot quotes API.
    
    Args:
        quote_data (dict): Basic quote information
        
    Returns:
        dict: Enriched data from Claude
    """
    
    prompt = f"""You are a sales quote enrichment agent. Review this quote:

Quote Title: {quote_data['hs_title']}
Expiration Date: {quote_data.get('hs_expiration_date', 'Unknown')}

Tasks:
1. Suggest quote status (choose ONE from these exact options):
   DRAFT, APPROVAL_NOT_NEEDED, PENDING_APPROVAL, APPROVED, REJECTED

2. Provide a brief recommendation about this quote (1-2 sentences)

Return ONLY in this exact format (no extra text):
STATUS: DRAFT/APPROVAL_NOT_NEEDED/PENDING_APPROVAL/APPROVED/REJECTED
RECOMMENDATION: [brief recommendation]
"""
    
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response = message.content[0].text
    
    # Parse Claude's response
    enriched = {}
    for line in response.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            enriched[key.strip()] = value.strip()
    
    return enriched


def create_single_quote(quote_data, enrich=True):
    """
    Creates a single quote in HubSpot.
    
    Args:
        quote_data (dict): Quote information
        enrich (bool): Whether to enrich with Claude AI
        
    Returns:
        object: HubSpot API response or None if failed
    """
    
    print(f"\nProcessing: {quote_data['hs_title']}")
    
    # Enrich if requested (for display purposes only)
    enriched_data = {}
    if enrich:
        print("  Enriching with Claude AI")
        enriched_data = enrich_quote_with_claude(quote_data)
        print("  Enrichment complete")
        if enriched_data.get('RECOMMENDATION'):
            print(f"  AI Recommendation: {enriched_data['RECOMMENDATION']}")
    
    # Prepare properties - only basic fields that HubSpot allows
    properties = {
        "hs_title": quote_data['hs_title'],
        "hs_expiration_date": quote_data.get('hs_expiration_date', ''),
        "hs_language": "en"  # Required field - language code
    }
    
    # Try to add status if enriched
    if enriched_data.get('STATUS'):
        properties['hs_status'] = enriched_data['STATUS']
    
    # Create quote
    try:
        api_response = hubspot.crm.quotes.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        
        print(f"  Success: Quote ID {api_response.id}")
        return api_response
        
    except Exception as e:
        print(f"  Error: {e}")
        return None


def create_quotes_in_batches(quotes, batch_size=BATCH_SIZE, enrich_sample=False):
    """
    Creates multiple quotes in HubSpot using batch API.
    
    Args:
        quotes (list): List of quote dictionaries
        batch_size (int): Number of quotes per batch
        enrich_sample (bool): Whether to enrich first 10 with Claude
        
    Returns:
        tuple: (created_count, failed_count)
    """
    
    total = len(quotes)
    created = 0
    failed = 0
    
    print(f"\nStarting bulk creation of {total} quotes")
    print(f"Batch size: {batch_size} quotes per request")
    print("=" * 70)
    
    # Optional: Enrich sample (for recommendations only)
    if enrich_sample and total > 0:
        print("\nEnriching first 10 quotes with Claude AI for recommendations")
        sample_size = min(10, total)
        for i in range(sample_size):
            print(f"  Enriching {i+1}/{sample_size}: {quotes[i]['hs_title']}")
            enriched = enrich_quote_with_claude(quotes[i])
            
            if enriched.get('STATUS'):
                quotes[i]['hs_status'] = enriched['STATUS']
            if enriched.get('RECOMMENDATION'):
                print(f"    Recommendation: {enriched['RECOMMENDATION']}")
        print("Sample enrichment complete\n")
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = quotes[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        print(f"\nBatch {batch_num}/{total_batches}: Processing {len(batch)} quotes")
        
        # Prepare batch input
        inputs = []
        for quote in batch:
            properties = {
                "hs_title": quote['hs_title'],
                "hs_expiration_date": quote.get('hs_expiration_date', ''),
                "hs_language": "en"  # Required field - language code
            }
            
            # Add status if present from enrichment
            if quote.get('hs_status'):
                properties['hs_status'] = quote['hs_status']
            
            inputs.append({"properties": properties})
        
        batch_input = {"inputs": inputs}
        
        try:
            start_time = time.time()
            api_response = hubspot.crm.quotes.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create=batch_input
            )
            elapsed = time.time() - start_time
            
            batch_created = len(api_response.results)
            created += batch_created
            
            print(f"Batch {batch_num} complete: {batch_created} quotes created in {elapsed:.2f}s")
            
            progress = (created / total) * 100
            print(f"Progress: {created}/{total} ({progress:.1f}%)")
            
            if i + batch_size < total:
                print(f"Waiting {RATE_LIMIT_DELAY}s before next batch")
                time.sleep(RATE_LIMIT_DELAY)
            
        except Exception as e:
            failed += len(batch)
            print(f"Batch {batch_num} failed: {e}")
            print(f"Failed quotes: {len(batch)}")
    
    return created, failed


def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("FLEXIBLE QUOTE CREATOR")
    print("=" * 70 + "\n")
    
    # CONFIGURATION - Change these values based on your needs
    MODE = "bulk"                # "single" or "bulk"
    TOTAL_QUOTES = 100           # For bulk mode: how many to create
    ENRICH_WITH_CLAUDE = True    # For single: whether to enrich
    ENRICH_SAMPLE = False        # For bulk: enrich first 10 only
    
    print(f"Mode: {MODE.upper()}")
    print(f"Claude enrichment: {'Enabled' if ENRICH_WITH_CLAUDE or ENRICH_SAMPLE else 'Disabled'}")
    print("Note: HubSpot quotes have limited editable fields via API")
    
    if MODE == "single":
        # Single quote creation
        print("\n" + "=" * 70)
        print("SINGLE QUOTE MODE")
        print("=" * 70)
        
        result = create_single_quote(SINGLE_QUOTE, enrich=ENRICH_WITH_CLAUDE)
        
        if result:
            print("\n" + "=" * 70)
            print("SUCCESS: Quote created in HubSpot")
            print(f"Quote ID: {result.id}")
            print(f"View: https://app.hubspot.com/quotes/{result.id}")
            print("=" * 70)
        else:
            print("\nFailed to create quote")
    
    elif MODE == "bulk":
        # Bulk quote creation
        print(f"Creating {TOTAL_QUOTES} quotes\n")
        
        quotes = generate_mock_quotes(TOTAL_QUOTES)
        created, failed = create_quotes_in_batches(
            quotes, 
            batch_size=BATCH_SIZE,
            enrich_sample=ENRICH_SAMPLE
        )
        
        print("\n" + "=" * 70)
        print("BULK CREATION SUMMARY")
        print("=" * 70)
        print(f"Successfully created: {created} quotes")
        print(f"Failed: {failed} quotes")
        print(f"Success rate: {(created/(created+failed)*100):.1f}%")
        print(f"\nView in HubSpot: https://app.hubspot.com/quotes")
        print("=" * 70)
    
    else:
        print(f"Invalid MODE: {MODE}. Use 'single' or 'bulk'")


if __name__ == "__main__":
    main()