"""
Unit tests for lifecycle events.
"""

import pytest
from unittest.mock import patch, MagicMock

from app.core import lifecycle


def test_startup_event_success():
    """Test startup_event loads model successfully."""
    with patch.object(lifecycle.classifier, 'load') as mock_load, \
         patch.object(lifecycle.classifier, 'get_model_info') as mock_info:
        mock_info.return_value = {"model_type": "LinearSVC"}
        
        import asyncio
        asyncio.run(lifecycle.startup_event())
        
        mock_load.assert_called_once()
        mock_info.assert_called_once()


def test_startup_event_failure():
    """Test startup_event raises exception on load failure."""
    with patch.object(lifecycle.classifier, 'load', side_effect=RuntimeError("Load failed")):
        import asyncio
        with pytest.raises(RuntimeError):
            asyncio.run(lifecycle.startup_event())


def test_shutdown_event():
    """Test shutdown_event runs without errors."""
    import asyncio
    asyncio.run(lifecycle.shutdown_event())

