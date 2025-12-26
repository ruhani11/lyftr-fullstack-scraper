import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright


# -----------------------------
# Helpers
# -----------------------------
def guess_section_type(tag_name: str) -> str:
    if tag_name == "header":
        return "hero"
    if tag_name == "nav":
        return "nav"
    if tag_name == "footer":
        return "footer"
    if tag_name in ("section", "main"):
        return "section"
    return "unknown"


def extract_section_content(tag, base_url):
    headings = [h.get_text(strip=True) for h in tag.find_all(["h1", "h2", "h3"])]

    paragraphs = [p.get_text(strip=True) for p in tag.find_all("p")]
    text = " ".join(paragraphs)

    links = [
        {"text": a.get_text(strip=True), "href": urljoin(base_url, a["href"])}
        for a in tag.find_all("a", href=True)
    ]

    images = [
        {"src": urljoin(base_url, img["src"]), "alt": img.get("alt", "")}
        for img in tag.find_all("img", src=True)
    ]

    return headings, text, links, images


def parse_html(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")

    # -------- META --------
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    description = ""
    desc = soup.find("meta", attrs={"name": "description"})
    if desc and desc.get("content"):
        description = desc["content"].strip()

    language = soup.html.get("lang") if soup.html else ""

    canonical = None
    canon = soup.find("link", rel="canonical")
    if canon and canon.get("href"):
        canonical = canon["href"]

    # -------- SECTIONS --------
    sections = []
    section_tags = soup.find_all(["header", "nav", "main", "section", "footer"])

    if not section_tags and soup.body:
        section_tags = [soup.body]

    for idx, tag in enumerate(section_tags):
        headings, text, links, images = extract_section_content(tag, url)

        if not text and not headings:
            continue

        label = headings[0] if headings else " ".join(text.split()[:6])

        sections.append({
            "id": f"{tag.name}-{idx}",
            "type": guess_section_type(tag.name),
            "label": label,
            "sourceUrl": url,
            "content": {
                "headings": headings,
                "text": text,
                "links": links,
                "images": images,
                "lists": [],
                "tables": []
            },
            "rawHtml": str(tag)[:1000],
            "truncated": True
        })

    return {
        "meta": {
            "title": title,
            "description": description,
            "language": language,
            "canonical": canonical
        },
        "sections": sections
    }


# -----------------------------
# STATIC SCRAPE
# -----------------------------
def static_scrape(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    with httpx.Client(headers=headers, timeout=10, follow_redirects=True) as client:
        response = client.get(url)

    response.raise_for_status()
    return parse_html(response.text, url)


# -----------------------------
# PLAYWRIGHT SCRAPE + SCROLL
# -----------------------------
def playwright_scrape(url: str):
    interactions = {
        "clicks": [],
        "scrolls": 0,
        "pages": [url]
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="networkidle", timeout=30000)

        # ---- SCROLL 3 TIMES ----
        for _ in range(3):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            interactions["scrolls"] += 1

        html = page.content()
        browser.close()

    parsed = parse_html(html, url)
    return parsed, interactions


# -----------------------------
# MAIN ENTRY
# -----------------------------
def scrape_with_fallback(url: str):
    errors = []
    interactions = {
        "clicks": [],
        "scrolls": 0,
        "pages": [url]
    }

    try:
        parsed = static_scrape(url)
        if not parsed["sections"]:
            raise Exception("No content from static scrape")
        strategy = "static"
    except Exception as e:
        errors.append({"message": str(e), "phase": "static"})
        parsed, interactions = playwright_scrape(url)
        strategy = "playwright"

    return {
        "url": url,
        "scrapedAt": datetime.now(timezone.utc).isoformat(),
        "meta": parsed["meta"],
        "sections": parsed["sections"],
        "interactions": interactions,
        "errors": errors,
        "strategy": strategy
    }
