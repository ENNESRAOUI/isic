# 🎯 ISIC Backend-Frontend Integration - Complete Setup

A comprehensive guide for setting up and running the fully integrated ISIC Sports Press Review application with FastAPI backend and modern frontend architecture.

## ✨ What's New

This integration provides a complete transformation of the ISIC application:

### Backend (FastAPI)
- ✅ RESTful API for all data operations
- ✅ Database-backed storage (SQLite/PostgreSQL)
- ✅ Pipeline orchestration and monitoring
- ✅ AI analysis through centralized endpoint
- ✅ Report generation and management
- ✅ Automatic data import from CSV

### Frontend
- ✅ Seamless API integration
- ✅ Smart fallback to CSV when API unavailable
- ✅ Automatic article loading from database
- ✅ Real-time categorization and filtering
- ✅ AI-powered article analysis via API
- ✅ Report generation through backend

## 📁 Project Structure

```
isic/
├── backend/                    # New FastAPI Backend
│   ├── main.py                # Main application
│   ├── database.py            # Database setup
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   ├── routes/
│   │   ├── articles.py        # Article endpoints
│   │   ├── pipeline.py        # Pipeline endpoints
│   │   ├── reports.py         # Report endpoints
│   │   └── ai.py              # AI analysis endpoints
│   └── __init__.py
│
├── frontend/                   # Updated Frontend
│   └── js/
│       └── api.js             # API client library
│
├── web/
│   └── index.html             # Updated main app
│
├── src/                       # Existing Python modules
│   ├── scraper.py
│   ├── ai_organizer.py
│   ├── data_enricher.py
│   ├── source_verifier.py
│   ├── report_generator.py
│   └── run_pipeline.py
│
├── data/                      # Data files
├── docs/                      # Reports
├── database/                  # Database scripts
│
├── requirements.txt           # Updated with new deps
├── .env.example              # Configuration template
├── BACKEND_SETUP.md          # Backend documentation
├── FRONTEND_INTEGRATION.md   # Integration guide
└── API_INTEGRATION.md        # This file
```

## 🚀 Quick Start (5 minutes)

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY
```

### 3. Start Backend

```bash
cd c:\Users\Med Ennesraoui\isic
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Frontend

Open browser: `http://localhost:8000/web/index.html`

API Docs: `http://localhost:8000/docs`

## 📊 Data Flow Architecture

### Article Loading Flow

```
Frontend loads (DOMContentLoaded)
    ↓
loadData() called
    ↓
Try: loadDataFromAPI()
    ↓
fetch /api/articles?page=1&page_size=200
    ↓
Backend (database.py)
    ↓
SQLAlchemy queries Article table
    ↓
Return JSON paginated articles
    ↓
Frontend: convertAPIArticles(data)
    ↓
Display in grouped by date layout
    ↓
[Success!] ✅

If API fails → Fallback to CSV files
```

### AI Analysis Flow

```
User clicks article detail
    ↓
openDetail(articleId)
    ↓
fetchAI(article)
    ↓
analyzeArticleWithAPI(articleId, 'general')
    ↓
fetch /api/ai/{articleId}/general
    ↓
Backend (routes/ai.py)
    ↓
Call Claude API with article context
    ↓
Return analysis result
    ↓
Display in article detail drawer
    ↓
[Success!] ✅
```

### Pipeline Execution Flow

```
POST /api/pipeline/run
    ↓
Create PipelineRun record in database
    ↓
Add background task: run_pipeline_async()
    ↓
Sequential execution:
    ├─ scraper.py
    ├─ ai_organizer.py
    ├─ data_enricher.py
    ├─ source_verifier.py
    └─ report_generator.py
    ↓
Update database with status
    ↓
frontend: monitorPipeline(runId)
    ↓
Poll GET /api/pipeline/status/{runId}
    ↓
Display progress updates
    ↓
[Completed!] ✅
```

## 🔌 API Endpoints Reference

### Base URL
```
http://localhost:8000/api
```

### Articles Module
```
GET    /articles/                 List articles (paginated, filterable)
GET    /articles/{id}             Get single article
GET    /articles/categories       List all categories
GET    /articles/sources          List all sources
GET    /articles/stats            Get statistics
POST   /articles/import-csv       Import from CSV files
```

### Pipeline Module
```
POST   /pipeline/run              Start pipeline execution
GET    /pipeline/status/{id}      Get specific run status
GET    /pipeline/latest           Get latest run
GET    /pipeline/runs             List all runs
```

### Reports Module
```
GET    /reports/latest            Get latest report
GET    /reports/by-date/{date}    Get report by date
GET    /reports/latest/html       Download HTML
GET    /reports/latest/json       Download JSON
GET    /reports/latest/txt        Download TXT
```

### AI Module
```
POST   /ai/analyze                Analyze article (request body)
GET    /ai/{id}/general           General analysis
GET    /ai/{id}/summary           Summary analysis
GET    /ai/{id}/detailed          Detailed analysis
POST   /ai/report-analysis        Generate report intro
```

## 💻 Frontend JavaScript API

All functions in `frontend/js/api.js`:

```javascript
// Articles
fetchArticlesFromAPI(page, pageSize, filters)
fetchCategories()
fetchSources()
fetchArticleStats()
importArticlesFromCSV()

// Pipeline
runPipeline()
getPipelineStatus(runId)
getLatestPipelineRun()
monitorPipeline(runId, callback)

// Reports
getLatestReport()
getReportHTML()
getReportJSON()

// AI Analysis
analyzeArticleWithAPI(articleId, type)
streamAnalysisFromAPI(articleId, type, element)

// Utility
loadDataFromAPI()
convertAPIArticles(apiData)
```

## 🗄️ Database Schema

### Articles Table
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    source VARCHAR(255) NOT NULL,
    url VARCHAR(1000),
    category VARCHAR(100) NOT NULL,
    summary TEXT,
    content TEXT,
    publication_date DATETIME,
    scraped_date DATETIME DEFAULT NOW(),
    credibility_score FLOAT DEFAULT 0,
    source_reliability VARCHAR(50),
    wikipedia_image_url VARCHAR(1000),
    wikipedia_image_caption VARCHAR(500),
    is_verified BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW()
)
```

### Daily Reports Table
```sql
CREATE TABLE daily_reports (
    id INTEGER PRIMARY KEY,
    report_date DATETIME UNIQUE NOT NULL,
    introduction TEXT,
    highlights TEXT,
    source_analysis TEXT,
    conclusion TEXT,
    total_articles INTEGER,
    total_sources INTEGER,
    articles_by_category VARCHAR(1000),
    html_output VARCHAR(1000),
    json_output VARCHAR(1000),
    txt_output VARCHAR(1000),
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW()
)
```

### Pipeline Runs Table
```sql
CREATE TABLE pipeline_runs (
    id INTEGER PRIMARY KEY,
    status VARCHAR(50) DEFAULT 'pending',
    step VARCHAR(100),
    progress INTEGER DEFAULT 0,
    scraper_completed BOOLEAN DEFAULT FALSE,
    organizer_completed BOOLEAN DEFAULT FALSE,
    enricher_completed BOOLEAN DEFAULT FALSE,
    verifier_completed BOOLEAN DEFAULT FALSE,
    report_generator_completed BOOLEAN DEFAULT FALSE,
    start_time DATETIME DEFAULT NOW(),
    end_time DATETIME,
    error_message TEXT,
    created_at DATETIME DEFAULT NOW()
)
```

## 🔐 Security Features

- CORS middleware configured
- API key validation for external services
- Database connection pooling
- Environment variable protection
- Input validation via Pydantic schemas
- Error handling and logging

## 🧪 Testing Checklist

- [ ] Backend starts without errors
- [ ] Health check returns OK
- [ ] Articles load from API
- [ ] Categories and sources populate
- [ ] Filters work correctly
- [ ] Article detail drawer opens
- [ ] AI analysis generates content
- [ ] CSV import works
- [ ] Pipeline can be started
- [ ] Pipeline monitoring works
- [ ] Reports display correctly
- [ ] Frontend falls back to CSV when API unavailable

## 📋 Configuration Options

### Environment Variables (.env)

```bash
# Required
ANTHROPIC_API_KEY=sk_xxxxxxx

# Optional
DATABASE_URL=sqlite:///./isic.db
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4
CORS_ORIGINS=["*"]
PIPELINE_TIMEOUT=600
```

### Database Options

**SQLite (Default)**
```
DATABASE_URL=sqlite:///./isic.db
```

**PostgreSQL (Production)**
```
DATABASE_URL=postgresql://user:password@localhost:5432/isic
```

**MySQL**
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/isic
```

## 🚀 Deployment Options

### Local Development
```bash
python -m uvicorn backend.main:app --reload
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app
```

### Docker
```bash
docker build -t isic .
docker run -p 8000:8000 isic
```

### Systemd Service
See BACKEND_SETUP.md for systemd configuration

## 🔄 Workflow Examples

### Daily Workflow

```bash
# 1. Start backend
python -m uvicorn backend.main:app --reload

# 2. Open frontend
# Browser: http://localhost:8000/web/index.html

# 3. Articles load automatically from API

# 4. To regenerate data:
# POST /api/pipeline/run (or click button in admin panel)

# 5. Monitor progress
# GET /api/pipeline/latest

# 6. Get report
# GET /api/reports/latest/html
```

### Adding New Data

```python
# Option 1: Run pipeline through API
POST /api/pipeline/run

# Option 2: Import existing CSV
POST /api/articles/import-csv

# Option 3: Add articles programmatically
from backend.database import SessionLocal
from backend.models import Article

db = SessionLocal()
article = Article(
    title="Article Title",
    source="Source Name",
    category="Football",
    credibility_score=4.0
)
db.add(article)
db.commit()
```

### Monitoring Pipeline

```javascript
// In browser console
const runId = 1;
const status = await getPipelineStatus(runId);
console.log(status);

// Or monitor continuously
monitorPipeline(runId, (status) => {
    console.log(`Progress: ${status.progress}% - ${status.step}`);
});
```

## 🐛 Troubleshooting Guide

### Issue: API not responding
**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart backend
python -m uvicorn backend.main:app --reload
```

### Issue: Articles not loading
**Solution:**
```javascript
// Check API response
const data = await fetchArticlesFromAPI(1, 100);
console.log(data);

// Import from CSV
await importArticlesFromCSV();
```

### Issue: Database locked (SQLite)
**Solution:**
```bash
# Delete database and restart
rm isic.db
# Backend will recreate it
```

### Issue: AI analysis fails
**Solution:**
```bash
# Check API key in .env
cat .env | grep ANTHROPIC_API_KEY

# Test Claude API
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-sonnet","max_tokens":100,"messages":[{"role":"user","content":"test"}]}'
```

### Issue: CORS errors
**Solution:**
```bash
# Update CORS_ORIGINS in .env
CORS_ORIGINS=["http://localhost", "http://localhost:3000"]

# Or allow all (dev only)
CORS_ORIGINS=["*"]
```

## 📈 Performance Tips

1. **Use PostgreSQL** for production (SQLite for dev)
2. **Enable caching** for reports
3. **Paginate articles** (default 20 per page)
4. **Batch CSV imports** in chunks
5. **Monitor database** size and CPU
6. **Use Gunicorn workers** (4-8 for production)

## 📚 Documentation

- **Backend Setup**: See [BACKEND_SETUP.md](BACKEND_SETUP.md)
- **Frontend Integration**: See [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
- JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

## ✅ Verification Checklist

- [x] Backend created and configured
- [x] Database models defined
- [x] API routes implemented
- [x] Frontend API client created
- [x] HTML updated for API integration
- [x] AI analysis using API
- [x] Pipeline management API
- [x] Report generation API
- [x] Documentation complete
- [x] Environment configuration ready

## 🎉 Next Steps

1. **Start Backend**: `python -m uvicorn backend.main:app --reload`
2. **Open Frontend**: `http://localhost:8000/web/index.html`
3. **Explore API Docs**: `http://localhost:8000/docs`
4. **Import Data**: Run pipeline or import CSV
5. **Customize**: Modify API or frontend as needed

## 📞 Support & Issues

- Check API logs in terminal
- Review browser console (F12)
- Check ANTHROPIC_API_KEY in .env
- Read error messages carefully
- Test endpoints with curl or Postman

## 📄 License

MIT License - Full integration ready for production use

---

**Status**: ✅ Complete Integration Ready

Last Updated: March 2026
