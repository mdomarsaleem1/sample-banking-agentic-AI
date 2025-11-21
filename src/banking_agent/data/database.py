"""
Mock Database - Simulates banking data storage with realistic sample data.
"""

import random
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional

from .models import (
    Customer, Account, Transaction, Loan, Card, SupportTicket,
    Address, AccountType, AccountStatus, TransactionType, TransactionStatus,
    LoanType, LoanStatus, CardType, CardStatus, TicketStatus, TicketPriority,
    TicketCategory, CustomerProfile
)


class MockDatabase:
    """
    Mock database simulating banking data sources.
    In a real system, this would connect to actual databases/microservices.
    """

    def __init__(self):
        self._customers: Dict[str, Customer] = {}
        self._accounts: Dict[str, Account] = {}
        self._transactions: Dict[str, Transaction] = {}
        self._loans: Dict[str, Loan] = {}
        self._cards: Dict[str, Card] = {}
        self._tickets: Dict[str, SupportTicket] = {}

        # Index mappings for efficient lookups
        self._customer_accounts: Dict[str, List[str]] = {}
        self._account_transactions: Dict[str, List[str]] = {}
        self._customer_loans: Dict[str, List[str]] = {}
        self._customer_cards: Dict[str, List[str]] = {}
        self._customer_tickets: Dict[str, List[str]] = {}

        # Phone/Email to customer mapping for authentication
        self._phone_to_customer: Dict[str, str] = {}
        self._email_to_customer: Dict[str, str] = {}

        self._initialize_sample_data()

    def _initialize_sample_data(self):
        """Initialize the database with realistic sample data."""

        # Sample Customers
        customers_data = [
            {
                "customer_id": "CUST001",
                "first_name": "John",
                "last_name": "Anderson",
                "email": "john.anderson@email.com",
                "phone": "+1-555-0101",
                "date_of_birth": date(1985, 3, 15),
                "ssn_last_four": "4521",
                "address": Address(
                    street="123 Oak Street",
                    city="San Francisco",
                    state="CA",
                    zip_code="94102"
                ),
                "created_at": datetime(2019, 6, 15, 10, 30, 0),
                "segment": "premium",
                "risk_score": 25
            },
            {
                "customer_id": "CUST002",
                "first_name": "Sarah",
                "last_name": "Mitchell",
                "email": "sarah.mitchell@email.com",
                "phone": "+1-555-0102",
                "date_of_birth": date(1990, 7, 22),
                "ssn_last_four": "7834",
                "address": Address(
                    street="456 Pine Avenue",
                    city="Los Angeles",
                    state="CA",
                    zip_code="90001"
                ),
                "created_at": datetime(2020, 1, 10, 14, 45, 0),
                "segment": "standard",
                "risk_score": 35
            },
            {
                "customer_id": "CUST003",
                "first_name": "Michael",
                "last_name": "Chen",
                "email": "michael.chen@email.com",
                "phone": "+1-555-0103",
                "date_of_birth": date(1978, 11, 8),
                "ssn_last_four": "2156",
                "address": Address(
                    street="789 Maple Drive",
                    city="Seattle",
                    state="WA",
                    zip_code="98101"
                ),
                "created_at": datetime(2015, 3, 20, 9, 15, 0),
                "segment": "private",
                "risk_score": 15
            },
            {
                "customer_id": "CUST004",
                "first_name": "Emily",
                "last_name": "Rodriguez",
                "email": "emily.rodriguez@email.com",
                "phone": "+1-555-0104",
                "date_of_birth": date(1995, 5, 30),
                "ssn_last_four": "9012",
                "address": Address(
                    street="321 Cedar Lane",
                    city="Austin",
                    state="TX",
                    zip_code="78701"
                ),
                "created_at": datetime(2022, 8, 5, 11, 0, 0),
                "segment": "standard",
                "risk_score": 45
            },
            {
                "customer_id": "CUST005",
                "first_name": "Robert",
                "last_name": "Thompson",
                "email": "robert.thompson@email.com",
                "phone": "+1-555-0105",
                "date_of_birth": date(1968, 9, 12),
                "ssn_last_four": "3478",
                "address": Address(
                    street="555 Birch Road",
                    city="Chicago",
                    state="IL",
                    zip_code="60601"
                ),
                "created_at": datetime(2010, 11, 25, 16, 30, 0),
                "segment": "private",
                "risk_score": 20
            }
        ]

        for data in customers_data:
            customer = Customer(**data)
            self._customers[customer.customer_id] = customer
            self._phone_to_customer[customer.phone] = customer.customer_id
            self._email_to_customer[customer.email] = customer.customer_id

        # Sample Accounts
        accounts_data = [
            # John Anderson's accounts
            {
                "account_id": "ACC001",
                "customer_id": "CUST001",
                "account_type": AccountType.CHECKING,
                "account_number": "****4521",
                "routing_number": "121000358",
                "balance": Decimal("15432.67"),
                "available_balance": Decimal("14932.67"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2019, 6, 15),
                "overdraft_limit": Decimal("500.00"),
                "last_activity_date": datetime.now() - timedelta(hours=2)
            },
            {
                "account_id": "ACC002",
                "customer_id": "CUST001",
                "account_type": AccountType.SAVINGS,
                "account_number": "****4522",
                "routing_number": "121000358",
                "balance": Decimal("52150.00"),
                "available_balance": Decimal("52150.00"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2019, 7, 1),
                "interest_rate": Decimal("4.25"),
                "last_activity_date": datetime.now() - timedelta(days=5)
            },
            # Sarah Mitchell's accounts
            {
                "account_id": "ACC003",
                "customer_id": "CUST002",
                "account_type": AccountType.CHECKING,
                "account_number": "****7834",
                "routing_number": "121000358",
                "balance": Decimal("3245.89"),
                "available_balance": Decimal("3245.89"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2020, 1, 10),
                "overdraft_limit": Decimal("200.00"),
                "last_activity_date": datetime.now() - timedelta(hours=12)
            },
            # Michael Chen's accounts
            {
                "account_id": "ACC004",
                "customer_id": "CUST003",
                "account_type": AccountType.CHECKING,
                "account_number": "****2156",
                "routing_number": "121000358",
                "balance": Decimal("89234.50"),
                "available_balance": Decimal("88734.50"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2015, 3, 20),
                "overdraft_limit": Decimal("2000.00"),
                "last_activity_date": datetime.now() - timedelta(hours=1)
            },
            {
                "account_id": "ACC005",
                "customer_id": "CUST003",
                "account_type": AccountType.SAVINGS,
                "account_number": "****2157",
                "routing_number": "121000358",
                "balance": Decimal("245000.00"),
                "available_balance": Decimal("245000.00"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2015, 4, 1),
                "interest_rate": Decimal("4.50"),
                "last_activity_date": datetime.now() - timedelta(days=3)
            },
            {
                "account_id": "ACC006",
                "customer_id": "CUST003",
                "account_type": AccountType.MONEY_MARKET,
                "account_number": "****2158",
                "routing_number": "121000358",
                "balance": Decimal("150000.00"),
                "available_balance": Decimal("150000.00"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2018, 1, 15),
                "interest_rate": Decimal("5.00"),
                "last_activity_date": datetime.now() - timedelta(days=10)
            },
            # Emily Rodriguez's accounts
            {
                "account_id": "ACC007",
                "customer_id": "CUST004",
                "account_type": AccountType.CHECKING,
                "account_number": "****9012",
                "routing_number": "121000358",
                "balance": Decimal("1876.43"),
                "available_balance": Decimal("1876.43"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2022, 8, 5),
                "overdraft_limit": Decimal("100.00"),
                "last_activity_date": datetime.now() - timedelta(hours=6)
            },
            # Robert Thompson's accounts
            {
                "account_id": "ACC008",
                "customer_id": "CUST005",
                "account_type": AccountType.CHECKING,
                "account_number": "****3478",
                "routing_number": "121000358",
                "balance": Decimal("45678.90"),
                "available_balance": Decimal("45178.90"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2010, 11, 25),
                "overdraft_limit": Decimal("1000.00"),
                "last_activity_date": datetime.now() - timedelta(hours=4)
            },
            {
                "account_id": "ACC009",
                "customer_id": "CUST005",
                "account_type": AccountType.SAVINGS,
                "account_number": "****3479",
                "routing_number": "121000358",
                "balance": Decimal("320000.00"),
                "available_balance": Decimal("320000.00"),
                "status": AccountStatus.ACTIVE,
                "opened_date": date(2010, 12, 1),
                "interest_rate": Decimal("4.75"),
                "last_activity_date": datetime.now() - timedelta(days=7)
            },
        ]

        for data in accounts_data:
            account = Account(**data)
            self._accounts[account.account_id] = account
            if account.customer_id not in self._customer_accounts:
                self._customer_accounts[account.customer_id] = []
            self._customer_accounts[account.customer_id].append(account.account_id)

        # Generate transactions for each account
        self._generate_transactions()

        # Sample Loans
        loans_data = [
            {
                "loan_id": "LOAN001",
                "customer_id": "CUST001",
                "loan_type": LoanType.AUTO,
                "principal_amount": Decimal("35000.00"),
                "current_balance": Decimal("28456.78"),
                "interest_rate": Decimal("6.5"),
                "term_months": 60,
                "monthly_payment": Decimal("685.50"),
                "next_payment_date": date.today() + timedelta(days=15),
                "next_payment_amount": Decimal("685.50"),
                "status": LoanStatus.ACTIVE,
                "origination_date": date(2022, 3, 1),
                "maturity_date": date(2027, 3, 1),
                "payments_made": 20,
                "payments_remaining": 40,
                "collateral": "2022 Toyota Camry"
            },
            {
                "loan_id": "LOAN002",
                "customer_id": "CUST003",
                "loan_type": LoanType.MORTGAGE,
                "principal_amount": Decimal("650000.00"),
                "current_balance": Decimal("542345.67"),
                "interest_rate": Decimal("6.875"),
                "term_months": 360,
                "monthly_payment": Decimal("4267.89"),
                "next_payment_date": date.today() + timedelta(days=8),
                "next_payment_amount": Decimal("4267.89"),
                "status": LoanStatus.ACTIVE,
                "origination_date": date(2019, 6, 1),
                "maturity_date": date(2049, 6, 1),
                "payments_made": 54,
                "payments_remaining": 306,
                "collateral": "789 Maple Drive, Seattle, WA"
            },
            {
                "loan_id": "LOAN003",
                "customer_id": "CUST004",
                "loan_type": LoanType.PERSONAL,
                "principal_amount": Decimal("10000.00"),
                "current_balance": Decimal("7234.56"),
                "interest_rate": Decimal("9.99"),
                "term_months": 36,
                "monthly_payment": Decimal("322.67"),
                "next_payment_date": date.today() + timedelta(days=3),
                "next_payment_amount": Decimal("322.67"),
                "status": LoanStatus.ACTIVE,
                "origination_date": date(2023, 5, 1),
                "maturity_date": date(2026, 5, 1),
                "payments_made": 18,
                "payments_remaining": 18
            },
            {
                "loan_id": "LOAN004",
                "customer_id": "CUST005",
                "loan_type": LoanType.CREDIT_LINE,
                "principal_amount": Decimal("50000.00"),
                "current_balance": Decimal("12500.00"),
                "interest_rate": Decimal("8.25"),
                "term_months": 120,
                "monthly_payment": Decimal("500.00"),
                "next_payment_date": date.today() + timedelta(days=20),
                "next_payment_amount": Decimal("500.00"),
                "status": LoanStatus.ACTIVE,
                "origination_date": date(2020, 1, 1),
                "maturity_date": date(2030, 1, 1),
                "payments_made": 48,
                "payments_remaining": 72
            }
        ]

        for data in loans_data:
            loan = Loan(**data)
            self._loans[loan.loan_id] = loan
            if loan.customer_id not in self._customer_loans:
                self._customer_loans[loan.customer_id] = []
            self._customer_loans[loan.customer_id].append(loan.loan_id)

        # Sample Cards
        cards_data = [
            {
                "card_id": "CARD001",
                "customer_id": "CUST001",
                "account_id": "ACC001",
                "card_type": CardType.DEBIT,
                "card_number_masked": "****-****-****-4521",
                "expiration_date": "09/26",
                "status": CardStatus.ACTIVE,
                "issued_date": date(2023, 9, 1),
                "daily_limit": Decimal("5000.00"),
                "international_enabled": True,
                "contactless_enabled": True
            },
            {
                "card_id": "CARD002",
                "customer_id": "CUST001",
                "account_id": "ACC001",
                "card_type": CardType.CREDIT,
                "card_number_masked": "****-****-****-8834",
                "expiration_date": "12/27",
                "status": CardStatus.ACTIVE,
                "credit_limit": Decimal("15000.00"),
                "current_balance": Decimal("3456.78"),
                "available_credit": Decimal("11543.22"),
                "issued_date": date(2022, 12, 1),
                "daily_limit": Decimal("10000.00")
            },
            {
                "card_id": "CARD003",
                "customer_id": "CUST002",
                "account_id": "ACC003",
                "card_type": CardType.DEBIT,
                "card_number_masked": "****-****-****-7834",
                "expiration_date": "03/25",
                "status": CardStatus.ACTIVE,
                "issued_date": date(2022, 3, 15),
                "daily_limit": Decimal("2000.00")
            },
            {
                "card_id": "CARD004",
                "customer_id": "CUST003",
                "account_id": "ACC004",
                "card_type": CardType.DEBIT,
                "card_number_masked": "****-****-****-2156",
                "expiration_date": "06/26",
                "status": CardStatus.ACTIVE,
                "issued_date": date(2023, 6, 1),
                "daily_limit": Decimal("10000.00")
            },
            {
                "card_id": "CARD005",
                "customer_id": "CUST003",
                "account_id": "ACC004",
                "card_type": CardType.CREDIT,
                "card_number_masked": "****-****-****-5567",
                "expiration_date": "08/28",
                "status": CardStatus.ACTIVE,
                "credit_limit": Decimal("50000.00"),
                "current_balance": Decimal("8234.56"),
                "available_credit": Decimal("41765.44"),
                "issued_date": date(2021, 8, 1),
                "daily_limit": Decimal("25000.00")
            },
            {
                "card_id": "CARD006",
                "customer_id": "CUST004",
                "account_id": "ACC007",
                "card_type": CardType.DEBIT,
                "card_number_masked": "****-****-****-9012",
                "expiration_date": "11/25",
                "status": CardStatus.ACTIVE,
                "issued_date": date(2022, 11, 1),
                "daily_limit": Decimal("1500.00")
            },
            {
                "card_id": "CARD007",
                "customer_id": "CUST005",
                "account_id": "ACC008",
                "card_type": CardType.DEBIT,
                "card_number_masked": "****-****-****-3478",
                "expiration_date": "04/26",
                "status": CardStatus.ACTIVE,
                "issued_date": date(2023, 4, 1),
                "daily_limit": Decimal("7500.00")
            },
            {
                "card_id": "CARD008",
                "customer_id": "CUST002",
                "account_id": "ACC003",
                "card_type": CardType.CREDIT,
                "card_number_masked": "****-****-****-1199",
                "expiration_date": "01/24",
                "status": CardStatus.LOST,  # Reported lost
                "credit_limit": Decimal("5000.00"),
                "current_balance": Decimal("1234.56"),
                "available_credit": Decimal("3765.44"),
                "issued_date": date(2021, 1, 15),
                "daily_limit": Decimal("3000.00")
            }
        ]

        for data in cards_data:
            card = Card(**data)
            self._cards[card.card_id] = card
            if card.customer_id not in self._customer_cards:
                self._customer_cards[card.customer_id] = []
            self._customer_cards[card.customer_id].append(card.card_id)

        # Sample Support Tickets
        tickets_data = [
            {
                "ticket_id": "TKT001",
                "customer_id": "CUST001",
                "category": TicketCategory.TRANSACTION_DISPUTE,
                "subject": "Unauthorized charge dispute",
                "description": "I noticed a charge of $89.99 from 'UNKNOWN MERCHANT' that I did not authorize.",
                "status": TicketStatus.IN_PROGRESS,
                "priority": TicketPriority.HIGH,
                "created_at": datetime.now() - timedelta(days=2),
                "updated_at": datetime.now() - timedelta(hours=4),
                "assigned_to": "Agent Smith",
                "related_account_id": "ACC001",
                "notes": [
                    "Customer contacted via phone",
                    "Investigating merchant details",
                    "Provisional credit issued"
                ]
            },
            {
                "ticket_id": "TKT002",
                "customer_id": "CUST002",
                "category": TicketCategory.CARD_ISSUE,
                "subject": "Lost credit card",
                "description": "Lost my credit card ending in 1199. Need replacement.",
                "status": TicketStatus.RESOLVED,
                "priority": TicketPriority.URGENT,
                "created_at": datetime.now() - timedelta(days=5),
                "updated_at": datetime.now() - timedelta(days=3),
                "assigned_to": "Agent Johnson",
                "resolution": "Card blocked immediately. New card shipped via express delivery.",
                "notes": [
                    "Card blocked at 2:34 PM",
                    "No fraudulent transactions detected",
                    "New card shipped to home address"
                ]
            },
            {
                "ticket_id": "TKT003",
                "customer_id": "CUST004",
                "category": TicketCategory.LOAN_INQUIRY,
                "subject": "Question about payment schedule",
                "description": "Want to understand my loan payment schedule and if I can make extra payments.",
                "status": TicketStatus.OPEN,
                "priority": TicketPriority.MEDIUM,
                "created_at": datetime.now() - timedelta(hours=6),
                "updated_at": datetime.now() - timedelta(hours=6),
                "notes": []
            },
            {
                "ticket_id": "TKT004",
                "customer_id": "CUST003",
                "category": TicketCategory.TECHNICAL_ISSUE,
                "subject": "Mobile app not loading account info",
                "description": "The mobile banking app shows an error when trying to view account details.",
                "status": TicketStatus.RESOLVED,
                "priority": TicketPriority.LOW,
                "created_at": datetime.now() - timedelta(days=10),
                "updated_at": datetime.now() - timedelta(days=8),
                "assigned_to": "Tech Support",
                "resolution": "App cache cleared. Issue resolved after app update.",
                "notes": [
                    "Customer using iOS 16.5",
                    "Recommended clearing cache",
                    "Issue resolved after cache clear"
                ]
            }
        ]

        for data in tickets_data:
            ticket = SupportTicket(**data)
            self._tickets[ticket.ticket_id] = ticket
            if ticket.customer_id not in self._customer_tickets:
                self._customer_tickets[ticket.customer_id] = []
            self._customer_tickets[ticket.customer_id].append(ticket.ticket_id)

    def _generate_transactions(self):
        """Generate realistic transaction history for all accounts."""

        merchants = [
            ("Amazon", "Online Shopping"),
            ("Whole Foods", "Grocery"),
            ("Shell Gas Station", "Gas"),
            ("Netflix", "Entertainment"),
            ("Spotify", "Entertainment"),
            ("Target", "Retail"),
            ("Starbucks", "Restaurant"),
            ("Uber", "Transportation"),
            ("AT&T", "Utilities"),
            ("PG&E", "Utilities"),
            ("CVS Pharmacy", "Healthcare"),
            ("Home Depot", "Home Improvement"),
            ("Apple Store", "Electronics"),
            ("Costco", "Wholesale"),
            ("Trader Joe's", "Grocery"),
        ]

        locations = [
            "San Francisco, CA",
            "Los Angeles, CA",
            "Seattle, WA",
            "Austin, TX",
            "Chicago, IL",
            "New York, NY",
            "Online"
        ]

        transaction_counter = 1

        for account_id, account in self._accounts.items():
            num_transactions = random.randint(15, 30)
            current_balance = account.balance

            self._account_transactions[account_id] = []

            for i in range(num_transactions):
                days_ago = random.randint(0, 60)
                hours_ago = random.randint(0, 23)
                timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)

                # Determine transaction type
                tx_type = random.choice([
                    TransactionType.PURCHASE,
                    TransactionType.PURCHASE,
                    TransactionType.PURCHASE,
                    TransactionType.DEPOSIT,
                    TransactionType.WITHDRAWAL,
                    TransactionType.PAYMENT,
                    TransactionType.TRANSFER_OUT,
                    TransactionType.ATM_WITHDRAWAL,
                ])

                # Generate amount based on transaction type
                if tx_type == TransactionType.DEPOSIT:
                    amount = Decimal(str(random.randint(100, 5000)))
                    description = "Direct Deposit - Payroll"
                    merchant_name = None
                    merchant_cat = None
                elif tx_type == TransactionType.PURCHASE:
                    merchant_name, merchant_cat = random.choice(merchants)
                    amount = Decimal(str(round(random.uniform(5, 500), 2)))
                    description = f"Purchase at {merchant_name}"
                elif tx_type == TransactionType.ATM_WITHDRAWAL:
                    amount = Decimal(str(random.choice([20, 40, 60, 80, 100, 200, 300])))
                    description = "ATM Withdrawal"
                    merchant_name = "ATM"
                    merchant_cat = "ATM"
                elif tx_type == TransactionType.PAYMENT:
                    amount = Decimal(str(round(random.uniform(50, 500), 2)))
                    description = random.choice([
                        "Bill Payment - Electric",
                        "Bill Payment - Internet",
                        "Bill Payment - Phone",
                        "Insurance Premium",
                        "Subscription Payment"
                    ])
                    merchant_name = None
                    merchant_cat = "Bills"
                elif tx_type == TransactionType.TRANSFER_OUT:
                    amount = Decimal(str(random.randint(100, 2000)))
                    description = "Transfer to External Account"
                    merchant_name = None
                    merchant_cat = None
                else:
                    amount = Decimal(str(round(random.uniform(20, 300), 2)))
                    description = "Withdrawal"
                    merchant_name = None
                    merchant_cat = None

                # Calculate balance after transaction
                if tx_type in [TransactionType.DEPOSIT, TransactionType.TRANSFER_IN, TransactionType.REFUND]:
                    balance_after = current_balance + amount
                else:
                    balance_after = current_balance - amount

                current_balance = balance_after

                transaction = Transaction(
                    transaction_id=f"TXN{str(transaction_counter).zfill(6)}",
                    account_id=account_id,
                    transaction_type=tx_type,
                    amount=amount,
                    description=description,
                    merchant_name=merchant_name if tx_type == TransactionType.PURCHASE else None,
                    merchant_category=merchant_cat if tx_type == TransactionType.PURCHASE else None,
                    status=TransactionStatus.COMPLETED,
                    timestamp=timestamp,
                    reference_number=f"REF{random.randint(100000, 999999)}",
                    balance_after=balance_after,
                    location=random.choice(locations) if tx_type != TransactionType.DEPOSIT else None
                )

                self._transactions[transaction.transaction_id] = transaction
                self._account_transactions[account_id].append(transaction.transaction_id)
                transaction_counter += 1

    # ========== Query Methods ==========

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        return self._customers.get(customer_id)

    def get_customer_by_phone(self, phone: str) -> Optional[Customer]:
        """Get customer by phone number."""
        customer_id = self._phone_to_customer.get(phone)
        return self._customers.get(customer_id) if customer_id else None

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        customer_id = self._email_to_customer.get(email)
        return self._customers.get(customer_id) if customer_id else None

    def search_customer(self, query: str) -> List[Customer]:
        """Search customers by name, email, or phone."""
        results = []
        query_lower = query.lower()
        for customer in self._customers.values():
            if (query_lower in customer.first_name.lower() or
                query_lower in customer.last_name.lower() or
                query_lower in customer.email.lower() or
                query in customer.phone):
                results.append(customer)
        return results

    def get_account(self, account_id: str) -> Optional[Account]:
        """Get account by ID."""
        return self._accounts.get(account_id)

    def get_customer_accounts(self, customer_id: str) -> List[Account]:
        """Get all accounts for a customer."""
        account_ids = self._customer_accounts.get(customer_id, [])
        return [self._accounts[aid] for aid in account_ids if aid in self._accounts]

    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get transaction by ID."""
        return self._transactions.get(transaction_id)

    def get_account_transactions(
        self,
        account_id: str,
        limit: int = 10,
        days: int = 30
    ) -> List[Transaction]:
        """Get recent transactions for an account."""
        tx_ids = self._account_transactions.get(account_id, [])
        transactions = [self._transactions[tid] for tid in tx_ids if tid in self._transactions]

        # Filter by date
        cutoff = datetime.now() - timedelta(days=days)
        transactions = [tx for tx in transactions if tx.timestamp >= cutoff]

        # Sort by timestamp descending
        transactions.sort(key=lambda x: x.timestamp, reverse=True)

        return transactions[:limit]

    def get_loan(self, loan_id: str) -> Optional[Loan]:
        """Get loan by ID."""
        return self._loans.get(loan_id)

    def get_customer_loans(self, customer_id: str) -> List[Loan]:
        """Get all loans for a customer."""
        loan_ids = self._customer_loans.get(customer_id, [])
        return [self._loans[lid] for lid in loan_ids if lid in self._loans]

    def get_card(self, card_id: str) -> Optional[Card]:
        """Get card by ID."""
        return self._cards.get(card_id)

    def get_customer_cards(self, customer_id: str) -> List[Card]:
        """Get all cards for a customer."""
        card_ids = self._customer_cards.get(customer_id, [])
        return [self._cards[cid] for cid in card_ids if cid in self._cards]

    def get_ticket(self, ticket_id: str) -> Optional[SupportTicket]:
        """Get support ticket by ID."""
        return self._tickets.get(ticket_id)

    def get_customer_tickets(
        self,
        customer_id: str,
        include_closed: bool = False
    ) -> List[SupportTicket]:
        """Get support tickets for a customer."""
        ticket_ids = self._customer_tickets.get(customer_id, [])
        tickets = [self._tickets[tid] for tid in ticket_ids if tid in self._tickets]

        if not include_closed:
            tickets = [t for t in tickets if t.status not in [TicketStatus.CLOSED, TicketStatus.RESOLVED]]

        return tickets

    def get_customer_profile(self, customer_id: str) -> Optional[CustomerProfile]:
        """Get comprehensive customer profile."""
        customer = self.get_customer(customer_id)
        if not customer:
            return None

        accounts = self.get_customer_accounts(customer_id)

        # Get recent transactions from all accounts
        all_transactions = []
        for account in accounts:
            txs = self.get_account_transactions(account.account_id, limit=5)
            all_transactions.extend(txs)

        # Sort and limit transactions
        all_transactions.sort(key=lambda x: x.timestamp, reverse=True)
        recent_transactions = all_transactions[:10]

        # Calculate total relationship value
        total_value = sum(acc.balance for acc in accounts)

        # Calculate years as customer
        years = (datetime.now() - customer.created_at).days // 365

        return CustomerProfile(
            customer=customer,
            accounts=accounts,
            recent_transactions=recent_transactions,
            loans=self.get_customer_loans(customer_id),
            cards=self.get_customer_cards(customer_id),
            open_tickets=self.get_customer_tickets(customer_id),
            total_relationship_value=total_value,
            customer_since_years=years
        )

    # ========== Mutation Methods ==========

    def block_card(self, card_id: str, reason: CardStatus) -> bool:
        """Block a card."""
        card = self._cards.get(card_id)
        if card:
            card.status = reason
            return True
        return False

    def create_ticket(self, ticket: SupportTicket) -> str:
        """Create a new support ticket."""
        self._tickets[ticket.ticket_id] = ticket
        if ticket.customer_id not in self._customer_tickets:
            self._customer_tickets[ticket.customer_id] = []
        self._customer_tickets[ticket.customer_id].append(ticket.ticket_id)
        return ticket.ticket_id

    def update_ticket(self, ticket_id: str, **kwargs) -> bool:
        """Update a support ticket."""
        ticket = self._tickets.get(ticket_id)
        if ticket:
            for key, value in kwargs.items():
                if hasattr(ticket, key):
                    setattr(ticket, key, value)
            ticket.updated_at = datetime.now()
            return True
        return False

    def transfer_funds(
        self,
        from_account_id: str,
        to_account_id: str,
        amount: Decimal,
        description: str = "Internal Transfer"
    ) -> Optional[str]:
        """Transfer funds between accounts."""
        from_account = self._accounts.get(from_account_id)
        to_account = self._accounts.get(to_account_id)

        if not from_account or not to_account:
            return None

        if from_account.available_balance < amount:
            return None

        # Create transactions
        timestamp = datetime.now()

        # Debit transaction
        debit_tx = Transaction(
            transaction_id=f"TXN{random.randint(100000, 999999)}",
            account_id=from_account_id,
            transaction_type=TransactionType.TRANSFER_OUT,
            amount=amount,
            description=description,
            status=TransactionStatus.COMPLETED,
            timestamp=timestamp,
            reference_number=f"REF{random.randint(100000, 999999)}",
            balance_after=from_account.balance - amount
        )

        # Credit transaction
        credit_tx = Transaction(
            transaction_id=f"TXN{random.randint(100000, 999999)}",
            account_id=to_account_id,
            transaction_type=TransactionType.TRANSFER_IN,
            amount=amount,
            description=description,
            status=TransactionStatus.COMPLETED,
            timestamp=timestamp,
            reference_number=debit_tx.reference_number,
            balance_after=to_account.balance + amount
        )

        # Update balances
        from_account.balance -= amount
        from_account.available_balance -= amount
        to_account.balance += amount
        to_account.available_balance += amount

        # Store transactions
        self._transactions[debit_tx.transaction_id] = debit_tx
        self._transactions[credit_tx.transaction_id] = credit_tx

        if from_account_id not in self._account_transactions:
            self._account_transactions[from_account_id] = []
        if to_account_id not in self._account_transactions:
            self._account_transactions[to_account_id] = []

        self._account_transactions[from_account_id].append(debit_tx.transaction_id)
        self._account_transactions[to_account_id].append(credit_tx.transaction_id)

        return debit_tx.reference_number

    def get_all_customers(self) -> List[Customer]:
        """Get all customers (for demo purposes)."""
        return list(self._customers.values())


# Global database instance
db = MockDatabase()
