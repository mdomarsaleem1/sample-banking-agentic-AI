"""
Main entry point for the Banking Call Center AI Agent.

This module provides both CLI and programmatic interfaces to the agent.
"""

import asyncio
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich import print as rprint

from .agent import BankingAgent
from .data.database import db
from .utils.config import get_config
from .utils.logging_config import setup_logging


console = Console()


def print_welcome():
    """Print welcome message and instructions."""
    welcome_text = """
# SecureBank AI Call Center Agent

Welcome to the Banking Call Center AI demonstration!

## Available Demo Customers:
| Customer ID | Name | Phone | Segment |
|------------|------|-------|---------|
| CUST001 | John Anderson | +1-555-0101 | Premium |
| CUST002 | Sarah Mitchell | +1-555-0102 | Standard |
| CUST003 | Michael Chen | +1-555-0103 | Private |
| CUST004 | Emily Rodriguez | +1-555-0104 | Standard |
| CUST005 | Robert Thompson | +1-555-0105 | Private |

## Sample Queries to Try:
- "My phone number is +1-555-0101"
- "What's my account balance?"
- "Show me my recent transactions"
- "I lost my card ending in 4521"
- "What loans do I have?"
- "Tell me about my cards"
- "I need to file a complaint"

## Commands:
- Type your message to interact with the agent
- Type 'quit' or 'exit' to end the session
- Type 'clear' to start a new session
- Type 'customers' to see available demo customers
- Type 'tools' to see available agent tools
- Type 'help' for this message
"""
    console.print(Markdown(welcome_text))


def print_customers():
    """Print available demo customers."""
    table = Table(title="Available Demo Customers")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Phone")
    table.add_column("Email")
    table.add_column("Segment", style="yellow")

    customers = db.get_all_customers()
    for customer in customers:
        table.add_row(
            customer.customer_id,
            customer.full_name,
            customer.phone,
            customer.email,
            customer.segment
        )

    console.print(table)


def print_tools(agent: BankingAgent):
    """Print available agent tools."""
    table = Table(title="Available Agent Tools")
    table.add_column("Tool Name", style="cyan")
    table.add_column("Description")

    for tool in agent.get_available_tools():
        table.add_row(tool["name"], tool["description"][:80] + "...")

    console.print(table)


async def run_interactive_session():
    """Run an interactive demo session."""
    config = get_config()
    setup_logging(config.log_level)

    # Initialize agent
    agent = BankingAgent(ai_provider=config.ai_provider)

    # Print welcome
    print_welcome()

    # Create session
    session_id = agent.create_session()
    console.print(f"\n[dim]Session created: {session_id}[/dim]\n")

    # Initial greeting
    result = await agent.process_message(session_id, "hello")
    console.print(Panel(result["response"], title="Agent", border_style="green"))

    # Interactive loop
    while True:
        try:
            # Get user input
            console.print()
            user_input = console.input("[bold blue]You:[/bold blue] ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                # End session
                summary = agent.end_session(session_id)
                console.print("\n[yellow]Session Summary:[/yellow]")
                console.print(f"  Duration: {summary.get('duration_seconds', 0):.1f} seconds")
                console.print(f"  Messages: {summary.get('messages_count', 0)}")
                console.print(f"  Actions: {summary.get('actions_taken', 0)}")
                console.print("\n[green]Thank you for using SecureBank AI. Goodbye![/green]")
                break

            elif user_input.lower() == 'clear':
                # Start new session
                agent.end_session(session_id)
                session_id = agent.create_session()
                console.print("[yellow]Starting new session...[/yellow]\n")
                result = await agent.process_message(session_id, "hello")
                console.print(Panel(result["response"], title="Agent", border_style="green"))
                continue

            elif user_input.lower() == 'customers':
                print_customers()
                continue

            elif user_input.lower() == 'tools':
                print_tools(agent)
                continue

            elif user_input.lower() == 'help':
                print_welcome()
                continue

            elif user_input.lower() == 'debug':
                # Show session debug info
                context = agent.get_context(session_id)
                if context:
                    console.print("\n[yellow]Debug Info:[/yellow]")
                    console.print(f"  Customer ID: {context.get_customer_id()}")
                    console.print(f"  Identified: {context.is_customer_identified()}")
                    console.print(f"  Verified: {context.is_customer_verified()}")
                    console.print(f"  Intents: {context.intent_history}")
                    console.print(f"  Actions: {len(context.actions_taken)}")
                continue

            # Process message
            with console.status("[bold green]Processing...[/bold green]"):
                result = await agent.process_message(session_id, user_input)

            # Display response
            console.print()
            console.print(Panel(
                result["response"],
                title="Agent",
                subtitle=f"Intent: {result.get('intent', 'unknown')}",
                border_style="green"
            ))

            # Show tools called (if any)
            if result.get("tools_called"):
                tools_str = ", ".join(result["tools_called"])
                console.print(f"[dim]Tools used: {tools_str}[/dim]")

        except KeyboardInterrupt:
            console.print("\n\n[yellow]Session interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
            continue


async def demo_scenario():
    """Run a pre-defined demo scenario."""
    config = get_config()
    setup_logging("WARNING")  # Reduce noise for demo

    console.print(Panel(
        "Running automated demo scenario...",
        title="SecureBank AI Demo",
        border_style="blue"
    ))

    agent = BankingAgent(ai_provider=config.ai_provider)
    session_id = agent.create_session()

    # Demo scenarios
    scenarios = [
        ("Starting conversation...", "Hello, I need help with my account"),
        ("Identifying customer...", "My phone number is +1-555-0101"),
        ("Checking balance...", "What's my account balance?"),
        ("Viewing transactions...", "Show me my recent transactions"),
        ("Checking cards...", "What cards do I have?"),
        ("Checking loans...", "Tell me about my loans"),
        ("Reporting lost card...", "I lost my card ending in 4521"),
    ]

    for description, message in scenarios:
        console.print(f"\n[bold cyan]{description}[/bold cyan]")
        console.print(f"[blue]User:[/blue] {message}")

        with console.status("[bold green]Processing...[/bold green]"):
            result = await agent.process_message(session_id, message)

        console.print(Panel(
            result["response"],
            title="Agent Response",
            border_style="green"
        ))

        if result.get("tools_called"):
            console.print(f"[dim]APIs called: {', '.join(result['tools_called'])}[/dim]")

        await asyncio.sleep(1)  # Pause between scenarios

    # End session
    summary = agent.end_session(session_id)
    console.print("\n[bold]Demo Complete![/bold]")
    console.print(f"Total API calls: {summary.get('actions_taken', 0)}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Banking Call Center AI Agent"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run automated demo scenario"
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )

    args = parser.parse_args()

    if args.demo:
        asyncio.run(demo_scenario())
    else:
        asyncio.run(run_interactive_session())


if __name__ == "__main__":
    main()
