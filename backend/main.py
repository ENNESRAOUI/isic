#!/usr/bin/env python3
"""
ISIC Backend - Application principale
Architecture: Couches (MVC + Repository Pattern)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Créer l'application FastAPI
app = FastAPI(
    title="ISIC API",
    description="API pour le système de veille sportive multilingue",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ROUTES PRINCIPALES
# ==========================================

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "ISIC API v2.0",
        "status": "running",
        "docs": "/api/docs",
        "version": "2.0.0"
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "service": "ISIC API",
        "version": "2.0.0"
    }


@app.get("/api/v1")
async def api_info():
    """Informations API"""
    return {
        "api": "ISIC",
        "version": "2.0.0",
        "endpoints": {
            "articles": "/api/v1/articles",
            "sources": "/api/v1/sources",
            "reviews": "/api/v1/reviews"
        }
    }


# ==========================================
# IMPORT DES ROUTERS
# ==========================================

# Import des routers si les fichiers existent
try:
    from backend.views import articles, sources, reviews
    
    app.include_router(articles.router)
    app.include_router(sources.router)
    app.include_router(reviews.router)
    
    logger.info("✓ Routers chargés avec succès")
except ImportError as e:
    logger.warning(f"Attention: Routers non trouvés ({e})")


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

