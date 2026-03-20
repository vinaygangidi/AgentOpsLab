"""
Bulk HubSpot Contact Creator
Creates 900+ contacts in HubSpot with batching and error handling
"""

import os
import time
from anthropic import Anthropic
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()

claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

def generate_mock_contacts(count=900):
    """
    Generate mock contact data for testing
    In production, you'd load this from CSV or database
    """
    print(f"📊 Generating {count} mock contacts...")
    
    first_names = ["John", "Sarah", "Michael", "Emily", "David", "Jessica", "James", "Ashley", "Robert", "Amanda"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    companies = ["TechCorp", "Innovate Inc", "Digital Solutions", "CloudSystems", "DataWorks", "SmartTech", "FutureLabs", "ByteForce", "CodeCraft", "NetPros"]
    industries = ["Technology", "Software", "Manufacturing", "Healthcare", "Finance", "Retail", "Education", "Consulting"]
    job_titles = ["Sales Manager", "Software Engineer", "Product Manager", "Marketing Director", "VP Sales", "CTO", "Account Executive", "Business Analyst"]
    
    contacts = []
    for i in range(count):
        contact = {
            "firstname": first_names[i % len(first_names)],
            "lastname": f"{last_names[i % len(last_names)]}{i}",  # Make unique
            "email": f"contact{i}@{companies[i % len(companies)].lower().replace(' ', '')}.com",
            "phone": f"555{str(i).zfill(7)}",
            "company": companies[i % len(companies)],
            "jobtitle": job_titles[i % len(job_titles)],
            "industry": industries[i % len(industries)]
        }
        contacts.append(contact)
    
    print(f"✅ Generated {len(contacts)} contacts")
    return contacts

def create_contacts_in_batches(contacts, batch_size=100):
    """
    Create contacts in HubSpot using batch API
    HubSpot allows up to 100 contacts per batch request
    """
    
    total = len(contacts)
    created = 0
    failed = 0
    
    print(f"\n🚀 Starting bulk creation of {total} contacts...")
    print(f"📦 Batch size: {batch_size} contacts per request")
    print("=" * 70)
    
    # Process in batches
    for i in range(0, total, batch_size):
        batch = contacts[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        print(f"\n📤 Batch {batch_num}/{total_batches}: Processing {len(batch)} contacts...")
        
        # Prepare batch input
        inputs = []
        for contact in batch:
            inputs.append({"properties": contact})
        
        batch_input = {"inputs": inputs}
        
        try:
            # Create batch in HubSpot
            start_time = time.time()
            api_response = hubspot.crm.contacts.batch_api.create(
                batch_input_simple_public_object_batch_input_for_create=batch_input
            )
            elapsed = time.time() - start_time
            
            # Count results
            batch_created = len(api_response.results)
            created += batch_created
            
            print(f"✅ Batch {batch_num} complete: {batch_created} contacts created in {elapsed:.2f}s")
            
            # Show progress
            progress = (created / total) * 100
            print(f"📊 Progress: {created}/{total} ({progress:.1f}%)")
            
            # Rate limiting - wait between batches to respect HubSpot limits
            if i + batch_size < total:
                wait_time = 0.5  # Wait 0.5 seconds between batches
                print(f"⏳ Waiting {wait_time}s before next batch...")
                time.sleep(wait_time)
            
        except Exception as e:
            failed += len(batch)
            print(f"❌ Batch {batch_num} failed: {e}")
            print(f"   Failed contacts: {len(batch)}")
            # Continue with next batch even if this one fails
    
    return created, failed

def enrich_sample_contacts_with_claude(contacts, sample_size=10):
    """
    Enrich a sample of contacts with Claude (to save API costs)
    In production, you might enrich high-value contacts only
    """
    
    print(f"\n🤖 Enriching {sample_size} sample contacts with Claude AI...")
    
    for i, contact in enumerate(contacts[:sample_size]):
        print(f"  Enriching {i+1}/{sample_size}: {contact['firstname']} {contact['lastname']}...")
        
        prompt = f"""Suggest a better job title for this contact:
Name: {contact['firstname']} {contact['lastname']}
Company: {contact['company']}
Current Title: {contact['jobtitle']}
Industry: {contact['industry']}

Return ONLY the improved job title, nothing else."""
        
        try:
            message = claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            
            improved_title = message.content[0].text.strip()
            contact['jobtitle'] = improved_title
            print(f"    ✅ Improved title: {improved_title}")
            
        except Exception as e:
            print(f"    ⚠️  Enrichment failed: {e}")
    
    return contacts

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 BULK HUBSPOT CONTACT CREATOR")
    print("=" * 70)
    
    # Configuration
    TOTAL_CONTACTS = 900
    BATCH_SIZE = 100  # HubSpot batch API limit
    ENRICH_SAMPLE = False  # Set to True to enrich first 10 contacts with Claude
    
    # Step 1: Generate contacts
    contacts = generate_mock_contacts(TOTAL_CONTACTS)
    
    # Step 2 (Optional): Enrich a sample with Claude
    if ENRICH_SAMPLE:
        contacts = enrich_sample_contacts_with_claude(contacts, sample_size=10)
    
    # Step 3: Create in HubSpot
    created, failed = create_contacts_in_batches(contacts, batch_size=BATCH_SIZE)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 BULK CREATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully created: {created} contacts")
    print(f"❌ Failed: {failed} contacts")
    print(f"📈 Success rate: {(created/(created+failed)*100):.1f}%")
    print("\n🔗 View in HubSpot: https://app.hubspot.com/contacts")
    print("=" * 70)