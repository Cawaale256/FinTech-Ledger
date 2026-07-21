from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.accounts import router as accounts_router
from app.api.transactions import router as transactions_router
from app.api.transfers import router as transfers_router

# Setting
#from app.core.config import settings


def create_application() -> FastAPI:
    app = FastAPI(
        title="FinTech Ledger API",
        version="1.0.0",
        description="A minimal financial ledger with idempotency, transactions, and secure access control."
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
    
    return app

app = create_application()
