# -*- coding: utf-8 -*-
"""
Dash Web Server Log Analysis Dashboard
---------------------------------------
Interactive dashboard for AI-Solutions web server log analysis.
Provides real-time KPIs, visualizations, and business insights.
"""

import dash
from dash import dcc, html, callback, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

APP_TITLE = "AI-Solutions Web Server Analytics"
DATA_FILE = "web_server_logs.csv"
THEME_COLOR = "#2563EB"
BG_COLOR = "#0F172A"
CARD_BG = "#1E293B"
TEXT_COLOR = "#F1F5F9"

COLOR_PALETTE = [
    "#2563EB", "#7C3AED", "#059669", "#D97706", "#DC2626",
    "#0891B2", "#65A30D", "#9333EA", "#EA580C", "#0F766E",
    "#B45309", "#BE185D"
]

# ─────────────────────────────────────────────────────────────────────────────
# Load and Process Data
# ─────────────────────────────────────────────────────────────────────────────

def load_and_process_data():
    """Load CSV and add derived columns."""
    df = pd.read_csv(DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df["datetime"] = pd.to_datetime(df["date"].astype(str) + " " + df["time"])

    # Derived columns
    df["month"] = df["datetime"].dt.month
    df["month_name"] = df["datetime"].dt.strftime("%b")
    df["hour"] = df["datetime"].dt.hour
    df["day"] = df["datetime"].dt.day

    # Feature flags
    df["is_schedule_demo"] = df["request"].str.contains("scheduledemo", case=False, na=False)
    df["is_ai_assistant"] = df["request"].str.contains("ai-assistant", case=False, na=False)
    df["is_job"] = df["request"].str.contains("jobs", case=False, na=False)
    df["is_event"] = df["request"].str.contains("event", case=False, na=False)
    df["is_prototype"] = df["request"].str.contains("prototype", case=False, na=False)
    df["is_successful"] = df["status_code"] == 200
    df["is_error"] = df["status_code"].isin([404, 500])

    return df

df = load_and_process_data()

# ─────────────────────────────────────────────────────────────────────────────
# Initialize Dash App
# ─────────────────────────────────────────────────────────────────────────────

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = APP_TITLE

# ─────────────────────────────────────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────────────────────────────────────

app.layout = html.Div(
    style={
        "backgroundColor": BG_COLOR,
        "color": TEXT_COLOR,
        "fontFamily": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
        "minHeight": "100vh",
        "padding": "20px"
    },
    children=[
        # Header with Logo
        html.Div(
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "20px",
                "marginBottom": "30px",
                "paddingBottom": "20px",
                "borderBottom": "2px solid #334155"
            },
            children=[
                # Logo (if it exists)
                html.Div(
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center"
                    },
                    children=[
                        html.Img(
                            src="/assets/logo_transparent.png" if os.path.exists("assets/logo_transparent.png") else "/assets/logo_optimized.png" if os.path.exists("assets/logo_optimized.png") else None,
                            alt="Company Logo",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "display": "block" if (os.path.exists("assets/logo_transparent.png") or os.path.exists("assets/logo_optimized.png")) else "none"
                            }
                        ) if (os.path.exists("assets/logo_transparent.png") or os.path.exists("assets/logo_optimized.png")) else None
                    ]
                ) if (os.path.exists("assets/logo_transparent.png") or os.path.exists("assets/logo_optimized.png")) else html.Div(),

                # Title and Subtitle
                html.Div(
                    children=[
                        html.H1(
                            APP_TITLE,
                            style={
                                "fontSize": "32px",
                                "fontWeight": "700",
                                "marginBottom": "5px",
                                "color": TEXT_COLOR
                            }
                        ),
                        html.P(
                            "Real-time web server activity analysis and business insights",
                            style={
                                "fontSize": "14px",
                                "color": "#94A3B8",
                                "marginBottom": "0"
                            }
                        )
                    ]
                )
            ]
        ),

        # Filters Row
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                "gap": "15px",
                "marginBottom": "30px"
            },
            children=[
                # Country Filter
                html.Div([
                    html.Label("Select Country:", style={"fontSize": "12px", "fontWeight": "600", "marginBottom": "8px", "display": "block"}),
                    dcc.Dropdown(
                        id="country-filter",
                        options=[{"label": "All Countries", "value": "all"}] +
                               [{"label": c, "value": c} for c in sorted(df["country"].unique())],
                        value="all",
                        style={"color": BG_COLOR}
                    )
                ]),

                # Date Range Filter
                html.Div([
                    html.Label("Date Range:", style={"fontSize": "12px", "fontWeight": "600", "marginBottom": "8px", "display": "block"}),
                    dcc.DatePickerRange(
                        id="date-range",
                        start_date=df["date"].min(),
                        end_date=df["date"].max(),
                        display_format="YYYY-MM-DD",
                        style={"width": "100%"}
                    )
                ]),

                # Request Type Filter
                html.Div([
                    html.Label("Request Type:", style={"fontSize": "12px", "fontWeight": "600", "marginBottom": "8px", "display": "block"}),
                    dcc.Dropdown(
                        id="request-type-filter",
                        options=[
                            {"label": "All Requests", "value": "all"},
                            {"label": "Schedule Demo", "value": "demo"},
                            {"label": "AI Assistant", "value": "ai"},
                            {"label": "Jobs", "value": "jobs"},
                            {"label": "Events", "value": "events"},
                            {"label": "Prototype", "value": "prototype"}
                        ],
                        value="all",
                        style={"color": BG_COLOR}
                    )
                ])
            ]
        ),

        # KPI Cards
        html.Div(
            id="kpi-container",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                "gap": "15px",
                "marginBottom": "30px"
            }
        ),

        # Charts Row 1
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",
                "gap": "20px",
                "marginBottom": "30px"
            },
            children=[
                dcc.Graph(id="chart-requests-by-country"),
                dcc.Graph(id="chart-status-distribution")
            ]
        ),

        # Charts Row 2
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",
                "gap": "20px",
                "marginBottom": "30px"
            },
            children=[
                dcc.Graph(id="chart-requests-by-page"),
                dcc.Graph(id="chart-feature-comparison")
            ]
        ),

        # Charts Row 3
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr",
                "gap": "20px",
                "marginBottom": "30px"
            },
            children=[
                dcc.Graph(id="chart-monthly-trend")
            ]
        ),

        # Charts Row 4
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(500px, 1fr))",
                "gap": "20px",
                "marginBottom": "30px"
            },
            children=[
                dcc.Graph(id="chart-hourly-traffic"),
                dcc.Graph(id="chart-referrer-sources")
            ]
        ),

        # Summary Table
        html.Div(
            style={
                "backgroundColor": CARD_BG,
                "borderRadius": "8px",
                "padding": "20px",
                "marginBottom": "30px"
            },
            children=[
                html.H3("Summary Statistics", style={"marginBottom": "15px", "fontSize": "18px", "fontWeight": "600"}),
                html.Div(id="summary-table")
            ]
        )
    ]
)

# ─────────────────────────────────────────────────────────────────────────────
# Callback Functions
# ─────────────────────────────────────────────────────────────────────────────

def filter_data(country, date_start, date_end, request_type):
    """Filter dataframe based on selected criteria."""
    filtered = df.copy()

    if country != "all":
        filtered = filtered[filtered["country"] == country]

    if date_start and date_end:
        filtered = filtered[
            (filtered["date"] >= date_start) & (filtered["date"] <= date_end)
        ]

    if request_type == "demo":
        filtered = filtered[filtered["is_schedule_demo"]]
    elif request_type == "ai":
        filtered = filtered[filtered["is_ai_assistant"]]
    elif request_type == "jobs":
        filtered = filtered[filtered["is_job"]]
    elif request_type == "events":
        filtered = filtered[filtered["is_event"]]
    elif request_type == "prototype":
        filtered = filtered[filtered["is_prototype"]]

    return filtered

@callback(
    [Output("kpi-container", "children"),
     Output("chart-requests-by-country", "figure"),
     Output("chart-status-distribution", "figure"),
     Output("chart-requests-by-page", "figure"),
     Output("chart-feature-comparison", "figure"),
     Output("chart-monthly-trend", "figure"),
     Output("chart-hourly-traffic", "figure"),
     Output("chart-referrer-sources", "figure"),
     Output("summary-table", "children")],
    [Input("country-filter", "value"),
     Input("date-range", "start_date"),
     Input("date-range", "end_date"),
     Input("request-type-filter", "value")]
)
def update_dashboard(country, date_start, date_end, request_type):
    """Update all dashboard components based on filters."""

    filtered_df = filter_data(country, date_start, date_end, request_type)

    if len(filtered_df) == 0:
        empty_fig = go.Figure().add_annotation(
            text="No data available for selected filters",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=TEXT_COLOR)
        )
        empty_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_COLOR, family="Inter")
        )
        return [html.P("No data available")], empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, html.P("No data available")

    # ─────────────────────────────────────────────────────────────────────────
    # KPI Cards
    # ─────────────────────────────────────────────────────────────────────────

    total_requests = len(filtered_df)
    successful = filtered_df["is_successful"].sum()
    errors = filtered_df["is_error"].sum()
    demo_requests = filtered_df["is_schedule_demo"].sum()
    success_rate = (successful / total_requests * 100) if total_requests > 0 else 0
    avg_bytes = filtered_df["bytes_sent"].mean()

    kpi_cards = [
        create_kpi_card("Total Requests", f"{total_requests:,}", "#2563EB"),
        create_kpi_card("Success Rate", f"{success_rate:.1f}%", "#059669" if success_rate > 90 else "#D97706"),
        create_kpi_card("Demo Requests", f"{demo_requests:,}", "#7C3AED"),
        create_kpi_card("Errors", f"{errors:,}", "#DC2626" if errors > 10 else "#059669"),
        create_kpi_card("Avg Bytes/Request", f"{avg_bytes:,.0f}B", "#0891B2"),
    ]

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 1: Requests by Country
    # ─────────────────────────────────────────────────────────────────────────

    country_data = filtered_df["country"].value_counts().reset_index()
    country_data.columns = ["country", "count"]

    fig_country = px.bar(
        country_data,
        y="country",
        x="count",
        orientation="h",
        title="Requests by Country",
        labels={"count": "Number of Requests", "country": "Country"},
        color="count",
        color_continuous_scale=["#7C3AED", "#2563EB", "#059669"]
    )
    fig_country.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
        hovermode="closest"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 2: HTTP Status Distribution
    # ─────────────────────────────────────────────────────────────────────────

    status_data = filtered_df["status_code"].value_counts().reset_index()
    status_data.columns = ["status_code", "count"]
    status_data["status_code"] = status_data["status_code"].astype(str)

    fig_status = px.pie(
        status_data,
        values="count",
        names="status_code",
        title="HTTP Status Code Distribution",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_status.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 3: Requests by Page Type
    # ─────────────────────────────────────────────────────────────────────────

    page_data = filtered_df["page_label"].value_counts().reset_index()
    page_data.columns = ["page_label", "count"]

    fig_page = px.bar(
        page_data,
        x="page_label",
        y="count",
        title="Requests by Page Type",
        labels={"count": "Number of Requests", "page_label": "Page"},
        color="count",
        color_continuous_scale=["#D97706", "#2563EB", "#059669"]
    )
    fig_page.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
        xaxis_tickangle=-45,
        hovermode="closest"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 4: Key Feature Comparison
    # ─────────────────────────────────────────────────────────────────────────

    features = {
        "Schedule Demo": filtered_df["is_schedule_demo"].sum(),
        "AI Assistant": filtered_df["is_ai_assistant"].sum(),
        "Jobs": filtered_df["is_job"].sum(),
        "Events": filtered_df["is_event"].sum(),
        "Prototype": filtered_df["is_prototype"].sum(),
    }

    feature_df = pd.DataFrame(list(features.items()), columns=["feature", "count"])

    fig_feature = px.bar(
        feature_df,
        x="feature",
        y="count",
        title="Key Feature Requests",
        labels={"count": "Number of Requests", "feature": "Feature"},
        color="count",
        color_continuous_scale=["#9333EA", "#7C3AED", "#2563EB", "#059669"]
    )
    fig_feature.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
        hovermode="closest"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 5: Monthly Trend
    # ─────────────────────────────────────────────────────────────────────────

    monthly_data = filtered_df.groupby("month_name").size().reset_index(name="count")
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_data["month_name"] = pd.Categorical(monthly_data["month_name"], categories=month_order, ordered=True)
    monthly_data = monthly_data.sort_values("month_name")

    fig_monthly = px.line(
        monthly_data,
        x="month_name",
        y="count",
        title="Monthly Request Volume",
        labels={"count": "Requests", "month_name": "Month"},
        markers=True,
        line_shape="spline"
    )
    fig_monthly.update_traces(line=dict(color=THEME_COLOR, width=3), marker=dict(size=8))
    fig_monthly.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
        hovermode="x unified"
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 6: Hourly Traffic
    # ─────────────────────────────────────────────────────────────────────────

    hourly_data = filtered_df.groupby("hour").size().reset_index(name="count")
    hourly_data["hour_label"] = hourly_data["hour"].apply(lambda h: f"{h:02d}:00")

    fig_hourly = px.bar(
        hourly_data,
        x="hour_label",
        y="count",
        title="Hourly Traffic Distribution",
        labels={"count": "Requests", "hour_label": "Hour"},
        color="count",
        color_continuous_scale=["#7C3AED", "#2563EB", "#059669"]
    )
    fig_hourly.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
        hovermode="closest",
        xaxis_tickangle=-45
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Chart 7: Referrer Sources
    # ─────────────────────────────────────────────────────────────────────────

    referer_clean = filtered_df["referer"].replace("-", "Direct / None")
    referer_data = referer_clean.value_counts().reset_index()
    referer_data.columns = ["referer", "count"]

    fig_referrer = px.pie(
        referer_data,
        values="count",
        names="referer",
        title="Traffic Referrer Sources",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig_referrer.update_layout(
        template="plotly_dark",
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_COLOR, family="Inter"),
    )

    # ─────────────────────────────────────────────────────────────────────────
    # Summary Table
    # ─────────────────────────────────────────────────────────────────────────

    summary_data = {
        "Total Requests": total_requests,
        "Successful (200)": successful,
        "Errors (404/500)": errors,
        "Average Response Size": f"{avg_bytes:,.0f} bytes",
        "Unique Countries": filtered_df["country"].nunique(),
        "Date Range": f"{filtered_df['date'].min().strftime('%Y-%m-%d')} to {filtered_df['date'].max().strftime('%Y-%m-%d')}"
    }

    summary_table = html.Table([
        html.Tbody([
            html.Tr([
                html.Td(k, style={"padding": "10px", "borderBottom": "1px solid #334155", "fontWeight": "600"}),
                html.Td(str(v), style={"padding": "10px", "borderBottom": "1px solid #334155", "color": "#E2E8F0"})
            ])
            for k, v in summary_data.items()
        ])
    ], style={"width": "100%", "borderCollapse": "collapse"})

    return kpi_cards, fig_country, fig_status, fig_page, fig_feature, fig_monthly, fig_hourly, fig_referrer, summary_table

def create_kpi_card(title, value, color):
    """Create a KPI card component."""
    return html.Div(
        style={
            "backgroundColor": CARD_BG,
            "borderRadius": "8px",
            "padding": "20px",
            "borderLeft": f"4px solid {color}",
            "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.3)"
        },
        children=[
            html.P(
                title,
                style={
                    "fontSize": "12px",
                    "fontWeight": "600",
                    "color": "#94A3B8",
                    "marginBottom": "8px",
                    "textTransform": "uppercase",
                    "letterSpacing": "0.5px"
                }
            ),
            html.H3(
                value,
                style={
                    "fontSize": "28px",
                    "fontWeight": "700",
                    "color": color,
                    "marginTop": "0"
                }
            )
        ]
    )

# ─────────────────────────────────────────────────────────────────────────────
# Run Server
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Starting {APP_TITLE}")
    print(f"{'='*60}")
    print(f"  Data loaded: {len(df)} records")
    print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"\n  Dashboard available at: http://127.0.0.1:8050")
    print(f"{'='*60}\n")

    app.run(debug=True, host="127.0.0.1", port=8050)
