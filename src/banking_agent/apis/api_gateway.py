"""
API Gateway - Unified interface to all banking data APIs.

This serves as the single entry point for the AI agent to access all banking services.
In production, this would handle authentication, rate limiting, request routing, etc.
"""

import logging
from typing import Optional
from decimal import Decimal

from .customer_api import CustomerAPI
from .account_api import AccountAPI
from .transaction_api import TransactionAPI
from .loan_api import LoanAPI
from .card_api import CardAPI
from .support_api import SupportAPI

logger = logging.getLogger(__name__)


class APIGateway:
    """
    Unified API Gateway for all banking services.

    This class aggregates all banking APIs and provides a single interface
    for the AI agent to interact with banking data and services.
    """

    def __init__(self):
        """Initialize all API clients."""
        self.customer = CustomerAPI()
        self.account = AccountAPI()
        self.transaction = TransactionAPI()
        self.loan = LoanAPI()
        self.card = CardAPI()
        self.support = SupportAPI()

        logger.info("API Gateway initialized with all services")

    def get_api_stats(self) -> dict:
        """Get statistics from all APIs."""
        return {
            "customer_api": self.customer.get_stats(),
            "account_api": self.account.get_stats(),
            "transaction_api": self.transaction.get_stats(),
            "loan_api": self.loan.get_stats(),
            "card_api": self.card.get_stats(),
            "support_api": self.support.get_stats()
        }

    # ============ Customer Operations ============

    async def identify_customer(
        self,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        customer_id: Optional[str] = None
    ):
        """
        Identify a customer using phone, email, or customer ID.

        This is typically the first step when a customer calls in.
        """
        if customer_id:
            return await self.customer.get_customer(customer_id)
        elif phone:
            return await self.customer.get_customer_by_phone(phone)
        elif email:
            return await self.customer.get_customer_by_email(email)
        else:
            raise ValueError("Must provide phone, email, or customer_id")

    async def get_full_customer_context(self, customer_id: str):
        """
        Get comprehensive customer context for the agent.

        This aggregates data from multiple APIs to give the agent
        full context about the customer.
        """
        return await self.customer.get_customer_profile(customer_id)

    # ============ Account Operations ============

    async def check_balance(self, account_id: str):
        """Check account balance."""
        return await self.account.get_account_balance(account_id)

    async def get_all_balances(self, customer_id: str):
        """Get all account balances for a customer."""
        return await self.account.get_total_balance(customer_id)

    async def transfer_money(
        self,
        from_account: str,
        to_account: str,
        amount: Decimal,
        description: str = "Transfer"
    ):
        """Transfer funds between accounts."""
        return await self.account.transfer_funds(
            from_account, to_account, amount, description
        )

    # ============ Transaction Operations ============

    async def get_recent_activity(self, account_id: str, limit: int = 10):
        """Get recent transactions for an account."""
        return await self.transaction.get_recent_transactions(
            account_id, limit=limit
        )

    async def get_spending_analysis(self, account_id: str, days: int = 30):
        """Get spending analysis for an account."""
        return await self.transaction.get_spending_summary(account_id, days)

    async def find_transaction(self, transaction_id: str):
        """Find a specific transaction by ID."""
        return await self.transaction.get_transaction(transaction_id)

    # ============ Loan Operations ============

    async def get_loan_info(self, customer_id: str):
        """Get loan summary for a customer."""
        return await self.loan.get_loan_summary(customer_id)

    async def get_payment_schedule(self, loan_id: str):
        """Get payment schedule for a loan."""
        return await self.loan.get_payment_schedule(loan_id)

    async def get_payoff_quote(self, loan_id: str):
        """Get payoff amount for a loan."""
        return await self.loan.get_payoff_amount(loan_id)

    # ============ Card Operations ============

    async def get_card_info(self, customer_id: str):
        """Get card summary for a customer."""
        return await self.card.get_card_summary(customer_id)

    async def report_card_lost(
        self,
        customer_id: str,
        card_last_four: str,
        is_stolen: bool = False
    ):
        """Report a card as lost or stolen."""
        report_type = "stolen" if is_stolen else "lost"
        return await self.card.report_lost_stolen(
            customer_id, card_last_four, report_type
        )

    async def block_card(self, card_id: str, reason: str = "customer_request"):
        """Block a card."""
        return await self.card.block_card(card_id, reason)

    # ============ Support Operations ============

    async def get_open_tickets(self, customer_id: str):
        """Get open support tickets for a customer."""
        return await self.support.get_customer_tickets(customer_id)

    async def create_support_ticket(
        self,
        customer_id: str,
        category: str,
        subject: str,
        description: str,
        priority: str = "medium"
    ):
        """Create a new support ticket."""
        return await self.support.create_ticket(
            customer_id, category, subject, description, priority
        )

    async def get_ticket_status(self, ticket_id: str):
        """Get status of a support ticket."""
        return await self.support.get_ticket(ticket_id)

    async def escalate_issue(self, ticket_id: str, reason: str):
        """Escalate a support ticket."""
        return await self.support.escalate_ticket(ticket_id, reason)


# Global API Gateway instance
api_gateway = APIGateway()
