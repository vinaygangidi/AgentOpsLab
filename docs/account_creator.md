# Flexible Account Creator Agent Documentation

## Overview

The Flexible Account Creator Agent creates company/account records in HubSpot CRM. This agent can operate in two modes: single company creation for manual/testing purposes, or bulk creation for processing hundreds or thousands of companies. It uses Claude AI for optional data enrichment.

## Purpose

This agent demonstrates:
- Flexible design supporting both single and bulk operations
- Company/account creation in HubSpot
- AI-powered company data enrichment
- Batch processing with rate limiting
- Working with HubSpot's strict field requirements

## File Location

`agents/account_creator.py`

## Dual Mode Operation

### Single Mode
- Creates one company at a time
- Full Claude AI enrichment available
- Best for manual creation and testing
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
python agents/account_creator.py
```

**Expected Output:**
```
======================================================================
FLEXIBLE HUBSPOT ACCOUNT CREATOR
======================================================================

Mode: SINGLE
Claude enrichment: Enabled

======================================================================
SINGLE COMPANY MODE
======================================================================

Processing: TechVision Solutions
  Enriching with Claude AI
  Enrichment complete
  Success: Company ID 314517870288

======================================================================
SUCCESS: Company created in HubSpot
Company ID: 314517870288
View: https://app.hubspot.com/contacts/company/314517870288
======================================================================
```

### Bulk Mode Usage

**Configuration:**
```python
MODE = "bulk"
TOTAL_COMPANIES = 500
ENRICH_SAMPLE = False
```

**Run:**
```bash
python agents/account_creator.py
```

**Expected Output:**
```
======================================================================
FLEXIBLE HUBSPOT ACCOUNT CREATOR
======================================================================

Mode: BULK
Claude enrichment: Disabled
Creating 500 companies

Generating 500 mock companies
Generated 500 companies successfully

Starting bulk creation of 500 companies
Batch size: 100 companies per request
======================================================================

Batch 1/5: Processing 100 companies
Batch 1 complete: 100 companies created in 2.34s
Progress: 100/500 (20.0%)
Waiting 0.5s before next batch

[... continues for all batches ...]

======================================================================
BULK CREATION SUMMARY
======================================================================
Successfully created: 500 companies
Failed: 0 companies
Success rate: 100.0%

View in HubSpot: https://app.hubspot.com/contacts
======================================================================
```

## Code Structure

### Main Components

1. **Configuration Constants**
   - BATCH_SIZE: 100 (HubSpot limit)
   - RATE_LIMIT_DELAY: 0.5 seconds

2. **generate_mock_companies()**
   - Creates test data for bulk operations
   - Generates unique company names and domains

3. **enrich_company_with_claude()**
   - Calls Claude AI for data enrichment
   - Returns industry, employees, revenue, type, description

4. **create_single_company()**
   - Handles single company creation
   - Optional enrichment
   - Returns HubSpot company ID

5. **create_companies_in_batches()**
   - Batch API processing
   - Rate limiting
   - Progress tracking
   - Error handling

6. **main()**
   - Mode selection
   - Orchestrates single or bulk flow

## Use Cases

### When to Use Single Mode

- Testing the agent
- Creating individual high-value accounts
- Manual data entry with AI assistance
- Learning how the agent works
- Verifying API credentials

### When to Use Bulk Mode

- Importing company lists from spreadsheets
- Migrating from another CRM
- Processing leads from trade shows or events
- Creating test data for development
- Production data operations (100+ companies)

## Customization

### Modifying Test Company (Single Mode)

Edit the SINGLE_COMPANY dictionary:
```python
SINGLE_COMPANY = {
    "name": "Your Company",
    "domain": "yourcompany.com",
    "phone": "5551234567",
    "city": "Boston",
    "state": "Massachusetts"
}
```

### Changing Company Count (Bulk Mode)
```python
TOTAL_COMPANIES = 1000  # Create 1000 companies
```

### Enabling Sample Enrichment (Bulk Mode)

To enrich the first 10 companies with Claude AI:
```python
MODE = "bulk"
TOTAL_COMPANIES = 500
ENRICH_SAMPLE = True  # Enrich first 10
```

This balances cost and quality by enriching a representative sample.

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
                "domain": row['Domain'],
                "phone": row.get('Phone', ''),
                "city": row.get('City', ''),
                "state": row.get('State', '')
            }
            companies.append(company)
    return companies

# In main(), replace:
companies = load_companies_from_csv('companies.csv')
```

## HubSpot Field Requirements

### Industry Field
Must be exact enum value:
- COMPUTER_SOFTWARE
- INFORMATION_TECHNOLOGY_AND_SERVICES
- INTERNET
- TELECOMMUNICATIONS
- FINANCIAL_SERVICES
- MARKETING_AND_ADVERTISING
- MANAGEMENT_CONSULTING

### Number of Employees
Must be numeric:
- Correct: 250
- Incorrect: "Medium"

### Annual Revenue
Must be numeric in dollars:
- Correct: 10000000
- Incorrect: "$10M"

### Company Type
Must be one of:
- PROSPECT
- PARTNER
- RESELLER
- VENDOR
- OTHER

## Performance

### Single Mode
- 2-4 seconds per company with enrichment
- 1-2 seconds per company without enrichment

### Bulk Mode
- 100 companies: 5-10 seconds
- 500 companies: 20-30 seconds
- 1000 companies: 40-60 seconds
- 10000 companies: 6-10 minutes

### Scaling
The agent can handle any number of companies:
- Under 100: Use single or bulk mode
- 100-1000: Use bulk mode
- 1000-10000: Use bulk mode, no enrichment
- 10000+: Use bulk mode, process in multiple runs if needed

## Cost Considerations

### Claude API Costs (with enrichment)

**Single Mode:**
- Per company: ~$0.002
- 10 companies: ~$0.02
- 100 companies: ~$0.20

**Bulk Mode with Sample Enrichment:**
- First 10 enriched: ~$0.02
- Remaining companies: $0
- Total for 1000 companies: ~$0.02

**Bulk Mode without Enrichment:**
- Free (no Claude calls)

### HubSpot Costs
- API usage: Free within plan limits
- Company storage: Depends on subscription tier

## Error Handling

### Common Errors

**Invalid Field Value:**
```
Error: "Software was not one of the allowed options"
```
Solution: Claude must return exact HubSpot enum values

**Duplicate Domain:**
```
Error: "Company with domain already exists"
```
Solution: HubSpot prevents duplicate domains, check existing first

**Rate Limit Exceeded:**
```
Error: "Rate limit exceeded"
```
Solution: Increase RATE_LIMIT_DELAY or wait before retrying

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
- Remove duplicate domains
- Validate required fields (name, domain)
- Check domain format
- Ensure data quality

### Enrichment Strategy
- Single mode: Always enrich (it's fast)
- Bulk under 100: Enrich all if budget allows
- Bulk 100-1000: Enrich sample only
- Bulk 1000+: Skip enrichment, use existing data

### Testing
Create test companies with unique domains:
```python
test_domain = f"test-{int(time.time())}.com"
```

Delete test companies from HubSpot after verification.

## API Requirements

### HubSpot Scopes
Your Private App needs:
- `crm.objects.companies.read`
- `crm.objects.companies.write`

### Rate Limits
- Free/Starter: 100 requests per 10 seconds
- Professional/Enterprise: Higher limits

The agent respects these limits with automatic delays.

## Troubleshooting

### Single Mode Not Working
1. Check API keys in .env file
2. Verify HubSpot Private App scopes
3. Test with ENRICH_WITH_CLAUDE = False
4. Check error messages

### Bulk Mode Failing
1. Start with TOTAL_COMPANIES = 10
2. Check batch error messages
3. Verify data format
4. Ensure no duplicate domains

### All Companies Failing
1. Invalid API key
2. Missing permissions
3. Network issues
4. Check HubSpot status page

## Limitations

1. **Mock Data Only**
   - Current version generates test data
   - Production needs CSV or database integration

2. **No Duplicate Detection**
   - Does not check if company exists
   - HubSpot will reject duplicate domains

3. **Basic Fields Only**
   - Uses standard HubSpot fields
   - Custom properties not included

4. **No Rollback**
   - Cannot undo bulk creation
   - Must delete from HubSpot manually if needed

## Next Steps

After mastering this agent:

1. **CSV Integration**: Load real company data from files
2. **Database Integration**: Connect to your CRM or database
3. **Contact Association**: Link contacts to their companies
4. **Deal Creation**: Create opportunities for companies
5. **Duplicate Detection**: Check before creating
6. **Custom Fields**: Add your HubSpot custom properties

## Related Documentation

- [Contact Creator](contact_creator.md)
- [Real HubSpot Contact Creator](hubspot_contact_real.md)
- [Bulk Contact Creator](bulk_contact_creator.md)
- [HubSpot Companies API](https://developers.hubspot.com/docs/api/crm/companies)