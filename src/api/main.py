from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import time

from src.api.routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents
)

app = FastAPI(
    title="Financial Intelligence API",
    version="1.0.0"
)

# -------------------------
# SQLite Connection
# -------------------------

def get_db():
    return sqlite3.connect("database/nifty100.db")

# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Logging Middleware
# -------------------------

@app.middleware("http")
async def log_requests(request, call_next):

    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start

    print(
        f"{request.method} {request.url.path} "
        f"{process_time:.3f}s"
    )

    return response

# -------------------------
# Routers
# -------------------------

app.include_router(
    health.router,
    prefix="/api/v1"
)

app.include_router(
    companies.router,
    prefix="/api/v1"
)

app.include_router(
    screener.router,
    prefix="/api/v1"
)

app.include_router(
    sectors.router,
    prefix="/api/v1"
)

app.include_router(
    peers.router,
    prefix="/api/v1"
)

app.include_router(
    valuation.router,
    prefix="/api/v1"
)

app.include_router(
    portfolio.router,
    prefix="/api/v1"
)

app.include_router(
    documents.router,
    prefix="/api/v1"
)
