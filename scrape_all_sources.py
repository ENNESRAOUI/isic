#!/usr/bin/env python3
from src.scraper import scrape_all
import os

BASE = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE, "data", "output", "articles_test.csv")

# Scrape toutes les sources
df = scrape_all(output_path, delay=2.0)

print("\n" + "=" * 80)
print("RÉSUMÉ FINAL DU SCRAPING")
print("=" * 80)
print(f"Total articles trouvés: {len(df)}")
