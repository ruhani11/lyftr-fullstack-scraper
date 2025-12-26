# Lyftr AI — Full-Stack Assignment  
Universal Website Scraper (MVP) + JSON Viewer

## Overview
This project implements a **universal website scraper** with a minimal frontend JSON viewer.

Given a URL, the system:
- Scrapes static HTML content
- Falls back to **JS rendering using Playwright** when required
- Performs **automatic scrolling (depth ≥ 3)**
- Extracts **section-aware structured JSON**
- Provides a simple UI to view and download the JSON output

The implementation strictly follows the API contract and schema specified in the Lyftr AI assignment.

---

## Tech Stack
- **Language:** Python 3.10+
- **Backend:** FastAPI
- **Static Scraping:** httpx + BeautifulSoup
- **JS Rendering:** Playwright (Chromium)
- **Frontend:** Jinja2 (server-rendered)
- **Server:** Uvicorn

---

## How to Run

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd lyftr-fullstack-scraper
````

### 2. Run the project

```bash
chmod +x run.sh
./run.sh
```

This script will:

1. Create and activate a virtual environment
2. Install all dependencies
3. Install Playwright Chromium
4. Start the server on **[http://localhost:8000](http://localhost:8000)**

---

## API Endpoints

### Health Check

```http
GET /healthz
```

Response:

```json
{ "status": "ok" }
```

---

### Scrape a Website

```http
POST /scrape
```

Request body:

```json
{
  "url": "https://example.com"
}
```

Response includes:

* Metadata (title, description, language, canonical)
* Section-aware structured content
* Interaction metadata (scroll count, pages)
* Graceful error handling

---

## Frontend

The frontend is available at:

**[http://localhost:8000/](http://localhost:8000/)**

Features:

* URL input field
* Scrape button
* Loading indicator
* Expandable section viewer
* Full JSON preview
* Download JSON option

---

## Tested URLs

| URL                                                                                                            | Notes                                                 |
| -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [https://example.com](https://example.com)                                                                     | Static HTML page                                      |
| [https://en.wikipedia.org/wiki/Artificial_intelligence](https://en.wikipedia.org/wiki/Artificial_intelligence) | JS-rendered with bot protection (Playwright fallback) |
| [https://news.ycombinator.com](https://news.ycombinator.com)                                                   | Scroll / pagination behavior                          |

---

## Design Highlights

* Static-first scraping strategy for performance
* Automatic JS fallback using Playwright
* Scroll depth fixed to **3** for interaction coverage
* Semantic section grouping using HTML landmarks
* Schema-compliant JSON output
* Graceful error handling with partial results

Detailed design decisions are documented in `design_notes.md`.

---

## Limitations

* Scraping is limited to a single domain
* Click-based interactions are generic (no site-specific selectors)
* Some highly protected sites may still restrict automation

---

## Project Structure

```
lyftr-fullstack-scraper/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── scraper.py
│   └── templates/
│       └── index.html
│
├── run.sh
├── requirements.txt
├── README.md
├── design_notes.md
├── capabilities.json
├── .gitignore
```

---

## Setup Used

* VS Code
* Python virtual environment
* Playwright
* Occasional use of AI coding assistants for guidance

---

## Author

**Ruhani Bhatia**

```
