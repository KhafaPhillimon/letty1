# -*- coding: utf-8 -*-
"""
analyse_logs.py
---------------
Comprehensive analysis of IIS-format web server logs.
Produces:
  - Summary statistics (console + CSV)
  - Bar charts, Pie charts, Scatter plots
  - Saved to an 'output/' folder
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

# ── Output folder ─────────────────────────────────────────────────────────────
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Colour palette (professional / consistent) ────────────────────────────────
PALETTE = [
    "#2563EB", "#7C3AED", "#059669", "#D97706", "#DC2626",
    "#0891B2", "#65A30D", "#9333EA", "#EA580C", "#0F766E",
    "#B45309", "#BE185D",
]
BG      = "#0F172A"   # dark navy background
FG      = "#F1F5F9"   # light foreground text
ACCENT  = "#2563EB"   # primary accent blue
GRID_C  = "#1E293B"   # subtle grid lines

def apply_dark_style(fig, ax=None, axes=None):
    """Apply consistent dark theme to a figure / axes."""
    fig.patch.set_facecolor(BG)
    targets = [ax] if ax else (axes if axes else [])
    for a in targets:
        if a is None:
            continue
        a.set_facecolor(BG)
        a.tick_params(colors=FG, labelsize=9)
        a.xaxis.label.set_color(FG)
        a.yaxis.label.set_color(FG)
        a.title.set_color(FG)
        for spine in a.spines.values():
            spine.set_edgecolor(GRID_C)
        a.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  [saved] {path}")

# ═══════════════════════════════════════════════════════════════════════════════
# 1. LOAD DATA
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== Loading data ===")
df = pd.read_csv("web_server_logs.csv", parse_dates=["date"])
df["datetime"] = pd.to_datetime(df["date"].astype(str) + " " + df["time"])
df["month"]    = df["datetime"].dt.month
df["hour"]     = df["datetime"].dt.hour
df["month_name"] = df["datetime"].dt.strftime("%b")

print(f"  Rows loaded : {len(df):,}")
print(f"  Date range  : {df['date'].min()} to {df['date'].max()}")
print(f"  Columns     : {list(df.columns)}")

# ── Derived category flags ────────────────────────────────────────────────────
df["is_schedule_demo"]    = df["request"].str.contains("scheduledemo",  case=False)
df["is_ai_assistant"]     = df["request"].str.contains("ai-assistant",  case=False)
df["is_job"]              = df["request"].str.contains("jobs",           case=False)
df["is_event"]            = df["request"].str.contains("event",          case=False)
df["is_prototype"]        = df["request"].str.contains("prototype",      case=False)
df["is_successful"]       = df["status_code"] == 200
df["is_error"]            = df["status_code"].isin([404, 500])

# ═══════════════════════════════════════════════════════════════════════════════
# 2. SUMMARY STATISTICS (CONSOLE)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== Summary Statistics ===")

total    = len(df)
success  = df["is_successful"].sum()
errors   = df["is_error"].sum()
demos    = df["is_schedule_demo"].sum()
ai_req   = df["is_ai_assistant"].sum()
jobs     = df["is_job"].sum()
events   = df["is_event"].sum()

print(f"  Total Requests         : {total:,}")
print(f"  Successful (200)       : {success:,}  ({success/total*100:.1f}%)")
print(f"  Errors (404/500)       : {errors:,}   ({errors/total*100:.1f}%)")
print(f"  Schedule Demo Requests : {demos:,}")
print(f"  AI Virtual Asst. Req.  : {ai_req:,}")
print(f"  Jobs Page Requests     : {jobs:,}")
print(f"  Events Page Requests   : {events:,}")

bytes_desc = df["bytes_sent"].describe()
print(f"\n  Bytes Sent Statistics:")
print(f"    Mean   : {bytes_desc['mean']:,.0f} bytes")
print(f"    Std Dev: {bytes_desc['std']:,.0f} bytes")
print(f"    Min    : {bytes_desc['min']:,.0f} bytes")
print(f"    Max    : {bytes_desc['max']:,.0f} bytes")

# Save summary to CSV
summary_df = pd.DataFrame({
    "Metric": [
        "Total Requests", "Successful (200)", "Errors (404/500)",
        "Schedule Demo Requests", "AI Virtual Asst. Requests",
        "Jobs Page Requests", "Events Page Requests",
        "Avg Bytes Sent", "Std Dev Bytes Sent"
    ],
    "Value": [
        total, success, errors, demos, ai_req, jobs, events,
        round(bytes_desc["mean"], 2), round(bytes_desc["std"], 2)
    ]
})
summary_df.to_csv(os.path.join(OUTPUT_DIR, "summary_statistics.csv"), index=False)
print("\n  [saved] output/summary_statistics.csv")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. CHART 1 — Requests by Country (Horizontal Bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== Chart 1: Requests by Country ===")

country_counts = df["country"].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(10, 6))
apply_dark_style(fig, ax=ax)

bars = ax.barh(country_counts.index, country_counts.values,
               color=PALETTE[:len(country_counts)], edgecolor="none", height=0.6)

for bar, val in zip(bars, country_counts.values):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2,
            str(val), va="center", ha="left", color=FG, fontsize=9)

ax.set_xlabel("Number of Requests", color=FG)
ax.set_title("Web Server Requests by Country", color=FG, fontsize=14, fontweight="bold", pad=14)
ax.grid(axis="x", color=GRID_C, linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart1_requests_by_country.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. CHART 2 — Page Types Requested (Bar Chart)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 2: Requests by Page Type ===")

page_counts = df["page_label"].value_counts()
fig, ax = plt.subplots(figsize=(11, 5))
apply_dark_style(fig, ax=ax)

x = range(len(page_counts))
bars = ax.bar(x, page_counts.values,
              color=[PALETTE[i % len(PALETTE)] for i in x],
              edgecolor="none", width=0.6)

for bar, val in zip(bars, page_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            str(val), ha="center", va="bottom", color=FG, fontsize=9)

ax.set_xticks(list(x))
ax.set_xticklabels(page_counts.index, rotation=30, ha="right", color=FG, fontsize=9)
ax.set_ylabel("Number of Requests", color=FG)
ax.set_title("Requests by Page / Resource Type", color=FG, fontsize=14, fontweight="bold", pad=14)
ax.grid(axis="y", color=GRID_C, linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart2_requests_by_page_type.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. CHART 3 — HTTP Status Code Distribution (Pie Chart)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 3: HTTP Status Code Distribution ===")

status_counts = df["status_code"].value_counts()
fig, ax = plt.subplots(figsize=(7, 7))
apply_dark_style(fig, ax=ax)

wedge_colors = ["#059669", "#2563EB", "#D97706", "#DC2626", "#7C3AED"]
wedges, texts, autotexts = ax.pie(
    status_counts.values,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=wedge_colors[:len(status_counts)],
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    pctdistance=0.75,
)
for t in texts:
    t.set_color(FG); t.set_fontsize(11)
for a in autotexts:
    a.set_color(FG); a.set_fontsize(10); a.set_fontweight("bold")

ax.set_title("HTTP Status Code Distribution", color=FG, fontsize=14, fontweight="bold", pad=18)
fig.tight_layout()
save(fig, "chart3_status_code_pie.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. CHART 4 — Key Feature Requests Comparison (Bar Chart)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 4: Key Feature Requests ===")

features = {
    "Schedule Demo": demos,
    "AI Virtual\nAssistant": ai_req,
    "Jobs Placed": jobs,
    "Events": events,
    "Prototype": df["is_prototype"].sum(),
}

fig, ax = plt.subplots(figsize=(9, 5))
apply_dark_style(fig, ax=ax)

feat_colors = ["#2563EB", "#7C3AED", "#059669", "#D97706", "#EA580C"]
bars = ax.bar(features.keys(), features.values(),
              color=feat_colors, edgecolor="none", width=0.55)

for bar, val in zip(bars, features.values()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            str(val), ha="center", va="bottom", color=FG, fontsize=11, fontweight="bold")

ax.set_ylabel("Number of Requests", color=FG)
ax.set_title("Key Feature Page Requests", color=FG, fontsize=14, fontweight="bold", pad=14)
ax.grid(axis="y", color=GRID_C, linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart4_key_feature_requests.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. CHART 5 — Monthly Request Trend (Line + Area)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 5: Monthly Request Trend ===")

monthly = df.groupby("month").size().reset_index(name="requests")
month_labels = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
monthly["label"] = monthly["month"].apply(lambda m: month_labels[m-1])

fig, ax = plt.subplots(figsize=(11, 5))
apply_dark_style(fig, ax=ax)

ax.fill_between(monthly["month"], monthly["requests"],
                alpha=0.25, color=ACCENT)
ax.plot(monthly["month"], monthly["requests"],
        color=ACCENT, linewidth=2.5, marker="o",
        markerfacecolor=FG, markeredgecolor=ACCENT, markersize=7)

for _, row in monthly.iterrows():
    ax.text(row["month"], row["requests"] + 0.5, str(int(row["requests"])),
            ha="center", va="bottom", color=FG, fontsize=9)

ax.set_xticks(monthly["month"])
ax.set_xticklabels(monthly["label"], color=FG)
ax.set_ylabel("Total Requests", color=FG)
ax.set_title("Monthly Web Server Request Volume (2025)", color=FG, fontsize=14, fontweight="bold", pad=14)
ax.grid(color=GRID_C, linewidth=0.5)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart5_monthly_trend.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. CHART 6 — Hourly Traffic Distribution (Bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 6: Hourly Traffic Distribution ===")

hourly = df.groupby("hour").size().reset_index(name="requests")

fig, ax = plt.subplots(figsize=(12, 5))
apply_dark_style(fig, ax=ax)

bar_colors = [PALETTE[1] if h in range(9, 18) else PALETTE[0]
              for h in hourly["hour"]]
bars = ax.bar(hourly["hour"], hourly["requests"],
              color=bar_colors, edgecolor="none", width=0.7)

ax.set_xticks(range(0, 24))
ax.set_xticklabels([f"{h:02d}:00" for h in range(24)],
                   rotation=45, ha="right", color=FG, fontsize=8)
ax.set_ylabel("Requests", color=FG)
ax.set_title("Hourly Traffic Distribution", color=FG, fontsize=14, fontweight="bold", pad=14)
ax.grid(axis="y", color=GRID_C, linewidth=0.6)
ax.set_axisbelow(True)

patch_biz  = mpatches.Patch(color=PALETTE[1], label="Business Hours (09:00–17:00)")
patch_off  = mpatches.Patch(color=PALETTE[0], label="Off-Hours")
ax.legend(handles=[patch_biz, patch_off], facecolor=GRID_C,
          labelcolor=FG, fontsize=9, loc="upper left")
fig.tight_layout()
save(fig, "chart6_hourly_traffic.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. CHART 7 — Scatter: Bytes Sent vs Hour (coloured by Status)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 7: Scatter — Bytes Sent vs Hour ===")

scatter_df = df[df["bytes_sent"] > 0].copy()
status_color_map = {200: "#059669", 304: "#2563EB", 301: "#D97706",
                    404: "#DC2626", 500: "#7C3AED"}
colors_sc = scatter_df["status_code"].map(status_color_map).fillna("#94A3B8")

fig, ax = plt.subplots(figsize=(11, 6))
apply_dark_style(fig, ax=ax)

ax.scatter(scatter_df["hour"], scatter_df["bytes_sent"],
           c=colors_sc, alpha=0.6, s=22, edgecolors="none")

# Trend line
z = np.polyfit(scatter_df["hour"], scatter_df["bytes_sent"], 1)
p = np.poly1d(z)
xline = np.linspace(0, 23, 100)
ax.plot(xline, p(xline), color="#F59E0B", linewidth=1.8,
        linestyle="--", label="Trend Line")

ax.set_xlabel("Hour of Day", color=FG)
ax.set_ylabel("Bytes Sent", color=FG)
ax.set_title("Bytes Sent vs Hour of Day (by HTTP Status)", color=FG,
             fontsize=14, fontweight="bold", pad=14)
ax.set_xticks(range(0, 24))
ax.yaxis.set_major_formatter(
    mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
)

legend_patches = [mpatches.Patch(color=v, label=f"HTTP {k}")
                  for k, v in status_color_map.items()]
legend_patches.append(plt.Line2D([0], [0], color="#F59E0B",
                                  linestyle="--", label="Trend Line"))
ax.legend(handles=legend_patches, facecolor=GRID_C, labelcolor=FG,
          fontsize=9, loc="upper right")
ax.grid(color=GRID_C, linewidth=0.5)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart7_scatter_bytes_vs_hour.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 10. CHART 8 — Country × Feature Heatmap
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 8: Country x Feature Heatmap ===")

feature_cols = {
    "Schedule Demo":   "is_schedule_demo",
    "AI Assistant":    "is_ai_assistant",
    "Jobs":            "is_job",
    "Events":          "is_event",
    "Prototype":       "is_prototype",
}

heatmap_data = pd.DataFrame(
    {name: df.groupby("country")[col].sum()
     for name, col in feature_cols.items()}
).fillna(0)

fig, ax = plt.subplots(figsize=(10, 7))
apply_dark_style(fig, ax=ax)

im = ax.imshow(heatmap_data.values, cmap="Blues", aspect="auto")

ax.set_xticks(range(len(heatmap_data.columns)))
ax.set_xticklabels(heatmap_data.columns, color=FG, fontsize=10)
ax.set_yticks(range(len(heatmap_data.index)))
ax.set_yticklabels(heatmap_data.index, color=FG, fontsize=9)

for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = int(heatmap_data.values[i, j])
        txt_color = "white" if val > heatmap_data.values.max() * 0.5 else FG
        ax.text(j, i, str(val), ha="center", va="center",
                color=txt_color, fontsize=10, fontweight="bold")

cbar = fig.colorbar(im, ax=ax, pad=0.02)
cbar.ax.tick_params(colors=FG, labelsize=8)
cbar.ax.yaxis.label.set_color(FG)

ax.set_title("Feature Requests Heatmap by Country", color=FG,
             fontsize=14, fontweight="bold", pad=14)
fig.tight_layout()
save(fig, "chart8_heatmap_country_feature.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 11. CHART 9 — Referrer Source Pie Chart
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 9: Referrer Source Distribution ===")

ref_clean = df["referer"].replace("-", "Direct / None")
ref_counts = ref_clean.value_counts()

fig, ax = plt.subplots(figsize=(7, 7))
apply_dark_style(fig, ax=ax)

wedges, texts, autotexts = ax.pie(
    ref_counts.values,
    labels=ref_counts.index,
    autopct="%1.1f%%",
    startangle=100,
    colors=PALETTE[:len(ref_counts)],
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    pctdistance=0.78,
)
for t in texts:
    t.set_color(FG); t.set_fontsize(10)
for a in autotexts:
    a.set_color(FG); a.set_fontsize(9); a.set_fontweight("bold")

ax.set_title("Traffic Referrer Sources", color=FG, fontsize=14, fontweight="bold", pad=18)
fig.tight_layout()
save(fig, "chart9_referrer_pie.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 12. CHART 10 — Top Countries for Schedule Demo Requests (Bar)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 10: Top Countries for Schedule Demo ===")

demo_by_country = (df[df["is_schedule_demo"]]
                   .groupby("country").size()
                   .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(9, 5))
apply_dark_style(fig, ax=ax)

bars = ax.bar(demo_by_country.index, demo_by_country.values,
              color=PALETTE[:len(demo_by_country)], edgecolor="none", width=0.6)

for bar, val in zip(bars, demo_by_country.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            str(val), ha="center", va="bottom", color=FG, fontsize=10, fontweight="bold")

ax.set_xlabel("Country", color=FG)
ax.set_ylabel("Demo Requests", color=FG)
ax.set_title("Schedule Demo Requests by Country", color=FG, fontsize=14,
             fontweight="bold", pad=14)
ax.set_xticklabels(demo_by_country.index, rotation=30, ha="right", color=FG, fontsize=9)
ax.grid(axis="y", color=GRID_C, linewidth=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart10_demo_requests_by_country.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 13. CHART 11 — Stacked Bar: Monthly Feature Requests
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 11: Monthly Feature Requests (Stacked Bar) ===")

monthly_feat = df.groupby("month")[
    ["is_schedule_demo","is_ai_assistant","is_job","is_event","is_prototype"]
].sum().reset_index()

feat_labels = ["Schedule Demo", "AI Assistant", "Jobs", "Events", "Prototype"]
feat_keys   = ["is_schedule_demo","is_ai_assistant","is_job","is_event","is_prototype"]
feat_clrs   = ["#2563EB","#7C3AED","#059669","#D97706","#EA580C"]

fig, ax = plt.subplots(figsize=(12, 6))
apply_dark_style(fig, ax=ax)

bottoms = np.zeros(len(monthly_feat))
for label, key, clr in zip(feat_labels, feat_keys, feat_clrs):
    vals = monthly_feat[key].values.astype(float)
    ax.bar(monthly_feat["month"], vals, bottom=bottoms,
           label=label, color=clr, edgecolor="none", width=0.7)
    bottoms += vals

ax.set_xticks(monthly_feat["month"])
ax.set_xticklabels([month_labels[m-1] for m in monthly_feat["month"]],
                   color=FG, fontsize=9)
ax.set_ylabel("Number of Requests", color=FG)
ax.set_title("Monthly Feature Requests (Stacked)", color=FG, fontsize=14,
             fontweight="bold", pad=14)
ax.legend(facecolor=GRID_C, labelcolor=FG, fontsize=9, loc="upper right")
ax.grid(axis="y", color=GRID_C, linewidth=0.5)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "chart11_monthly_feature_stacked.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 14. CHART 12 — AI Assistant Requests by Country (Pie)
# ═══════════════════════════════════════════════════════════════════════════════
print("=== Chart 12: AI Assistant Requests by Country ===")

ai_by_country = (df[df["is_ai_assistant"]]
                 .groupby("country").size()
                 .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(8, 8))
apply_dark_style(fig, ax=ax)

wedges, texts, autotexts = ax.pie(
    ai_by_country.values,
    labels=ai_by_country.index,
    autopct="%1.1f%%",
    startangle=130,
    colors=PALETTE[:len(ai_by_country)],
    wedgeprops=dict(width=0.55, edgecolor=BG, linewidth=2),
    pctdistance=0.76,
)
for t in texts:
    t.set_color(FG); t.set_fontsize(9)
for a in autotexts:
    a.set_color(FG); a.set_fontsize(8); a.set_fontweight("bold")

ax.set_title("AI Virtual Assistant Requests by Country", color=FG,
             fontsize=14, fontweight="bold", pad=18)
fig.tight_layout()
save(fig, "chart12_ai_requests_by_country_pie.png")

# ═══════════════════════════════════════════════════════════════════════════════
# 15. FINAL SUMMARY PRINT
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*55)
print("  ANALYSIS COMPLETE")
print("="*55)
print(f"  Total charts generated : 12")
print(f"  Output folder          : {os.path.abspath(OUTPUT_DIR)}")
print(f"  Summary CSV            : output/summary_statistics.csv")
print("="*55 + "\n")
