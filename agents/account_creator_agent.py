"""
Flexible Account Creator Agent
Creates one or many company records in HubSpot with Claude AI enrichment
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

# Sample company data for single creation
SINGLE_COMPANY = {
    "name": "TechVision Solutions",
    "domain": "techvision.com",
    "phone": "4155551234",
    "city": "San Francisco",
    "state": "California"
}


def generate_mock_companies(count=10):
    """
    Generates mock company data for bulk testing.
    
    Args:
        count (int): Number of companies to generate
        
    Returns:
        list: List of company dictionaries
    """
    
    print(f"Generating {count} mock companies")
    
    company_names = ["TechVision", "CloudScale", "DataFlow", "InnovateLabs", "SmartSystems",
                     "FutureWorks", "ByteCraft", "NetSolutions", "CodeForge", "DigitalEdge"]
    cities = ["San Francisco", "New York", "Austin", "Seattle", "Boston",
              "Chicago", "Denver", "Atlanta", "Portland", "Miami"]
    states = ["California", "New York", "Texas", "Washington", "Massachusetts",
              "Illinois", "Colorado", "Georgia", "Oregon", "Florida"]
    
    companies = []
    for i in range(count):
        company = {
            "name": f"{company_names[i % len(company_names)]} {i}",
            "domain": f"{company_names[i % len(company_names)].lower()}{i}.com",
            "phone": f"555{str(i).zfill(7)}",
            "city": cities[i % len(cities)],
            "state": states[i % len(states)]
        }
        companies.append(company)
    
    print(f"Generated {len(companies)} companies successfully")
    return companies


def enrich_company_with_claude(company_data):
    """
    Enriches company data using Claude AI.
    
    Args:
        company_data (dict): Basic company information
        
    Returns:
        dict: Enriched data from Claude
    """
    
    prompt = f"""You are a company data enrichment agent. Review this company:

Company Name: {company_data['name']}
Domain: {company_data['domain']}
Location: {company_data.get('city', 'Unknown')}, {company_data.get('state', 'Unknown')}

Tasks:
1. Suggest the HubSpot industry code (choose ONE from these options):
   COMPUTER_SOFTWARE, INFORMATION_TECHNOLOGY_AND_SERVICES, INTERNET, COMPUTER_HARDWARE, 
   TELECOMMUNICATIONS, FINANCIAL_SERVICES, MARKETING_AND_ADVERTISING, MANAGEMENT_CONSULTING

2. Estimate number of employees (provide just a NUMBER like 50, 100, 250, 500, 1000)

3. Estimate annual revenue in dollars (provide just a NUMBER like 1000000 for $1M, 5000000 for $5M)

4. Suggest company type (choose ONE: PROSPECT, PARTNER, RESELLER, VENDOR, OTHER)

5. Write a brief company description (1-2 sentences)

Return ONLY in this exact format (no extra text, no dollar signs, no ranges):
INDUSTRY: [exact code from list above]
EMPLOYEES: [number only]
REVENUE: [number only]
TYPE: [exact type from list above]
DESCRIPTION: [brief description]
"""
    
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
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


def create_single_company(company_data, enrich=True):
    """
    Creates a single company in HubSpot.
    
    Args:
        company_data (dict): Company information
        enrich (bool): Whether to enrich with Claude AI
        
    Returns:
        object: HubSpot API response or None if failed
    """
    
    print(f"\nProcessing: {company_data['name']}")
    
    # Enrich if requested
    enriched_data = {}
    if enrich:
        print("  Enriching with Claude AI")
        enriched_data = enrich_company_with_claude(company_data)
        print("  Enrichment complete")
    
    # Prepare properties
    properties = {
        "name": company_data['name'],
        "domain": company_data['domain'],
        "city": company_data.get('city', ''),
        "state": company_data.get('state', ''),
        "phone": company_data.get('phone', ''),
        "website": f"https://{company_data['domain']}",
        "description": enriched_data.get('DESCRIPTION', '')
    }
    
    if enriched_data.get('INDUSTRY'):
        properties['industry'] = enriched_data['INDUSTRY']
    if enriched_data.get('EMPLOYEES'):
        properties['numberofemployees'] = enriched_data['EMPLOYEES']
    if enriched_data.get('REVENUE'):
        properties['annualrevenue'] = enriched_data['REVENUE']
    if enriched_data.get('TYPE'):
        properties['type'] = enriched_data['TYPE']
    
    # Create company
    try:
        api_response = hubspot.crm.companies.basic_api.create(
            simple_public_object_input_for_create={"properties": properties}
        )
        
        print(f"  Success: Company ID {api_response.id}")
        return api_response
        
    except Exception as e:
        print(f"  Error: {e}")
        return None


def create_companies_in_batches(companies, batch_size=BATCH_SIZE, enrich_sample=False):
    """
    Creates multiple companies in HubSpot using batch API.
    
    Args:
        companies (list): List of company dictionaries
        batch_size (int): Number of companies per batch
        enrich_sample (bool): Whether to enrich first 10 with Claude
        
    Returns:
        tuple: (created_count, failed_count)
    """
    
    total = len(companies)
    created = 0
    failed = 0
    
    print(f"\nStarting bulk creation of {total} companies")
    print(f"Batch size: {batch_size} companies per request")
    print("=" * 70)
    
    # Optional: Enrich sample
    if enrich_sample and total > 0:
        print("\nEnriching first 10 companies with Claude AI")
        sample_size = min(10, total)
        for i in range(sample_size):
            print(f"  Enriching {i+1}/{sample_size}: {companies[i]['name']}")
            enriched = enrich_company_with_claude(companies[i])
            
            if enriched.get('DESCRIPTION'):
                companies[i]['description'] = enriched['DESCRIPTION']
            if enriched.get('INDUSTRY'):
                companies[i]['industry'] = enriched['INDUSTRY']
            if enriched.get('EMPLOYEES'):
                companies[i]['numberofemployees'] = enriched['EMPLOYEES']
            if enriched.get('REVENUE'):
                companies[i]['annualrevenue'] = enriched['REVENUE']
            if enriched.get('TYPE'):
                companies[i]['type'] = enriched['TYPE']
        print("Sample enrichment complete\n")
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = companies[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        print(f"\nBatch {batch_num}/{total_batches}: Processing {len(batch)} companies")
        
        # Prepare batch input
        inputs = []
        for company in batch:
            properties = {
                "name": company['name'],
                "domain": company['domain'],
                "city": company.get('city', ''),
                "state": company.get('state', ''),
                "phone": company.get('phone', ''),
                "website": f"https://{company['domain']}"
            }
            
            # Add enriched fields if present
            if company.get('description'):
                properties['description'] = company['description']
            if company.get('industry'):
                properties['industry'] = company['industry']
            if company.get('numberofemployees'):
                properties['numberofemployees'] = company['numberofemployees']
            if company.get('annualrevenue'):
                properties['annualrevenue'] = company['annualrevenue']
            if company.get('type'):
                properties['type'] = company['type']
            
            inputs.append({"properties": properties})
        
        batch_input = {"inputs": inputs}
        
        try:
            start_time = time.time()
            api_response = hubspot.crm.companies.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create=batch_input
            )
            elapsed = time.time() - start_time
            
            batch_created = len(api_response.results)
            created += batch_created
            
            print(f"Batch {batch_num} complete: {batch_created} companies created in {elapsed:.2f}s")
            
            progress = (created / total) * 100
            print(f"Progress: {created}/{total} ({progress:.1f}%)")
            
            if i + batch_size < total:
                print(f"Waiting {RATE_LIMIT_DELAY}s before next batch")
                time.sleep(RATE_LIMIT_DELAY)
            
        except Exception as e:
            failed += len(batch)
            print(f"Batch {batch_num} failed: {e}")
            print(f"Failed companies: {len(batch)}")
    
    return created, failed


def main():
    """Main execution function"""
    print("\n" + "=" * 70)
    print("FLEXIBLE HUBSPOT ACCOUNT CREATOR")
    print("=" * 70 + "\n")
    
    # CONFIGURATION - Change these values based on your needs
    MODE = "single"              # "single" or "bulk"
    TOTAL_COMPANIES = 100        # For bulk mode: how many to create
    ENRICH_WITH_CLAUDE = True    # For single: whether to enrich
    ENRICH_SAMPLE = False        # For bulk: enrich first 10 only
    
    print(f"Mode: {MODE.upper()}")
    print(f"Claude enrichment: {'Enabled' if ENRICH_WITH_CLAUDE or ENRICH_SAMPLE else 'Disabled'}")
    
    if MODE == "single":
        # Single company creation
        print("\n" + "=" * 70)
        print("SINGLE COMPANY MODE")
        print("=" * 70)
        
        result = create_single_company(SINGLE_COMPANY, enrich=ENRICH_WITH_CLAUDE)
        
        if result:
            print("\n" + "=" * 70)
            print("SUCCESS: Company created in HubSpot")
            print(f"Company ID: {result.id}")
            print(f"View: https://app.hubspot.com/contacts/company/{result.id}")
            print("=" * 70)
        else:
            print("\nFailed to create company")
    
    elif MODE == "bulk":
        # Bulk company creation
        print(f"Creating {TOTAL_COMPANIES} companies\n")
        
        companies = generate_mock_companies(TOTAL_COMPANIES)
        created, failed = create_companies_in_batches(
            companies, 
            batch_size=BATCH_SIZE,
            enrich_sample=ENRICH_SAMPLE
        )
        
        print("\n" + "=" * 70)
        print("BULK CREATION SUMMARY")
        print("=" * 70)
        print(f"Successfully created: {created} companies")
        print(f"Failed: {failed} companies")
        print(f"Success rate: {(created/(created+failed)*100):.1f}%")
        print(f"\nView in HubSpot: https://app.hubspot.com/contacts")
        print("=" * 70)
    
    else:
        print(f"Invalid MODE: {MODE}. Use 'single' or 'bulk'")


if __name__ == "__main__":
    main()