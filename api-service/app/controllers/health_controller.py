"""
Controller for system health check.
"""

from datetime import datetime
from typing import Any, Dict


class HealthController:
    """Controller for system health status."""

    @staticmethod
    def get_health_status(classifier) -> Dict[str, Any]:
        """Return service health status."""
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "model_loaded": classifier.is_loaded,
            "version": "1.0.0",
        }

