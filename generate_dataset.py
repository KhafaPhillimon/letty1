"""
generate_dataset.py
-------------------
Generates a synthetic IIS-format web server log dataset (500 rows)
and saves it as web_server_logs.csv
"""

import csv
import random
from datetime import datetime, timedelta

# ── Configuration ────────────────────────────────────────────────────────────

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

NUM_RECORDS = 500
START_DATE  = datetime(2025, 1, 1)
END_DATE    = datetime(2025, 12, 31)

# Pages / endpoints that represent the company's software-solution marketing site
PAGES = {
    "/index.html":              ("Homepage",              0.20),
    "/products.html":           ("Products",              0.12),
    "/scheduledemo.php":        ("Schedule Demo",         0.10),
    "/events.php":              ("Events",                0.08),
    "/images/events.jpg":       ("Event Image",           0.06),
    "/prototype.php":           ("Prototype",             0.07),
    "/ai-assistant.php":        ("AI Virtual Assistant",  0.10),
    "/jobs.php":                ("Jobs Placed",           0.09),
    "/contact.php":             ("Contact",               0.06),
    "/pricing.php":             ("Pricing",               0.05),
    "/about.html":              ("About",                 0.04),
    "/blog.html":               ("Blog",                  0.03),
}

# HTTP status codes with realistic weights
STATUS_CODES = [200, 200, 200, 200, 200, 304, 304, 404, 301, 500]

# (Country, IP-prefix, weight)
COUNTRY_DATA = [
    ("Botswana",      "196.50",  0.18),
    ("South Africa",  "41.10",   0.15),
    ("Zimbabwe",      "41.189",  0.10),
    ("Kenya",         "197.248", 0.09),
    ("Nigeria",       "105.112", 0.09),
    ("United States", "128.1",   0.08),
    ("United Kingdom","155.55",  0.07),
    ("India",         "157.20",  0.07),
    ("Germany",       "91.198",  0.06),
    ("Australia",     "203.12",  0.05),
    ("Canada",        "24.48",   0.04),
    ("France",        "90.50",   0.02),
]

HTTP_METHODS = ["GET", "GET", "GET", "POST", "POST"]

# ── Helper functions ──────────────────────────────────────────────────────────

def random_ip(prefix: str) -> str:
    return f"{prefix}.{random.randint(0,255)}.{random.randint(0,255)}"

def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

def weighted_choice(items, weights):
    """Pick one item from *items* according to *weights* (must sum to ≈1)."""
    r = random.random()
    cumulative = 0.0
    for item, w in zip(items, weights):
        cumulative += w
        if r <= cumulative:
            return item
    return items[-1]

# ── Build records ─────────────────────────────────────────────────────────────

page_urls    = list(PAGES.keys())
page_weights = [PAGES[p][1] for p in page_urls]

country_names    = [c[0] for c in COUNTRY_DATA]
country_prefixes = [c[1] for c in COUNTRY_DATA]
country_weights  = [c[2] for c in COUNTRY_DATA]

records = []
for _ in range(NUM_RECORDS):
    dt         = random_datetime(START_DATE, END_DATE)
    time_str   = dt.strftime("%H:%M:%S")
    date_str   = dt.strftime("%Y-%m-%d")

    # Country / IP
    idx     = weighted_choice(list(range(len(COUNTRY_DATA))),
                              country_weights)
    country = country_names[idx]
    ip      = random_ip(country_prefixes[idx])

    # Page
    page    = weighted_choice(page_urls, page_weights)
    label   = PAGES[page][0]

    method  = random.choice(HTTP_METHODS)
    status  = random.choice(STATUS_CODES)
    bytes_  = random.randint(512, 102400) if status != 304 else 0
    referer = random.choice(["-", "https://google.com", "https://bing.com",
                             "https://linkedin.com", "https://facebook.com"])
    user_agent = random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) Safari/605",
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537",
        "curl/7.88.1",
        "Googlebot/2.1",
    ])

    records.append({
        "date":        date_str,
        "time":        time_str,
        "ip_address":  ip,
        "country":     country,
        "method":      method,
        "request":     page,
        "page_label":  label,
        "status_code": status,
        "bytes_sent":  bytes_,
        "referer":     referer,
        "user_agent":  user_agent,
    })

# ── Write CSV ─────────────────────────────────────────────────────────────────

OUTPUT_FILE = "web_server_logs.csv"

fieldnames = ["date", "time", "ip_address", "country", "method",
              "request", "page_label", "status_code", "bytes_sent",
              "referer", "user_agent"]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)

print(f"[OK] Dataset saved -> {OUTPUT_FILE}  ({NUM_RECORDS} records)")
