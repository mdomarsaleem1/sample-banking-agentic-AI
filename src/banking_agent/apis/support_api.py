"""
Support API - Handles support tickets and case management.
"""

import random
from datetime import datetime
from typing import List, Optional
from ..data.database import db
from ..data.models import (
    SupportTicket, TicketStatus, TicketPriority, TicketCategory
)
from .base import BaseAPI, APIResponse


class SupportAPI(BaseAPI):
    """
    Support Ticket Data API

    Provides access to support tickets and case management.
    In production, this would connect to the CRM/Ticketing System.
    """

    def __init__(self):
        super().__init__(
            name="SupportAPI",
            min_latency_ms=30,
            max_latency_ms=120
        )

    async def get_ticket(self, ticket_id: str) -> APIResponse[SupportTicket]:
        """
        Get support ticket by ID.

        Args:
            ticket_id: The unique ticket identifier

        Returns:
            APIResponse containing SupportTicket data or error
        """
        return await self._execute_request(
            operation=f"get_ticket({ticket_id})",
            handler=lambda: db.get_ticket(ticket_id)
        )

    async def get_customer_tickets(
        self,
        customer_id: str,
        include_closed: bool = False
    ) -> APIResponse[List[SupportTicket]]:
        """
        Get all tickets for a customer.

        Args:
            customer_id: The customer identifier
            include_closed: Whether to include closed/resolved tickets

        Returns:
            APIResponse containing list of tickets
        """
        return await self._execute_request(
            operation=f"get_customer_tickets({customer_id})",
            handler=lambda: db.get_customer_tickets(customer_id, include_closed)
        )

    async def create_ticket(
        self,
        customer_id: str,
        category: str,
        subject: str,
        description: str,
        priority: str = "medium",
        related_account_id: Optional[str] = None,
        related_transaction_id: Optional[str] = None
    ) -> APIResponse[dict]:
        """
        Create a new support ticket.

        Args:
            customer_id: The customer identifier
            category: Ticket category
            subject: Ticket subject
            description: Detailed description
            priority: Ticket priority (low, medium, high, urgent)
            related_account_id: Optional related account
            related_transaction_id: Optional related transaction

        Returns:
            APIResponse containing created ticket info
        """
        def create():
            # Generate ticket ID
            ticket_id = f"TKT{random.randint(10000, 99999)}"

            # Map string values to enums
            try:
                cat_enum = TicketCategory(category.lower())
            except ValueError:
                cat_enum = TicketCategory.GENERAL_INQUIRY

            try:
                pri_enum = TicketPriority(priority.lower())
            except ValueError:
                pri_enum = TicketPriority.MEDIUM

            ticket = SupportTicket(
                ticket_id=ticket_id,
                customer_id=customer_id,
                category=cat_enum,
                subject=subject,
                description=description,
                status=TicketStatus.OPEN,
                priority=pri_enum,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                related_account_id=related_account_id,
                related_transaction_id=related_transaction_id
            )

            db.create_ticket(ticket)

            return {
                "success": True,
                "ticket_id": ticket_id,
                "status": "open",
                "priority": pri_enum.value,
                "category": cat_enum.value,
                "created_at": ticket.created_at.isoformat(),
                "message": f"Your support ticket #{ticket_id} has been created. "
                          f"A representative will review your request shortly.",
                "expected_response_time": self._get_response_time(pri_enum)
            }

        return await self._execute_request(
            operation=f"create_ticket({customer_id}, {category})",
            handler=create
        )

    def _get_response_time(self, priority: TicketPriority) -> str:
        """Get expected response time based on priority."""
        times = {
            TicketPriority.URGENT: "Within 1 hour",
            TicketPriority.HIGH: "Within 4 hours",
            TicketPriority.MEDIUM: "Within 24 hours",
            TicketPriority.LOW: "Within 48 hours"
        }
        return times.get(priority, "Within 24 hours")

    async def update_ticket(
        self,
        ticket_id: str,
        status: Optional[str] = None,
        add_note: Optional[str] = None,
        resolution: Optional[str] = None
    ) -> APIResponse[dict]:
        """
        Update a support ticket.

        Args:
            ticket_id: The ticket identifier
            status: New status (optional)
            add_note: Note to add (optional)
            resolution: Resolution text (optional)

        Returns:
            APIResponse containing update confirmation
        """
        def update():
            ticket = db.get_ticket(ticket_id)
            if not ticket:
                raise ValueError(f"Ticket {ticket_id} not found")

            updates = {}

            if status:
                try:
                    status_enum = TicketStatus(status.lower())
                    updates["status"] = status_enum
                except ValueError:
                    pass

            if add_note:
                current_notes = ticket.notes.copy()
                current_notes.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {add_note}")
                updates["notes"] = current_notes

            if resolution:
                updates["resolution"] = resolution
                updates["status"] = TicketStatus.RESOLVED

            db.update_ticket(ticket_id, **updates)

            return {
                "success": True,
                "ticket_id": ticket_id,
                "updates_applied": list(updates.keys()),
                "current_status": updates.get("status", ticket.status).value if isinstance(
                    updates.get("status", ticket.status), TicketStatus
                ) else ticket.status.value,
                "updated_at": datetime.now().isoformat()
            }

        return await self._execute_request(
            operation=f"update_ticket({ticket_id})",
            handler=update
        )

    async def get_ticket_history(self, customer_id: str) -> APIResponse[dict]:
        """
        Get ticket history summary for a customer.

        Args:
            customer_id: The customer identifier

        Returns:
            APIResponse containing ticket history summary
        """
        def get_history():
            all_tickets = db.get_customer_tickets(customer_id, include_closed=True)

            open_tickets = [t for t in all_tickets if t.status == TicketStatus.OPEN]
            in_progress = [t for t in all_tickets if t.status == TicketStatus.IN_PROGRESS]
            resolved = [t for t in all_tickets if t.status == TicketStatus.RESOLVED]
            closed = [t for t in all_tickets if t.status == TicketStatus.CLOSED]

            return {
                "customer_id": customer_id,
                "total_tickets": len(all_tickets),
                "open": len(open_tickets),
                "in_progress": len(in_progress),
                "resolved": len(resolved),
                "closed": len(closed),
                "recent_tickets": [
                    {
                        "ticket_id": t.ticket_id,
                        "subject": t.subject,
                        "category": t.category.value,
                        "status": t.status.value,
                        "created_at": t.created_at.isoformat(),
                        "resolution": t.resolution
                    }
                    for t in sorted(all_tickets, key=lambda x: x.created_at, reverse=True)[:5]
                ]
            }

        return await self._execute_request(
            operation=f"get_ticket_history({customer_id})",
            handler=get_history
        )

    async def escalate_ticket(
        self,
        ticket_id: str,
        reason: str
    ) -> APIResponse[dict]:
        """
        Escalate a ticket to higher priority.

        Args:
            ticket_id: The ticket identifier
            reason: Reason for escalation

        Returns:
            APIResponse containing escalation confirmation
        """
        def escalate():
            ticket = db.get_ticket(ticket_id)
            if not ticket:
                raise ValueError(f"Ticket {ticket_id} not found")

            # Increase priority
            priority_order = [
                TicketPriority.LOW,
                TicketPriority.MEDIUM,
                TicketPriority.HIGH,
                TicketPriority.URGENT
            ]
            current_idx = priority_order.index(ticket.priority)
            new_priority = priority_order[min(current_idx + 1, len(priority_order) - 1)]

            # Update ticket
            current_notes = ticket.notes.copy()
            current_notes.append(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] "
                f"ESCALATED: {reason}"
            )

            db.update_ticket(
                ticket_id,
                priority=new_priority,
                status=TicketStatus.ESCALATED,
                notes=current_notes
            )

            return {
                "success": True,
                "ticket_id": ticket_id,
                "previous_priority": ticket.priority.value,
                "new_priority": new_priority.value,
                "status": "escalated",
                "reason": reason,
                "escalated_at": datetime.now().isoformat(),
                "message": "Your ticket has been escalated and will receive priority attention."
            }

        return await self._execute_request(
            operation=f"escalate_ticket({ticket_id})",
            handler=escalate
        )
