"""
Mock Data Layer - Simulates banking databases and data sources.
"""

from .database import MockDatabase
from .models import (
    Customer,
    Account,
    Transaction,
    Loan,
    Card,
    SupportTicket,
    CustomerProfile,
)

__all__ = [
    "MockDatabase",
    "Customer",
    "Account",
    "Transaction",
    "Loan",
    "Card",
    "SupportTicket",
    "CustomerProfile",
]
