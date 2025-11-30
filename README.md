# Banking Call Center Agentic AI

A lightweight, customer-service agent that orchestrates banking APIs to resolve common requests without waiting on a human representative.

- **What you get:** a mock banking stack (customers, accounts, cards, loans, support tickets) plus an agent that chains tool calls to solve tasks.
- **How to try it:** install dependencies, open the notebooks, and run the guided demos.
- **Want details?** The full architecture, business case, and improvement ideas live in [`docs/README.md`](docs/README.md).

## Quick start (notebooks first)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch Jupyter and open the notebooks:
   ```bash
   jupyter lab  # or jupyter notebook
   ```
3. Run the demos inside:
   - `notebooks/agent_demo.ipynb` for the end-to-end agent flow
   - `notebooks/api_demo.ipynb` for the underlying data APIs

> Prefer the CLI? You can still run `python run_demo.py --demo` or `python run_api_demo.py`, but the notebooks are the primary entry points.

## Repository layout (cookie-cutter friendly)
```
├── credentials/   # ignored in git; place secrets/env files here
├── data/          # ignored in git; local datasets or exports
├── docs/          # full architecture, business case, and guides
├── notebooks/     # runnable demos (agent and API notebooks)
├── src/           # agent, tools, and mock API implementations
└── README.md      # high-level overview
```

For deeper guidance, diagrams, and sample conversations, see [`docs/README.md`](docs/README.md).
