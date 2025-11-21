"""
Conversation Context Management - Maintains state during customer interactions.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ..data.models import Customer, CustomerProfile


class Message(BaseModel):
    """A single message in the conversation."""
    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    tool_name: Optional[str] = None
    tool_result: Optional[Any] = None


class CustomerSession(BaseModel):
    """Represents an authenticated customer session."""
    customer_id: str
    customer: Optional[Customer] = None
    profile: Optional[CustomerProfile] = None
    verified: bool = False
    verification_level: str = "none"  # none, basic, full
    started_at: datetime = Field(default_factory=datetime.now)


class ConversationContext(BaseModel):
    """
    Maintains conversation context throughout a customer interaction.

    This context is used by the AI agent to understand:
    - Who the customer is
    - What they've discussed
    - What actions have been taken
    - What information has been retrieved
    """

    session_id: str
    session: Optional[CustomerSession] = None
    messages: List[Message] = Field(default_factory=list)
    retrieved_data: Dict[str, Any] = Field(default_factory=dict)
    actions_taken: List[Dict[str, Any]] = Field(default_factory=list)
    intent_history: List[str] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)

    class Config:
        arbitrary_types_allowed = True

    def add_message(
        self,
        role: str,
        content: str,
        tool_name: Optional[str] = None,
        tool_result: Optional[Any] = None
    ):
        """Add a message to the conversation history."""
        message = Message(
            role=role,
            content=content,
            tool_name=tool_name,
            tool_result=tool_result
        )
        self.messages.append(message)
        self.last_activity = datetime.now()

    def add_user_message(self, content: str):
        """Add a user message."""
        self.add_message("user", content)

    def add_assistant_message(self, content: str):
        """Add an assistant message."""
        self.add_message("assistant", content)

    def add_tool_result(self, tool_name: str, result: Any):
        """Add a tool execution result."""
        self.add_message(
            "tool",
            f"Tool '{tool_name}' executed",
            tool_name=tool_name,
            tool_result=result
        )
        # Also store in retrieved_data for easy access
        self.retrieved_data[tool_name] = result

    def record_action(self, action_type: str, details: Dict[str, Any]):
        """Record an action taken during the conversation."""
        self.actions_taken.append({
            "type": action_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def add_intent(self, intent: str):
        """Record detected customer intent."""
        self.intent_history.append(intent)

    def set_customer_session(self, session: CustomerSession):
        """Set the customer session after identification."""
        self.session = session

    def is_customer_identified(self) -> bool:
        """Check if customer has been identified."""
        return self.session is not None and self.session.customer is not None

    def is_customer_verified(self) -> bool:
        """Check if customer identity has been verified."""
        return self.session is not None and self.session.verified

    def get_customer_id(self) -> Optional[str]:
        """Get the current customer ID if available."""
        if self.session:
            return self.session.customer_id
        return None

    def get_conversation_summary(self) -> str:
        """Get a brief summary of the conversation for the agent."""
        summary_parts = []

        if self.session and self.session.customer:
            summary_parts.append(
                f"Customer: {self.session.customer.full_name} "
                f"(ID: {self.session.customer_id})"
            )
            summary_parts.append(
                f"Verification: {self.session.verification_level}"
            )

        if self.intent_history:
            summary_parts.append(f"Intents: {', '.join(self.intent_history[-3:])}")

        if self.actions_taken:
            recent_actions = [a['type'] for a in self.actions_taken[-3:]]
            summary_parts.append(f"Recent actions: {', '.join(recent_actions)}")

        return " | ".join(summary_parts) if summary_parts else "New conversation"

    def get_message_history_for_llm(self, max_messages: int = 20) -> List[Dict[str, str]]:
        """Get formatted message history for LLM input."""
        # Get recent messages, excluding tool results
        recent = self.messages[-max_messages:]
        formatted = []

        for msg in recent:
            if msg.role in ["user", "assistant"]:
                formatted.append({
                    "role": msg.role,
                    "content": msg.content
                })

        return formatted
