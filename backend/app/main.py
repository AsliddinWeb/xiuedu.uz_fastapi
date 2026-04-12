import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.database import AsyncSessionLocal
from app.middleware import RequestLoggingMiddleware, limiter
from app.routers import api_router
from app.services.auth_service import ensure_superadmin

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
)
log = logging.getLogger("xiuedu")


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    try:
        async with AsyncSessionLocal() as db:
            await ensure_superadmin(db)
        log.info("Superadmin bootstrap OK (%s)", settings.ADMIN_EMAIL)
    except Exception as e:  # noqa: BLE001
        log.warning("Superadmin bootstrap skipped: %s", e)
    yield


app = FastAPI(
    title=f"{settings.SITE_NAME} API",
    description="XIU Edu v2 — official API for xiuedu.uz",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# ===== Rate limiter =====
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

# ===== GZip + access log =====
app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(RequestLoggingMiddleware)

# ===== Static media =====
app.mount("/media", StaticFiles(directory=settings.UPLOAD_DIR), name="media")

# ===== Routes =====
app.include_router(api_router, prefix="/api")


@app.get("/api/health", tags=["health"])
async def health():
    return {"status": "ok", "service": settings.SITE_NAME, "env": settings.ENV}


# ===== Error handlers =====

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "not_found", "path": request.url.path, "detail": "Resource not found"},
    )


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": "validation_error", "detail": exc.errors()},
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    log.exception("Unhandled error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "detail": "Something went wrong"},
    )
