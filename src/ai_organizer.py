"""
ai_organizer.py - Classification multilingue des articles sportifs.
Supporte arabe, francais, anglais et espagnol.
"""

from __future__ import annotations

import os
import re
import unicodedata
from urllib.parse import unquote

import pandas as pd

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "Football": [
        "كرة القدم", "كرة قدم", "الكرة", "الدوري", "المنتخب", "مباراة", "هدف", "أهداف", "لاعب", "مدرب",
        "دوري ابطال", "دوري أبطال", "كأس العالم", "كاس العالم", "فيفا", "يويفا",
        "football", "foot", "soccer", "goal", "goals", "but", "buts", "penalty",
        "goalkeeper", "striker", "midfielder", "defender", "transfer",
        "coupe du monde", "world cup", "mondial", "ligue des champions", "champions league",
        "premier league", "la liga", "liga", "bundesliga", "serie a", "botola",
        "real madrid", "barcelona", "arsenal", "liverpool", "manchester", "psg",
        "atletico", "raja", "wydad", "copa sudamericana",
        "yallagoal", "يلاجول",
    ],
    "Tennis": [
        "التنس", "رولان غاروس", "ويمبلدون", "غراند سلام", "atp", "wta",
        "tennis", "roland garros", "wimbledon", "grand slam", "raquette",
        "racket", "tie break", "tie-break", "backhand", "forehand", "novak djokovic",
        "nadal", "federer",
    ],
    "Basketball": [
        "كرة السلة", "السلة", "ان بي ايه", "nba",
        "basketball", "basket", "dunk", "rebound", "rebond", "three pointer",
        "three-pointer", "playoff", "playoffs", "euroleague", "lakers", "celtics",
        "thunder", "warriors", "knicks",
    ],
    "Rugby": [
        "الرغبي", "ستة امم", "كأس العالم للرغبي",
        "rugby", "essai", "melee", "mêlée", "plaquage", "six nations",
        "top 14", "scrum", "lineout", "tackle", "rugby world cup",
    ],
    "Cyclisme": [
        "الدراجات", "سباق الدراجات", "تور دو فرانس",
        "cyclisme", "cycling", "velo", "vélo", "tour de france", "giro", "vuelta",
        "peloton", "maillot jaune", "yellow jersey", "contre la montre", "time trial",
    ],
    "Natation": [
        "السباحة", "سباق السباحة",
        "natation", "swimming", "nage", "crawl", "brasse", "papillon", "dos",
        "freestyle", "butterfly", "breaststroke", "backstroke",
    ],
    "Athletisme": [
        "العاب القوى", "ألعاب القوى", "ماراثون", "سباق",
        "athletisme", "athlétisme", "athletics", "sprint", "marathon", "hurdles",
        "relay", "relais", "decathlon", "decathlon", "javelin", "discus", "shot put",
    ],
    "Boxe": [
        "الملاكمة", "ضربة قاضية", "بطل العالم",
        "boxe", "boxing", "boxer", "knockout", "k o", "ko", "ring",
        "heavyweight", "welterweight", "round",
    ],
    "Formule 1": [
        "الفورمولا 1", "فورمولا 1", "سباق السيارات", "سباق جائزة كبرى",
        "formule 1", "formula 1", "f1", "grand prix", "pit stop", "pole position",
        "ferrari", "mercedes", "red bull", "mclaren", "verstappen", "hamilton",
    ],
    "Golf": [
        "الغولف",
        "golf", "pga", "birdie", "bogey", "fairway", "tee", "ryder cup",
    ],
    "Handball": [
        "كرة اليد",
        "handball", "pivot", "ailier", "sept metres", "7 metres", "7 meter",
    ],
    "Volleyball": [
        "الكرة الطائرة", "طائرة",
        "volleyball", "volley", "libero", "spike", "smash", "filet",
    ],
    "Auto/Moto": [
        "رالي", "سيارات", "دراجات نارية",
        "auto moto", "auto-moto", "automobile", "rally", "rallye", "historic rally",
        "motogp", "moto gp", "superbike", "wrc", "karting",
    ],
    "Combat": [
        "كيندو", "جودو", "كاراتيه", "تايكوندو",
        "combat", "arts martiaux", "mma", "ufc", "kendo", "judo", "karate",
        "taekwondo", "kickboxing",
    ],
}

SOURCE_HINTS = {
    "tennis explorer": "Tennis",
    "onefootball": "Football",
    "90min": "Football",
}

MIN_CATEGORY_SCORE = 2
FIELD_WEIGHTS = {
    "title": 6,
    "url": 5,
    "summary": 4,
    "source": 2,
}


def normalize_text(text: str) -> str:
    value = unquote(str(text or "")).lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.replace("’", "'").replace("`", "'")
    value = re.sub(r"[^a-z0-9\u0600-\u06FF]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def contains_keyword(haystack: str, keyword: str) -> bool:
    normalized_keyword = normalize_text(keyword)
    if not normalized_keyword:
        return False
    wrapped_haystack = f" {haystack} "
    wrapped_keyword = f" {normalized_keyword} "
    return wrapped_keyword in wrapped_haystack


def keyword_weight(keyword: str) -> int:
    token_count = len(normalize_text(keyword).split())
    return max(1, token_count)


def category_score(category: str, fields: dict[str, str]) -> int:
    score = 0
    for field_name, field_weight in FIELD_WEIGHTS.items():
        text = fields[field_name]
        if not text:
            continue
        for keyword in CATEGORY_KEYWORDS[category]:
            if contains_keyword(text, keyword):
                score += field_weight * keyword_weight(keyword)
    return score


def classify_article(title: str, source: str = "", url: str = "", summary: str = "") -> str:
    fields = {
        "title": normalize_text(title),
        "source": normalize_text(source),
        "url": normalize_text(url),
        "summary": normalize_text(summary),
    }

    best_category = "Autre"
    best_score = 0

    for category in CATEGORY_KEYWORDS:
        score = category_score(category, fields)
        if score > best_score:
            best_score = score
            best_category = category

    if best_score >= MIN_CATEGORY_SCORE:
        return best_category

    source_key = fields["source"]
    for source_hint, category in SOURCE_HINTS.items():
        if contains_keyword(source_key, source_hint):
            return category
    return "Autre"


def organize_articles(input_path: str, output_path: str) -> pd.DataFrame:
    print(f"Lecture : {input_path}")
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    df.columns = [str(column).strip().lower() for column in df.columns]
    col_map = {
        "titre": "title",
        "title": "title",
        "source": "source",
        "categorie": "category",
        "category": "category",
        "discipline": "category",
        "date": "date",
        "resume": "summary",
        "summary": "summary",
        "url": "url",
        "lien": "url",
        "credibility": "credibility",
        "credibilite": "credibility",
    }
    df = df.rename(columns={column: col_map.get(column, column) for column in df.columns})

    if "title" not in df.columns:
        raise ValueError("Colonne 'titre' ou 'title' introuvable dans le CSV")

    print(f"{len(df)} articles a classifier...")
    df["category"] = df.apply(
        lambda row: classify_article(
            str(row.get("title", "")),
            str(row.get("source", "")),
            str(row.get("url", "")),
            str(row.get("summary", "")),
        ),
        axis=1,
    )

    counts = df["category"].value_counts()
    print("\nResultats de classification :")
    for category, count in counts.items():
        pct = count / len(df) * 100
        print(f"   {category:20s} -> {count:4d} articles ({pct:.1f}%)")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nSauvegarde : {output_path}")
    return df


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "output", "articles.csv")
    output_file = os.path.join(base_dir, "data", "output", "organized_articles.csv")

    if not os.path.exists(input_file):
        print(f"Fichier introuvable : {input_file}")
        print("Executez d'abord scraper.py")
    else:
        organize_articles(input_file, output_file)
