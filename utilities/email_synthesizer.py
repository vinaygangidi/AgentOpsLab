"""
Email Conversation Synthesizer
Generates realistic, messy email conversations for testing
Creates conversations with noise, multiple topics, and varying complexity
"""

import os
import json
from datetime import datetime, timedelta
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
claude = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def generate_enterprise_software_conversation():
    """Generates a complex enterprise software deal conversation"""
    
    prompt = """Generate a realistic, messy email conversation between a potential customer and a software vendor. This should be a complex enterprise software deal.

Requirements:
- 8-10 email exchanges over 3 weeks
- 3-4 participants (buyer, vendor sales rep, technical lead, maybe a manager)
- Mix signal and noise - include off-topic discussions, scheduling conflicts, personal remarks
- Discuss multiple products: Enterprise Software License, Professional Services, Training, Support
- Include pricing negotiations (starting at $100k, negotiate down to $75k)
- Mention timeline pressures and budget cycles
- Some emails should be short ("Thanks!", "Let me check with my team"), others long
- Include technical jargon mixed with business language
- Sentiment shifts from excited → cautious → optimistic
- Include actual numbers: team size (50 users), budget ($75k), timeline (Q2 2026)
- Contact: Sarah Chen, VP of Engineering at TechFlow Industries
- Company: TechFlow Industries, 200 employees, software development, $20M revenue
- Vendor: Your company selling enterprise software

Format as actual email thread with:
- From/To headers
- Subject line
- Timestamps
- Email bodies with natural conversation flow

Make it realistic and messy like real business emails."""

    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text


def generate_hardware_services_conversation():
    """Generates a hardware + services bundle conversation"""
    
    prompt = """Generate a realistic email conversation for a hardware and services deal.

Requirements:
- 5-7 email exchanges over 2 weeks
- 2-3 participants (procurement manager, sales rep, maybe IT director)
- Discussing: 50 laptops, setup services, 3-year warranty
- Volume discount negotiations (from $100k to $85k)
- Delivery timeline concerns (need by end of month)
- Mix in some scheduling emails and off-topic remarks
- Contact: Michael Torres, IT Procurement Manager at Riverside Medical
- Company: Riverside Medical, healthcare, 500 employees, urgent IT refresh needed
- Include specs discussions, some impatience about timeline
- Sentiment: Professional but time-pressured

Format as actual email thread with headers and timestamps."""

    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text


def generate_professional_services_conversation():
    """Generates a professional services engagement conversation"""
    
    prompt = """Generate a realistic email conversation for a professional services consulting engagement.

Requirements:
- 6-8 email exchanges over 10 days
- 3 participants (client executive, consulting partner, project manager)
- Discussing: 6-month implementation project, 3 consultants, mix of hourly and fixed price
- Scope creep concerns, resource allocation discussions
- From $150k proposal down to $125k with reduced scope
- Contact: Jennifer Walsh, Chief Operations Officer at DataVault Corp
- Company: DataVault Corp, data analytics startup, 80 employees, Series B funded
- Include project plan discussions, timeline negotiations, resource availability
- Some urgency around board meeting deadlines
- Sentiment: Eager but budget-conscious

Format as actual email thread with headers and timestamps."""

    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text


def save_conversation(conversation, filename):
    """Saves conversation to file"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data/email_conversations', exist_ok=True)
    
    filepath = f'data/email_conversations/{filename}'
    
    with open(filepath, 'w') as f:
        f.write(conversation)
    
    print(f"✅ Saved: {filepath}")
    return filepath


def main():
    """Generate all conversation types"""
    
    print("\n" + "="*70)
    print("EMAIL CONVERSATION SYNTHESIZER")
    print("="*70 + "\n")
    
    print("Generating realistic email conversations for testing...\n")
    
    # Generate conversation 1: Enterprise Software
    print("1. Generating enterprise software deal conversation...")
    conv1 = generate_enterprise_software_conversation()
    save_conversation(conv1, "enterprise_software_deal.txt")
    print(f"   Length: {len(conv1)} characters\n")
    
    # Generate conversation 2: Hardware + Services
    print("2. Generating hardware + services deal conversation...")
    conv2 = generate_hardware_services_conversation()
    save_conversation(conv2, "hardware_services_deal.txt")
    print(f"   Length: {len(conv2)} characters\n")
    
    # Generate conversation 3: Professional Services
    print("3. Generating professional services deal conversation...")
    conv3 = generate_professional_services_conversation()
    save_conversation(conv3, "professional_services_deal.txt")
    print(f"   Length: {len(conv3)} characters\n")
    
    print("="*70)
    print("SYNTHESIS COMPLETE")
    print("="*70)
    print("\nGenerated 3 realistic email conversations:")
    print("1. data/email_conversations/enterprise_software_deal.txt")
    print("2. data/email_conversations/hardware_services_deal.txt")
    print("3. data/email_conversations/professional_services_deal.txt")
    print("\nThese conversations can now be used with email_intelligence_agent.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()