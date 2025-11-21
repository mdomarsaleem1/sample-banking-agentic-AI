"""
Account API - Handles bank account queries and operations.
"""

from decimal import Decimal
from typing import List, Optional
from ..data.database import db
from ..data.models import Account
from .base import BaseAPI, APIResponse


class AccountAPI(BaseAPI):
    """
    Account Data API

    Provides access to bank account information, balances, and account operations.
    In production, this would connect to the Core Banking System.
    """

    def __init__(self):
        super().__init__(
            name="AccountAPI",
            min_latency_ms=40,
            max_latency_ms=180
        )

    async def get_account(self, account_id: str) -> APIResponse[Account]:
        """
        Retrieve account by ID.

        Args:
            account_id: The unique account identifier

        Returns:
            APIResponse containing Account data or error
        """
        return await self._execute_request(
            operation=f"get_account({account_id})",
            handler=lambda: db.get_account(account_id)
        )

    async def get_customer_accounts(self, customer_id: str) -> APIResponse[List[Account]]:
        """
        Get all accounts for a customer.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing list of customer accounts
        """
        return await self._execute_request(
            operation=f"get_customer_accounts({customer_id})",
            handler=lambda: db.get_customer_accounts(customer_id)
        )

    async def get_account_balance(self, account_id: str) -> APIResponse[dict]:
        """
        Get current balance for an account.

        Args:
            account_id: The account identifier

        Returns:
            APIResponse containing balance information
        """
        def get_balance():
            account = db.get_account(account_id)
            if not account:
                return None
            return {
                "account_id": account.account_id,
                "account_type": account.account_type.value,
                "balance": str(account.balance),
                "available_balance": str(account.available_balance),
                "currency": account.currency,
                "last_updated": account.last_activity_date.isoformat()
            }

        return await self._execute_request(
            operation=f"get_account_balance({account_id})",
            handler=get_balance
        )

    async def get_total_balance(self, customer_id: str) -> APIResponse[dict]:
        """
        Get total balance across all customer accounts.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing total balance summary
        """
        def calculate_total():
            accounts = db.get_customer_accounts(customer_id)
            if not accounts:
                return None

            total_balance = sum(acc.balance for acc in accounts)
            total_available = sum(acc.available_balance for acc in accounts)

            return {
                "customer_id": customer_id,
                "total_balance": str(total_balance),
                "total_available": str(total_available),
                "account_count": len(accounts),
                "breakdown": [
                    {
                        "account_id": acc.account_id,
                        "account_type": acc.account_type.value,
                        "balance": str(acc.balance)
                    }
                    for acc in accounts
                ]
            }

        return await self._execute_request(
            operation=f"get_total_balance({customer_id})",
            handler=calculate_total
        )

    async def transfer_funds(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: Decimal,
        description: str = "Transfer"
    ) -> APIResponse[dict]:
        """
        Transfer funds between accounts.

        Args:
            from_account_id: Source account ID
            to_account_id: Destination account ID
            amount: Amount to transfer
            description: Transfer description

        Returns:
            APIResponse containing transfer result
        """
        def execute_transfer():
            # Validate accounts
            from_acc = db.get_account(from_account_id)
            to_acc = db.get_account(to_account_id)

            if not from_acc:
                raise ValueError(f"Source account {from_account_id} not found")
            if not to_acc:
                raise ValueError(f"Destination account {to_account_id} not found")

            if from_acc.available_balance < amount:
                raise ValueError(
                    f"Insufficient funds. Available: ${from_acc.available_balance}, "
                    f"Requested: ${amount}"
                )

            reference = db.transfer_funds(
                from_account_id,
                to_account_id,
                amount,
                description
            )

            if not reference:
                raise Exception("Transfer failed")

            return {
                "success": True,
                "reference_number": reference,
                "from_account": from_account_id,
                "to_account": to_account_id,
                "amount": str(amount),
                "description": description,
                "new_balance_from": str(from_acc.balance),
                "new_balance_to": str(to_acc.balance)
            }

        return await self._execute_request(
            operation=f"transfer_funds({from_account_id} -> {to_account_id}, ${amount})",
            handler=execute_transfer
        )
