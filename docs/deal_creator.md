# Flexible Deal Creator Agent Documentation

## Overview

The Flexible Deal Creator Agent creates deal/opportunity records in HubSpot CRM. This agent operates in two modes: single deal creation for manual operations, or bulk creation for processing hundreds or thousands of deals. It uses Claude AI for optional data enrichment.

## Purpose

This agent demonstrates:
- Flexible design supporting both single and bulk deal creation
- AI-powered deal data enrichment and forecasting
- Batch processing with rate limiting
- Working with HubSpot deal pipelines and stages
- Probability calculations and close date estimation

## File Location

`agents/deal_creator.py`

## Dual Mode Operation

### Single Mode
- Creates one deal at a time
- Full Claude AI enrichment available
- Best for manual deal entry
- Immediate results with detailed output

### Bulk Mode
- Creates hundreds or thousands of deals
- Batch API processing (100 deals per request)
- Optional sample enrichment (first 10 deals)
- Progress tracking and error handling
- Production-ready for large datasets

## How to Use

### Configuration

At the bottom of the file, adjust these settings:
```python
MODE = "single"              # "single" or "bulk"
TOTAL_DEALS = 100            # For bulk mode: how many to create
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
python agents/deal_creator.py
```

**Expected Output:**
```
======================================================================
FLEXIBLE DEAL CREATOR
======================================================================

Mode: SINGLE
Claude enrichment: Enabled

======================================================================
SINGLE DEAL MODE
======================================================================

Processing: Enterprise Software License - Acme Corp
  Enriching with Claude AI
  Enrichment complete
  Success: Deal ID 12345678

======================================================================
SUCCESS: Deal created in HubSpot
Deal ID: 12345678
View: https://app.hubspot.com/contacts/deal/12345678
======================================================================
```

### Bulk Mode Usage

**Configuration:**
```python
MODE = "bulk"
TOTAL_DEALS = 100
ENRICH_SAMPLE = False
```

**Run:**
```bash
python agents/deal_creator.py
```

**Expected Output:**
```
======================================================================
FLEXIBLE DEAL CREATOR
======================================================================

Mode: BULK
Claude enrichment: Disabled
Creating 100 deals

Generating 100 mock deals
Generated 100 deals successfully

Starting bulk creation of 100 deals
Batch size: 100 deals per request
======================================================================

Batch 1/1: Processing 100 deals
Batch 1 complete: 100 deals created in 2.45s
Progress: 100/100 (100.0%)

======================================================================
BULK CREATION SUMMARY
======================================================================
Successfully created: 100 deals
Failed: 0 deals
Success rate: 100.0%

View in HubSpot: https://app.hubspot.com/contacts/deals
======================================================================
```

## Code Structure

### Main Components

1. **Configuration Constants**
   - BATCH_SIZE: 100 (HubSpot limit)
   - RATE_LIMIT_DELAY: 0.5 seconds

2. **generate_mock_deals()**
   - Creates test data for bulk operations
   - Generates unique deal names and amounts

3. **enrich_deal_with_claude()**
   - Calls Claude AI for data enrichment
   - Returns close date, priority, deal type, probability

4. **create_single_deal()**
   - Handles single deal creation
   - Optional enrichment
   - Returns HubSpot deal ID

5. **create_deals_in_batches()**
   - Batch API processing
   - Rate limiting
   - Progress tracking
   - Error handling

6. **main()**
   - Mode selection
   - Orchestrates single or bulk flow

## Claude AI Enrichment

When enrichment is enabled, Claude analyzes each deal and provides:

### Close Date Prediction
- Realistic close date based on deal stage
- Typically 30-90 days from current date
- Format: YYYY-MM-DD

### Deal Priority
- Assessed based on deal size and stage
- Values: high, medium, low
- Helps sales prioritize efforts

### Deal Type Classification
- newbusiness: New customer acquisition
- existingbusiness: Expansion/upsell to existing customer
- newbusiness_from_existing: New division/unit of existing customer

### Probability to Close
- Estimated likelihood of closing (0-100%)
- Converted to decimal (0-1) for HubSpot
- Based on deal stage and characteristics

## HubSpot Field Requirements

### Deal Stage
Must match your pipeline configuration. Common stages:
- appointmentscheduled
- qualifiedtobuy
- presentationscheduled
- decisionmakerboughtin
- contractsent
- closedwon
- closedlost

### Pipeline
Default: "default"
Custom pipelines require specific pipeline IDs from your HubSpot account.

### Amount
Numeric value as string:
- Correct: "50000"
- Incorrect: "$50,000"

### Priority
Must be lowercase:
- Correct: "high", "medium", "low"
- Incorrect: "HIGH", "Medium"

### Deal Stage Probability
Decimal value between 0 and 1:
- Correct: "0.75" (75%)
- Incorrect: "75"

## Use Cases

### When to Use Single Mode

- Creating individual deals manually
- High-value enterprise deals requiring attention
- Testing deal creation workflow
- Learning how the agent works
- Deals requiring full AI enrichment

### When to Use Bulk Mode

- Importing deals from spreadsheets
- Migrating from another CRM
- Creating pipeline from trade show leads
- Generating test data for development
- Production deal operations (100+ deals)

## Customization

### Modifying Test Deal (Single Mode)

Edit the SINGLE_DEAL dictionary:
```python
SINGLE_DEAL = {
    "dealname": "Your Deal Name",
    "amount": "75000",
    "pipeline": "default",
    "dealstage": "qualifiedtobuy"
}
```

### Changing Deal Count (Bulk Mode)
```python
TOTAL_DEALS = 500  # Create 500 deals
```

### Enabling Sample Enrichment (Bulk Mode)

To enrich the first 10 deals with Claude AI:
```python
MODE = "bulk"
TOTAL_DEALS = 500
ENRICH_SAMPLE = True  # Enrich first 10
```

This balances cost and quality.

### Loading from CSV (Production)

Replace `generate_mock_deals()` with CSV loading:
```python
import csv

def load_deals_from_csv(filename):
    deals = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            deal = {
                "dealname": row['Deal Name'],
                "amount": row['Amount'],
                "pipeline": row.get('Pipeline', 'default'),
                "dealstage": row.get('Stage', 'qualifiedtobuy')
            }
            deals.append(deal)
    return deals

# In main(), replace:
deals = load_deals_from_csv('deals.csv')
```

## Performance

### Single Mode
- 2-4 seconds per deal with enrichment
- 1-2 seconds per deal without enrichment

### Bulk Mode
- 100 deals: 5-10 seconds
- 500 deals: 20-30 seconds
- 1000 deals: 40-60 seconds
- 10000 deals: 6-10 minutes

### Scaling
The agent can handle any number of deals:
- Under 100: Use single or bulk mode
- 100-1000: Use bulk mode
- 1000-10000: Use bulk mode, no enrichment
- 10000+: Use bulk mode, process in batches

## Cost Considerations

### Claude API Costs (with enrichment)

**Single Mode:**
- Per deal: ~$0.001-$0.002
- 10 deals: ~$0.01-$0.02
- 100 deals: ~$0.10-$0.20

**Bulk Mode with Sample Enrichment:**
- First 10 enriched: ~$0.02
- Remaining deals: $0
- Total for 1000 deals: ~$0.02

**Bulk Mode without Enrichment:**
- Free (no Claude calls)

### HubSpot Costs
- API usage: Free within plan limits
- Deal storage: Depends on subscription tier

## Error Handling

### Common Errors

**Invalid Deal Stage:**
```
Error: "stage123 is not a valid deal stage"
```
Solution: Use valid stage from your pipeline configuration

**Invalid Priority Value:**
```
Error: "HIGH was not one of the allowed options"
```
Solution: Use lowercase: high, medium, low

**Invalid Probability:**
```
Error: "75 is not a valid probability value"
```
Solution: Agent automatically converts percentage to decimal

**Pipeline Not Found:**
```
Error: "Pipeline does not exist"
```
Solution: Use "default" or verify custom pipeline ID

### Batch Failure Handling

If a batch fails:
- Error is logged
- Failed count increases
- Processing continues with next batch
- Final summary shows total failures

## Best Practices

### Start Small
When first using bulk mode:
1. Test with 10 deals
2. Verify in HubSpot
3. Scale to 100
4. Then process full dataset

### Data Validation
Before bulk processing:
- Validate deal amounts (numeric strings)
- Check deal stages match your pipeline
- Ensure deal names are unique
- Verify data quality

### Enrichment Strategy
- Single mode: Always enrich (fast and valuable)
- Bulk under 100: Enrich all if budget allows
- Bulk 100-1000: Enrich sample only
- Bulk 1000+: Skip enrichment, use existing data

### Testing
Create test deals with unique names:
```python
test_dealname = f"TEST - Deal {int(time.time())}"
```

Delete test deals from HubSpot after verification.

## API Requirements

### HubSpot Scopes
Your Private App needs:
- `crm.objects.deals.read`
- `crm.objects.deals.write`

### Rate Limits
- Free/Starter: 100 requests per 10 seconds
- Professional/Enterprise: Higher limits

The agent respects these limits with automatic delays.

## Advanced Features

### Associating Deals with Contacts/Companies

To link deals to contacts or companies, add associations:
```python
# After creating deal, associate with contact
hubspot.crm.deals.associations_api.create(
    deal_id=api_response.id,
    to_object_type="contacts",
    to_object_id=contact_id,
    association_type="deal_to_contact"
)
```

### Custom Deal Properties

Add custom fields to properties dictionary:
```python
properties = {
    "dealname": deal_data['dealname'],
    "amount": deal_data['amount'],
    # Custom fields
    "competitor": "CompetitorCo",
    "lead_source": "Trade Show",
    "deal_owner": "12345"  # HubSpot user ID
}
```

## Troubleshooting

### Single Mode Not Working
1. Check API keys in .env file
2. Verify HubSpot Private App scopes
3. Test with ENRICH_WITH_CLAUDE = False
4. Check error messages

### Bulk Mode Failing
1. Start with TOTAL_DEALS = 10
2. Check batch error messages
3. Verify deal stage names
4. Ensure amounts are numeric strings

### All Deals Failing
1. Invalid API key
2. Missing permissions
3. Network issues
4. Invalid pipeline or stage values

## Limitations

1. **Mock Data Only**
   - Current version generates test data
   - Production needs CSV or database integration

2. **No Duplicate Detection**
   - Does not check if deal exists
   - May create duplicate deal names

3. **Basic Fields Only**
   - Uses standard HubSpot fields
   - Custom properties not included by default

4. **No Deal Associations**
   - Deals not linked to contacts/companies
   - Requires additional API calls

## Next Steps

After mastering this agent:

1. **CSV Integration**: Load real deal data from files
2. **Database Integration**: Connect to your CRM or database
3. **Deal Associations**: Link deals to contacts and companies
4. **Product Line Items**: Add products to deals
5. **Deal Stages**: Update deals through pipeline stages
6. **Custom Properties**: Add your HubSpot custom fields

## Related Documentation

- [Contact Creator](contact_creator.md)
- [Account Creator](account_creator.md)
- [Bulk Contact Creator](bulk_contact_creator.md)
- [HubSpot Deals API](https://developers.hubspot.com/docs/api/crm/deals)