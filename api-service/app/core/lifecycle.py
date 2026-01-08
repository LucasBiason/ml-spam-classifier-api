"""
Application lifecycle events.

Manages model loading on startup.
"""

import logging

from ..models import SpamClassifier

logger = logging.getLogger(__name__)

classifier = SpamClassifier(models_dir="models")


async def startup_event():
    """Load ML model on startup."""
    try:
        logger.info("Loading classification model...")
        classifier.load()
        logger.info("Model loaded successfully")
        logger.info(f"Model info: {classifier.get_model_info()}")
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise


async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down API...")

