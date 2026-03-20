Solution: Don't try to set amount via API - it's calculated from line items

## Best Practices

### Quote Creation Workflow

1. **Run Agent** - Create quote shells
2. **Review in HubSpot** - Check created quotes
3. **Add Details** - Complete quotes with line items in UI
4. **Apply Template** - Use HubSpot quote templates
5. **Send to Customer** - Use HubSpot send functionality

### Naming Convention

Use descriptive quote titles:
- Include product/service
- Include customer name or company
- Include time period (Q1 2026, etc.)
- Include quote number

Example: "Enterprise Software License - Acme Corp - Q1 2026 #001"

### Data Validation

Before bulk creation:
- Ensure unique quote titles
- Valid expiration dates (YYYY-MM-DD format)
- Language codes are valid

## Limitations

1. **API Field Restrictions**
   - Cannot set pricing via API
   - Cannot add line items via API
   - Limited to basic quote metadata

2. **No Line Items**
   - Quotes created as shells only
   - Must add products manually in HubSpot UI

3. **No Template Application**
   - Cannot apply quote templates via API
   - Templates must be applied in UI

4. **No PDF Generation**
   - Quote PDFs generated in HubSpot UI only
   - Cannot generate via API

## Workarounds

### For Complete Quote Creation

If you need fully populated quotes:
1. Create deal first (with line items)
2. Generate quote from deal in HubSpot UI
3. Or use HubSpot Workflows to auto-populate quotes

### For Pricing Integration

If you need external pricing:
1. Use deals API (supports line items)
2. Link deals to quotes
3. Or use HubSpot product catalog

## Troubleshooting

### Quotes Not Appearing

- Check that quotes feature is enabled
- Verify you have correct permissions
- Check HubSpot plan includes quotes

### Cannot Edit Quote Amount

- This is expected - amount is calculated
- Add line items in HubSpot UI instead
- Amount will calculate automatically

### Status Not Updating

- Verify status value is valid
- Use exact enum values (DRAFT, APPROVED, etc.)
- Check HubSpot approval workflows

## Next Steps

After mastering this agent:

1. **Deal Integration**: Create deals with line items instead
2. **Workflow Automation**: Use HubSpot workflows to complete quotes
3. **Template Management**: Set up quote templates in HubSpot
4. **Product Catalog**: Populate HubSpot product catalog
5. **Quote-to-Deal**: Link quotes to deals for tracking

## Related Documentation

- [Contact Creator](contact_creator.md)
- [Account Creator](account_creator.md)
- [Deal Creator](deal_creator.md)
- [HubSpot Quotes API](https://developers.hubspot.com/docs/api/crm/quotes)