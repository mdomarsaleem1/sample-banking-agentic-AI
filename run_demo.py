#!/usr/bin/env python3
"""
Quick start script for the Banking Call Center AI Agent demo.

This script provides an easy way to run the demo without installing the package.
"""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from banking_agent.main import main

if __name__ == "__main__":
    main()
