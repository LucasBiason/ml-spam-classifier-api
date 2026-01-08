"""
FastAPI application for email spam classification.

Uses trained ML model to identify emails as spam or ham.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import shutdown_event, startup_event
from .routers import health_router, predictions_router

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="ML Spam Classifier API",
    description="API for email spam classification",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.on_event("startup")(startup_event)
app.on_event("shutdown")(shutdown_event)

app.include_router(health_router, tags=["health"])
app.include_router(predictions_router, prefix="/api/v1", tags=["predictions"])

