# Banking Call Center Agentic AI — Detailed Documentation

This folder centralizes the detailed reference material for the sample agentic AI system. Use it to understand the full architecture, data APIs, and ways to extend the solution.

## Business case

Banks and credit unions can use an agentic AI to triage and resolve common support requests (balances, card issues, loan schedules) without waiting for a human representative. The system also hands off complex cases with full context to minimize customer effort and reduce average handle time.

## Architecture

```mermaid
flowchart LR
    C[Customer via Phone/Chat]
    Agent[AI Agent Core\nIntent detection, context, and responses]
    Tools[Tool Executor\nMaps tool calls to API requests]
    Gateway[API Gateway\nRoutes and coordinates API calls]
    APIs[Data APIs Layer\nCustomer | Account | Transaction | Loan | Card | Support]
    DB[(Mock Banking Data\nCustomers, Accounts, Transactions, Loans, Cards, Tickets)]

    C <--> Agent
    Agent <--> Tools
    Tools <--> Gateway
    Gateway <--> APIs
    APIs --> DB
```

### Component highlights
- **AI Agent Core**: Understands intents, keeps conversation context, and crafts responses.
- **Tool Executor**: Selects and invokes tools that map to backend capabilities.
- **API Gateway**: Provides a single entry point to banking microservices and handles latency simulation.
- **Data APIs Layer**: Independent services for customer, account, transaction, loan, card, and support data.
- **Mock Database**: Pre-populated demo data to keep experimentation self-contained.

## Features

### Data APIs
The system simulates six banking microservices:
1. Customer API — Customer profiles, identification, verification.
2. Account API — Account information, balances, transfers.
3. Transaction API — Transaction history, search, spending analysis.
4. Loan API — Loan details, payment schedules, payoff calculations.
5. Card API — Card management, lost/stolen reporting, blocking.
6. Support API — Ticket creation, tracking, escalation.

### Agent capabilities (tools)
- Customer identification by phone/email and verification.
- Balance checks across accounts and transaction history search.
- Transfers, loan payment schedules, and payoff lookups.
- Card blocking, lost/stolen handling, and replacement workflows.
- Support ticket creation, updates, and escalation paths.

### Mock data
- Five demo customers with varied segments and products.
- Checking, savings, and money market accounts with balances.
- Rich transaction history with diverse merchants.
- Active auto, mortgage, and personal loans.
- Debit and credit cards plus support ticket history.

## Operations

### Prerequisites
- Python 3.9+
- `pip`

### Setup
```bash
pip install -r requirements.txt
```

### Run the demos
```bash
python run_demo.py        # Chat with the agent
python run_api_demo.py    # See each API exercised
```

### Configuration
Environment variables (set via `.env`):
```bash
# AI Provider (mock for demo, openai or anthropic for production)
AI_PROVIDER=mock

# API Simulation Settings
API_LATENCY_MIN_MS=50
API_LATENCY_MAX_MS=200

# Logging
LOG_LEVEL=INFO
```

## Sample interaction
```
You: Hello, I need help with my account

Agent: Hello! Welcome to SecureBank. I'd be happy to help you today.
To get started, could you please provide your phone number or email
so I can look up your account?

You: My phone number is +1-555-0101

Agent: I found your account. Hello John Anderson! You're registered
as a premium customer. How can I assist you today?

You: What's my account balance?

Agent: Your total balance across all accounts is $67,582.67.

Here's the breakdown:
- Checking (ACC001): $15,432.67
- Savings (ACC002): $52,150.00

You: I lost my card ending in 4521

Agent: I've processed your report for the card ending in 4521.

Actions taken:
- Card has been immediately blocked
- All pending transactions will be reviewed
- A replacement card will be shipped within 5-7 business days

Please monitor your account for any unauthorized transactions.
If you see any suspicious activity, please report it immediately.
```

## Future improvements
- Plug in real LLM providers for production-grade responses.
- Add authentication/authorization around the tool executor.
- Expand observability with tracing across API calls.
- Provide CI-ready notebooks for benchmarking and evaluation.
- Add more edge-case demos (disputes, travel notices, rate comparisons).
