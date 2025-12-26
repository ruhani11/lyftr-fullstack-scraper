# Design Notes

## Static vs JS Fallback
- Strategy: Attempt static HTML scraping first using httpx and BeautifulSoup.
- If static scraping fails (HTTP error, empty sections, or missing main content), fall back to Playwright-based JS rendering.
- This ensures robustness across both static and JS-heavy websites.

## Wait Strategy for JS
- [x] Network idle
- [ ] Fixed sleep
- [ ] Wait for selectors
- Details: Playwright navigates using `wait_until="networkidle"` to ensure all dynamic resources are loaded before extraction.

## Click & Scroll Strategy
- Click flows implemented: None (generic scraper; avoids site-specific logic).
- Scroll / pagination approach: Automatic vertical scrolling 3 times using `window.scrollTo` to load additional content.
- Stop conditions: Fixed scroll depth of 3 to satisfy assignment requirements.

## Section Grouping & Labels
- DOM grouped using semantic landmarks: `header`, `nav`, `main`, `section`, `footer`.
- Section `type` inferred from tag name.
- Section `label` derived from first heading (`h1–h3`) or first 5–6 words of text as fallback.

## Noise Filtering & Truncation
- Noise filtering: Relies on semantic tags; avoids modal overlays by default.
- HTML truncation: `rawHtml` limited to 1000 characters.
- `truncated` set to true whenever truncation occurs.
