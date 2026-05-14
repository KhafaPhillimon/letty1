# -*- coding: utf-8 -*-
"""
Peo Analytics - Professional Web Server Dashboard
Multi-Page Dash Application with Premium Design
"""

import dash
from dash import dcc, html, callback, Input, Output
import pandas as pd
import os

# ─────────────────────────────────────────────────────────────────────────────
# Application Configuration & Constants
# ─────────────────────────────────────────────────────────────────────────────

# Branding & Identity
APP_NAME = "Peo Analytics"
APP_VERSION = "2.4.0-pro"
DATA_SOURCE = "web_server_logs.csv"

# Design Tokens (Synced with assets/style.css)
COLORS = {
    "primary": "#3b82f6",
    "secondary": "#8b5cf6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "text": "#f8fafc",
    "muted": "#94a3b8"
}
# ─────────────────────────────────────────────────────────────────────────────

def load_and_process_data():
    """
    Main data ingestion pipeline. Loads raw logs and generates 
    synthetic features for granular dashboard analysis.
    """
    if not os.path.exists(DATA_SOURCE):
        print(f"[Critical] Data source missing: {DATA_SOURCE}")
        return pd.DataFrame()
    
    # Ingesting raw server logs
    raw_logs = pd.read_csv(DATA_SOURCE)
    
    # Temporal normalization
    raw_logs["date"] = pd.to_datetime(raw_logs["date"])
    raw_logs["datetime"] = pd.to_datetime(raw_logs["date"].astype(str) + " " + raw_logs["time"])

    # Feature Engineering
    processed = raw_logs.copy()
    processed["month"] = processed["datetime"].dt.month
    processed["month_name"] = processed["datetime"].dt.strftime("%b")
    processed["hour"] = processed["datetime"].dt.hour
    processed["day_of_week"] = processed["datetime"].dt.day_name()

    # Domain-specific logic flags
    # We identify requests based on endpoint signatures
    processed["is_demo"] = processed["request"].str.contains("scheduledemo", case=False, na=False)
    processed["is_ai_service"] = processed["request"].str.contains("ai-assistant", case=False, na=False)
    processed["is_career"] = processed["request"].str.contains("jobs", case=False, na=False)
    processed["is_event_hub"] = processed["request"].str.contains("event", case=False, na=False)
    processed["is_prototype_v1"] = processed["request"].str.contains("prototype", case=False, na=False)
    
    # Status code classifications
    processed["is_healthy"] = processed["status_code"] == 200
    processed["is_incident"] = processed["status_code"].isin([404, 500])

    return processed

df_master = load_and_process_data()

# ─────────────────────────────────────────────────────────────────────────────
# App Initialization
# ─────────────────────────────────────────────────────────────────────────────

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    pages_folder="pages",
    use_pages=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ]
)

server = app.server


app.title = APP_NAME

# Navigation Items
nav_items = [
    {"name": "Overview", "icon": "fa-solid fa-house", "href": "/"},
    {"name": "Country Insights", "icon": "fa-solid fa-globe", "href": "/requests-by-country"},
    {"name": "Page Analytics", "icon": "fa-solid fa-file-lines", "href": "/requests-by-page"},
    {"name": "System Health", "icon": "fa-solid fa-server", "href": "/http-status"},
    {"name": "Feature Usage", "icon": "fa-solid fa-star", "href": "/feature-comparison"},
    {"name": "Time Analysis", "icon": "fa-solid fa-clock", "href": "/hourly-traffic"},
    {"name": "Monthly Trends", "icon": "fa-solid fa-chart-line", "href": "/monthly-trends"},
    {"name": "Heatmaps", "icon": "fa-solid fa-fire", "href": "/heatmap-country-feature"},
    {"name": "Referrers", "icon": "fa-solid fa-link", "href": "/referrer-sources"},
    {"name": "Demo Funnel", "icon": "fa-solid fa-video", "href": "/demo-requests-by-country"},
    {"name": "AI Intelligence", "icon": "fa-solid fa-robot", "href": "/ai-requests-by-country"},
    {"name": "Raw Logs", "icon": "fa-solid fa-list", "href": "/logs"},
]

app.layout = html.Div(
    className="animate-fade-in",
    children=[
        # Sidebar
        html.Div(
            className="sidebar",
            children=[
                html.Div(
                    className="logo-container",
                    children=[
                        html.Div(className="logo-icon", children=[html.I(className="fa-solid fa-chart-pie", style={"fontSize": "24px", "color": "#3b82f6"})]),
                        html.Span("PEO ANALYTICS", className="logo-text")
                    ]
                ),

                # Navigation
                html.Div(
                    children=[
                        dcc.Link(
                            html.Div(
                                id={"type": "nav-link", "index": item["href"]},
                                className="nav-link",
                                children=[
                                    html.I(className=f"nav-icon {item['icon']}"),
                                    html.Span(item["name"])
                                ]
                            ),
                            href=item["href"]
                        ) for item in nav_items
                    ]
                ),

                # Filters Section
                html.Div(
                    className="filters-panel",
                    children=[
                        html.Span("Analysis Filters", className="filter-label", style={"marginBottom": "16px"}),
                        
                        html.Div(
                            className="filter-group",
                            children=[
                                html.Label("Active Markets", className="filter-label"),
                                dcc.Dropdown(
                                    id="sidebar-country-filter",
                                    options=[{"label": "Global Overview", "value": "all"}] +
                                           [{"label": c, "value": c} for c in sorted(df_master["country"].unique())],
                                    value="all",
                                    clearable=False,
                                    searchable=True
                                )
                            ]
                        ),

                        html.Div(
                            className="filter-group",
                            children=[
                                html.Label("Date Range", className="filter-label"),
                                dcc.DatePickerRange(
                                    id="sidebar-date-range",
                                    start_date=df_master["date"].min(),
                                    end_date=df_master["date"].max(),
                                    display_format="MMM DD, YYYY",
                                )
                            ]
                        ),

                        html.Div(
                            className="filter-group",
                            children=[
                                html.Label("Request Category", className="filter-label"),
                                dcc.Dropdown(
                                    id="sidebar-request-type-filter",
                                    options=[
                                        {"label": "All Traffic", "value": "all"},
                                        {"label": "Demos", "value": "demo"},
                                        {"label": "AI Assistant", "value": "ai"},
                                        {"label": "Job Inquiries", "value": "jobs"},
                                        {"label": "Event Traffic", "value": "events"}
                                    ],
                                    value="all",
                                    clearable=False
                                )
                            ]
                        )
                    ]
                )
            ]
        ),

        # Main Content
        html.Div(
            className="main-content",
            children=[
                # Header
                html.Div(
                    className="header",
                    children=[
                        html.H1("Performance Overview", id="page-title", className="header-title"),
                        html.Div(
                            style={"display": "flex", "gap": "12px"},
                            children=[
                                html.Button(children=[html.I(className="fa-solid fa-download"), " Export"], className="nav-link", style={"border": "1px solid var(--card-border)", "cursor": "pointer", "backgroundColor": "transparent"}),
                                html.Button(children=[html.I(className="fa-solid fa-arrows-rotate")], className="nav-link", style={"border": "1px solid var(--card-border)", "cursor": "pointer", "backgroundColor": "transparent"})
                            ]
                        )
                    ]
                ),

                # Summary Cards Row
                html.Div(
                    className="dashboard-grid",
                    style={"marginBottom": "32px"},
                    children=[
                        html.Div(
                            className="summary-card",
                            children=[
                                html.Div([
                                    html.Span("Total Requests", className="summary-label"),
                                    html.H3(f"{len(df_master):,}", className="summary-value"),
                                    html.Div([
                                        html.I(className="fa-solid fa-arrow-up trend-up"),
                                        html.Span("12% vs last period", className="trend-up")
                                    ], className="summary-trend")
                                ])
                            ]
                        ),
                        html.Div(
                            className="summary-card",
                            children=[
                                html.Div([
                                    html.Span("Success Rate", className="summary-label"),
                                    html.H3(f"{(df_master['is_healthy'].mean()*100):.1f}%", className="summary-value"),
                                    html.Div([
                                        html.I(className="fa-solid fa-arrow-up trend-up"),
                                        html.Span("0.5% improvement", className="trend-up")
                                    ], className="summary-trend")
                                ])
                            ]
                        ),
                        html.Div(
                            className="summary-card",
                            children=[
                                html.Div([
                                    html.Span("Total Bandwidth", className="summary-label"),
                                    html.H3(f"{(df_master['bytes_sent'].sum() / 1e6):.1f} MB", className="summary-value"),
                                    html.Div([
                                        html.I(className="fa-solid fa-arrow-down trend-down"),
                                        html.Span("4% optimization", className="trend-down")
                                    ], className="summary-trend")
                                ])
                            ]
                        ),
                        html.Div(
                            className="summary-card",
                            children=[
                                html.Div([
                                    html.Span("Global Presence", className="summary-label"),
                                    html.H3(f"{df_master['country'].nunique()}", className="summary-value"),
                                    html.Div([
                                        html.I(className="fa-solid fa-earth-africa", style={"color": "var(--accent-primary)"}),
                                        html.Span("Active markets", style={"color": "var(--text-muted)", "marginLeft": "4px"})
                                    ], className="summary-trend")
                                ])
                            ]
                        ),
                    ]
                ),

                # Page Container
                html.Div(dash.page_container, className="animate-fade-in"),

                # Shared Store for Filters
                dcc.Store(id="filter-store", data={
                    "country": "all",
                    "date_start": df_master["date"].min().isoformat(),
                    "date_end": df_master["date"].max().isoformat(),
                    "request_type": "all"
                })
            ]
        )
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# Callbacks
# ─────────────────────────────────────────────────────────────────────────────

@app.callback(
    Output("filter-store", "data"),
    [Input("sidebar-country-filter", "value"),
     Input("sidebar-date-range", "start_date"),
     Input("sidebar-date-range", "end_date"),
     Input("sidebar-request-type-filter", "value")]
)
def update_filters(country, date_start, date_end, request_type):
    return {
        "country": country,
        "date_start": date_start,
        "date_end": date_end,
        "request_type": request_type
    }

# ─────────────────────────────────────────────────────────────────────────────
# Run Server
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Starting {APP_NAME}")
    print(f"{'='*60}")
    print(f"  Data loaded: {len(df_master)} records")
    print(f"  Dashboard available at: http://127.0.0.1:8050")
    print(f"{'='*60}\n")

    app.run(debug=True, host="127.0.0.1", port=8050)
