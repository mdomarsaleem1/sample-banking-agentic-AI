"""
Transaction API - Handles transaction history and details.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional
from ..data.database import db
from ..data.models import Transaction, TransactionType
from .base import BaseAPI, APIResponse


class TransactionAPI(BaseAPI):
    """
    Transaction Data API

    Provides access to transaction history, search, and analytics.
    In production, this would connect to the Transaction Processing System.
    """

    def __init__(self):
        super().__init__(
            name="TransactionAPI",
            min_latency_ms=50,
            max_latency_ms=250
        )

    async def get_transaction(self, transaction_id: str) -> APIResponse[Transaction]:
        """
        Get transaction by ID.

        Args:
            transaction_id: The unique transaction identifier

        Returns:
            APIResponse containing Transaction data or error
        """
        return await self._execute_request(
            operation=f"get_transaction({transaction_id})",
            handler=lambda: db.get_transaction(transaction_id)
        )

    async def get_recent_transactions(
        self,
        account_id: str,
        limit: int = 10,
        days: int = 30
    ) -> APIResponse[List[Transaction]]:
        """
        Get recent transactions for an account.

        Args:
            account_id: The account identifier
            limit: Maximum number of transactions to return
            days: Number of days to look back

        Returns:
            APIResponse containing list of transactions
        """
        return await self._execute_request(
            operation=f"get_recent_transactions({account_id}, limit={limit})",
            handler=lambda: db.get_account_transactions(account_id, limit, days)
        )

    async def search_transactions(
        self,
        account_id: str,
        merchant_name: Optional[str] = None,
        min_amount: Optional[Decimal] = None,
        max_amount: Optional[Decimal] = None,
        transaction_type: Optional[TransactionType] = None,
        days: int = 90
    ) -> APIResponse[List[Transaction]]:
        """
        Search transactions with filters.

        Args:
            account_id: The account identifier
            merchant_name: Filter by merchant name (partial match)
            min_amount: Minimum transaction amount
            max_amount: Maximum transaction amount
            transaction_type: Filter by transaction type
            days: Number of days to search

        Returns:
            APIResponse containing filtered transactions
        """
        def search():
            transactions = db.get_account_transactions(account_id, limit=100, days=days)

            results = []
            for tx in transactions:
                # Apply filters
                if merchant_name and tx.merchant_name:
                    if merchant_name.lower() not in tx.merchant_name.lower():
                        continue
                if min_amount and tx.amount < min_amount:
                    continue
                if max_amount and tx.amount > max_amount:
                    continue
                if transaction_type and tx.transaction_type != transaction_type:
                    continue
                results.append(tx)

            return results

        return await self._execute_request(
            operation=f"search_transactions({account_id})",
            handler=search
        )

    async def get_spending_summary(
        self,
        account_id: str,
        days: int = 30
    ) -> APIResponse[dict]:
        """
        Get spending summary by category.

        Args:
            account_id: The account identifier
            days: Number of days to analyze

        Returns:
            APIResponse containing spending breakdown
        """
        def calculate_summary():
            transactions = db.get_account_transactions(account_id, limit=100, days=days)

            # Calculate totals by category
            category_totals = {}
            total_spending = Decimal("0")
            total_income = Decimal("0")

            for tx in transactions:
                if tx.transaction_type in [
                    TransactionType.PURCHASE,
                    TransactionType.WITHDRAWAL,
                    TransactionType.ATM_WITHDRAWAL,
                    TransactionType.PAYMENT,
                    TransactionType.TRANSFER_OUT,
                    TransactionType.FEE
                ]:
                    total_spending += tx.amount
                    category = tx.merchant_category or "Other"
                    category_totals[category] = category_totals.get(category, Decimal("0")) + tx.amount
                elif tx.transaction_type in [
                    TransactionType.DEPOSIT,
                    TransactionType.TRANSFER_IN,
                    TransactionType.REFUND,
                    TransactionType.INTEREST
                ]:
                    total_income += tx.amount

            return {
                "account_id": account_id,
                "period_days": days,
                "total_spending": str(total_spending),
                "total_income": str(total_income),
                "net_change": str(total_income - total_spending),
                "transaction_count": len(transactions),
                "by_category": {k: str(v) for k, v in sorted(
                    category_totals.items(),
                    key=lambda x: x[1],
                    reverse=True
                )}
            }

        return await self._execute_request(
            operation=f"get_spending_summary({account_id}, days={days})",
            handler=calculate_summary
        )

    async def get_large_transactions(
        self,
        account_id: str,
        threshold: Decimal = Decimal("500"),
        days: int = 30
    ) -> APIResponse[List[Transaction]]:
        """
        Get transactions above a certain threshold.

        Args:
            account_id: The account identifier
            threshold: Minimum amount to include
            days: Number of days to search

        Returns:
            APIResponse containing large transactions
        """
        def find_large():
            transactions = db.get_account_transactions(account_id, limit=100, days=days)
            return [tx for tx in transactions if tx.amount >= threshold]

        return await self._execute_request(
            operation=f"get_large_transactions({account_id}, threshold=${threshold})",
            handler=find_large
        )
