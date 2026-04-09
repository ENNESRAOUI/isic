"""
data_enricher.py — Enrichissement des articles
- Résumés automatiques (scraping + extraction)
- Images depuis Wikipedia REST API
- Nettoyage des textes arabes/français/anglais
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import re
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ISIC-Enricher/1.0)",
    "Accept-Language": "fr-FR,fr;q=0.9,ar;q=0.8,en;q=0.7",
}

WIKIPEDIA_LANGS = ["ar", "fr", "en"]


def clean_text(text: str) -> str:
    """Nettoie un texte (arabe, français, anglais)."""
    if not text:
        return ""
    # Supprimer les caractères de contrôle
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
    # Réduire les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Supprimer les caractères HTML résiduels
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
    text = text.replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()


def extract_summary_from_url(url: str, max_chars: int = 300) -> str:
    """Tente d'extraire un résumé depuis l'URL de l'article."""
    if not url or not url.startswith("http"):
        return ""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        # Enlever scripts/styles
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        # Chercher le premier paragraphe substantiel
        for p in soup.find_all("p"):
            text = clean_text(p.get_text())
            if len(text) > 60:
                return text[:max_chars] + ("…" if len(text) > max_chars else "")
    except Exception:
        pass
    return ""


def fetch_wikipedia_image(title: str, lang: str = "fr") -> dict:
    """
    Cherche une image sur Wikipedia pour un titre donné.
    Retourne {"url": ..., "caption": ...} ou {}
    """
    # Essayer plusieurs langues
    for l in ([lang] + [x for x in WIKIPEDIA_LANGS if x != lang]):
        try:
            # Recherche Wikipedia
            search_url = f"https://{l}.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": title,
                "srlimit": 1,
            }
            r = requests.get(search_url, params=params, headers=HEADERS, timeout=8)
            data = r.json()
            results = data.get("query", {}).get("search", [])
            if not results:
                continue

            page_title = results[0]["title"]

            # Récupérer la thumbnail via REST API
            rest_url = f"https://{l}.wikipedia.org/api/rest_v1/page/summary/{quote(page_title)}"
            r2 = requests.get(rest_url, headers=HEADERS, timeout=8)
            if not r2.ok:
                continue
            page = r2.json()

            thumb = page.get("thumbnail", {})
            if thumb.get("source"):
                # Agrandir l'image (800px)
                img_url = re.sub(r'/\d+px-', '/800px-', thumb["source"])
                return {
                    "url": img_url,
                    "caption": page.get("description", ""),
                    "source": f"Wikipedia ({l})",
                }
        except Exception:
            continue
    return {}


def detect_article_lang(title: str) -> str:
    """Détecte la langue dominante d'un titre."""
    arabic = len(re.findall(r'[\u0600-\u06FF]', title))
    total = len(title.replace(" ", ""))
    if total == 0:
        return "fr"
    if arabic / total > 0.25:
        return "ar"
    # Heuristique simple FR vs EN
    fr_words = ["le", "la", "les", "du", "des", "un", "une", "et", "en", "au", "aux"]
    words = title.lower().split()
    if any(w in fr_words for w in words[:5]):
        return "fr"
    return "en"


def enrich_dataframe(df: pd.DataFrame, enrich_images: bool = True,
                     enrich_summaries: bool = True, max_articles: int = None) -> pd.DataFrame:
    """
    Enrichit le DataFrame avec images et résumés.
    """
    if df.empty:
        return df

    # Colonnes par défaut
    if "image_url" not in df.columns:
        df["image_url"] = ""
    if "image_caption" not in df.columns:
        df["image_caption"] = ""
    if "resume" not in df.columns:
        df["resume"] = ""
    if "lang" not in df.columns:
        df["lang"] = df["title"].apply(detect_article_lang) if "title" in df.columns else "fr"

    limit = min(max_articles or len(df), len(df))
    print(f"\n🔍 Enrichissement de {limit} articles…")

    for i, idx in enumerate(df.index[:limit]):
        row = df.loc[idx]
        title = str(row.get("title", ""))
        url = str(row.get("url", ""))
        lang = str(row.get("lang", "fr"))

        print(f"  [{i+1:3d}/{limit}] {title[:55]}…", end="\r")

        # ── Résumé ──
        if enrich_summaries:
            current_resume = str(row.get("resume", "")).strip()
            if not current_resume or current_resume == "nan":
                resume = extract_summary_from_url(url)
                if resume:
                    df.at[idx, "resume"] = resume

        # ── Image ──
        if enrich_images:
            current_img = str(row.get("image_url", "")).strip()
            if not current_img or current_img == "nan":
                # Choisir la langue Wikipedia selon la langue de l'article
                wiki_lang = "ar" if lang == "ar" else "fr" if lang == "fr" else "en"
                img_data = fetch_wikipedia_image(title, wiki_lang)
                if img_data:
                    df.at[idx, "image_url"] = img_data["url"]
                    df.at[idx, "image_caption"] = img_data.get("caption", "")

        time.sleep(0.3)  # Poli

    print(f"\n✅ Enrichissement terminé")
    return df


def run_enrichment(input_path: str, output_path: str,
                   images: bool = True, summaries: bool = True,
                   max_articles: int = 50):
    """Point d'entrée principal."""
    print(f"📂 Lecture : {input_path}")
    df = pd.read_csv(input_path, encoding="utf-8-sig")
    print(f"   {len(df)} articles chargés")

    df = enrich_dataframe(df, enrich_images=images,
                          enrich_summaries=summaries,
                          max_articles=max_articles)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n💾 Sauvegardé : {output_path}")

    # Stats
    n_img = (df["image_url"].notna() & (df["image_url"] != "")).sum()
    n_res = (df["resume"].notna() & (df["resume"] != "")).sum()
    print(f"   📸 Articles avec image  : {n_img}/{len(df)}")
    print(f"   📝 Articles avec résumé : {n_res}/{len(df)}")

    return df


if __name__ == "__main__":
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inp = os.path.join(BASE, "data", "output", "organized_articles.csv")
    out = os.path.join(BASE, "data", "output", "organized_articles.csv")

    if not os.path.exists(inp):
        print(f"❌ Fichier introuvable : {inp}")
    else:
        run_enrichment(inp, out, images=True, summaries=True, max_articles=100)