from fastapi import APIRouter, Depends
from fastyr.infrastructure.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/liveness")
async def liveness():
    """Basic health check endpoint."""
    return {"status": "alive"}

@router.get("/readiness")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Check if application is ready to handle requests."""
    try:
        await db.execute("SELECT 1")
        return {"status": "ready", "database": "connected"}
    except Exception:
        return {"status": "not ready", "database": "disconnected"} 