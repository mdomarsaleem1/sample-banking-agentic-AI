"""
Banking Agent Core - The main AI agent for handling customer queries.

This module implements the core agent logic that:
1. Processes customer queries
2. Determines appropriate tools to call
3. Executes tools via the API layer
4. Generates responses
"""

import json
import logging
import uuid
from typing import Any, Dict, List, Optional

from ..apis import APIGateway
from ..tools.definitions import get_tool_definitions
from ..tools.executor import ToolExecutor
from .context import ConversationContext, CustomerSession

logger = logging.getLogger(__name__)

# System prompt for the banking agent
SYSTEM_PROMPT = """You are an AI assistant for SecureBank's call center. Your role is to help customers with their banking needs professionally and efficiently.

## Your Capabilities:
1. **Customer Identification**: Look up customers by phone or email
2. **Account Information**: Check balances, view accounts, transfer funds
3. **Transaction History**: View recent transactions, search for specific transactions, spending analysis
4. **Loan Services**: View loan details, payment schedules, payoff amounts
5. **Card Services**: View cards, report lost/stolen cards, block cards
6. **Support**: View and create support tickets, escalate issues

## Guidelines:
1. **Always identify the customer first** before providing account-specific information
2. **For sensitive operations** (transfers, blocking cards), verify the customer's identity first
3. **Be helpful and professional** - explain what you're doing and why
4. **Protect customer privacy** - don't reveal full account numbers or sensitive data unnecessarily
5. **Create support tickets** for issues that can't be resolved immediately
6. **Escalate appropriately** when customers are frustrated or have urgent issues

## Response Format:
- Be concise but thorough
- Explain the results of your actions
- Offer relevant follow-up assistance
- Always confirm important actions before executing

## Tools Available:
You have access to various banking tools. Use them appropriately based on the customer's request.
"""


class BankingAgent:
    """
    The main banking call center AI agent.

    This agent:
    - Manages conversation context
    - Interprets customer intents
    - Calls appropriate tools
    - Generates helpful responses
    """

    def __init__(
        self,
        api_gateway: Optional[APIGateway] = None,
        ai_provider: str = "mock"  # "openai", "anthropic", or "mock"
    ):
        """
        Initialize the banking agent.

        Args:
            api_gateway: Optional API gateway instance
            ai_provider: AI provider to use for LLM calls
        """
        self.api = api_gateway or APIGateway()
        self.tool_executor = ToolExecutor(self.api)
        self.ai_provider = ai_provider
        self.tools = get_tool_definitions()
        self.active_contexts: Dict[str, ConversationContext] = {}

        logger.info(f"Banking Agent initialized with provider: {ai_provider}")

    def create_session(self) -> str:
        """Create a new conversation session."""
        session_id = str(uuid.uuid4())
        self.active_contexts[session_id] = ConversationContext(session_id=session_id)
        logger.info(f"Created new session: {session_id}")
        return session_id

    def get_context(self, session_id: str) -> Optional[ConversationContext]:
        """Get the context for a session."""
        return self.active_contexts.get(session_id)

    async def process_message(
        self,
        session_id: str,
        user_message: str
    ) -> Dict[str, Any]:
        """
        Process a user message and generate a response.

        Args:
            session_id: The conversation session ID
            user_message: The user's message

        Returns:
            Response containing the agent's reply and any actions taken
        """
        context = self.get_context(session_id)
        if not context:
            return {
                "error": "Invalid session ID",
                "response": "I'm sorry, but your session has expired. Please start a new conversation."
            }

        # Add user message to context
        context.add_user_message(user_message)

        # Determine intent and required tools
        intent = self._analyze_intent(user_message)
        context.add_intent(intent)

        # Execute the agentic loop
        response = await self._agentic_loop(context, user_message, intent)

        # Add assistant response to context
        context.add_assistant_message(response["response"])

        return response

    def _analyze_intent(self, message: str) -> str:
        """
        Analyze the user's message to determine intent.

        In a production system, this might use NLP/ML.
        For this demo, we use keyword matching.
        """
        message_lower = message.lower()

        # Intent patterns
        intent_patterns = {
            "balance_inquiry": ["balance", "how much", "account balance", "available"],
            "transaction_history": ["transactions", "history", "recent", "statement", "spending"],
            "transfer_funds": ["transfer", "send money", "move money", "pay"],
            "lost_card": ["lost", "stolen", "missing card", "can't find my card"],
            "block_card": ["block", "freeze", "deactivate", "stop card"],
            "loan_inquiry": ["loan", "payment schedule", "payoff", "mortgage"],
            "support_ticket": ["complaint", "issue", "problem", "help", "support"],
            "account_info": ["accounts", "my accounts", "account details"],
            "card_info": ["cards", "credit card", "debit card", "card status"],
            "identify": ["my name", "identify", "phone", "email", "who am i"],
        }

        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if pattern in message_lower:
                    return intent

        return "general_inquiry"

    async def _agentic_loop(
        self,
        context: ConversationContext,
        user_message: str,
        intent: str
    ) -> Dict[str, Any]:
        """
        Execute the agentic loop to handle the user's request.

        This loop:
        1. Determines which tools to call based on intent and context
        2. Executes tools and collects results
        3. Generates a response based on results
        """
        tools_called = []
        tool_results = []

        # Determine required tools based on intent and context
        tools_to_call = self._plan_tool_calls(context, intent, user_message)

        # Execute tools
        for tool_call in tools_to_call:
            tool_name = tool_call["name"]
            params = tool_call["parameters"]

            logger.info(f"Calling tool: {tool_name} with params: {params}")

            result = await self.tool_executor.execute(tool_name, params, context)

            tools_called.append(tool_name)
            tool_results.append({
                "tool": tool_name,
                "result": result
            })

            # Add tool result to context
            context.add_tool_result(tool_name, result)

        # Generate response based on results
        response_text = self._generate_response(context, intent, tool_results)

        return {
            "response": response_text,
            "intent": intent,
            "tools_called": tools_called,
            "tool_results": tool_results,
            "customer_identified": context.is_customer_identified(),
            "session_summary": context.get_conversation_summary()
        }

    def _plan_tool_calls(
        self,
        context: ConversationContext,
        intent: str,
        user_message: str
    ) -> List[Dict[str, Any]]:
        """
        Plan which tools to call based on intent and context.

        In a production system, this would use the LLM's function calling.
        For this demo, we use rule-based planning.
        """
        tools_to_call = []
        customer_id = context.get_customer_id()

        # Extract parameters from message
        params = self._extract_parameters(user_message)

        # Handle different intents
        if intent == "identify":
            if "phone" in params:
                tools_to_call.append({
                    "name": "identify_customer_by_phone",
                    "parameters": {"phone_number": params["phone"]}
                })
            elif "email" in params:
                tools_to_call.append({
                    "name": "identify_customer_by_email",
                    "parameters": {"email": params["email"]}
                })

        elif intent == "balance_inquiry":
            if customer_id:
                tools_to_call.append({
                    "name": "get_all_account_balances",
                    "parameters": {"customer_id": customer_id}
                })
            else:
                # Need to identify customer first
                pass

        elif intent == "transaction_history":
            if customer_id:
                # First get accounts, then transactions
                tools_to_call.append({
                    "name": "get_customer_accounts",
                    "parameters": {"customer_id": customer_id}
                })
                # Note: In a more sophisticated implementation,
                # we'd call get_recent_transactions after getting accounts

        elif intent == "account_info":
            if customer_id:
                tools_to_call.append({
                    "name": "get_customer_accounts",
                    "parameters": {"customer_id": customer_id}
                })

        elif intent == "card_info":
            if customer_id:
                tools_to_call.append({
                    "name": "get_card_summary",
                    "parameters": {"customer_id": customer_id}
                })

        elif intent == "lost_card":
            if customer_id and "last_four" in params:
                is_stolen = "stolen" in user_message.lower()
                tools_to_call.append({
                    "name": "report_card_lost_stolen",
                    "parameters": {
                        "customer_id": customer_id,
                        "card_last_four": params["last_four"],
                        "is_stolen": is_stolen
                    }
                })
            elif customer_id:
                # Get cards first so user can specify
                tools_to_call.append({
                    "name": "get_card_summary",
                    "parameters": {"customer_id": customer_id}
                })

        elif intent == "loan_inquiry":
            if customer_id:
                tools_to_call.append({
                    "name": "get_loan_summary",
                    "parameters": {"customer_id": customer_id}
                })

        elif intent == "support_ticket":
            if customer_id:
                tools_to_call.append({
                    "name": "get_open_tickets",
                    "parameters": {"customer_id": customer_id}
                })

        elif intent == "transfer_funds":
            if customer_id:
                # Get accounts first for transfer
                tools_to_call.append({
                    "name": "get_customer_accounts",
                    "parameters": {"customer_id": customer_id}
                })

        # If no specific tools planned and customer is identified, get profile
        if not tools_to_call and customer_id:
            tools_to_call.append({
                "name": "get_customer_profile",
                "parameters": {"customer_id": customer_id}
            })

        return tools_to_call

    def _extract_parameters(self, message: str) -> Dict[str, Any]:
        """Extract parameters from the user's message."""
        params = {}

        # Extract phone number
        import re
        phone_match = re.search(r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', message)
        if phone_match:
            params["phone"] = phone_match.group()

        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', message)
        if email_match:
            params["email"] = email_match.group()

        # Extract card last 4 digits
        last_four_match = re.search(r'(?:ending in |last four |card )?(\d{4})', message)
        if last_four_match:
            params["last_four"] = last_four_match.group(1)

        # Extract amounts
        amount_match = re.search(r'\$?([\d,]+\.?\d*)', message)
        if amount_match:
            params["amount"] = amount_match.group(1).replace(",", "")

        return params

    def _generate_response(
        self,
        context: ConversationContext,
        intent: str,
        tool_results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate a natural language response based on tool results.

        In production, this would use the LLM to generate responses.
        For this demo, we use template-based responses.
        """
        if not tool_results:
            if not context.is_customer_identified():
                return (
                    "Hello! Welcome to SecureBank. I'd be happy to help you today. "
                    "To get started, could you please provide your phone number or email "
                    "so I can look up your account?"
                )
            else:
                customer_name = context.session.customer.first_name if context.session and context.session.customer else "there"
                return f"Hello {customer_name}! How can I assist you today? I can help you with account balances, transactions, cards, loans, or any other banking needs."

        # Process results and generate response
        responses = []

        for result in tool_results:
            tool_name = result["tool"]
            data = result["result"]

            if not data.get("success", False) and "error" in data:
                responses.append(f"I encountered an issue: {data['error']}")
                continue

            # Generate tool-specific responses
            response = self._format_tool_result(tool_name, data, context)
            if response:
                responses.append(response)

        if responses:
            return "\n\n".join(responses)
        else:
            return "I've processed your request. Is there anything else I can help you with?"

    def _format_tool_result(
        self,
        tool_name: str,
        data: Dict[str, Any],
        context: ConversationContext
    ) -> str:
        """Format a tool result into a natural language response."""

        if tool_name == "identify_customer_by_phone" or tool_name == "identify_customer_by_email":
            if data.get("customer_found"):
                # Update session with customer info
                self._update_session_with_customer(context, data)
                return (
                    f"I found your account. Hello {data['name']}! "
                    f"You're registered as a {data['segment']} customer. "
                    f"How can I assist you today?"
                )
            else:
                return (
                    "I couldn't find an account with that information. "
                    "Could you please verify your phone number or email?"
                )

        elif tool_name == "get_all_account_balances":
            total = data.get("total_balance", "0")
            breakdown = data.get("breakdown", [])
            response = f"Your total balance across all accounts is ${total}.\n\nHere's the breakdown:"
            for acc in breakdown:
                response += f"\n- {acc['account_type'].title()} ({acc['account_id']}): ${acc['balance']}"
            return response

        elif tool_name == "get_customer_accounts":
            accounts = data.get("accounts", [])
            if not accounts:
                return "You don't have any accounts on file."
            response = f"You have {len(accounts)} account(s):"
            for acc in accounts:
                response += f"\n- {acc['type'].title()} ({acc['account_number']}): ${acc['balance']} available - Status: {acc['status']}"
            return response

        elif tool_name == "get_recent_transactions":
            txs = data.get("transactions", [])
            if not txs:
                return "No recent transactions found."
            response = f"Here are your {len(txs)} most recent transactions:"
            for tx in txs[:5]:  # Show max 5
                response += f"\n- {tx['date']}: {tx['description']} - ${tx['amount']} ({tx['type']})"
            if len(txs) > 5:
                response += f"\n...and {len(txs) - 5} more transactions."
            return response

        elif tool_name == "get_card_summary":
            cards = data.get("cards", [])
            if not cards:
                return "You don't have any cards on file."
            response = f"You have {len(cards)} card(s):"
            for card in cards:
                status_icon = "Active" if card['status'] == 'active' else f"{card['status'].upper()}"
                response += f"\n- {card['type'].title()} card ending in {card['last_four']}: {status_icon}"
                if card.get('credit_limit'):
                    response += f" (Credit limit: ${card['credit_limit']}, Balance: ${card.get('current_balance', '0')})"
            return response

        elif tool_name == "report_card_lost_stolen":
            if data.get("success"):
                actions = [a for a in data.get("actions_taken", []) if a]
                response = f"I've processed your report for the card ending in {data.get('card_number_masked', '').split('-')[-1]}.\n\nActions taken:"
                for action in actions:
                    response += f"\n- {action}"
                response += f"\n\n{data.get('next_steps', '')}"
                return response

        elif tool_name == "get_loan_summary":
            loans = data.get("loans", [])
            if not loans:
                return "You don't have any active loans."
            response = f"You have {len(loans)} loan(s) with a total balance of ${data.get('total_balance', '0')}:"
            for loan in loans:
                response += f"\n- {loan['type'].title()} Loan ({loan['loan_id']}): ${loan['balance']} remaining"
                response += f"\n  Monthly payment: ${loan['monthly_payment']} - Next due: {loan['next_payment_date']}"
            return response

        elif tool_name == "get_open_tickets":
            tickets = data.get("tickets", [])
            if not tickets:
                return "You don't have any open support tickets."
            response = f"You have {len(tickets)} open support ticket(s):"
            for ticket in tickets:
                response += f"\n- {ticket['ticket_id']}: {ticket['subject']}"
                response += f"\n  Status: {ticket['status']} | Priority: {ticket['priority']} | Created: {ticket['created_at']}"
            return response

        elif tool_name == "get_customer_profile":
            response = f"Here's your account overview:\n"
            response += f"- Accounts: {data.get('accounts_count', 0)}\n"
            response += f"- Total value: ${data.get('total_relationship_value', '0')}\n"
            response += f"- Active loans: {data.get('active_loans_count', 0)}\n"
            response += f"- Cards: {data.get('cards_count', 0)}\n"
            response += f"- Open tickets: {data.get('open_tickets_count', 0)}\n"
            response += f"\nYou've been a valued customer for {data.get('customer_since_years', 0)} years."
            return response

        elif tool_name == "transfer_funds":
            if data.get("success"):
                return (
                    f"Transfer completed successfully!\n"
                    f"Reference number: {data.get('reference_number')}\n"
                    f"Amount: ${data.get('amount')}\n"
                    f"From account: {data.get('from_account')}\n"
                    f"To account: {data.get('to_account')}"
                )
            else:
                return f"Transfer failed: {data.get('error', 'Unknown error')}"

        elif tool_name == "create_support_ticket":
            if data.get("success"):
                return (
                    f"I've created a support ticket for you.\n"
                    f"Ticket ID: {data.get('ticket_id')}\n"
                    f"Expected response: {data.get('expected_response_time')}\n\n"
                    f"{data.get('message', '')}"
                )

        # Default response for unhandled tools
        return None

    def _update_session_with_customer(
        self,
        context: ConversationContext,
        customer_data: Dict[str, Any]
    ):
        """Update the session with identified customer information."""
        from ..data.database import db

        customer = db.get_customer(customer_data["customer_id"])
        if customer:
            session = CustomerSession(
                customer_id=customer_data["customer_id"],
                customer=customer,
                verified=False,
                verification_level="basic"
            )
            context.set_customer_session(session)

    async def identify_customer(
        self,
        session_id: str,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Manually identify a customer for a session.

        This is useful for pre-populating customer info from caller ID.
        """
        context = self.get_context(session_id)
        if not context:
            return {"error": "Invalid session"}

        if phone:
            result = await self.tool_executor.execute(
                "identify_customer_by_phone",
                {"phone_number": phone},
                context
            )
        elif email:
            result = await self.tool_executor.execute(
                "identify_customer_by_email",
                {"email": email},
                context
            )
        else:
            return {"error": "Must provide phone or email"}

        if result.get("customer_found"):
            self._update_session_with_customer(context, result)

        return result

    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End a conversation session."""
        if session_id in self.active_contexts:
            context = self.active_contexts.pop(session_id)
            return {
                "session_id": session_id,
                "duration_seconds": (context.last_activity - context.started_at).total_seconds(),
                "messages_count": len(context.messages),
                "actions_taken": len(context.actions_taken),
                "intents_detected": context.intent_history
            }
        return {"error": "Session not found"}

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools with descriptions."""
        return [
            {"name": tool["name"], "description": tool["description"]}
            for tool in self.tools
        ]
