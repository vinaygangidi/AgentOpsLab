"""
Flexible Deal Creator Agent
Creates deal/opportunity records in HubSpot with Claude AI enrichment
Handles both single record creation and bulk operations
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

# Sample deal data for single creation
SINGLE_DEAL = {
    "dealname": "Enterprise Software License - Acme Corp",
    "amount": "50000",
    "pipeline": "default",
    "dealstage": "qualifiedtobuy"
}


def generate_mock_deals(count=10):
    """
    Generates mock deal data for bulk testing.
    
    Args:
        count (int): Number of deals to generate
        
    Returns:
        list: List of deal dictionaries
    """
    
    print(f"Generating {count} mock deals")
    
    deal_types = ["New Business", "Upsell", "Renewal", "Cross-sell"]
    products = ["Enterprise Software", "Professional Services", "Annual License", 
                "Consulting Package", "Support Contract"]
    companies = ["Acme Corp", "TechVision", "DataFlow", "CloudScale", "InnovateLabs"]
    
    deals = []
    for i in range(count):
        deal = {
            "dealname": f"{products[i % len(products)]} - {companies[i % len(companies)]} {i}",
            "amount": str((i + 1) * 5000),
            "pipeline": "default",
            "dealstage": "qualifiedtobuy"
        }
        deals.append(deal)
    
    print(f"Generated {len(deals)} deals successfully")
    return deals


def enrich_deal_with_claude(deal_data):
    """
    Enriches deal data using Claude AI.
    
    Args:
        deal_data (dict): Basic deal information
        
    Returns:
        dict: Enriched data from Claude
    """
    
    prompt = f"""You are a sales deal enrichment agent. Review this deal:

Deal Name: {deal_data['dealname']}
Amount: ${deal_data.get('amount', 'Unknown')}
Current Stage: {deal_data.get('dealstage', 'Unknown')}

Tasks:
1. Suggest a realistic close date (provide in YYYY-MM-DD format, 30-90 days from today which is March 20, 2026)

2. Suggest deal priority (choose ONE: high, medium, low) - must be lowercase

3. Suggest deal type (choose ONE from these exact options):
   newbusiness, existingbusiness, newbusiness_from_existing

4. Estimate probability to close as percentage (provide just a NUMBER like 25, 50, 75)

Return ONLY in this exact format (no extra text):
CLOSEDATE: YYYY-MM-DD
PRIORITY: high/medium/low
DEALTYPE: newbusiness/existingbusiness/newbusiness_from_existing
PROBABILITY: [number only, 0-100]
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


def create_single_deal(deal_data, enrich=True):
    """
    Creates a single deal in HubSpot.
    
    Args:
        deal_data (dict): Deal information
        enrich (bool): Whether to enrich with Claude AI
        
    Returns:
        object: HubSpot API response or None if failed
    """
    
    print(f"\nProcessing: {deal_data['dealname']}")
    
    # Enrich if requested
    enriched_data = {}
    if enrich:
        print("  Enriching with Claude AI")
        enriched_data = enrich_deal_with_claude(deal_data)
        print("  Enrichment complete")
    
    # Prepare properties
    properties = {
        "dealname": deal_data['dealname'],
        "amount": deal_data.get('amount', '0'),
        "pipeline": deal_data.get('pipeline', 'default'),
        "dealstage": deal_data.get('dealstage', 'qualifiedtobuy')
    }
    
    # Add enriched fields if present
    if enriched_data.get('CLOSEDATE'):
        properties['closedate'] = enriched_data['CLOSEDATE']
    if enriched_data.get('PRIORITY'):
        properties['hs_priority'] = enriched_data['PRIORITY']
    if enriched_data.get('DEALTYPE'):
        properties['dealtype'] = enriched_data['DEALTYPE']
    if enriched_data.get('PROBABILITY'):
        # Convert percentage (0-100) to decimal (0-1) for HubSpot
        probability_percent = enriched_data['PROBABILITY']
        try:
            probability_decimal = float(probability_percent) / 100.0
            properties['hs_deal_stage_probability'] = str(probability_decimal)
        except ValueError:
            pass  # Skip if conversion fails
    
    # Create deal
    try:
        api_response = hubspot.crm.deals.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        
        print(f"  Success: Deal ID {api_response.id}")
        return api_response
        
    except Exception as e:
        print(f"  Error: {e}")
        return None


def create_deals_in_batches(deals, batch_size=BATCH_SIZE, enrich_sample=False):
    """
    Creates multiple deals in HubSpot using batch API.
    
    Args:
        deals (list): List of deal dictionaries
        batch_size (int): Number of deals per batch
        enrich_sample (bool): Whether to enrich first 10 with Claude
        
    Returns:
        tuple: (created_count, failed_count)
    """
    
    total = len(deals)
    created = 0
    failed = 0
    
    print(f"\nStarting bulk creation of {total} deals")
    print(f"Batch size: {batch_size} deals per request")
    print("=" * 70)
    
    # Optional: Enrich sample
    if enrich_sample and total > 0:
        print("\nEnriching first 10 deals with Claude AI")
        sample_size = min(10, total)
        for i in range(sample_size):
            print(f"  Enriching {i+1}/{sample_size}: {deals[i]['dealname']}")
            enriched = enrich_deal_with_claude(deals[i])
            
            if enriched.get('CLOSEDATE'):
                deals[i]['closedate'] = enriched['CLOSEDATE']
            if enriched.get('PRIORITY'):
                deals[i]['hs_priority'] = enriched['PRIORITY']
            if enriched.get('DEALTYPE'):
                deals[i]['dealtype'] = enriched['DEALTYPE']
            if enriched.get('PROBABILITY'):
                # Convert percentage to decimal
                try:
                    probability_decimal = float(enriched['PROBABILITY']) / 100.0
                    deals[i]['hs_deal_stage_probability'] = str(probability_decimal)
                except ValueError:
                    pass
        print("Sample enrichment complete\n")
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = deals[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        print(f"\nBatch {batch_num}/{total_batches}: Processing {len(batch)} deals")
        
        # Prepare batch input
        inputs = []
        for deal in batch:
            properties = {
                "dealname": deal['dealname'],
                "amount": deal.get('amount', '0'),
                "pipeline": deal.get('pipeline', 'default'),
                "dealstage": deal.get('dealstage', 'qualifiedtobuy')
            }
            
            # Add enriched fields if present
            if deal.get('closedate'):
                properties['closedate'] = deal['closedate']
            if deal.get('hs_priority'):
                properties['hs_priority'] = deal['hs_priority']
            if deal.get('dealtype'):
                properties['dealtype'] = deal['dealtype']
            if deal.get('hs_deal_stage_probability'):
                properties['hs_deal_stage_probability'] = deal['hs_deal_stage_probability']
            
            inputs.append({"properties": properties})
        
        batch_input = {"inputs": inputs}
        
        try:
            start_time = time.time()
            api_response = hubspot.crm.deals.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create=batch_input
            )
            elapsed = time.time() - start_time
            
            batch_created = len(api_response.results)
            created += batch_created
            
            print(f"Batch {batch_num} complete: {batch_created} deals created in {elapsed:.2f}s")
            
            progress = (created / total) * 100
            print(f"Progress: {created}/{total} ({progress:.1f}%)")
            
            if i + batch_size < total:
                print(f"Waiting {RATE_LIMIT_DELAY}s before next batch")
                time.sleep(RATE_LIMIT_DELAY)
            
        except Exception as e:
            failed += len(batch)
            print(f"Batch {batch_num} failed: {e}")
            print(f"Failed deals: {len(batch)}")
    
    return created, failed


def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("FLEXIBLE DEAL CREATOR")
    print("=" * 70 + "\n")
    
    # CONFIGURATION - Change these values based on your needs
    MODE = "bulk"                # "single" or "bulk"
    TOTAL_DEALS = 100            # For bulk mode: how many to create
    ENRICH_WITH_CLAUDE = True    # For single: whether to enrich
    ENRICH_SAMPLE = False        # For bulk: enrich first 10 only
    
    print(f"Mode: {MODE.upper()}")
    print(f"Claude enrichment: {'Enabled' if ENRICH_WITH_CLAUDE or ENRICH_SAMPLE else 'Disabled'}")
    
    if MODE == "single":
        # Single deal creation
        print("\n" + "=" * 70)
        print("SINGLE DEAL MODE")
        print("=" * 70)
        
        result = create_single_deal(SINGLE_DEAL, enrich=ENRICH_WITH_CLAUDE)
        
        if result:
            print("\n" + "=" * 70)
            print("SUCCESS: Deal created in HubSpot")
            print(f"Deal ID: {result.id}")
            print(f"View: https://app.hubspot.com/contacts/deal/{result.id}")
            print("=" * 70)
        else:
            print("\nFailed to create deal")
    
    elif MODE == "bulk":
        # Bulk deal creation
        print(f"Creating {TOTAL_DEALS} deals\n")
        
        deals = generate_mock_deals(TOTAL_DEALS)
        created, failed = create_deals_in_batches(
            deals, 
            batch_size=BATCH_SIZE,
            enrich_sample=ENRICH_SAMPLE
        )
        
        print("\n" + "=" * 70)
        print("BULK CREATION SUMMARY")
        print("=" * 70)
        print(f"Successfully created: {created} deals")
        print(f"Failed: {failed} deals")
        print(f"Success rate: {(created/(created+failed)*100):.1f}%")
        print(f"\nView in HubSpot: https://app.hubspot.com/contacts/deals")
        print("=" * 70)
    
    else:
        print(f"Invalid MODE: {MODE}. Use 'single' or 'bulk'")


if __name__ == "__main__":
    main()