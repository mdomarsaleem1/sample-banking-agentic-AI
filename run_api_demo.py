#!/usr/bin/env python3
"""
Demo script showcasing the Data APIs layer of the Banking Agent.

This script demonstrates how the AI agent interacts with multiple
data APIs to fetch customer information.
"""

import asyncio
import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from banking_agent.apis import APIGateway
from banking_agent.data.database import db

console = Console()


async def demonstrate_apis():
    """Demonstrate the various Data APIs."""

    console.print(Panel(
        "[bold]Banking Data APIs Demonstration[/bold]\n\n"
        "This demo showcases how the AI agent interacts with multiple\n"
        "data APIs to fetch and process banking information.",
        title="API Demo",
        border_style="blue"
    ))

    # Initialize API Gateway
    api = APIGateway()

    # Demo customer
    customer_id = "CUST001"
    console.print(f"\n[bold cyan]Using demo customer: {customer_id}[/bold cyan]\n")

    # 1. Customer API
    console.print("[bold yellow]1. Customer API - Fetching customer profile...[/bold yellow]")
    result = await api.customer.get_customer(customer_id)
    if result.success and result.data:
        customer = result.data
        console.print(f"   Name: {customer.full_name}")
        console.print(f"   Email: {customer.email}")
        console.print(f"   Phone: {customer.phone}")
        console.print(f"   Segment: {customer.segment}")
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # 2. Account API
    console.print("\n[bold yellow]2. Account API - Fetching accounts...[/bold yellow]")
    result = await api.account.get_customer_accounts(customer_id)
    if result.success and result.data:
        table = Table(title="Customer Accounts")
        table.add_column("Account ID")
        table.add_column("Type")
        table.add_column("Balance")
        table.add_column("Status")

        for acc in result.data:
            table.add_row(
                acc.account_id,
                acc.account_type.value,
                f"${acc.balance:,.2f}",
                acc.status.value
            )
        console.print(table)
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # 3. Transaction API
    console.print("\n[bold yellow]3. Transaction API - Fetching recent transactions...[/bold yellow]")
    account_id = "ACC001"
    result = await api.transaction.get_recent_transactions(account_id, limit=5)
    if result.success and result.data:
        table = Table(title=f"Recent Transactions ({account_id})")
        table.add_column("Date")
        table.add_column("Type")
        table.add_column("Description")
        table.add_column("Amount", justify="right")

        for tx in result.data[:5]:
            table.add_row(
                tx.timestamp.strftime("%Y-%m-%d"),
                tx.transaction_type.value,
                tx.description[:30],
                f"${tx.amount:,.2f}"
            )
        console.print(table)
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # 4. Spending Summary API
    console.print("\n[bold yellow]4. Transaction API - Spending analysis...[/bold yellow]")
    result = await api.transaction.get_spending_summary(account_id, days=30)
    if result.success and result.data:
        data = result.data
        console.print(f"   Total Spending (30 days): ${data['total_spending']}")
        console.print(f"   Total Income: ${data['total_income']}")
        console.print(f"   Net Change: ${data['net_change']}")
        console.print("   Spending by Category:")
        for cat, amount in list(data['by_category'].items())[:5]:
            console.print(f"      - {cat}: ${amount}")
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # 5. Loan API
    console.print("\n[bold yellow]5. Loan API - Fetching loan information...[/bold yellow]")
    result = await api.loan.get_loan_summary(customer_id)
    if result.success and result.data:
        data = result.data
        console.print(f"   Total Loans: {data['total_loans']}")
        console.print(f"   Total Balance: ${data['total_balance']}")
        console.print(f"   Monthly Payment: ${data['total_monthly_payment']}")
        for loan in data['loans']:
            console.print(f"   - {loan['type']}: ${loan['balance']} (Next: {loan['next_payment_date']})")
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # 6. Card API
    console.print("\n[bold yellow]6. Card API - Fetching card information...[/bold yellow]")
    result = await api.card.get_card_summary(customer_id)
    if result.success and result.data:
        data = result.data
        console.print(f"   Total Cards: {data['total_cards']}")
        console.print(f"   Credit Limit: ${data['total_credit_limit']}")
        console.print(f"   Credit Used: ${data['total_credit_used']}")
        for card in data['cards']:
            status = "Active" if card['status'] == 'active' else card['status'].upper()
            console.print(f"   - {card['type'].title()} ****{card['last_four']}: {status}")
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # 7. Support API
    console.print("\n[bold yellow]7. Support API - Fetching support tickets...[/bold yellow]")
    result = await api.support.get_customer_tickets(customer_id, include_closed=True)
    if result.success and result.data:
        if result.data:
            for ticket in result.data:
                console.print(f"   - {ticket.ticket_id}: {ticket.subject}")
                console.print(f"     Status: {ticket.status.value} | Priority: {ticket.priority.value}")
        else:
            console.print("   No support tickets found")
        console.print(f"   [dim]Latency: {result.latency_ms}ms[/dim]")

    # Print API Statistics
    console.print("\n[bold green]API Gateway Statistics:[/bold green]")
    stats = api.get_api_stats()
    for api_name, api_stats in stats.items():
        console.print(f"   {api_name}: {api_stats['total_requests']} requests")

    console.print("\n[bold]Demo Complete![/bold]")


def main():
    """Main entry point."""
    asyncio.run(demonstrate_apis())


if __name__ == "__main__":
    main()
