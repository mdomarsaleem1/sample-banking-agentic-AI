# Banking Call Center Agentic AI System

A sample agentic AI system that demonstrates how an intelligent agent can handle customer queries in a banking call center by interacting with multiple Data APIs.

## Overview

This project showcases a modern agentic AI architecture for customer service, featuring:

- **Intelligent Agent Core**: An AI agent that understands customer intents and orchestrates responses
- **Multiple Data APIs**: Simulated banking microservices (Customer, Account, Transaction, Loan, Card, Support)
- **Tool-based Architecture**: The agent uses defined tools/functions to interact with banking services
- **Conversation Context Management**: Maintains state across the conversation for coherent interactions
- **Mock Data Layer**: Realistic banking data for demonstration purposes

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Banking Call Center AI                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐     ┌──────────────────┐     ┌─────────────────────────┐  │
│  │   Customer  │────▶│   AI Agent Core  │────▶│     Tool Executor       │  │
│  │   (Phone/   │◀────│                  │◀────│                         │  │
│  │   Chat)     │     │  - Intent        │     │  - Maps tool calls      │  │
│  └─────────────┘     │    Detection     │     │    to API calls         │  │
│                      │  - Context       │     │  - Handles responses    │  │
│                      │    Management    │     └───────────┬─────────────┘  │
│                      │  - Response      │                 │                 │
│                      │    Generation    │                 ▼                 │
│                      └──────────────────┘     ┌─────────────────────────┐  │
│                                               │      API Gateway         │  │
│                                               └───────────┬─────────────┘  │
│                                                           │                 │
│  ┌────────────────────────────────────────────────────────┼────────────┐   │
│  │                         Data APIs Layer                │            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────┐  ┌───────┴───────┐   │   │
│  │  │ Customer │  │ Account  │  │ Transaction │  │     Loan      │   │   │
│  │  │   API    │  │   API    │  │     API     │  │     API       │   │   │
│  │  └──────────┘  └──────────┘  └─────────────┘  └───────────────┘   │   │
│  │  ┌──────────┐  ┌──────────┐                                       │   │
│  │  │   Card   │  │ Support  │   (Each API simulates network latency │   │
│  │  │   API    │  │   API    │    and can be configured for testing) │   │
│  │  └──────────┘  └──────────┘                                       │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       Mock Database Layer                            │   │
│  │  - Customers    - Accounts    - Transactions                        │   │
│  │  - Loans        - Cards       - Support Tickets                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Features

### Data APIs
The system simulates 6 different banking microservices:

1. **Customer API** - Customer profiles, identification, verification
2. **Account API** - Account information, balances, transfers
3. **Transaction API** - Transaction history, search, spending analysis
4. **Loan API** - Loan details, payment schedules, payoff calculations
5. **Card API** - Card management, lost/stolen reporting, blocking
6. **Support API** - Ticket creation, tracking, escalation

### Agent Capabilities (Tools)
The AI agent has access to 25+ tools including:

- Customer identification by phone/email
- Identity verification
- Balance checking across all accounts
- Transaction history and search
- Fund transfers
- Loan payment schedules
- Card blocking and lost/stolen reporting
- Support ticket management

### Mock Data
Pre-populated with realistic banking data:
- 5 demo customers with different profiles
- Multiple accounts (checking, savings, money market)
- Transaction history with various merchants
- Active loans (auto, mortgage, personal)
- Debit and credit cards
- Support ticket history

## Installation

### Prerequisites
- Python 3.9 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd sample-banking-agentic-AI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Copy and configure environment:
```bash
cp .env.example .env
# Edit .env to configure AI provider if needed
```

## Running the Demo

### Interactive Chat Demo
Start an interactive session with the AI agent:

```bash
python run_demo.py
```

This launches a chat interface where you can interact with the banking agent.

### API Demo
See all the Data APIs in action:

```bash
python run_api_demo.py
```

This demonstrates each API being called with sample data.

### Automated Demo Scenario
Run a pre-defined conversation scenario:

```bash
python run_demo.py --demo
```

## Sample Interaction

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

## Project Structure

```
sample-banking-agentic-AI/
├── src/
│   └── banking_agent/
│       ├── __init__.py
│       ├── main.py              # CLI entry point
│       ├── agent/               # AI Agent Core
│       │   ├── __init__.py
│       │   ├── core.py          # Main agent logic
│       │   └── context.py       # Conversation context
│       ├── apis/                # Data APIs Layer
│       │   ├── __init__.py
│       │   ├── base.py          # Base API class
│       │   ├── api_gateway.py   # Unified API gateway
│       │   ├── customer_api.py  # Customer service
│       │   ├── account_api.py   # Account service
│       │   ├── transaction_api.py
│       │   ├── loan_api.py
│       │   ├── card_api.py
│       │   └── support_api.py
│       ├── data/                # Data Layer
│       │   ├── __init__.py
│       │   ├── models.py        # Pydantic models
│       │   └── database.py      # Mock database
│       ├── tools/               # Agent Tools
│       │   ├── __init__.py
│       │   ├── definitions.py   # Tool definitions
│       │   └── executor.py      # Tool execution
│       └── utils/               # Utilities
│           ├── __init__.py
│           ├── config.py
│           └── logging_config.py
├── run_demo.py                  # Quick start script
├── run_api_demo.py             # API demonstration
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Configuration

Environment variables (`.env`):

```bash
# AI Provider (mock for demo, openai or anthropic for production)
AI_PROVIDER=mock

# API Simulation Settings
API_LATENCY_MIN_MS=50
API_LATENCY_MAX_MS=200

# Logging
LOG_LEVEL=INFO
```

## Demo Customers

| ID | Name | Phone | Segment | Notes |
|----|------|-------|---------|-------|
| CUST001 | John Anderson | +1-555-0101 | Premium | Has auto loan, credit card |
| CUST002 | Sarah Mitchell | +1-555-0102 | Standard | Has lost card scenario |
| CUST003 | Michael Chen | +1-555-0103 | Private | High-value customer, mortgage |
| CUST004 | Emily Rodriguez | +1-555-0104 | Standard | Personal loan, open ticket |
| CUST005 | Robert Thompson | +1-555-0105 | Private | Credit line, long-term customer |

## Extending the System

### Adding New Tools

1. Add tool definition in `tools/definitions.py`:
```python
{
    "name": "my_new_tool",
    "description": "Description of what the tool does",
    "parameters": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "..."}
        },
        "required": ["param1"]
    }
}
```

2. Add handler in `tools/executor.py`:
```python
async def _my_new_tool(self, params: Dict, context):
    # Implementation
    return {"success": True, ...}
```

3. Register handler in `_get_handler()` method.

### Adding New APIs

1. Create new API class in `apis/`:
```python
from .base import BaseAPI, APIResponse

class MyNewAPI(BaseAPI):
    def __init__(self):
        super().__init__(name="MyNewAPI")

    async def my_operation(self, param: str) -> APIResponse:
        return await self._execute_request(
            operation="my_operation",
            handler=lambda: self._do_something(param)
        )
```

2. Add to `api_gateway.py`.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
