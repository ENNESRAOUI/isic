#!/usr/bin/env python3
"""
Application FastAPI pour ISIC - Veille Sportive
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path
import json
import csv

# Initialiser l'app FastAPI
app = FastAPI(
    title="ISIC API",
    description="API pour le système de veille sportive",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemin du répertoire data
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "output"
WEB_DIR = BASE_DIR / "web"

# Routes API v1
API_PREFIX = "/api/v1"

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "ISIC API v1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    """Vérifier l'état de l'API"""
    return {"status": "ok", "service": "ISIC API"}

@app.get(f"{API_PREFIX}/articles")
async def get_articles():
    """Récupérer les articles organisés"""
    try:
        csv_file = DATA_DIR / "organized_articles.csv"
        
        if not csv_file.exists():
            # Créer un fichier d'exemple si nécessaire
            return {"articles": [], "total": 0, "message": "Aucun article trouvé"}
        
        articles = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                articles.append(row)
        
        return {"articles": articles, "total": len(articles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{API_PREFIX}/ai/report")
async def get_report():
    """Rapport IA généré"""
    try:
        report_file = DATA_DIR / "ai_report.json"
        
        if report_file.exists():
            with open(report_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Rapport par défaut
        return {
            "status": "success",
            "summary": "Rapport IA - Veille Sportive",
            "articles_analyzed": 0,
            "key_findings": [],
            "trends": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{API_PREFIX}/ai/report")
async def generate_report(data: dict = None):
    """Générer un rapport IA"""
    try:
        return {
            "status": "success",
            "message": "Rapport généré avec succès",
            "report": {
                "summary": "Analyse des articles",
                "articles_processed": 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{API_PREFIX}/ai/analyze/{{article_id}}")
async def analyze_article(article_id: str, analysis_type: str = "general"):
    """Analyser un article avec l'IA"""
    try:
        return {
            "status": "success",
            "article_id": article_id,
            "analysis_type": analysis_type,
            "analysis": {
                "sentiment": "neutral",
                "key_topics": [],
                "credibility_score": 0.5,
                "summary": f"Analyse de l'article {article_id}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{API_PREFIX}/filter")
async def filter_articles(category: str = None, source: str = None):
    """Filtrer les articles par catégorie ou source"""
    try:
        articles = []
        csv_file = DATA_DIR / "organized_articles.csv"
        
        if csv_file.exists():
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if category and row.get('category') != category:
                        continue
                    if source and row.get('source') != source:
                        continue
                    articles.append(row)
        
        return {"articles": articles, "total": len(articles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{API_PREFIX}/stats")
async def get_stats():
    """Obtenir les statistiques globales"""
    try:
        csv_file = DATA_DIR / "organized_articles.csv"
        article_count = 0
        
        if csv_file.exists():
            with open(csv_file, 'r', encoding='utf-8') as f:
                article_count = sum(1 for _ in f) - 1  # Exclure l'en-tête
        
        return {
            "total_articles": article_count,
            "total_sources": 0,
            "categories": [],
            "last_update": "2026-03-30"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir les fichiers statiques du frontend
@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    """Servir les fichiers statiques"""
    file_full_path = WEB_DIR / file_path
    
    if file_full_path.exists() and file_full_path.is_file():
        return FileResponse(file_full_path)
    
    # Par défaut, servir index.html
    index_file = WEB_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    
    raise HTTPException(status_code=404, detail="Fichier non trouvé")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
