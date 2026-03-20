# Utility Scripts Documentation

## Overview

The `utilities/` folder contains simple, non-AI scripts for verifying and inspecting data in HubSpot, as well as tools for generating test data. These scripts use the HubSpot API directly without any Claude AI enrichment.

## Available Utilities

### verify_contacts.py
Displays the first 20 contacts in your HubSpot account.

**Usage:**
```bash
python utilities/verify_contacts.py
```

**Output:**
- Contact ID
- Name
- Email
- Company
- Link to view in HubSpot

**Example:**
```
Total contacts found: 998

Contact ID: 123456
  Name: Sarah Chen
  Email: s.chen@example.com
  Company: TechFlow Industries
  View: https://app.hubspot.com/contacts/contact/123456
```

---

### verify_companies.py
Displays the first 20 companies in your HubSpot account.

**Usage:**
```bash
python utilities/verify_companies.py
```

**Output:**
- Company ID
- Name
- Domain
- Industry
- Link to view in HubSpot

**Example:**
```
Total companies found: 156

Company ID: 789012
  Name: TechFlow Industries
  Domain: techflow.com
  Industry: Software Development
  View: https://app.hubspot.com/contacts/company/789012
```

---

### verify_deals.py
Displays the first 20 deals in your HubSpot account.

**Usage:**
```bash
python utilities/verify_deals.py
```

**Output:**
- Deal ID
- Name
- Amount
- Stage
- Link to view in HubSpot

**Example:**
```
Total deals found: 112

Deal ID: 345678
  Name: Q2 2026 Enterprise Software - TechFlow
  Amount: $75000
  Stage: contractsent
  View: https://app.hubspot.com/contacts/deal/345678
```

---

### verify_quotes.py
Displays the first 10 quotes in your HubSpot account.

**Usage:**
```bash
python utilities/verify_quotes.py
```

**Output:**
- Quote ID
- Title
- Status
- Created date
- Link to view in HubSpot

**Example:**
```
Total quotes found: 24

Quote ID: 901234
  Title: Enterprise Package Q2
  Status: DRAFT
  Created: 2026-03-15
  View: https://app.hubspot.com/contacts/quote/901234
```

**Note:** Requires quote scopes and Sales Hub Professional/Enterprise

---

### verify_products.py
Displays the first 20 products in your HubSpot catalog.

**Usage:**
```bash
python utilities/verify_products.py
```

**Output:**
- Product ID
- Name
- SKU
- Price
- Link to view in HubSpot

**Example:**
```
Total products found: 156

Product ID: 567890
  Name: Enterprise Software License
  SKU: ENT-SW-001
  Price: $25000
  View: https://app.hubspot.com/products/567890
```

---

### product_catalog_generator.py
Generates and creates 100+ products in HubSpot catalog programmatically.

**Usage:**
```bash
python utilities/product_catalog_generator.py
```

**What it does:**
- Generates products across 6 categories
- Creates SKUs systematically
- Sets realistic pricing and costs
- Bulk creates in HubSpot using batch API

**Output:**
- 100 products created (configurable)
- Categories: Software Licenses, Professional Services, Support Contracts, Hardware, Cloud Services, Subscription Services
- Each with name, SKU, price, cost of goods sold

**Example Output:**
```
======================================================================
PRODUCT CATALOG GENERATOR
======================================================================

Creating 100 products across multiple categories

Generating 100 products for catalog...
Generated 100 products successfully

Starting bulk product creation: 100 products
Batch size: 100 products per request

Batch 1/1: Processing 100 products
Batch 1 complete: 100 products created in 2.34s
Progress: 100/100 (100.0%)

======================================================================
PRODUCT CATALOG CREATION SUMMARY
======================================================================
Successfully created: 100 products
Failed: 0 products
Success rate: 100.0%

View in HubSpot: https://app.hubspot.com/products-library
======================================================================
```

**Configuration:**
Edit `TOTAL_PRODUCTS` variable in the file to create more or fewer products.

**Categories Generated:**
1. **Software Licenses** ($10K-$15K) - Enterprise Suite, Professional Edition, etc.
2. **Professional Services** ($15K-$25K) - Implementation, Consulting, Training
3. **Support Contracts** ($5K-$8K) - Premium Support, 24/7 Support, etc.
4. **Hardware** ($2K-$3.5K) - Servers, Workstations, Laptops
5. **Cloud Services** ($500-$900) - Hosting, Storage, Compute
6. **Subscription Services** ($1K-$1.8K) - Monthly/Annual Plans

**SKU Format:** `[CATEGORY_CODE]-[4-DIGIT-NUMBER]`
- Example: SL-0001, PS-0023, SC-0045

**Performance:**
- 100 products: ~2-5 seconds
- 500 products: ~10-20 seconds
- No Claude API costs (utility only)

**Note:** This is a utility (no AI) - generates products programmatically without Claude enrichment.

---

### email_synthesizer.py
Generates realistic, messy email conversations for testing the Email Intelligence Agent.

**Usage:**
```bash
python utilities/email_synthesizer.py
```

**What it creates:**
- 3 email conversation files in `data/email_conversations/`
- Each conversation uses Claude AI to generate realistic business emails

**Output Files:**
1. **enterprise_software_deal.txt**
   - 8-10 email exchanges
   - 3-4 participants
   - Complex negotiation with multiple products
   - Budget discussions ($100k → $75k)
   - Timeline pressures and decision-making
   
2. **hardware_services_deal.txt**
   - 5-7 email exchanges
   - 2-3 participants
   - Hardware purchase with services
   - Volume discounts
   - Delivery timeline concerns
   
3. **professional_services_deal.txt**
   - 6-8 email exchanges
   - 3 participants
   - Consulting engagement
   - Scope discussions
   - Hourly vs fixed pricing

**Example Output:**
```
======================================================================
EMAIL CONVERSATION SYNTHESIZER
======================================================================

Generating realistic email conversations for testing...

1. Generating enterprise software deal conversation...
✅ Saved: data/email_conversations/enterprise_software_deal.txt
   Length: 13752 characters

2. Generating hardware + services deal conversation...
✅ Saved: data/email_conversations/hardware_services_deal.txt
   Length: 9834 characters

3. Generating professional services deal conversation...
✅ Saved: data/email_conversations/professional_services_deal.txt
   Length: 11245 characters

======================================================================
SYNTHESIS COMPLETE
======================================================================

Generated 3 realistic email conversations
These conversations can now be used with email_intelligence_agent.py
======================================================================
```

**Conversation Characteristics:**

**Signal (Valuable Data):**
- Contact names, titles, emails
- Company information
- Product requirements
- Budget numbers
- Timeline constraints
- Pricing negotiations

**Noise (Realistic Clutter):**
- Short responses ("Thanks!", "Sounds good!")
- Scheduling conflicts
- Personal remarks
- Off-topic discussions
- Informal language
- Multiple threads mixed

**Use With:**
- `agents/email_intelligence_reader.py` - See extraction without creating records
- `agents/email_intelligence_agent.py` - Create full pipeline in HubSpot

**Cost:** ~$0.01-$0.02 per run (Claude API to generate conversations)

---

## When to Use Utilities vs Agents

### Use Utilities When:
- ✅ Quickly checking if data exists
- ✅ Inspecting recent records
- ✅ Verifying API connectivity
- ✅ Debugging issues
- ✅ No AI enrichment needed
- ✅ Generating test data
- ✅ Instant results

### Use Agents When:
- ✅ Creating new records
- ✅ Bulk operations
- ✅ Data enrichment needed
- ✅ Intelligent processing required
- ✅ Complex workflows

---

## Common Use Cases

### Quick Health Check
```bash
python utilities/verify_contacts.py
python utilities/verify_companies.py
python utilities/verify_deals.py
```

### Verify Recent Bulk Operations
After running a bulk agent, verify the results:
```bash
python agents/contact_creator_agent.py
python utilities/verify_contacts.py
```

### Check Product Catalog
```bash
python utilities/verify_products.py
```

### Setup Product Catalog
```bash
python utilities/product_catalog_generator.py
python utilities/verify_products.py
```

### Test Email Intelligence
```bash
# Generate test conversations
python utilities/email_synthesizer.py

# Extract intelligence without creating records
python agents/email_intelligence_reader.py

# Verify what exists
python utilities/verify_contacts.py
python utilities/verify_deals.py
```

---

## Extending Utilities

To create a new utility script:

1. Create file in `utilities/` folder
2. Import HubSpot client (no Claude needed)
3. Query the API
4. Display results

**Template:**
```python
"""
Description of what this utility does
"""

import os
from hubspot import HubSpot
from dotenv import load_dotenv

load_dotenv()
hubspot = HubSpot(access_token=os.getenv('HUBSPOT_API_KEY'))

try:
    response = hubspot.crm.OBJECT.basic_api.get_page(limit=20)
    
    print(f"\nTotal found: {response.total}")
    
    for item in response.results:
        print(f"ID: {item.id}")
        # Display properties
        
except Exception as e:
    print(f"Error: {e}")
```

---

## Performance Comparison

| Utility | Speed | AI Cost | Use Case |
|---------|-------|---------|----------|
| verify_contacts.py | <1 sec | $0 | Quick check |
| verify_companies.py | <1 sec | $0 | Quick check |
| verify_deals.py | <1 sec | $0 | Quick check |
| verify_quotes.py | <1 sec | $0 | Quick check |
| verify_products.py | <1 sec | $0 | Quick check |
| product_catalog_generator.py | 2-5 sec | $0 | Setup catalog |
| email_synthesizer.py | 10-20 sec | ~$0.015 | Generate test data |

---

## Troubleshooting

### Common Issues

**"Module not found" Error:**
```bash
source venv/bin/activate
pip install hubspot-api-client python-dotenv anthropic
```

**"API key not found" Error:**
```bash
cat .env  # Verify HUBSPOT_API_KEY exists
```

**No results showing:**
- Verify you have created records in HubSpot
- Check that scopes are enabled
- Regenerate access token if scopes were added

**Product catalog generator fails:**
- Ensure `crm.objects.products.write` scope enabled
- Regenerate access token
- Check for existing products with same SKUs

**Email synthesizer fails:**
- Verify `ANTHROPIC_API_KEY` in .env
- Check Claude API limits/credits

---

## Related Documentation

- [Email Intelligence Agent](email_intelligence_agent.md)
- [Product Catalog Generator](product_catalog_generator.md)
- [Contact Creator Agent](contact_creator_agent.md)
- [Quote CPQ Agent](quote_cpq_agent.md)