# Account Creator Agent Documentation

## Overview

The Account Creator Agent creates company/account records in HubSpot CRM with AI-powered enrichment. This agent operates in two modes: single account creation for manual operations, or bulk creation for processing hundreds or thousands of companies. It uses Claude AI to enrich company data intelligently.

## Purpose

This agent demonstrates:
- Flexible design supporting both single and bulk account creation
- AI-powered company data enrichment
- Industry classification and revenue estimation
- Batch processing with rate limiting
- Production-ready company record management

## File Location

`agents/account_creator_agent.py`

## Dual Mode Operation

### Single Mode
- Creates one company at a time
- Full Claude AI enrichment available
- Best for manual account entry
- Immediate results with detailed output

### Bulk Mode
- Creates hundreds or thousands of companies
- Batch API processing (100 companies per request)
- Optional sample enrichment (first 10 companies)
- Progress tracking and error handling
- Production-ready for large datasets

## How to Use

### Configuration

At the bottom of the file, adjust these settings:
```python
MODE = "single"              # "single" or "bulk"
TOTAL_COMPANIES = 100        # For bulk mode: how many to create
ENRICH_WITH_CLAUDE = True    # For single: whether to enrich
ENRICH_SAMPLE = False        # For bulk: enrich first 10 only
```

### Single Mode Usage

**Configuration:**
```python
MODE = "single"
ENRICH_WITH_CLAUDE = True
```

**Run:**
```bash
python agents/account_creator_agent.py
```

**Expected Output:**
```
======================================================================
FLEXIBLE ACCOUNT CREATOR
======================================================================

Mode: SINGLE
Claude enrichment: Enabled

======================================================================
SINGLE ACCOUNT MODE
======================================================================

Processing: TechFlow Industries
  Enriching with Claude AI
  Enrichment complete
  Success: Company ID 987654321

======================================================================
SUCCESS: Company created in HubSpot
Company ID: 987654321
View: https://app.hubspot.com/contacts/company/987654321
======================================================================
```

### Bulk Mode Usage

**Configuration:**
```python
MODE = "bulk"
TOTAL_COMPANIES = 100
ENRICH_SAMPLE = False
```

**Run:**
```bash
python agents/account_creator_agent.py
```

**Expected Output:**
```
======================================================================
FLEXIBLE ACCOUNT CREATOR
======================================================================

Mode: BULK
Claude enrichment: Disabled
Creating 100 companies

Generating 100 mock companies
Generated 100 companies successfully

Starting bulk creation of 100 companies
Batch size: 100 companies per request
======================================================================

Batch 1/1: Processing 100 companies
Batch 1 complete: 100 companies created in 2.67s
Progress: 100/100 (100.0%)

======================================================================
BULK CREATION SUMMARY
======================================================================
Successfully created: 100 companies
Failed: 0 companies
Success rate: 100.0%

View in HubSpot: https://app.hubspot.com/contacts/companies
======================================================================
```

## Claude AI Enrichment

When enrichment is enabled, Claude analyzes each company and provides:

### Industry Classification
- Accurate industry categorization
- Based on company name and context
- Uses standard industry codes
- Examples: "Technology", "Healthcare", "Manufacturing"

### Company Size Estimation
- Employee count estimation
- Based on company type and context
- Ranges: 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+

### Revenue Estimation
- Annual revenue prediction
- Based on company size and industry
- Realistic ranges for company type
- Examples: $5M, $20M, $100M

### Business Description
- Clear, concise company description
- Explains what the company does
- Professional language
- 1-2 sentences

## Company Data Structure

### Required Fields
- **name**: Company name (required)
- **domain**: Company website domain

### Optional Fields (AI-Enhanced)
- **industry**: Industry classification
- **numberofemployees**: Employee count estimate
- **annualrevenue**: Revenue estimate
- **description**: Business description
- **city**: Location
- **state**: State/Province
- **country**: Country

## Use Cases

### When to Use Single Mode

- Creating individual companies manually
- High-value enterprise accounts
- Testing company creation workflow
- Learning how the agent works
- Companies requiring full AI enrichment

### When to Use Bulk Mode

- Importing companies from spreadsheets
- Migrating from another CRM
- Creating accounts from trade show leads
- Generating test data for development
- Production company operations (100+ companies)

## Performance

### Single Mode
- 2-4 seconds per company with enrichment
- 1-2 seconds per company without enrichment

### Bulk Mode
- 100 companies: 5-10 seconds
- 500 companies: 20-30 seconds
- 1000 companies: 40-60 seconds
- 10000 companies: 6-10 minutes

## Cost Considerations

### Claude API Costs (with enrichment)

**Single Mode:**
- Per company: ~$0.001-$0.002
- 10 companies: ~$0.01-$0.02
- 100 companies: ~$0.10-$0.20

**Bulk Mode with Sample Enrichment:**
- First 10 enriched: ~$0.02
- Remaining companies: $0
- Total for 1000 companies: ~$0.02

**Bulk Mode without Enrichment:**
- Free (no Claude calls)

### HubSpot Costs
- API usage: Free within plan limits
- Company storage: Depends on subscription tier

## Customization

### Modifying Test Company (Single Mode)

Edit the SINGLE_COMPANY dictionary:
```python
SINGLE_COMPANY = {
    "name": "Your Company Name",
    "domain": "yourcompany.com",
    "city": "San Francisco",
    "state": "California",
    "country": "United States"
}
```

### Changing Company Count (Bulk Mode)
```python
TOTAL_COMPANIES = 500  # Create 500 companies
```

### Enabling Sample Enrichment (Bulk Mode)

To enrich the first 10 companies with Claude AI:
```python
MODE = "bulk"
TOTAL_COMPANIES = 500
ENRICH_SAMPLE = True  # Enrich first 10
```

### Loading from CSV (Production)

Replace `generate_mock_companies()` with CSV loading:
```python
import csv

def load_companies_from_csv(filename):
    companies = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            company = {
                "name": row['Company Name'],
                "domain": row.get('Domain', ''),
                "industry": row.get('Industry', ''),
                "city": row.get('City', ''),
                "state": row.get('State', ''),
                "country": row.get('Country', 'United States')
            }
            companies.append(company)
    return companies

# In main(), replace:
companies = load_companies_from_csv('companies.csv')
```

## HubSpot Field Requirements

### Company Name
- Required field
- Should be unique
- Example: "TechFlow Industries"

### Domain
- Company website domain
- Format: "techflow.com" (no http://)
- Used for deduplication

### Industry
- Standard industry names
- Examples: "Technology", "Healthcare", "Finance"
- HubSpot has predefined industry list

### Number of Employees
- String representation of number
- Examples: "50", "200", "1000"
- Or use ranges: "51-200"

### Annual Revenue
- Numeric value as string
- Examples: "5000000", "20000000"
- No currency symbols or commas

## Error Handling

### Common Errors

**Duplicate Domain:**
```
Error: Company with domain already exists
```
Solution: HubSpot uses domain for deduplication. Check existing companies.

**Invalid Industry:**
```
Error: Industry value not recognized
```
Solution: Use standard HubSpot industry values.

**Missing Company Name:**
```
Error: Name is required
```
Solution: Ensure all companies have names.

### Batch Failure Handling

If a batch fails:
- Error is logged
- Failed count increases
- Processing continues with next batch
- Final summary shows total failures

## Best Practices

### Start Small
When first using bulk mode:
1. Test with 10 companies
2. Verify in HubSpot
3. Scale to 100
4. Then process full dataset

### Data Validation
Before bulk processing:
- Ensure company names are present
- Validate domain formats
- Check for duplicate domains
- Verify data quality

### Enrichment Strategy
- Single mode: Always enrich (fast and valuable)
- Bulk under 100: Enrich all if budget allows
- Bulk 100-1000: Enrich sample only
- Bulk 1000+: Skip enrichment, use existing data

## API Requirements

### HubSpot Scopes
Your Private App needs:
- `crm.objects.companies.read`
- `crm.objects.companies.write`

### Rate Limits
- Free/Starter: 100 requests per 10 seconds
- Professional/Enterprise: Higher limits

The agent respects these limits with automatic delays.

## Advanced Features

### Associating Companies with Contacts

After creating companies, associate with contacts:
```python
# After creating company, associate with contact
hubspot.crm.companies.associations_api.create(
    company_id=company.id,
    to_object_type="contacts",
    to_object_id=contact_id,
    association_type="company_to_contact"
)
```

### Custom Company Properties

Add custom fields to properties dictionary:
```python
properties = {
    "name": company_data['name'],
    "domain": company_data['domain'],
    # Custom fields
    "company_tier": "Enterprise",
    "lead_source": "Trade Show",
    "account_owner": "12345"  # HubSpot user ID
}
```

## Troubleshooting

### Single Mode Not Working
1. Check API keys in .env file
2. Verify HubSpot Private App scopes
3. Test with ENRICH_WITH_CLAUDE = False
4. Check error messages

### Bulk Mode Failing
1. Start with TOTAL_COMPANIES = 10
2. Check batch error messages
3. Verify company names are present
4. Ensure domains are valid

### All Companies Failing
1. Invalid API key
2. Missing permissions
3. Network issues
4. Invalid field values

## Related Documentation

- [Contact Creator Agent](contact_creator_agent.md)
- [Deal Creator Agent](deal_creator_agent.md)
- [Quote CPQ Agent](quote_cpq_agent.md)
- [HubSpot Companies API](https://developers.hubspot.com/docs/api/crm/companies)