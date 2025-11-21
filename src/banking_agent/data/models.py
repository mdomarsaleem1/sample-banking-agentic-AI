"""
Data models representing banking entities.
"""

from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    MONEY_MARKET = "money_market"
    CD = "certificate_of_deposit"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"
    PENDING = "pending"


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    PAYMENT = "payment"
    FEE = "fee"
    INTEREST = "interest"
    REFUND = "refund"
    PURCHASE = "purchase"
    ATM_WITHDRAWAL = "atm_withdrawal"


class TransactionStatus(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"
    FAILED = "failed"
    REVERSED = "reversed"


class LoanType(str, Enum):
    PERSONAL = "personal"
    MORTGAGE = "mortgage"
    AUTO = "auto"
    STUDENT = "student"
    CREDIT_LINE = "credit_line"


class LoanStatus(str, Enum):
    ACTIVE = "active"
    PAID_OFF = "paid_off"
    DEFAULTED = "defaulted"
    PENDING_APPROVAL = "pending_approval"


class CardType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"
    PREPAID = "prepaid"


class CardStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    EXPIRED = "expired"
    LOST = "lost"
    STOLEN = "stolen"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketCategory(str, Enum):
    ACCOUNT_INQUIRY = "account_inquiry"
    TRANSACTION_DISPUTE = "transaction_dispute"
    CARD_ISSUE = "card_issue"
    LOAN_INQUIRY = "loan_inquiry"
    TECHNICAL_ISSUE = "technical_issue"
    FRAUD_REPORT = "fraud_report"
    GENERAL_INQUIRY = "general_inquiry"
    COMPLAINT = "complaint"


class Address(BaseModel):
    """Customer address model."""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"


class Customer(BaseModel):
    """Customer entity model."""
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: date
    ssn_last_four: str  # Last 4 digits only for security
    address: Address
    created_at: datetime
    is_verified: bool = True
    risk_score: int = Field(ge=0, le=100, default=50)
    segment: str = "standard"  # standard, premium, private

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Account(BaseModel):
    """Bank account model."""
    account_id: str
    customer_id: str
    account_type: AccountType
    account_number: str  # Masked for security
    routing_number: str
    balance: Decimal
    available_balance: Decimal
    currency: str = "USD"
    status: AccountStatus
    opened_date: date
    interest_rate: Optional[Decimal] = None
    overdraft_limit: Decimal = Decimal("0")
    last_activity_date: datetime


class Transaction(BaseModel):
    """Transaction model."""
    transaction_id: str
    account_id: str
    transaction_type: TransactionType
    amount: Decimal
    currency: str = "USD"
    description: str
    merchant_name: Optional[str] = None
    merchant_category: Optional[str] = None
    status: TransactionStatus
    timestamp: datetime
    reference_number: str
    balance_after: Decimal
    location: Optional[str] = None


class Loan(BaseModel):
    """Loan model."""
    loan_id: str
    customer_id: str
    loan_type: LoanType
    principal_amount: Decimal
    current_balance: Decimal
    interest_rate: Decimal
    term_months: int
    monthly_payment: Decimal
    next_payment_date: date
    next_payment_amount: Decimal
    status: LoanStatus
    origination_date: date
    maturity_date: date
    payments_made: int
    payments_remaining: int
    collateral: Optional[str] = None


class Card(BaseModel):
    """Card model."""
    card_id: str
    customer_id: str
    account_id: str
    card_type: CardType
    card_number_masked: str  # e.g., "****-****-****-1234"
    expiration_date: str  # MM/YY format
    status: CardStatus
    credit_limit: Optional[Decimal] = None
    current_balance: Optional[Decimal] = None
    available_credit: Optional[Decimal] = None
    issued_date: date
    daily_limit: Decimal
    international_enabled: bool = True
    contactless_enabled: bool = True


class SupportTicket(BaseModel):
    """Support ticket model."""
    ticket_id: str
    customer_id: str
    category: TicketCategory
    subject: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    related_account_id: Optional[str] = None
    related_transaction_id: Optional[str] = None
    notes: List[str] = Field(default_factory=list)


class CustomerProfile(BaseModel):
    """Comprehensive customer profile combining all data."""
    customer: Customer
    accounts: List[Account] = Field(default_factory=list)
    recent_transactions: List[Transaction] = Field(default_factory=list)
    loans: List[Loan] = Field(default_factory=list)
    cards: List[Card] = Field(default_factory=list)
    open_tickets: List[SupportTicket] = Field(default_factory=list)
    total_relationship_value: Decimal = Decimal("0")
    customer_since_years: int = 0
