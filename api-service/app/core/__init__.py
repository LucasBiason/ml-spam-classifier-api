"""
Core module - lifecycle and configuration.
"""

from .lifecycle import classifier, shutdown_event, startup_event

__all__ = ["startup_event", "shutdown_event", "classifier"]

