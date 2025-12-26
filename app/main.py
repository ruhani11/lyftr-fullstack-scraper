from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl
from app.scraper import scrape_with_fallback


app = FastAPI()

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Health Check
# -----------------------------
@app.get("/healthz")
def health_check():
    return {"status": "ok"}


# -----------------------------
# Frontend Home Page
# -----------------------------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -----------------------------
# Request Model for /scrape
# -----------------------------
class ScrapeRequest(BaseModel):
    url: HttpUrl


# -----------------------------
# Scrape Endpoint
# -----------------------------
@app.post("/scrape")
def scrape(req: ScrapeRequest):
    return {
        "result": scrape_with_fallback(str(req.url))
    }
