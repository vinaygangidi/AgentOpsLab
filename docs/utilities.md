# Utility Scripts Documentation

## Overview

The `utilities/` folder contains simple, non-AI scripts for verifying and inspecting data in HubSpot. These scripts use the HubSpot API directly without any Claude AI enrichment.

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

---

### product_catalog_generator.py
Generates and creates 100+ products in HubSpot catalog.

**Usage:**
```bash
python utilities/product_catalog_generator.py
```

**What it does:**
- Generates products across 6 categories
- Creates SKUs systematically
- Sets realistic pricing
- Bulk creates in HubSpot

**Output:**
- 100 products created (configurable)
- Categories: Software, Services, Support, Hardware, Cloud, Subscriptions
- Each with name, SKU, price, cost

**Note:** This is a utility (no AI) - generates products programmatically without Claude enrichment.

**Configuration:**
Edit `TOTAL_PRODUCTS` in the file to create more or fewer products.

---

## When to Use Utilities vs Agents

### Use Utilities When:
- Quickly checking if data exists
- Inspecting recent records
- Verifying API connectivity
- Debugging issues
- No AI enrichment needed

### Use Agents When:
- Creating new records
- Bulk operations
- Data enrichment needed
- Intelligent processing required
- Complex workflows

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
python agents/bulk_contact_creator.py
python utilities/verify_contacts.py
```

### Check Product Catalog
```bash
python utilities/verify_products.py
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