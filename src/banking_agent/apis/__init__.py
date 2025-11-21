"""
Data APIs - Simulates various banking microservices and data APIs.

These APIs represent the data layer that the AI agent interacts with
to fetch customer information, transaction history, account details, etc.
"""

from .customer_api import CustomerAPI
from .account_api import AccountAPI
from .transaction_api import TransactionAPI
from .loan_api import LoanAPI
from .card_api import CardAPI
from .support_api import SupportAPI
from .api_gateway import APIGateway

__all__ = [
    "CustomerAPI",
    "AccountAPI",
    "TransactionAPI",
    "LoanAPI",
    "CardAPI",
    "SupportAPI",
    "APIGateway",
]
