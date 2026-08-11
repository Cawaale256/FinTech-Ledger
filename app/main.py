from fastapi import FastAPI, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Routers
from app.api.accounts import router as accounts_router
from app.api.transactions import router as transactions_router
from app.api.transfers import router as transfers_router
from app.api.admin import router as admin_router
from app.api.auth import router as auth_router

# Setting
from app.core.config import settings
from app.schemas.errors import ErrorResponse
from app.core.rate_limit import request_log, MAX_REQUESTS, WINDOW_SECONDS
import time

def create_application() -> FastAPI:
    app = FastAPI(
        title="FinTech Ledger API",
        version="1.0.0",
        description="A minimal financial ledger with idempotency, transactions, and secure access control."
    )


    # rate‑limit middleware
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        # Identify client (user_id if authenticated, else IP)
        client_id = request.client.host

        now = time.time()
        window_start = now - WINDOW_SECONDS

        # Clean old timestamps
        request_log[client_id] = [
            ts for ts in request_log[client_id] if ts > window_start
    ]

        # Check limit
        if len(request_log[client_id]) >= MAX_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail=ErrorResponse(
                    detail="Too many requests",
                    code="RATE_LIMIT_EXCEEDED",
                    hint=f"Limit is {MAX_REQUESTS} requests per {WINDOW_SECONDS} seconds"
                ).model_dump()
        )

        # Record request
        request_log[client_id].append(now)

        return await call_next(request)
    

    # Global Error Handling Middleware    
    @app.middleware("http")
    async def global_error_handler(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content=ErrorResponse(
                    detail="Internal server error",
                    code="SERVER_ERROR",
                    hint=str(exc)
                ).model_dump()
            )
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(accounts_router, prefix="/accounts", tags=["Accounts"])
    app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])
    app.include_router(transfers_router, prefix="/transfers", tags=["Transfers"])
    app.include_router(admin_router, prefix="/admin", tags=["admin"])
    app.include_router(auth_router, prefix="/auth", tags= ["auth"])
    return app

app = create_application()
