from fastapi import FastAPI, Request
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

def create_application() -> FastAPI:
    app = FastAPI(
        title="FinTech Ledger API",
        version="1.0.0",
        description="A minimal financial ledger with idempotency, transactions, and secure access control."
    )

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
