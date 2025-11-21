"""
Customer API - Handles customer profile and information queries.
"""

from typing import List, Optional
from ..data.database import db
from ..data.models import Customer, CustomerProfile
from .base import BaseAPI, APIResponse


class CustomerAPI(BaseAPI):
    """
    Customer Data API

    Provides access to customer profiles, verification, and search functionality.
    In production, this would connect to the Customer Information System (CIS).
    """

    def __init__(self):
        super().__init__(
            name="CustomerAPI",
            min_latency_ms=30,
            max_latency_ms=150
        )

    async def get_customer(self, customer_id: str) -> APIResponse[Customer]:
        """
        Retrieve customer by ID.

        Args:
            customer_id: The unique customer identifier

        Returns:
            APIResponse containing Customer data or error
        """
        return await self._execute_request(
            operation=f"get_customer({customer_id})",
            handler=lambda: db.get_customer(customer_id)
        )

    async def get_customer_by_phone(self, phone: str) -> APIResponse[Customer]:
        """
        Retrieve customer by phone number.
        Used for caller identification in call center.

        Args:
            phone: Customer phone number

        Returns:
            APIResponse containing Customer data or error
        """
        return await self._execute_request(
            operation=f"get_customer_by_phone({phone})",
            handler=lambda: db.get_customer_by_phone(phone)
        )

    async def get_customer_by_email(self, email: str) -> APIResponse[Customer]:
        """
        Retrieve customer by email address.

        Args:
            email: Customer email address

        Returns:
            APIResponse containing Customer data or error
        """
        return await self._execute_request(
            operation=f"get_customer_by_email({email})",
            handler=lambda: db.get_customer_by_email(email)
        )

    async def search_customers(self, query: str) -> APIResponse[List[Customer]]:
        """
        Search for customers by name, email, or phone.

        Args:
            query: Search query string

        Returns:
            APIResponse containing list of matching customers
        """
        return await self._execute_request(
            operation=f"search_customers({query})",
            handler=lambda: db.search_customer(query)
        )

    async def get_customer_profile(self, customer_id: str) -> APIResponse[CustomerProfile]:
        """
        Get comprehensive customer profile including accounts, transactions, etc.

        Args:
            customer_id: The unique customer identifier

        Returns:
            APIResponse containing full CustomerProfile or error
        """
        return await self._execute_request(
            operation=f"get_customer_profile({customer_id})",
            handler=lambda: db.get_customer_profile(customer_id)
        )

    async def verify_customer(
        self,
        customer_id: str,
        ssn_last_four: str,
        date_of_birth: str
    ) -> APIResponse[bool]:
        """
        Verify customer identity using SSN last 4 and DOB.

        Args:
            customer_id: Customer ID to verify
            ssn_last_four: Last 4 digits of SSN
            date_of_birth: Date of birth in YYYY-MM-DD format

        Returns:
            APIResponse containing verification result (True/False)
        """
        def verify():
            customer = db.get_customer(customer_id)
            if not customer:
                return False
            return (
                customer.ssn_last_four == ssn_last_four and
                customer.date_of_birth.isoformat() == date_of_birth
            )

        return await self._execute_request(
            operation=f"verify_customer({customer_id})",
            handler=verify
        )

    async def get_all_customers(self) -> APIResponse[List[Customer]]:
        """
        Get all customers (for demo/testing purposes).

        Returns:
            APIResponse containing list of all customers
        """
        return await self._execute_request(
            operation="get_all_customers()",
            handler=lambda: db.get_all_customers()
        )
