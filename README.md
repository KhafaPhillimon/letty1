# AI-Solutions Web Server Analytics Dashboard

A comprehensive, interactive web-based dashboard for analyzing web server logs and generating business insights for the AI-Solutions sales team.

## Overview

This Dash-based analytics platform provides:
- **Real-time KPI Metrics** - Total requests, success rates, demo requests, error tracking
- **Interactive Visualizations** - Charts, graphs, and trends that update based on filters
- **Business Intelligence** - Track demo requests, AI assistant inquiries, job placements, and events
- **Geographic Analysis** - Understand traffic patterns by country
- **Time-Series Trends** - Monitor hourly and monthly traffic patterns
- **User-Friendly Interface** - Designed for non-technical stakeholders

## Features

### KPI Cards
- **Total Requests** - Overall traffic volume
- **Success Rate** - Percentage of successful (HTTP 200) responses
- **Demo Requests** - Count of schedule demo page visits
- **Errors** - Failed requests (HTTP 404, 500)
- **Average Response Size** - Data consumption metrics

### Interactive Charts
1. **Requests by Country** - Geographic distribution of traffic
2. **HTTP Status Distribution** - Success/error breakdown (pie chart)
3. **Requests by Page Type** - Identify most visited pages
4. **Key Feature Requests** - Track demo, AI, jobs, events, prototype pages
5. **Monthly Trend** - Traffic volume trends over time
6. **Hourly Traffic Distribution** - Peak traffic patterns
7. **Referrer Sources** - Understand traffic origin (Google, Bing, LinkedIn, etc.)

### Smart Filters
- **Country Filter** - Drill down to specific geographic regions
- **Date Range** - Analyze specific time periods
- **Request Type** - Focus on specific features (Demo, AI Assistant, Jobs, etc.)

### Summary Statistics
- Quick reference table with key metrics
- Date range information
- Unique country count

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Generate Dataset (if needed)

If you don't have the web server logs dataset:

```bash
python generate_dataset.py
```

This creates `web_server_logs.csv` with 500 synthetic IIS log records.

### Step 3: Run the Dashboard

```bash
python dashboard.py
```

The dashboard will start and display:
```
============================================================
  Starting AI-Solutions Web Server Analytics
============================================================
  Data loaded: 500 records
  Date range: 2025-01-01 to 2025-12-31

  🌐 Dashboard available at: http://127.0.0.1:8050
============================================================
```

Open your browser and navigate to: **http://127.0.0.1:8050**

## Project Structure

```
Peo _dashboard/
├── dashboard.py           # Main Dash application
├── generate_dataset.py    # Synthetic data generator
├── analyse_logs.py        # Static analysis script (matplotlib)
├── web_server_logs.csv    # Web server log dataset
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── output/               # Static charts (from analyse_logs.py)
```

## Data Fields

Each log record includes:
- **date/time** - Request timestamp
- **ip_address** - Client IP address
- **country** - Derived from IP prefix
- **method** - HTTP method (GET, POST)
- **request** - Request endpoint/page
- **page_label** - Friendly page name
- **status_code** - HTTP status (200, 304, 404, 500, etc.)
- **bytes_sent** - Response size
- **referer** - Traffic source
- **user_agent** - Client browser/device

## Usage Examples

### Analyze Demo Requests from Botswana
1. Select "Botswana" in the Country Filter
2. Select "Schedule Demo" in the Request Type Filter
3. View how many demo requests came from that region

### Track Monthly Performance
1. Use the Monthly Trend chart to identify peak months
2. Correlate with marketing campaigns or product launches
3. Make data-driven decisions about resource allocation

### Monitor Error Rates
1. Check the "Errors" KPI card
2. Drill down to specific countries if needed
3. Identify problem areas and technical issues

## Customization

### Change Port
Edit `dashboard.py`:
```python
app.run_server(debug=True, host="127.0.0.1", port=8050)  # Change 8050
```

### Change Colors
Update the color constants in `dashboard.py`:
```python
THEME_COLOR = "#2563EB"        # Primary blue
BG_COLOR = "#0F172A"           # Dark background
CARD_BG = "#1E293B"            # Card background
COLOR_PALETTE = [...]          # Chart colors
```

### Add More Filters
Add new `dcc.Dropdown` or `dcc.DatePickerRange` components in the layout, then extend the `filter_data()` function to apply the filter.

## Production Deployment

For production, use Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8050 dashboard:app
```

Or use a process manager like systemd, supervisor, or Docker.

## Client Meeting Deliverables

✅ **Generated web server log data** - 500 records from CSV  
✅ **Extracted & cleaned data** - All key fields processed  
✅ **Interactive visualizations** - Non-technical friendly charts  
✅ **Clear categorization** - Demo, Jobs, AI, Events, Prototype tracking  
✅ **Accurate counting** - Job requests, placements, sales performance  
✅ **Statistics & summaries** - KPI cards and summary table  
✅ **Web-based dashboard** - Easy access for the sales team  

## Future Enhancements

- Export reports to PDF/Excel
- Email scheduled reports
- Custom metric definitions
- Anomaly detection alerts
- Competitor benchmarking
- Forecasting models
- Mobile responsive optimization

## Support & Troubleshooting

**Dashboard won't start?**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8050 is available
- Run in a fresh Python environment

**Data not loading?**
- Verify `web_server_logs.csv` exists in the project directory
- Ensure CSV file format matches expected structure
- Run `python generate_dataset.py` to create fresh dataset

**Charts not displaying?**
- Check browser console for errors
- Clear browser cache and refresh
- Ensure Plotly library is installed: `pip install plotly --upgrade`

## License & Confidentiality

This dashboard contains proprietary business data for AI-Solutions. For internal use only.

---

**Created for AI-Solutions Web Server Analytics Initiative**  
*Data Analyst Consultant Project*
