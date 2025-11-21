"""
Loan API - Handles loan information and payment queries.
"""

from datetime import date, timedelta
from decimal import Decimal
from typing import List, Optional
from ..data.database import db
from ..data.models import Loan, LoanStatus
from .base import BaseAPI, APIResponse


class LoanAPI(BaseAPI):
    """
    Loan Data API

    Provides access to loan information, payment schedules, and loan operations.
    In production, this would connect to the Loan Origination/Servicing System.
    """

    def __init__(self):
        super().__init__(
            name="LoanAPI",
            min_latency_ms=60,
            max_latency_ms=200
        )

    async def get_loan(self, loan_id: str) -> APIResponse[Loan]:
        """
        Get loan by ID.

        Args:
            loan_id: The unique loan identifier

        Returns:
            APIResponse containing Loan data or error
        """
        return await self._execute_request(
            operation=f"get_loan({loan_id})",
            handler=lambda: db.get_loan(loan_id)
        )

    async def get_customer_loans(self, customer_id: str) -> APIResponse[List[Loan]]:
        """
        Get all loans for a customer.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing list of customer loans
        """
        return await self._execute_request(
            operation=f"get_customer_loans({customer_id})",
            handler=lambda: db.get_customer_loans(customer_id)
        )

    async def get_loan_summary(self, customer_id: str) -> APIResponse[dict]:
        """
        Get loan summary for a customer.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing loan summary
        """
        def calculate_summary():
            loans = db.get_customer_loans(customer_id)
            if not loans:
                return {
                    "customer_id": customer_id,
                    "total_loans": 0,
                    "total_balance": "0",
                    "total_monthly_payment": "0",
                    "loans": []
                }

            active_loans = [l for l in loans if l.status == LoanStatus.ACTIVE]
            total_balance = sum(l.current_balance for l in active_loans)
            total_monthly = sum(l.monthly_payment for l in active_loans)

            return {
                "customer_id": customer_id,
                "total_loans": len(loans),
                "active_loans": len(active_loans),
                "total_balance": str(total_balance),
                "total_monthly_payment": str(total_monthly),
                "loans": [
                    {
                        "loan_id": l.loan_id,
                        "type": l.loan_type.value,
                        "balance": str(l.current_balance),
                        "monthly_payment": str(l.monthly_payment),
                        "next_payment_date": l.next_payment_date.isoformat(),
                        "status": l.status.value
                    }
                    for l in loans
                ]
            }

        return await self._execute_request(
            operation=f"get_loan_summary({customer_id})",
            handler=calculate_summary
        )

    async def get_payment_schedule(self, loan_id: str) -> APIResponse[dict]:
        """
        Get upcoming payment schedule for a loan.

        Args:
            loan_id: The loan identifier

        Returns:
            APIResponse containing payment schedule
        """
        def get_schedule():
            loan = db.get_loan(loan_id)
            if not loan:
                return None

            # Generate next 6 payment dates
            payments = []
            next_date = loan.next_payment_date

            for i in range(min(6, loan.payments_remaining)):
                payments.append({
                    "payment_number": loan.payments_made + i + 1,
                    "due_date": next_date.isoformat(),
                    "amount": str(loan.monthly_payment),
                    "principal_estimate": str(round(loan.monthly_payment * Decimal("0.7"), 2)),
                    "interest_estimate": str(round(loan.monthly_payment * Decimal("0.3"), 2))
                })
                # Move to next month
                if next_date.month == 12:
                    next_date = date(next_date.year + 1, 1, next_date.day)
                else:
                    try:
                        next_date = date(next_date.year, next_date.month + 1, next_date.day)
                    except ValueError:
                        # Handle months with fewer days
                        next_date = date(next_date.year, next_date.month + 1, 28)

            return {
                "loan_id": loan_id,
                "loan_type": loan.loan_type.value,
                "current_balance": str(loan.current_balance),
                "interest_rate": str(loan.interest_rate),
                "payments_made": loan.payments_made,
                "payments_remaining": loan.payments_remaining,
                "maturity_date": loan.maturity_date.isoformat(),
                "upcoming_payments": payments
            }

        return await self._execute_request(
            operation=f"get_payment_schedule({loan_id})",
            handler=get_schedule
        )

    async def get_payoff_amount(self, loan_id: str) -> APIResponse[dict]:
        """
        Calculate payoff amount for a loan.

        Args:
            loan_id: The loan identifier

        Returns:
            APIResponse containing payoff information
        """
        def calculate_payoff():
            loan = db.get_loan(loan_id)
            if not loan:
                return None

            # Simple payoff calculation (in reality would be more complex)
            # Current balance + estimated accrued interest
            days_to_payoff = 10  # Assuming 10 days to process
            daily_rate = loan.interest_rate / Decimal("365") / Decimal("100")
            accrued_interest = loan.current_balance * daily_rate * Decimal(str(days_to_payoff))
            payoff_amount = loan.current_balance + accrued_interest

            return {
                "loan_id": loan_id,
                "current_balance": str(loan.current_balance),
                "accrued_interest": str(round(accrued_interest, 2)),
                "payoff_amount": str(round(payoff_amount, 2)),
                "valid_through": (date.today() + timedelta(days=10)).isoformat(),
                "note": "Payoff amount valid for 10 days. Contact us for exact payoff after this date."
            }

        return await self._execute_request(
            operation=f"get_payoff_amount({loan_id})",
            handler=calculate_payoff
        )
