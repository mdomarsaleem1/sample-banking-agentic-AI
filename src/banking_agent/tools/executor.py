"""
Tool Executor - Executes tools called by the AI agent.
"""

import logging
from decimal import Decimal
from typing import Any, Dict, Optional

from ..apis import APIGateway
from ..agent.context import ConversationContext

logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executes tools called by the AI agent.

    Maps tool names to API calls and handles parameter conversion,
    error handling, and result formatting.
    """

    def __init__(self, api_gateway: Optional[APIGateway] = None):
        """Initialize the tool executor with an API gateway."""
        self.api = api_gateway or APIGateway()

    async def execute(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: Optional[ConversationContext] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool with the given parameters.

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters
            context: Optional conversation context

        Returns:
            Tool execution result
        """
        logger.info(f"Executing tool: {tool_name} with params: {parameters}")

        try:
            # Route to appropriate handler
            handler = self._get_handler(tool_name)
            if not handler:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

            result = await handler(parameters, context)

            # Record action in context if available
            if context:
                context.record_action(tool_name, {
                    "parameters": parameters,
                    "success": result.get("success", True) if isinstance(result, dict) else True
                })

            return result

        except Exception as e:
            logger.error(f"Tool execution error: {tool_name} - {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def _get_handler(self, tool_name: str):
        """Get the handler function for a tool."""
        handlers = {
            # Customer tools
            "identify_customer_by_phone": self._identify_by_phone,
            "identify_customer_by_email": self._identify_by_email,
            "verify_customer_identity": self._verify_customer,
            "get_customer_profile": self._get_customer_profile,

            # Account tools
            "check_account_balance": self._check_balance,
            "get_all_account_balances": self._get_all_balances,
            "get_customer_accounts": self._get_customer_accounts,
            "transfer_funds": self._transfer_funds,

            # Transaction tools
            "get_recent_transactions": self._get_recent_transactions,
            "search_transactions": self._search_transactions,
            "get_spending_summary": self._get_spending_summary,
            "find_transaction": self._find_transaction,

            # Loan tools
            "get_loan_summary": self._get_loan_summary,
            "get_loan_details": self._get_loan_details,
            "get_payment_schedule": self._get_payment_schedule,
            "get_payoff_amount": self._get_payoff_amount,

            # Card tools
            "get_card_summary": self._get_card_summary,
            "check_card_status": self._check_card_status,
            "report_card_lost_stolen": self._report_card_lost_stolen,
            "block_card": self._block_card,

            # Support tools
            "get_open_tickets": self._get_open_tickets,
            "get_ticket_details": self._get_ticket_details,
            "create_support_ticket": self._create_support_ticket,
            "escalate_ticket": self._escalate_ticket,
            "get_ticket_history": self._get_ticket_history,
        }
        return handlers.get(tool_name)

    # ============ Customer Handlers ============

    async def _identify_by_phone(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.customer.get_customer_by_phone(params["phone_number"])
        if response.success and response.data:
            return {
                "success": True,
                "customer_found": True,
                "customer_id": response.data.customer_id,
                "name": response.data.full_name,
                "email": response.data.email,
                "segment": response.data.segment
            }
        return {"success": True, "customer_found": False, "message": "No customer found with this phone number"}

    async def _identify_by_email(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.customer.get_customer_by_email(params["email"])
        if response.success and response.data:
            return {
                "success": True,
                "customer_found": True,
                "customer_id": response.data.customer_id,
                "name": response.data.full_name,
                "phone": response.data.phone,
                "segment": response.data.segment
            }
        return {"success": True, "customer_found": False, "message": "No customer found with this email"}

    async def _verify_customer(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.customer.verify_customer(
            params["customer_id"],
            params["ssn_last_four"],
            params["date_of_birth"]
        )
        return {
            "success": True,
            "verified": response.data if response.success else False,
            "message": "Identity verified successfully" if response.data else "Verification failed"
        }

    async def _get_customer_profile(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.customer.get_customer_profile(params["customer_id"])
        if response.success and response.data:
            profile = response.data
            return {
                "success": True,
                "customer": {
                    "id": profile.customer.customer_id,
                    "name": profile.customer.full_name,
                    "email": profile.customer.email,
                    "phone": profile.customer.phone,
                    "segment": profile.customer.segment,
                    "address": f"{profile.customer.address.city}, {profile.customer.address.state}"
                },
                "accounts_count": len(profile.accounts),
                "total_relationship_value": str(profile.total_relationship_value),
                "customer_since_years": profile.customer_since_years,
                "open_tickets_count": len(profile.open_tickets),
                "active_loans_count": len(profile.loans),
                "cards_count": len(profile.cards)
            }
        return {"success": False, "error": "Customer not found"}

    # ============ Account Handlers ============

    async def _check_balance(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.account.get_account_balance(params["account_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Account not found"}

    async def _get_all_balances(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.account.get_total_balance(params["customer_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not retrieve balances"}

    async def _get_customer_accounts(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.account.get_customer_accounts(params["customer_id"])
        if response.success and response.data:
            accounts = [
                {
                    "account_id": acc.account_id,
                    "type": acc.account_type.value,
                    "account_number": acc.account_number,
                    "balance": str(acc.balance),
                    "available_balance": str(acc.available_balance),
                    "status": acc.status.value
                }
                for acc in response.data
            ]
            return {"success": True, "accounts": accounts, "count": len(accounts)}
        return {"success": False, "error": "Could not retrieve accounts"}

    async def _transfer_funds(self, params: Dict, context: Optional[ConversationContext]):
        amount = Decimal(str(params["amount"]))
        description = params.get("description", "Transfer")
        response = await self.api.account.transfer_funds(
            params["from_account_id"],
            params["to_account_id"],
            amount,
            description
        )
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": response.error or "Transfer failed"}

    # ============ Transaction Handlers ============

    async def _get_recent_transactions(self, params: Dict, context: Optional[ConversationContext]):
        limit = params.get("limit", 10)
        days = params.get("days", 30)
        response = await self.api.transaction.get_recent_transactions(
            params["account_id"], limit, days
        )
        if response.success and response.data:
            transactions = [
                {
                    "id": tx.transaction_id,
                    "date": tx.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "type": tx.transaction_type.value,
                    "amount": str(tx.amount),
                    "description": tx.description,
                    "merchant": tx.merchant_name,
                    "status": tx.status.value,
                    "balance_after": str(tx.balance_after)
                }
                for tx in response.data
            ]
            return {"success": True, "transactions": transactions, "count": len(transactions)}
        return {"success": False, "error": "Could not retrieve transactions"}

    async def _search_transactions(self, params: Dict, context: Optional[ConversationContext]):
        from ..data.models import TransactionType

        tx_type = None
        if "transaction_type" in params:
            try:
                tx_type = TransactionType(params["transaction_type"])
            except ValueError:
                pass

        response = await self.api.transaction.search_transactions(
            account_id=params["account_id"],
            merchant_name=params.get("merchant_name"),
            min_amount=Decimal(str(params["min_amount"])) if "min_amount" in params else None,
            max_amount=Decimal(str(params["max_amount"])) if "max_amount" in params else None,
            transaction_type=tx_type
        )
        if response.success and response.data:
            transactions = [
                {
                    "id": tx.transaction_id,
                    "date": tx.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "type": tx.transaction_type.value,
                    "amount": str(tx.amount),
                    "description": tx.description,
                    "merchant": tx.merchant_name
                }
                for tx in response.data
            ]
            return {"success": True, "transactions": transactions, "count": len(transactions)}
        return {"success": False, "error": "Search failed"}

    async def _get_spending_summary(self, params: Dict, context: Optional[ConversationContext]):
        days = params.get("days", 30)
        response = await self.api.transaction.get_spending_summary(
            params["account_id"], days
        )
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not generate spending summary"}

    async def _find_transaction(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.transaction.get_transaction(params["transaction_id"])
        if response.success and response.data:
            tx = response.data
            return {
                "success": True,
                "transaction": {
                    "id": tx.transaction_id,
                    "date": tx.timestamp.strftime("%Y-%m-%d %H:%M"),
                    "type": tx.transaction_type.value,
                    "amount": str(tx.amount),
                    "description": tx.description,
                    "merchant": tx.merchant_name,
                    "status": tx.status.value,
                    "reference": tx.reference_number
                }
            }
        return {"success": False, "error": "Transaction not found"}

    # ============ Loan Handlers ============

    async def _get_loan_summary(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.loan.get_loan_summary(params["customer_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not retrieve loan information"}

    async def _get_loan_details(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.loan.get_loan(params["loan_id"])
        if response.success and response.data:
            loan = response.data
            return {
                "success": True,
                "loan": {
                    "id": loan.loan_id,
                    "type": loan.loan_type.value,
                    "principal": str(loan.principal_amount),
                    "current_balance": str(loan.current_balance),
                    "interest_rate": str(loan.interest_rate),
                    "monthly_payment": str(loan.monthly_payment),
                    "next_payment_date": loan.next_payment_date.isoformat(),
                    "payments_made": loan.payments_made,
                    "payments_remaining": loan.payments_remaining,
                    "status": loan.status.value
                }
            }
        return {"success": False, "error": "Loan not found"}

    async def _get_payment_schedule(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.loan.get_payment_schedule(params["loan_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not retrieve payment schedule"}

    async def _get_payoff_amount(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.loan.get_payoff_amount(params["loan_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not calculate payoff amount"}

    # ============ Card Handlers ============

    async def _get_card_summary(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.card.get_card_summary(params["customer_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not retrieve card information"}

    async def _check_card_status(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.card.check_card_status(params["card_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Card not found"}

    async def _report_card_lost_stolen(self, params: Dict, context: Optional[ConversationContext]):
        is_stolen = params.get("is_stolen", False)
        response = await self.api.card.report_lost_stolen(
            params["customer_id"],
            params["card_last_four"],
            "stolen" if is_stolen else "lost"
        )
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": response.error or "Could not process report"}

    async def _block_card(self, params: Dict, context: Optional[ConversationContext]):
        reason = params.get("reason", "customer_request")
        response = await self.api.card.block_card(params["card_id"], reason)
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": response.error or "Could not block card"}

    # ============ Support Handlers ============

    async def _get_open_tickets(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.support.get_customer_tickets(params["customer_id"])
        if response.success and response.data:
            tickets = [
                {
                    "ticket_id": t.ticket_id,
                    "subject": t.subject,
                    "category": t.category.value,
                    "status": t.status.value,
                    "priority": t.priority.value,
                    "created_at": t.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for t in response.data
            ]
            return {"success": True, "tickets": tickets, "count": len(tickets)}
        return {"success": False, "error": "Could not retrieve tickets"}

    async def _get_ticket_details(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.support.get_ticket(params["ticket_id"])
        if response.success and response.data:
            t = response.data
            return {
                "success": True,
                "ticket": {
                    "ticket_id": t.ticket_id,
                    "subject": t.subject,
                    "description": t.description,
                    "category": t.category.value,
                    "status": t.status.value,
                    "priority": t.priority.value,
                    "created_at": t.created_at.strftime("%Y-%m-%d %H:%M"),
                    "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M"),
                    "assigned_to": t.assigned_to,
                    "resolution": t.resolution,
                    "notes": t.notes
                }
            }
        return {"success": False, "error": "Ticket not found"}

    async def _create_support_ticket(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.support.create_ticket(
            customer_id=params["customer_id"],
            category=params["category"],
            subject=params["subject"],
            description=params["description"],
            priority=params.get("priority", "medium")
        )
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not create ticket"}

    async def _escalate_ticket(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.support.escalate_ticket(
            params["ticket_id"],
            params["reason"]
        )
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not escalate ticket"}

    async def _get_ticket_history(self, params: Dict, context: Optional[ConversationContext]):
        response = await self.api.support.get_ticket_history(params["customer_id"])
        if response.success and response.data:
            return {"success": True, **response.data}
        return {"success": False, "error": "Could not retrieve ticket history"}
