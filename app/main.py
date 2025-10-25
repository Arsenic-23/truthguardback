import logging
from fastapi import FastAPI
from app.startup import *
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

try:
    from app.routers import text as text_router_module
    from app.routers import url as url_router_module
    from app.routers import pdf as pdf_router_module
    have_routers = True
except Exception:
    have_routers = False

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="0.1.0",
        debug=(settings.APP_ENV != "production")
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.APP_NAME} (env={settings.APP_ENV})")
        
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down")

    if have_routers:
        logger.info("Mounting routers: text, url, pdf")
        app.include_router(text_router_module.router, prefix="/verify", tags=["verify"])
        app.include_router(url_router_module.router, prefix="/verify", tags=["verify"])
        app.include_router(pdf_router_module.router, prefix="/verify", tags=["verify"])
    else:
        logger.warning("Routers not found yet — create app.routers.text, .url and .pdf files to mount routes.")

    @app.get("/healthz", tags=["health"])
    async def healthz():
        return {"status": "ok", "app": settings.APP_NAME}

    return app

app = create_app()

