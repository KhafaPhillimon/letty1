import plotly.graph_objects as go
import plotly.io as pio

# Peo Analytics Chart Theme
CHART_THEME = {
    "layout": go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif", "color": "#f8fafc"},
        margin={"t": 40, "b": 40, "l": 40, "r": 40},
        hovermode="closest",
        xaxis={
            "gridcolor": "rgba(255,255,255,0.05)",
            "linecolor": "rgba(255,255,255,0.1)",
            "showgrid": True,
            "zeroline": False,
        },
        yaxis={
            "gridcolor": "rgba(255,255,255,0.05)",
            "linecolor": "rgba(255,255,255,0.1)",
            "showgrid": True,
            "zeroline": False,
        },
        colorway=["#3b82f6", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#06b6d4"],
    )
}

# Register the template
pio.templates["peo_premium"] = go.layout.Template(CHART_THEME)
pio.templates.default = "peo_premium"
