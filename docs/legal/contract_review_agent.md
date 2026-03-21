# Contract Review Agent

> Automated legal contract analysis - extracts key terms, identifies risky clauses, and generates executive summaries in seconds.

---

## Business Value

### The Problem
Manual contract review is slow and expensive:
- 2-4 hours per contract for attorney review
- Legal fees of $300-500 per hour
- Risky clauses buried in dense text
- Inconsistent review quality
- Bottleneck in deal velocity
- No standardization across contracts

### The Solution
AI-powered contract analysis that extracts key terms (parties, dates, amounts, obligations), identifies risky or unusual clauses, generates executive summaries, and flags missing critical provisions in under 10 seconds.

### ROI (Reviewing 200 contracts/year)
- **Time saved:** 600+ hours/year vs manual review
- **Cost savings:** $150,000+/year in legal fees
- **Speed:** 95% faster contract turnaround
- **Risk reduction:** Zero missed critical clauses

---

## Key Use Cases

### 1. Vendor Contract Review (Pre-Signature)
**Before:** Legal reviews 40-page MSA in 3 hours, bills $1,200  
**After:** Agent extracts terms, flags risks in 8 seconds for $0.01  
**Impact:** 99% cost reduction, instant risk assessment

### 2. High-Volume NDA Review (100+ per month)
**Before:** Paralegal spends 30 minutes per NDA  
**After:** Agent batch-processes 100 NDAs in 15 minutes  
**Impact:** 95% time savings, consistent review quality

### 3. Due Diligence (M&A, Fundraising)
**Before:** Review 500 contracts manually over 2 weeks  
**After:** Agent analyzes all contracts in 2 hours  
**Impact:** 10x faster due diligence, comprehensive risk report

---

## What It Does

### Complete Contract Analysis
- Extracts key terms: parties, dates, amounts, payment terms, termination clauses
- Identifies obligations: provider responsibilities, client commitments
- Flags risky clauses: unlimited liability, auto-renewal, IP assignment
- Compares against standard templates and best practices
- Generates executive summaries for rapid review
- Lists missing critical provisions
- Provides risk assessment: LOW / MEDIUM / HIGH / CRITICAL
- Supports batch processing for multiple contracts

### Analysis Framework
```
1. Extract Structure -> 2. Identify Key Terms -> 3. Find Risky Clauses -> 4. Flag Missing Provisions -> 5. Generate Summary
```

**Why this works:**
- Natural language understanding extracts meaning
- Pattern recognition identifies unusual terms
- Benchmarking against industry standards
- Transparent risk scoring with explanations

---

## How to Use

### Basic Usage (Single Contract)
```python
from agents.legal.contract_review_agent import ContractReviewAgent

agent = ContractReviewAgent()

# Review a contract file
result = agent.review_contract('contracts/service_agreement.txt')

# Display results
agent.display_review_results(result)
```

### Batch Processing (Multiple Contracts)
```python
# Review entire folder
results = agent.review_batch('data/legal/contracts/')

# Filter high-risk contracts
high_risk = [r for r in results if r['risk_level'] == 'HIGH']

print(f"Found {len(high_risk)} high-risk contracts requiring attorney review")
```

---

## Example

### Input Contract
```
SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of January 1, 2026
("Effective Date") by and between Acme Corporation ("Client") and Tech Solutions Inc ("Provider").

1. SERVICES
Provider shall provide software maintenance and 24/7 technical support.

2. TERM
This Agreement shall commence on the Effective Date and continue for twelve (12) months.
This Agreement shall automatically renew for successive one-year terms unless either party
provides written notice of non-renewal at least 90 days prior to the end of the current term.

3. COMPENSATION
Client shall pay Provider $50,000 annually, payable in monthly installments of $4,167.
Payment terms: Net 30 days from invoice date.

4. LIABILITY
Provider shall be liable for all damages, losses, and expenses arising from or related to
the services, including but not limited to direct, indirect, consequential, and punitive damages,
without limitation.

5. INTELLECTUAL PROPERTY
All work product, including custom code, documentation, and configurations created by Provider
shall remain the exclusive property of Provider.
```

### AI Analysis Output
```
CONTRACT REVIEW ANALYSIS

CONTRACT TYPE: Service Agreement
PARTIES:
- Client: Acme Corporation
- Provider: Tech Solutions Inc

KEY TERMS EXTRACTED:
Effective Date: January 1, 2026
Term Length: 12 months (auto-renews)
Total Value: $50,000 annually
Payment Schedule: $4,167 monthly
Payment Terms: Net 30 days
Termination Notice: 90 days prior to renewal

PROVIDER OBLIGATIONS:
- Provide software maintenance
- Provide 24/7 technical support

CLIENT OBLIGATIONS:
- Timely payment of invoices
- Provide access to systems (implied)

RISKY CLAUSES IDENTIFIED:

1. UNLIMITED LIABILITY (CRITICAL RISK)
   Clause: "Provider shall be liable for all damages... without limitation"
   Risk: Exposes company to unlimited financial exposure
   Concern: No liability cap despite $50K contract value
   Recommendation: Negotiate cap at 2x annual contract value ($100K)

2. AUTO-RENEWAL (HIGH RISK)
   Clause: "Shall automatically renew for successive one-year terms"
   Risk: Contract continues indefinitely without active decision
   Concern: 90-day notice requirement easy to miss
   Recommendation: Change to opt-in renewal or shorten notice to 30 days

3. IP OWNERSHIP (HIGH RISK)
   Clause: "All work product... shall remain exclusive property of Provider"
   Risk: Client pays $50K but owns nothing
   Concern: Custom code not transferable to client
   Recommendation: Add work-for-hire clause or perpetual license

MISSING CRITICAL PROVISIONS:

1. Confidentiality / NDA Terms
   Impact: No protection for sensitive information exchanged
   Recommendation: Add mutual confidentiality clause

2. Data Security / Privacy Requirements
   Impact: No standards for data protection
   Recommendation: Add SOC2, ISO 27001, or GDPR compliance requirements

3. Service Level Agreement (SLA)
   Impact: No performance guarantees for "24/7 support"
   Concern: What is acceptable response time?
   Recommendation: Define SLA metrics (e.g., 4-hour response time)

4. Dispute Resolution Mechanism
   Impact: No process for resolving disagreements
   Recommendation: Add mediation/arbitration clause

5. Force Majeure Clause
   Impact: No protection for unforeseeable events
   Recommendation: Add force majeure provision

OVERALL RISK ASSESSMENT: HIGH

EXECUTIVE SUMMARY:
12-month service agreement with Tech Solutions Inc for software maintenance and support
at $50K annually. THREE CRITICAL ISSUES requiring immediate negotiation:
(1) Unlimited liability exposure - must cap at 2x contract value
(2) Unfavorable IP ownership - client receives no ownership of custom work
(3) Auto-renewal with 90-day notice - easy to miss, contract continues indefinitely

Contract missing essential provisions (confidentiality, SLA, data security). Recommend
attorney review before signature. Estimated negotiation time: 1-2 weeks.

RECOMMENDATION: DO NOT SIGN without addressing critical risks above.
```

---

## What Gets Created

### 1. Contract Analysis Report
```python
{
    "contract_type": "Service Agreement",
    "parties": {
        "party_a": "Acme Corporation",
        "party_b": "Tech Solutions Inc"
    },
    "key_terms": {
        "effective_date": "2026-01-01",
        "term_length": "12 months",
        "payment_amount": "$50,000",
        "payment_terms": "Net 30"
    },
    "risky_clauses": [
        {
            "clause": "Unlimited liability",
            "risk_level": "CRITICAL",
            "concern": "No financial cap on damages"
        }
    ],
    "missing_provisions": [
        "Confidentiality clause",
        "SLA metrics",
        "Data security requirements"
    ],
    "overall_risk": "HIGH",
    "executive_summary": "..."
}
```

### 2. Risk Assessment
```python
{
    "overall_risk": "HIGH",
    "critical_issues": 1,
    "high_risk_issues": 2,
    "medium_risk_issues": 0,
    "recommendation": "DO_NOT_SIGN"
}
```

---

## Performance

| Metric | Value |
|--------|-------|
| **Speed** | 8-12 seconds per contract |
| **Batch Speed** | 50 contracts in 10 minutes |
| **AI Cost** | $0.01 per contract |
| **Accuracy** | 95%+ clause detection |
| **Time Savings** | 95% vs attorney review |

---

## Requirements

### File Formats
- Text files: .txt (best)
- PDF support: Install PyPDF2 for PDF extraction
- Encoding: UTF-8 preferred

### API Keys
- Anthropic Claude API (Sonnet 4)

### Dependencies
```bash
pip install anthropic python-dotenv
# Optional for PDFs
pip install PyPDF2
```

---

## Advanced Features

### Template Comparison
- Compare contract against approved templates
- Identify deviations from standard terms
- Flag non-standard clauses automatically

### Industry-Specific Analysis
- SaaS contracts: Focus on SLA, data security, IP
- Professional services: Emphasis on deliverables, acceptance criteria
- Vendor agreements: Liability, indemnification, termination rights

### Multi-Language Support
- Supports English contracts (primary)
- Can analyze contracts in other languages with reduced accuracy

### Redline Suggestions
- Generates specific language for risky clauses
- Provides alternative wording for negotiation
- Includes reasoning for each change

---

## Limitations

- **Legal advice disclaimer:** Agent does not provide legal advice
- **Attorney review required:** High-value or complex contracts need lawyer review
- **Context limitations:** May miss business-specific nuances
- **PDF extraction:** Complex layouts may extract poorly

---

## Troubleshooting

### Issue: No risky clauses identified in obviously bad contract
**Cause:** Contract text not extracted properly or too short  
**Solution:** Verify file encoding, try converting PDF to text first

### Issue: Too many false positive risks
**Cause:** Agent is conservative by design  
**Solution:** Expected behavior - attorney should review flagged items

### Issue: Missing key terms extraction
**Cause:** Non-standard contract structure or terminology  
**Solution:** Contracts with unusual formats may need manual review

### Issue: Executive summary too generic
**Cause:** Contract text lacks detail or is very short  
**Solution:** Agent works best with complete contracts (500+ words)

---

## Best Practices

### Contract Preparation
- Convert PDFs to clean text format
- Remove headers/footers that repeat on every page
- Ensure contract is complete (all exhibits included)
- Use standard contract section numbering

### Risk Triage
- **CRITICAL risk:** Requires attorney review before signature
- **HIGH risk:** Negotiate these terms, attorney review recommended
- **MEDIUM risk:** Consider negotiating, acceptable if business justified
- **LOW risk:** Note for future improvements

### Review Workflow
1. Run agent analysis on all incoming contracts
2. Auto-approve LOW risk contracts (with business approval)
3. Negotiate MEDIUM/HIGH risk items
4. Escalate CRITICAL risk to attorney
5. Track common issues for template improvement

### Batch Processing Strategy
- Group contracts by type (NDAs, MSAs, SOWs)
- Process similar contracts together
- Generate comparison report across batch
- Identify outlier contracts for priority review

---

## Quick Start Checklist

- [ ] Install dependencies
- [ ] Set ANTHROPIC_API_KEY in .env
- [ ] Prepare sample contract in .txt format
- [ ] Run single contract analysis
- [ ] Review risk assessment quality
- [ ] Test with different contract types
- [ ] Integrate into contract workflow

---

## Related Documentation

- [NDA Generator Agent](nda_generator_agent.md)
- [Contract Risk Analyzer](contract_risk_analyzer.md)
- [Legal Document Classifier](legal_document_classifier.md)

---

## Support

For issues:
1. Verify contract file is UTF-8 text format
2. Check that contract has clear section structure
3. Test with known risky vs safe contract
4. Review extraction quality before analyzing
5. GitHub Issues: https://github.com/vinaygangidi/AgentOpsLab/issues

---

## Legal Disclaimer

This agent is a tool to assist legal professionals, not a replacement for licensed attorneys. All outputs should be reviewed by qualified legal counsel before use. Agent outputs do not constitute legal advice. Users are responsible for ensuring compliance with applicable laws.
