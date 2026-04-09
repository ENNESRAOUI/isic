import pandas as pd
from pathlib import Path
from datetime import datetime
import json

# Définir le chemin
DATA_DIR = Path(__file__).parent.parent / "data" / "output"
DOCS_DIR = Path(__file__).parent.parent / "docs"
DOCS_DIR.mkdir(exist_ok=True)

def generate_daily_report(articles_csv):
    """Génère une revue de presse quotidienne"""
    
    try:
        df = pd.read_csv(articles_csv)
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé : {articles_csv}")
        return None
    
    if len(df) == 0:
        print("❌ Aucun article à traiter")
        return None
    
    # Date du rapport
    today = datetime.now().strftime("%d/%m/%Y")
    report_date = datetime.now().strftime("%Y%m%d")
    
    print("📰 Génération de la revue de presse...\n")
    
    # === RAPPORT HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Revue de Presse Sportive - {today}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .summary-box {{
            background: white;
            border-left: 4px solid #1e40af;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .summary-box h2 {{
            color: #1e40af;
            margin-bottom: 1rem;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        .stat {{
            background: #f0f4f8;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #1e40af;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #666;
        }}
        
        .section {{
            margin-bottom: 2rem;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            color: #1e40af;
            border-bottom: 2px solid #3b82f6;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .article {{
            background: white;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-top: 3px solid #3b82f6;
        }}
        
        .article-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 0.5rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .article-title {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #1e233c;
            flex: 1;
            min-width: 300px;
        }}
        
        .article-summary {{
            font-size: 0.95rem;
            color: #555;
            line-height: 1.5;
            margin: 0.75rem 0;
            padding: 0.75rem;
            background: #f9f9f9;
            border-left: 3px solid #e0e0e0;
            border-radius: 4px;
        }}
        
        .article-link {{
            display: inline-block;
            margin-top: 0.75rem;
            padding: 0.5rem 1rem;
            background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .article-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
        }}
        
        .article-meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.9rem;
            flex-wrap: wrap;
            margin-bottom: 0.5rem;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        
        .badge-category {{
            background: #dbeafe;
            color: #1e40af;
        }}
        
        .badge-source {{
            background: #dcfce7;
            color: #166534;
        }}
        
        .badge-credibility {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .top-stories {{
            background: linear-gradient(135deg, #fef3c7 0%, #fef08a 100%);
            border-left: 4px solid #f59e0b;
        }}
        
        .sources-list {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
        
        .sources-list h3 {{
            color: #1e40af;
            margin-bottom: 1rem;
        }}
        
        .source-item {{
            padding: 0.75rem;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .source-item:last-child {{
            border-bottom: none;
        }}
        
        .source-name {{
            font-weight: 600;
        }}
        
        .source-count {{
            background: #e0f2fe;
            color: #0369a1;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
        }}
        
        .footer {{
            background: #1e293b;
            color: white;
            padding: 2rem;
            text-align: center;
            margin-top: 3rem;
            border-radius: 8px;
        }}
        
        .footer p {{
            margin: 0.5rem 0;
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .article-header {{
                flex-direction: column;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📰 Revue de Presse Sportive</h1>
        <p>Synthèse des principales actualités sportives - {today}</p>
    </div>
    
    <div class="container">
        <!-- Résumé -->
        <div class="summary-box">
            <h2>📊 Résumé du jour</h2>
            <div class="stats">
"""

    # Ajouter les statistiques
    total_articles = len(df)
    categories = df["category"].nunique()
    sources = df["source"].nunique()
    
    html_content += f"""
                <div class="stat">
                    <div class="stat-value">{total_articles}</div>
                    <div class="stat-label">Articles</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{categories}</div>
                    <div class="stat-label">Disciplines</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{sources}</div>
                    <div class="stat-label">Sources</div>
                </div>
            </div>
        </div>
        
        <!-- Articles en vedette (les plus nombreux par catégorie) -->
        <div class="section">
            <h2 class="section-title">🔥 Actualités Majeures</h2>
"""
    
    # Top articles par catégorie
    for category in df["category"].unique():
        category_articles = df[df["category"] == category].head(2)
        html_content += f'<h3 style="color: #3b82f6; margin-top: 1rem; margin-bottom: 0.5rem;">📌 {category}</h3>'
        
        for idx, article in category_articles.iterrows():
            credibility = "⭐" * int(article.get("credibility", 3)) if "credibility" in article else "✓"
            url = article.get("url", "#")
            summary = article.get("summary", "")
            
            html_content += f"""
            <div class="article top-stories">
                <div class="article-header">
                    <div class="article-title">{article['title']}</div>
                </div>
                <div class="article-meta">
                    <span class="badge badge-category">{article['category']}</span>
                    <span class="badge badge-source">📍 {article['source']}</span>
                    <span class="badge badge-credibility">{credibility}</span>
                </div>
"""
            if summary:
                html_content += f'<div class="article-summary">{summary}</div>'
            
            if url and url != "#":
                html_content += f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="article-link">🔗 Lire l\'article</a>'
            
            html_content += """
            </div>
"""
    
    html_content += """
        </div>
        
        <!-- Tous les articles -->
        <div class="section">
            <h2 class="section-title">📋 Tous les articles</h2>
"""
    
    # Tous les articles
    for idx, article in df.iterrows():
        credibility = "⭐" * int(article.get("credibility", 3)) if "credibility" in article else "✓"
        url = article.get("url", "#")
        summary = article.get("summary", "")
        
        html_content += f"""
            <div class="article">
                <div class="article-header">
                    <div class="article-title">{article['title']}</div>
                </div>
                <div class="article-meta">
                    <span class="badge badge-category">{article['category']}</span>
                    <span class="badge badge-source">📍 {article['source']}</span>
                    <span class="badge badge-credibility">{credibility}</span>
                </div>
"""
        if summary:
            html_content += f'<div class="article-summary">{summary}</div>'
        
        if url and url != "#":
            html_content += f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="article-link">🔗 Lire l\'article</a>'
        
        html_content += """
            </div>
"""
    
    # Sources
    source_counts = df["source"].value_counts().sort_values(ascending=False)
    html_content += """
        </div>
        
        <!-- Vue d'ensemble des sources -->
        <div class="sources-list">
            <h3>🔗 Sources utilisées</h3>
"""
    
    for source, count in source_counts.items():
        html_content += f"""
            <div class="source-item">
                <span class="source-name">{source}</span>
                <span class="source-count">{count} article{'s' if count > 1 else ''}</span>
            </div>
"""
    
    html_content += """
        </div>
        
        <!-- Pied de page -->
        <div class="footer">
            <p>📰 Revue de presse automatisée - Agent IA de veille sportive</p>
            <p>Projet ISIC - Master Journalisme Sportif</p>
            <p style="margin-top: 1rem; opacity: 0.8;">Mise à jour automatique quotidienne</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Sauvegarder le rapport HTML
    html_file = DOCS_DIR / f"revue_presse_{report_date}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ Rapport HTML généré : {html_file}")
    
    # === RAPPORT JSON ===
    report_json = {
        "date": today,
        "summary": {
            "total_articles": int(total_articles),
            "categories": int(categories),
            "sources": int(sources)
        },
        "articles_by_category": {}
    }
    
    for category in df["category"].unique():
        count = len(df[df["category"] == category])
        report_json["articles_by_category"][category] = count
    
    json_file = DOCS_DIR / f"revue_presse_{report_date}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(report_json, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Rapport JSON généré : {json_file}")
    
    # === RAPPORT TEXTE ===
    text_report = f"""
╔══════════════════════════════════════════════════════════════════╗
║          REVUE DE PRESSE SPORTIVE - {today}               ║
║   Agent IA de Veille Sportive - Master Journalisme Sportif (ISIC) ║
╚══════════════════════════════════════════════════════════════════╝

📊 RÉSUMÉ QUOTIDIEN
─────────────────────────────────────────────────────────────────
Total d'articles traités: {total_articles}
Disciplines couverte: {categories}
Nombre de sources: {sources}

🔥 DISCIPLINES MAJEURES
─────────────────────────────────────────────────────────────────
"""
    
    for category in df["category"].unique():
        count = len(df[df["category"] == category])
        text_report += f"\n{category}: {count} article{'s' if count > 1 else ''}\n"
    
    text_report += f"\n\n🔗 SOURCES UTILISÉES\n─────────────────────────────────────────────────────────────────\n"
    
    for source, count in source_counts.items():
        text_report += f"{source}: {count} article{'s' if count > 1 else ''}\n"
    
    text_report += f"\n\n═══════════════════════════════════════════════════════════════════\nGénéré le {today} par le système automatisé ISIC\n═══════════════════════════════════════════════════════════════════\n"
    
    text_file = DOCS_DIR / f"revue_presse_{report_date}.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text_report)
    
    print(f"✅ Rapport Texte généré : {text_file}\n")
    
    print("📄 RÉSUMÉ DU RAPPORT")
    print(text_report)
    
    return {
        "html": html_file,
        "json": json_file,
        "text": text_file
    }

if __name__ == "__main__":
    articles_file = DATA_DIR / "verified_articles.csv"
    
    # Vérifier si verified_articles.csv existe sinon utiliser organized_articles.csv
    if not articles_file.exists():
        articles_file = DATA_DIR / "organized_articles.csv"
    
    if articles_file.exists():
        generate_daily_report(articles_file)
    else:
        print("❌ Aucun fichier d'articles trouvé!")
