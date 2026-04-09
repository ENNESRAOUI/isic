"""
Tests unitaires
"""

import pytest
import sys
from pathlib import Path

# Ajouter le backend au chemin
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestScraperService:
    """Tests du service de scraping"""
    
    def test_clean_text(self):
        from backend.services.nlp_service import NLPService
        nlp = NLPService()
        
        text = "  Bonjour   monde  \n  test  "
        cleaned = nlp.clean_text(text)
        assert cleaned == "Bonjour monde test"
    
    def test_extract_keywords(self):
        from backend.services.nlp_service import NLPService
        nlp = NLPService()
        
        text = "le football est un sport populaire football football"
        keywords = nlp.extract_keywords(text)
        assert "football" in keywords


class TestCredibilityService:
    """Tests du service de crédibilité"""
    
    def test_get_source_credibility(self):
        from backend.services.credibility_service import CredibilityService
        credibility = CredibilityService()
        
        score = credibility.get_source_credibility("BBC Sport")
        assert score == 5.0
    
    def test_unknown_source(self):
        from backend.services.credibility_service import CredibilityService
        credibility = CredibilityService()
        
        score = credibility.get_source_credibility("Unknown Source")
        assert score == 2.0


class TestRankingService:
    """Tests du service de classement"""
    
    def test_rank_by_credibility(self):
        from backend.services.ranking_service import RankingService
        ranking = RankingService()
        
        articles = [
            {"title": "A", "credibility_score": 5},
            {"title": "B", "credibility_score": 3},
            {"title": "C", "credibility_score": 1},
        ]
        
        ranked = ranking.rank_articles(articles, "credibility", "desc")
        assert ranked[0]["title"] == "A"
        assert ranked[2]["title"] == "C"


if __name__ == "__main__":
    pytest.main([__file__])
