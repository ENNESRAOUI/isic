"""
scraper.py — Collecte d'articles sportifs multilingues
Sources : Arabe + Français + Anglais (15+ sources)
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
import random
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar-SA,ar;q=0.9,fr-FR;q=0.8,fr;q=0.7,en;q=0.6",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cache-Control": "max-age=0",
}

# ─────────────────────────────────────────────
# SOURCES DÉFINIES
# Chaque source : nom, url, sélecteurs CSS, langue
# ─────────────────────────────────────────────
SOURCES = [
    # ── SOURCES ARABES ──
    {
        "name": "Le360 Sport",
        "url": "https://sport.le360.ma/",
        "lang": "ar",
        "selectors": {
            "articles": ".article, .post, article, .story, .item",
            "title": "h2, h3, .article-title, .title",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "Kooora",
        "url": "https://www.kooora.com/",
        "lang": "ar",
        "selectors": {
            "articles": ".news-item, .news_item, article, h3, .post",
            "title": "h3, h2, .title, span",
            "link": "a",
            "date": "span.date, .time, time",
        },
    },
    {
        "name": "Arab News Sports",
        "url": "https://www.arabnews.com/sports",
        "lang": "ar",
        "selectors": {
            "articles": "article, .post, .story, .news-item, .card",
            "title": "h2, h3, .title, .headline",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "Monde du Ballon",
        "url": "https://www.mondeduballon.com/",
        "lang": "fr",
        "selectors": {
            "articles": "article, .post, .story, .news",
            "title": "h2, h3, .title, a",
            "link": "a",
            "date": "time, .date, span",
        },
    },
    {
        "name": "ESPN UK",
        "url": "https://www.espn.co.uk/",
        "lang": "en",
        "selectors": {
            "articles": "article, .post, .story, .item",
            "title": "h2, h3, .headline, a",
            "link": "a",
            "date": "time, .date, span",
        },
    },

    # ── SOURCES FRANÇAISES ──
    {
        "name": "L'Équipe",
        "url": "https://www.lequipe.fr/",
        "lang": "fr",
        "selectors": {
            "articles": "article, .article, .js-push-article, .story",
            "title": "h2, h3, .article__title, .headline",
            "link": "a",
            "date": "time, .article__date",
        },
    },
    {
        "name": "RMC Sport",
        "url": "https://rmcsport.bfmtv.com/",
        "lang": "fr",
        "selectors": {
            "articles": "article, .story, .post, .news-item",
            "title": "h2, h3, .story__title, .headline",
            "link": "a",
            "date": "time, .story__date, .date",
        },
    },
    {
        "name": "beIN Sports",
        "url": "https://www.beinsports.com/france/",
        "lang": "fr",
        "selectors": {
            "articles": "article, .card, .post, .story",
            "title": "h2, h3, .title, .headline",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "France Bleu Sport",
        "url": "https://www.francebleu.fr/",
        "lang": "fr",
        "selectors": {
            "articles": "article, .post, .story, .news",
            "title": "h2, h3, .title",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "Tennis Explorer",
        "url": "https://www.tennisexplorer.com/",
        "lang": "fr",
        "selectors": {
            "articles": "article, .post, .story, tr, li",
            "title": "h2, h3, .title, a, span",
            "link": "a",
            "date": "time, .date, span",
        },
    },
    {
        "name": "BBC Sport",
        "url": "https://www.bbc.com/sport",
        "lang": "en",
        "selectors": {
            "articles": "article, .gs-c-promo, .sc-2c2c53f-0",
            "title": "h3, h2, .gs-c-promo-heading__title",
            "link": "a",
            "date": "time",
        },
    },
    {
        "name": "Sky Sports",
        "url": "https://www.skysports.com/",
        "lang": "en",
        "selectors": {
            "articles": "article, .news-list__item, .story",
            "title": "h2, h3, .news-list__headline, .headline",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "Goal.com",
        "url": "https://www.goal.com/en",
        "lang": "en",
        "selectors": {
            "articles": "article, .js-article, .post, .story",
            "title": "h3, h2, .title, .headline",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "90min",
        "url": "https://www.90min.com/",
        "lang": "en",
        "selectors": {
            "articles": "article, .article-card, .post, .story",
            "title": "h3, h2, .title, .headline",
            "link": "a",
            "date": "time, .date",
        },
    },
    {
        "name": "Transfermarkt",
        "url": "https://www.transfermarkt.com/",
        "lang": "en",
        "selectors": {
            "articles": "article, .post, .news, .story, tr",
            "title": "h2, h3, a, span",
            "link": "a",
            "date": "time, .date, span",
        },
    },
    {
        "name": "Sportal",
        "url": "https://www.sportal.bg/",
        "lang": "en",
        "selectors": {
            "articles": "article, .post, .story, .news",
            "title": "h2, h3, .title, a",
            "link": "a",
            "date": "time, .date, span",
        },
    },
    {
        "name": "OneFootball",
        "url": "https://onefootball.com/",
        "lang": "en",
        "selectors": {
            "articles": "article, .post, .story, .card",
            "title": "h2, h3, .title, span",
            "link": "a",
            "date": "time, .date",
        },
    },
]


def scrape_source(source: dict, retries: int = 3) -> list[dict]:
    """Scrape une source avec stratégies multiples et retries."""
    articles = []
    
    for attempt in range(retries):
        try:
            if attempt == 0:
                print(f"  🌐 {source['name']}…", end="", flush=True)
            else:
                print(f"  🔄 Retry {attempt}/{retries-1}…", end="", flush=True)
            
            # Utiliser une session pour gérer les cookies et connexions
            session = requests.Session()
            session.headers.update(HEADERS)
            
            resp = session.get(source["url"], timeout=15, allow_redirects=True, verify=True)
            resp.raise_for_status()  # Vérifier les erreurs HTTP
            resp.encoding = resp.apparent_encoding or "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")

            sel = source["selectors"]
            today = datetime.now().strftime("%Y-%m-%d")
            found_titles = set()

            # ─────────────────────────────────────────────
            # STRATÉGIE 1 : Conteneurs avec sélecteurs CSS
            # ─────────────────────────────────────────────
            containers = soup.select(sel["articles"])
            for container in containers[:30]:
                try:
                    title_el = container.select_one(sel["title"]) if isinstance(container, BeautifulSoup.__class__) else container
                    if not title_el:
                        title_el = container

                    title = title_el.get_text(strip=True) if title_el else ""
                    if len(title) < 10 or title in found_titles:
                        continue

                    # Extraire l'URL
                    url = ""
                    link_el = container.find("a", href=True)
                    if link_el:
                        href = link_el.get("href", "").strip()
                        if href:
                            url = href if href.startswith("http") else source["url"].rstrip("/") + "/" + href.lstrip("/")

                    # Extraire la date
                    date_el = container.select_one(sel.get("date", "time"))
                    date = today
                    if date_el:
                        date_text = (
                            date_el.get("datetime", "")
                            or date_el.get("content", "")
                            or date_el.get_text(strip=True)
                            or today
                        )
                        date = date_text[:10] if date_text else today

                    if title and url:  # Valider title et url
                        found_titles.add(title)
                        articles.append({
                            "title": title,
                            "source": source["name"],
                            "lang": source["lang"],
                            "url": url,
                            "date": date,
                            "summary": "",
                            "category": "",
                            "credibility": 0,
                        })
                except Exception as e:
                    pass  # Ignorer les erreurs individuelles

            # ─────────────────────────────────────────────
            # STRATÉGIE 2 : Tous les h1/h2/h3 + liens
            # ─────────────────────────────────────────────
            if len(articles) < 5:
                for tag in soup.find_all(["h1", "h2", "h3"])[:40]:
                    try:
                        title = tag.get_text(strip=True)
                        if len(title) < 10 or title in found_titles:
                            continue
                        
                        # Chercher un lien dans le tag ou ses parents
                        link_el = tag.find("a", href=True)
                        if not link_el:
                            link_el = tag.find_parent("a", href=True)
                        if not link_el and tag.find_next("a", href=True):
                            link_el = tag.find_next("a", href=True)
                        
                        url = ""
                        if link_el:
                            href = link_el.get("href", "").strip()
                            if href:
                                url = href if href.startswith("http") else source["url"].rstrip("/") + "/" + href.lstrip("/")

                        if title and url:
                            found_titles.add(title)
                            articles.append({
                                "title": title,
                                "source": source["name"],
                                "lang": source["lang"],
                                "url": url,
                                "date": today,
                                "summary": "",
                                "category": "",
                                "credibility": 0,
                            })
                    except Exception as e:
                        pass

            # ─────────────────────────────────────────────
            # STRATÉGIE 3 : Tous les liens avec texte long
            # ─────────────────────────────────────────────
            if len(articles) < 5:
                for link in soup.find_all("a", href=True)[:50]:
                    try:
                        title = link.get_text(strip=True)
                        if len(title) < 10 or title in found_titles or len(title) > 300:
                            continue
                        
                        href = link.get("href", "").strip()
                        if not href:
                            continue
                        
                        url = href if href.startswith("http") else source["url"].rstrip("/") + "/" + href.lstrip("/")
                        
                        if url and "javascript" not in url and "#" not in url:
                            found_titles.add(title)
                            articles.append({
                                "title": title,
                                "source": source["name"],
                                "lang": source["lang"],
                                "url": url,
                                "date": today,
                                "summary": "",
                                "category": "",
                                "credibility": 0,
                            })
                    except Exception as e:
                        pass

            print(f" {len(articles)} articles")
            break  # Succès, sortir de la boucle retry

        except requests.exceptions.Timeout:
            print(f" ⏱️ Timeout", end="")
            if attempt < retries - 1:
                time.sleep(3)
        except requests.exceptions.ConnectionError as e:
            print(f" 🔌 Erreur connexion", end="")
            if attempt < retries - 1:
                time.sleep(3)
        except requests.exceptions.HTTPError as e:
            print(f" 🚫 HTTP {e.response.status_code}", end="")
            if attempt < retries - 1:
                time.sleep(2)
        except Exception as e:
            print(f" ❌ {str(e)[:40]}", end="")
            if attempt < retries - 1:
                time.sleep(2)
    
    if not articles:
        print(f" ⚠️ Aucun article trouvé")

    return articles


def scrape_all(output_path: str, delay: float = 2.0) -> pd.DataFrame:
    """Scrape toutes les sources avec délais aléatoires."""
    all_articles = []
    print(f"\n🚀 Démarrage du scraping ({len(SOURCES)} sources)\n")

    for i, source in enumerate(SOURCES, 1):
        print(f"[{i:2d}/{len(SOURCES)}]", end=" ")
        articles = scrape_source(source, retries=3)
        all_articles.extend(articles)

        # Délai poli randomisé entre requêtes
        if i < len(SOURCES):
            sleep_time = delay + random.uniform(0.5, 2.5)
            time.sleep(sleep_time)

    # Déduplications par titre
    df = pd.DataFrame(all_articles)
    if df.empty:
        print("\n⚠️ Aucun article collecté.")
        return df

    before = len(df)
    df = df.drop_duplicates(subset=["title"])
    after = len(df)
    print(f"\n🗑️  Doublons supprimés : {before - after}")

    # Sauvegarder
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\n✅ {after} articles sauvegardés → {output_path}")
    print(f"\n📊 Par langue :")
    for lang, n in df["lang"].value_counts().items():
        print(f"   {lang}: {n}")
    print(f"\n📊 Par source :")
    for src, n in df["source"].value_counts().items():
        print(f"   {src:20s}: {n}")

    return df


if __name__ == "__main__":
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(BASE, "data", "output", "articles.csv")
    scrape_all(out)
