#!/usr/bin/env python3
"""Backward-compatible check-only entry point for Superpowers."""
from ensure_superpowers import main

if __name__ == "__main__":
    raise SystemExit(main())
