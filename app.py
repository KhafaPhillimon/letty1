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

}

# ── Authorised users (Production: use Environment Variables) ────────────────
ADMIN_USER = os.getenv("DASH_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("DASH_ADMIN_PASSWORD", "peo2026")

USERS = {
    ADMIN_USER: ADMIN_PASS,
    "analyst":  os.getenv("DASH_ANALYST_PASSWORD", "peo-analyst-123"),
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

# Render/Production: Set SECRET_KEY in environment variables for session stability
app.server.secret_key = os.getenv("SECRET_KEY", "peo-analytics-premium-secret-key")
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

# ═══════════════════════════════════════════════════════════════════════════════
#  LOGIN SYSTEM
# ═══════════════════════════════════════════════════════════════════════════════

login_layout = html.Div(
    style={
        "height": "100vh", "display": "flex", "alignItems": "center", "justifyContent": "center",
        "background": "radial-gradient(circle at top right, #1e293b, #0f172a)", "color": "white", "fontFamily": "'Inter', sans-serif"
    },
    children=[
        html.Div(
            style={
                "background": "rgba(30, 41, 59, 0.7)", "padding": "3rem", "borderRadius": "2rem",
                "width": "100%", "maxWidth": "450px", "backdropFilter": "blur(20px)",
                "border": "1px solid rgba(255, 255, 255, 0.1)", "boxShadow": "0 25px 50px -12px rgba(0, 0, 0, 0.5)"
            },
            className="animate-fade-in",
            children=[
                html.Div(style={"textAlign": "center", "marginBottom": "2.5rem"}, children=[
                    html.Div(className="logo-icon", children=[html.I(className="fa-solid fa-lock", style={"fontSize": "32px", "color": COLORS["primary"]})], style={"margin": "0 auto 1rem"}),
                    html.H2("PEO ANALYTICS", style={"fontSize": "1.75rem", "fontWeight": "800", "letterSpacing": "-0.04em", "margin": "0"}),
                    html.P("Enterprise Intelligence Portal", style={"color": COLORS["muted"], "fontSize": "0.75rem", "marginTop": "0.5rem", "textTransform": "uppercase", "letterSpacing": "0.1em"})
                ]),
                
                html.Div(style={"marginBottom": "1.5rem"}, children=[
                    html.Label("Access ID", style={"display": "block", "fontSize": "0.7rem", "fontWeight": "700", "color": COLORS["muted"], "marginBottom": "0.5rem", "textTransform": "uppercase"}),
                    dcc.Input(id="login-username", type="text", placeholder="Enter username", style={"width": "100%", "padding": "12px", "borderRadius": "0.75rem", "border": "1px solid rgba(255,255,255,0.1)", "background": "rgba(0,0,0,0.2)", "color": "white", "outline": "none"}),
                ]),
                
                html.Div(style={"marginBottom": "2rem"}, children=[
                    html.Label("Security Key", style={"display": "block", "fontSize": "0.7rem", "fontWeight": "700", "color": COLORS["muted"], "marginBottom": "0.5rem", "textTransform": "uppercase"}),
                    dcc.Input(id="login-password", type="password", placeholder="••••••••", style={"width": "100%", "padding": "12px", "borderRadius": "0.75rem", "border": "1px solid rgba(255,255,255,0.1)", "background": "rgba(0,0,0,0.2)", "color": "white", "outline": "none"}),
                ]),
                
                html.Div(id="login-error", style={"color": COLORS["danger"], "fontSize": "0.8rem", "marginBottom": "1.5rem", "textAlign": "center", "minHeight": "1rem"}),
                
                html.Button(
                    "INITIALIZE PORTAL", 
                    id="login-btn", 
                    n_clicks=0, 
                    style={
                        "width": "100%", "padding": "1rem", "background": COLORS["primary"], "color": "white", 
                        "border": "none", "borderRadius": "0.75rem", "fontSize": "0.875rem", "fontWeight": "700", 
                        "cursor": "pointer", "transition": "transform 0.2s"
                    }
                ),
            ]
        )
    ]
)

def dashboard_layout_wrapper(pathname):
    return html.Div(
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
                                    className=f"nav-link {'active' if pathname == item['href'] else ''}",
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
                                               [{"label": c, "value": c} for c in sorted(df_master["country"].unique())] if not df_master.empty else [],
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
                                        start_date=df_master["date"].min() if not df_master.empty else None,
                                        end_date=df_master["date"].max() if not df_master.empty else None,
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
                            ),
                            # Logout Button
                            html.Div(style={"marginTop": "2rem"}, children=[
                                html.Button([html.I(className="fa-solid fa-right-from-bracket"), " Sign Out"], id="logout-btn", n_clicks=0, className="nav-link", style={"width": "100%", "textAlign": "left", "border": "none", "background": "transparent", "cursor": "pointer"})
                            ])
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
                    # Page Container
                    html.Div(dash.page_container, className="animate-fade-in"),
                    # Shared Store for Filters
                    dcc.Store(id="filter-store", data={
                        "country": "all",
                        "date_start": df_master["date"].min().isoformat() if not df_master.empty else None,
                        "date_end": df_master["date"].max().isoformat() if not df_master.empty else None,
                        "request_type": "all"
                    })
                ]
            )
        ]
    )

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="session-store", storage_type="local"),
    html.Div(id="page-content")
])

# ─────────────────────────────────────────────────────────────────────────────
# Callbacks
# ─────────────────────────────────────────────────────────────────────────────

    }

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    Input("session-store", "data")
)
def display_page(pathname, session):
    if session and session.get("logged_in"):
        return dashboard_layout_wrapper(pathname)
    return login_layout

@app.callback(
    Output("session-store", "data"),
    Output("login-error", "children"),
    Output("url", "pathname", allow_duplicate=True),
    Input("login-btn", "n_clicks"),
    State("login-username", "value"),
    State("login-password", "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if not n_clicks:
        return dash.no_update, "", dash.no_update
    
    if not username or not password:
        return dash.no_update, "Credentials required.", dash.no_update
    
    u = username.strip().lower()
    p = password.strip()
    
    if u in USERS and USERS[u] == p:
        return {"logged_in": True, "user": u}, "", "/"
    
    return dash.no_update, "Invalid access credentials.", dash.no_update

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

@app.callback(
    Output("session-store", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    if n_clicks and n_clicks > 0:
        return {"logged_in": False}, "/"
    return dash.no_update, dash.no_update

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

    app.run(debug=False, host="0.0.0.0", port=8050)
