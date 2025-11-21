"""
Card API - Handles debit/credit card information and operations.
"""

from datetime import datetime
from typing import List, Optional
from ..data.database import db
from ..data.models import Card, CardStatus, CardType
from .base import BaseAPI, APIResponse


class CardAPI(BaseAPI):
    """
    Card Data API

    Provides access to card information and card management operations.
    In production, this would connect to the Card Management System.
    """

    def __init__(self):
        super().__init__(
            name="CardAPI",
            min_latency_ms=40,
            max_latency_ms=150
        )

    async def get_card(self, card_id: str) -> APIResponse[Card]:
        """
        Get card by ID.

        Args:
            card_id: The unique card identifier

        Returns:
            APIResponse containing Card data or error
        """
        return await self._execute_request(
            operation=f"get_card({card_id})",
            handler=lambda: db.get_card(card_id)
        )

    async def get_customer_cards(self, customer_id: str) -> APIResponse[List[Card]]:
        """
        Get all cards for a customer.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing list of customer cards
        """
        return await self._execute_request(
            operation=f"get_customer_cards({customer_id})",
            handler=lambda: db.get_customer_cards(customer_id)
        )

    async def get_card_summary(self, customer_id: str) -> APIResponse[dict]:
        """
        Get card summary for a customer.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing card summary
        """
        def calculate_summary():
            cards = db.get_customer_cards(customer_id)
            if not cards:
                return {
                    "customer_id": customer_id,
                    "total_cards": 0,
                    "cards": []
                }

            active_cards = [c for c in cards if c.status == CardStatus.ACTIVE]
            credit_cards = [c for c in cards if c.card_type == CardType.CREDIT]

            total_credit_limit = sum(
                c.credit_limit or 0 for c in credit_cards if c.credit_limit
            )
            total_credit_used = sum(
                c.current_balance or 0 for c in credit_cards if c.current_balance
            )

            return {
                "customer_id": customer_id,
                "total_cards": len(cards),
                "active_cards": len(active_cards),
                "debit_cards": len([c for c in cards if c.card_type == CardType.DEBIT]),
                "credit_cards": len(credit_cards),
                "total_credit_limit": str(total_credit_limit),
                "total_credit_used": str(total_credit_used),
                "total_available_credit": str(total_credit_limit - total_credit_used),
                "cards": [
                    {
                        "card_id": c.card_id,
                        "type": c.card_type.value,
                        "last_four": c.card_number_masked.split("-")[-1],
                        "expiration": c.expiration_date,
                        "status": c.status.value,
                        "credit_limit": str(c.credit_limit) if c.credit_limit else None,
                        "current_balance": str(c.current_balance) if c.current_balance else None
                    }
                    for c in cards
                ]
            }

        return await self._execute_request(
            operation=f"get_card_summary({customer_id})",
            handler=calculate_summary
        )

    async def block_card(
        self,
        card_id: str,
        reason: str = "lost"
    ) -> APIResponse[dict]:
        """
        Block/freeze a card.

        Args:
            card_id: The card identifier
            reason: Reason for blocking (lost, stolen, fraud, customer_request)

        Returns:
            APIResponse containing block confirmation
        """
        def execute_block():
            card = db.get_card(card_id)
            if not card:
                raise ValueError(f"Card {card_id} not found")

            if card.status in [CardStatus.BLOCKED, CardStatus.LOST, CardStatus.STOLEN]:
                return {
                    "success": True,
                    "card_id": card_id,
                    "message": f"Card is already blocked (status: {card.status.value})",
                    "previous_status": card.status.value,
                    "current_status": card.status.value
                }

            # Map reason to status
            status_map = {
                "lost": CardStatus.LOST,
                "stolen": CardStatus.STOLEN,
                "fraud": CardStatus.BLOCKED,
                "customer_request": CardStatus.BLOCKED
            }
            new_status = status_map.get(reason.lower(), CardStatus.BLOCKED)

            previous_status = card.status
            db.block_card(card_id, new_status)

            return {
                "success": True,
                "card_id": card_id,
                "card_number_masked": card.card_number_masked,
                "reason": reason,
                "previous_status": previous_status.value,
                "current_status": new_status.value,
                "blocked_at": datetime.now().isoformat(),
                "message": f"Card ending in {card.card_number_masked.split('-')[-1]} has been blocked. "
                          f"A replacement card will be shipped within 5-7 business days."
            }

        return await self._execute_request(
            operation=f"block_card({card_id}, reason={reason})",
            handler=execute_block
        )

    async def report_lost_stolen(
        self,
        customer_id: str,
        card_last_four: str,
        report_type: str = "lost"
    ) -> APIResponse[dict]:
        """
        Report a card as lost or stolen by last 4 digits.

        Args:
            customer_id: The customer identifier
            card_last_four: Last 4 digits of the card
            report_type: "lost" or "stolen"

        Returns:
            APIResponse containing report confirmation
        """
        def process_report():
            cards = db.get_customer_cards(customer_id)

            # Find matching card
            matching_card = None
            for card in cards:
                if card.card_number_masked.endswith(card_last_four):
                    matching_card = card
                    break

            if not matching_card:
                raise ValueError(
                    f"No card found ending in {card_last_four} for this customer"
                )

            # Block the card
            new_status = CardStatus.STOLEN if report_type == "stolen" else CardStatus.LOST
            db.block_card(matching_card.card_id, new_status)

            return {
                "success": True,
                "card_id": matching_card.card_id,
                "card_number_masked": matching_card.card_number_masked,
                "card_type": matching_card.card_type.value,
                "report_type": report_type,
                "status": new_status.value,
                "reported_at": datetime.now().isoformat(),
                "actions_taken": [
                    "Card has been immediately blocked",
                    "All pending transactions will be reviewed",
                    "Fraud monitoring team has been notified" if report_type == "stolen" else None,
                    "A replacement card will be shipped within 5-7 business days"
                ],
                "next_steps": "Please monitor your account for any unauthorized transactions. "
                             "If you see any suspicious activity, please report it immediately."
            }

        return await self._execute_request(
            operation=f"report_lost_stolen({customer_id}, ****{card_last_four}, {report_type})",
            handler=process_report
        )

    async def check_card_status(self, card_id: str) -> APIResponse[dict]:
        """
        Check the current status of a card.

        Args:
            card_id: The card identifier

        Returns:
            APIResponse containing card status details
        """
        def get_status():
            card = db.get_card(card_id)
            if not card:
                return None

            return {
                "card_id": card.card_id,
                "card_number_masked": card.card_number_masked,
                "card_type": card.card_type.value,
                "status": card.status.value,
                "is_active": card.status == CardStatus.ACTIVE,
                "expiration_date": card.expiration_date,
                "international_enabled": card.international_enabled,
                "contactless_enabled": card.contactless_enabled,
                "daily_limit": str(card.daily_limit)
            }

        return await self._execute_request(
            operation=f"check_card_status({card_id})",
            handler=get_status
        )
