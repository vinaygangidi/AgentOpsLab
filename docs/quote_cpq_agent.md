# Quote CPQ Agent Documentation

## Overview

The Quote CPQ Agent is a complete Configure-Price-Quote system that creates production-ready quotes with products, line items, pricing, discounts, and automatic total calculations. Unlike simple quote creators, this system creates complete deals with full product configurations ready for order conversion.

## Purpose

This agent demonstrates:
- Product catalog management
- Deal creation with line items
- Automatic pricing calculations
- Discount handling
- Full CPQ (Configure, Price, Quote) workflow
- Association management between products, line items, and deals

## File Location

`agents/quote_cpq_agent.py`

## Architecture

### The Complete Quote Workflow
```
1. Create/Get Products → 2. Create Deal → 3. Add Line Items → 4. Calculate Totals
```

**Why This Architecture:**
- Products live in HubSpot catalog (reusable)
- Line items attach to deals (not quotes directly)
- Deal totals calculate automatically from line items
- Ready to convert to invoices/orders

## How to Use

### Basic Usage

The system includes a working example in `main()`:
```bash
python agents/quote_cpq_agent.py
```

This creates a deal with:
- Enterprise Software License: $25,000 (10% discount) = $22,500
- Professional Services: $15,000
- Annual Support: $5,000
- **Total: $42,500**

### Custom Quote Creation

Edit the `products_to_quote` list in `main()`:
```python
products_to_quote = [
    {
        'product': {
            'name': 'Your Product Name',
            'description': 'Product description',
            'price': 10000,
            'sku': 'PROD-001',
            'cost': 4000
        },
        'quantity': 2,
        'price': 10000,  # Can override product price
        'discount': 15   # 15% discount
    }
]
```

## Function Reference

### create_product(product_data)

Creates or retrieves a product from HubSpot catalog.

**Parameters:**
```python
product_data = {
    'name': 'Product Name',
    'description': 'Product description',
    'price': 10000,
    'sku': 'UNIQUE-SKU',
    'cost': 4000  # Cost of goods sold
}
```

**Returns:** HubSpot product object or None

**Behavior:**
- Attempts to create product
- If SKU exists, searches for and returns existing product
- Prevents duplicate products in catalog

---

### create_deal_with_line_items(deal_data, line_items_data)

Creates a complete deal with products and pricing.

**Parameters:**
```python
deal_data = {
    'dealname': 'Deal Name',
    'dealstage': 'qualifiedtobuy',
    'pipeline': 'default',
    'closedate': '2026-05-15'
}

line_items_data = [
    {
        'product': { ... },  # Product info
        'quantity': 2,
        'price': 10000,
        'discount': 10  # Optional
    }
]
```

**Returns:** (deal_object, list_of_line_items)

**Process:**
1. Creates/gets all products
2. Creates the deal
3. Creates line items with pricing
4. Associates line items to deal
5. Calculates and updates deal total

---

### enrich_deal_with_claude(deal_data, line_items_data)

Uses Claude AI to suggest deal improvements.

**Returns:**
```python
{
    'CLOSEDATE': '2026-05-15',
    'DEALSTAGE': 'presentationscheduled',
    'PROBABILITY': '75',
    'RECOMMENDATION': 'AI recommendation text'
}
```

**AI Analysis:**
- Appropriate close date (30-60 days out)
- Suggested deal stage
- Win probability assessment
- Strategic recommendations

---

### create_complete_quote(deal_name, products_list, enrich=True)

Main orchestration function. Creates complete quote with all components.

**Example:**
```python
result = create_complete_quote(
    deal_name="Q1 2026 Enterprise Deal - Acme Corp",
    products_list=products_to_quote,
    enrich=True
)

if result:
    print(f"Deal ID: {result['deal'].id}")
    print(f"Line Items: {len(result['line_items'])}")
```

## Example Output
```
======================================================================
COMPLETE QUOTE SYSTEM - WITH PRODUCTS AND PRICING
======================================================================

Enriching deal with Claude AI...
AI Recommendation: This is a solid enterprise deal...
Enrichment complete

======================================================================
Creating complete deal: Enterprise Software Package - Acme Corp Q1 2026
======================================================================

Step 1: Managing products...
Creating product: Enterprise Software License
  Product created: ID 302161796800

Step 2: Creating deal...
  Deal created: ID 317208424154

Step 3: Adding line items to deal...
  Adding line item 1/3...
    Line item added: $22500.00
  Adding line item 2/3...
    Line item added: $15000.00
  Adding line item 3/3...
    Line item added: $5000.00

  Total deal amount: $42500.00
  Deal amount updated

======================================================================
SUCCESS: Complete quote created!
======================================================================
Deal ID: 317208424154
View in HubSpot: https://app.hubspot.com/contacts/deal/317208424154
Total Line Items: 3
======================================================================
```

## What Gets Created in HubSpot

### 1. Products (in Catalog)
- Name, description, SKU
- Base price and cost
- Reusable across multiple deals

### 2. Deal
- Deal name, stage, pipeline
- Close date (AI-suggested or manual)
- Total amount (calculated from line items)

### 3. Line Items
- Product reference
- Quantity
- Unit price (can differ from catalog price)
- Discount percentage
- Line total (calculated)
- Associated to deal

### 4. Associations
- Line items → Products
- Line items → Deal
- All properly linked

## Pricing Calculations

### Line Item Total
```
Line Total = (Price × Quantity) × (1 - Discount%)
```

**Example:**
- Price: $25,000
- Quantity: 1
- Discount: 10%
- Line Total: $25,000 × 1 × 0.90 = $22,500

### Deal Total
```
Deal Total = Sum of all Line Totals
```

## HubSpot Requirements

### Required Scopes

Your HubSpot Private App needs:
- `crm.objects.products.read`
- `crm.objects.products.write`
- `crm.objects.deals.read`
- `crm.objects.deals.write`
- `crm.objects.line_items.read`
- `crm.objects.line_items.write`
- `e-commerce`

### HubSpot Plan

Most features work on all HubSpot tiers. Product library is available on all plans.

## Common Use Cases

### 1. Enterprise Software Sales
```python
products_to_quote = [
    {'product': {..., 'price': 50000}, 'quantity': 1, 'discount': 15},
    {'product': {..., 'price': 25000}, 'quantity': 1, 'discount': 0},
    {'product': {..., 'price': 10000}, 'quantity': 1, 'discount': 0}
]
```

### 2. Professional Services Packages
```python
products_to_quote = [
    {'product': {..., 'price': 15000}, 'quantity': 80, 'discount': 0},  # Hours
    {'product': {..., 'price': 5000}, 'quantity': 1, 'discount': 0}     # Materials
]
```

### 3. Hardware + Support Bundle
```python
products_to_quote = [
    {'product': {..., 'price': 2000}, 'quantity': 10, 'discount': 10},  # Laptops
    {'product': {..., 'price': 5000}, 'quantity': 1, 'discount': 0}     # Support
]
```

## Advanced Features

### Product Reuse

Products are created once and reused:
- First run: Creates products
- Subsequent runs: Finds and uses existing products
- No duplicate SKUs in catalog

### Discount Handling

Discounts are percentage-based:
- Applied per line item
- Calculated automatically
- Stored in line item record

### AI Enrichment

Claude provides:
- Realistic close dates based on deal size
- Appropriate deal stage suggestions
- Win probability estimates
- Strategic recommendations

## Integration with Other Agents

### Typical Workflow

1. **Contact Creator** → Create contact
2. **Account Creator** → Create company
3. **Associate** contact to company
4. **Quote CPQ Agent** → Create deal with products
5. **Associate** deal to company and contact
6. Send quote to customer
7. Convert to order when won

## Troubleshooting

### Products Not Creating

**Issue:** Product creation fails with SKU error

**Cause:** SKU already exists in catalog

**Solution:** This is expected! The code automatically finds and uses the existing product. This prevents duplicate products.

### Line Items Not Appearing

**Issue:** Deal created but no line items

**Cause:** Association API error

**Solution:** Check that all required scopes are enabled and token is regenerated after adding scopes.

### Deal Total is Zero

**Issue:** Deal amount shows $0

**Cause:** Amount update failed

**Solution:** Amount updates automatically. If it fails, manually update in HubSpot UI.

## Performance

- Product creation: 1-2 seconds each
- Deal creation: 1 second
- Line item creation: 0.5 seconds each
- Total time for 3-product quote: ~5 seconds

## Cost Considerations

### Claude API Costs

With enrichment enabled:
- Per quote: ~$0.001
- 100 quotes: ~$0.10
- 1000 quotes: ~$1.00

### HubSpot Costs

No additional costs. Uses standard API limits.

## Limitations

### Current Limitations

1. **No Quote PDF Generation**
   - Creates deal with line items
   - Quote PDF must be generated in HubSpot UI

2. **No Email Sending**
   - Quote must be sent manually from HubSpot
   - Or integrate with email API separately

3. **No Custom Line Item Properties**
   - Uses standard HubSpot line item fields only

4. **No Tax Calculations**
   - Totals are pre-tax
   - Tax must be calculated separately

## Future Enhancements

Potential additions:
- Bulk quote creation
- Quote templates
- Email sending integration
- PDF generation
- Tax calculations
- Multi-currency support
- Payment terms automation

## Best Practices

### 1. Product Naming

Use descriptive, unique names:
-  "Enterprise Software License - Annual"
- "Software"

### 2. SKU Management

Use systematic SKU format:
- "ENT-SW-2026-001"
- "SKU1"

### 3. Pricing Strategy

Set realistic prices:
- Include both price and cost
- Apply discounts at line item level
- Keep product catalog prices as "list price"

### 4. Deal Naming

Include customer and period:
- "Q1 2026 Enterprise Package - Acme Corp"
- "Deal 123"

## Related Documentation

- [Product Catalog Generator](product_catalog_generator.md)
- [Deal Creator Agent](deal_creator_agent.md)
- [Account Creator Agent](account_creator_agent.md)
- [Email Intelligence Agent](email_intelligence_agent.md)

## Support

For issues or questions:
1. Check HubSpot API scopes
2. Verify token is regenerated after scope changes
3. Review error messages for specific property errors
4. Check utilities to verify data creation