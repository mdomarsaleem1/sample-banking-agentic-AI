"""
Tool Definitions - Defines all tools available to the AI agent.

These tool definitions follow the OpenAI function calling format,
which is also compatible with Anthropic's tool use.
"""

from typing import List, Dict, Any

# Tool definitions for the AI agent
TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    # ============ Customer Identification Tools ============
    {
        "name": "identify_customer_by_phone",
        "description": "Look up a customer using their phone number. Use this when a customer calls in and provides their phone number for identification.",
        "parameters": {
            "type": "object",
            "properties": {
                "phone_number": {
                    "type": "string",
                    "description": "The customer's phone number (e.g., +1-555-0101)"
                }
            },
            "required": ["phone_number"]
        }
    },
    {
        "name": "identify_customer_by_email",
        "description": "Look up a customer using their email address. Use this when a customer provides their email for identification.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The customer's email address"
                }
            },
            "required": ["email"]
        }
    },
    {
        "name": "verify_customer_identity",
        "description": "Verify a customer's identity using their date of birth and last 4 digits of SSN. Use this before performing sensitive operations.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                },
                "date_of_birth": {
                    "type": "string",
                    "description": "Customer's date of birth in YYYY-MM-DD format"
                },
                "ssn_last_four": {
                    "type": "string",
                    "description": "Last 4 digits of the customer's SSN"
                }
            },
            "required": ["customer_id", "date_of_birth", "ssn_last_four"]
        }
    },
    {
        "name": "get_customer_profile",
        "description": "Get a comprehensive customer profile including accounts, recent transactions, loans, cards, and support tickets. Use this to get full context about a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    },

    # ============ Account Tools ============
    {
        "name": "check_account_balance",
        "description": "Check the current balance of a specific account. Returns balance, available balance, and last activity.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "The account ID to check"
                }
            },
            "required": ["account_id"]
        }
    },
    {
        "name": "get_all_account_balances",
        "description": "Get balances for all accounts belonging to a customer. Returns total balance and breakdown by account.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "get_customer_accounts",
        "description": "List all accounts for a customer with details like account type, status, and balance.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "transfer_funds",
        "description": "Transfer money between accounts. Requires verification. Returns transfer confirmation and new balances.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_account_id": {
                    "type": "string",
                    "description": "Source account ID"
                },
                "to_account_id": {
                    "type": "string",
                    "description": "Destination account ID"
                },
                "amount": {
                    "type": "number",
                    "description": "Amount to transfer"
                },
                "description": {
                    "type": "string",
                    "description": "Transfer description/memo"
                }
            },
            "required": ["from_account_id", "to_account_id", "amount"]
        }
    },

    # ============ Transaction Tools ============
    {
        "name": "get_recent_transactions",
        "description": "Get recent transactions for an account. Returns transaction details including amount, merchant, date, and status.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "The account ID"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of transactions to return (default: 10)"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back (default: 30)"
                }
            },
            "required": ["account_id"]
        }
    },
    {
        "name": "search_transactions",
        "description": "Search for specific transactions with filters like merchant name, amount range, or transaction type.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "The account ID"
                },
                "merchant_name": {
                    "type": "string",
                    "description": "Filter by merchant name (partial match)"
                },
                "min_amount": {
                    "type": "number",
                    "description": "Minimum transaction amount"
                },
                "max_amount": {
                    "type": "number",
                    "description": "Maximum transaction amount"
                },
                "transaction_type": {
                    "type": "string",
                    "description": "Type of transaction (purchase, deposit, withdrawal, transfer_in, transfer_out, payment)"
                }
            },
            "required": ["account_id"]
        }
    },
    {
        "name": "get_spending_summary",
        "description": "Get a spending analysis breakdown by category for an account. Shows total spending, income, and category breakdown.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_id": {
                    "type": "string",
                    "description": "The account ID"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to analyze (default: 30)"
                }
            },
            "required": ["account_id"]
        }
    },
    {
        "name": "find_transaction",
        "description": "Look up a specific transaction by its ID or reference number.",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction_id": {
                    "type": "string",
                    "description": "The transaction ID or reference number"
                }
            },
            "required": ["transaction_id"]
        }
    },

    # ============ Loan Tools ============
    {
        "name": "get_loan_summary",
        "description": "Get summary of all loans for a customer including balances, monthly payments, and next payment dates.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "get_loan_details",
        "description": "Get detailed information about a specific loan.",
        "parameters": {
            "type": "object",
            "properties": {
                "loan_id": {
                    "type": "string",
                    "description": "The loan ID"
                }
            },
            "required": ["loan_id"]
        }
    },
    {
        "name": "get_payment_schedule",
        "description": "Get the upcoming payment schedule for a loan. Shows next 6 payments with dates and amounts.",
        "parameters": {
            "type": "object",
            "properties": {
                "loan_id": {
                    "type": "string",
                    "description": "The loan ID"
                }
            },
            "required": ["loan_id"]
        }
    },
    {
        "name": "get_payoff_amount",
        "description": "Calculate the payoff amount to pay off a loan in full. Valid for 10 days.",
        "parameters": {
            "type": "object",
            "properties": {
                "loan_id": {
                    "type": "string",
                    "description": "The loan ID"
                }
            },
            "required": ["loan_id"]
        }
    },

    # ============ Card Tools ============
    {
        "name": "get_card_summary",
        "description": "Get summary of all cards for a customer including card types, status, and credit limits.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "check_card_status",
        "description": "Check the current status of a specific card.",
        "parameters": {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "The card ID"
                }
            },
            "required": ["card_id"]
        }
    },
    {
        "name": "report_card_lost_stolen",
        "description": "Report a card as lost or stolen. This will immediately block the card and initiate a replacement.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                },
                "card_last_four": {
                    "type": "string",
                    "description": "Last 4 digits of the card number"
                },
                "is_stolen": {
                    "type": "boolean",
                    "description": "True if stolen, False if just lost"
                }
            },
            "required": ["customer_id", "card_last_four"]
        }
    },
    {
        "name": "block_card",
        "description": "Block/freeze a card temporarily. Use for suspected fraud or customer request.",
        "parameters": {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "The card ID to block"
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for blocking (lost, stolen, fraud, customer_request)"
                }
            },
            "required": ["card_id"]
        }
    },

    # ============ Support Ticket Tools ============
    {
        "name": "get_open_tickets",
        "description": "Get all open support tickets for a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "get_ticket_details",
        "description": "Get details of a specific support ticket.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "The ticket ID"
                }
            },
            "required": ["ticket_id"]
        }
    },
    {
        "name": "create_support_ticket",
        "description": "Create a new support ticket for an issue that cannot be resolved immediately.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                },
                "category": {
                    "type": "string",
                    "description": "Ticket category (account_inquiry, transaction_dispute, card_issue, loan_inquiry, technical_issue, fraud_report, general_inquiry, complaint)"
                },
                "subject": {
                    "type": "string",
                    "description": "Brief subject/title of the issue"
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the issue"
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level (low, medium, high, urgent)"
                }
            },
            "required": ["customer_id", "category", "subject", "description"]
        }
    },
    {
        "name": "escalate_ticket",
        "description": "Escalate a support ticket to higher priority for urgent attention.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "The ticket ID to escalate"
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for escalation"
                }
            },
            "required": ["ticket_id", "reason"]
        }
    },
    {
        "name": "get_ticket_history",
        "description": "Get complete ticket history for a customer including resolved tickets.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's ID"
                }
            },
            "required": ["customer_id"]
        }
    }
]


def get_tool_definitions() -> List[Dict[str, Any]]:
    """Get all tool definitions for the agent."""
    return TOOL_DEFINITIONS


def get_tool_names() -> List[str]:
    """Get list of all tool names."""
    return [tool["name"] for tool in TOOL_DEFINITIONS]


def get_tool_by_name(name: str) -> Dict[str, Any] | None:
    """Get a specific tool definition by name."""
    for tool in TOOL_DEFINITIONS:
        if tool["name"] == name:
            return tool
    return None
