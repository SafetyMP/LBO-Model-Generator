#!/usr/bin/env python3
"""
Entry point script for LBO Model Generator
Allows running from project root: python run.py [args]
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run main
from lbo_input_generator import main

if __name__ == "__main__":
    main()
