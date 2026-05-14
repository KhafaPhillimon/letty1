# Setup Guide: AI-Solutions Web Server Analytics Dashboard

## Quick Start (3 Minutes)

### Windows Users
Simply double-click: `run_dashboard.bat`

The script will:
1. ✅ Check Python installation
2. ✅ Install required packages
3. ✅ Generate dataset (if needed)
4. ✅ Start the dashboard

Then open your browser to: **http://127.0.0.1:8050**

### Mac/Linux Users
```bash
chmod +x run_dashboard.sh
./run_dashboard.sh
```

Then open your browser to: **http://127.0.0.1:8050**

---

## Detailed Setup Guide

### Step 1: Verify Python Installation

**Windows:**
```cmd
python --version
```

**Mac/Linux:**
```bash
python3 --version
```

You should see Python 3.8 or higher. If not, download from: https://www.python.org/downloads/

### Step 2: Create Virtual Environment (Optional but Recommended)

Creating a virtual environment keeps dependencies isolated:

**Windows:**
```cmd
python -m venv env
env\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **dash** - Web framework for the dashboard
- **plotly** - Interactive visualization library
- **pandas** - Data analysis and manipulation
- **numpy** - Numerical computing
- **gunicorn** - Production web server (optional)

### Step 4: Generate Dataset (if needed)

If `web_server_logs.csv` doesn't exist:

```bash
python generate_dataset.py
```

Output:
```
[OK] Dataset saved -> web_server_logs.csv  (500 records)
```

### Step 5: Start the Dashboard

```bash
python dashboard.py
```

Expected output:
```
============================================================
  Starting AI-Solutions Web Server Analytics
============================================================
  Data loaded: 500 records
  Date range: 2025-01-01 to 2025-12-31

  🌐 Dashboard available at: http://127.0.0.1:8050
============================================================
```

### Step 6: Open in Browser

Visit: **http://127.0.0.1:8050**

You should see the interactive dashboard with:
- KPI cards at the top
- Filter controls (Country, Date Range, Request Type)
- Multiple interactive charts
- Summary statistics table

---

## Dashboard Features Tour

### 1. KPI Cards (Top Section)
Shows key metrics at a glance:
- **Total Requests** - Overall traffic volume
- **Success Rate** - % of successful responses (green if >90%)
- **Demo Requests** - Schedule demo page visits
- **Errors** - Failed requests (red if >10)
- **Avg Bytes/Request** - Data consumption

### 2. Filters (Left Side)
Customize what data you see:
- **Country Filter** - Select one country or see all
- **Date Range** - Pick specific time periods
- **Request Type** - Focus on specific features

All charts update automatically when you change filters!

### 3. Charts

#### Row 1
- **Requests by Country** - Which countries are visiting?
- **HTTP Status Distribution** - Success vs error breakdown

#### Row 2
- **Requests by Page Type** - Most visited pages?
- **Key Feature Requests** - Interest in Demo/AI/Jobs/Events?

#### Row 3
- **Monthly Request Volume** - Trends throughout the year

#### Row 4
- **Hourly Traffic Distribution** - When are users most active?
- **Traffic Referrer Sources** - Where do visitors come from?

### 4. Summary Statistics Table
Quick reference with:
- Total request count
- Success/error counts
- Average response size
- Unique countries represented
- Date range of data

---

## Common Tasks

### Task: Find Which Country Has Most Demo Requests
1. Click "Schedule Demo" in Request Type Filter
2. Look at the "Key Feature Requests" chart
3. Or view "Top Countries for Schedule Demo" bar chart

### Task: Check if Errors Are Increasing
1. Look at the "Errors" KPI card
2. Check the "HTTP Status Distribution" pie chart
3. Note which status codes (404 vs 500) are causing issues

### Task: Understand Peak Traffic Times
1. Look at "Hourly Traffic Distribution" chart
2. Peak hours will have tallest bars
3. Use for resource planning and marketing timing

### Task: Analyze Performance by Time Period
1. Use the Date Range filter
2. Pick a specific month or week
3. All charts will update to show just that period
4. Compare with other time periods by changing dates

### Task: Focus on Specific Feature
1. Select feature in "Request Type Filter"
2. Dashboard shows only requests for that feature
3. See geographic distribution and time patterns for that feature

---

## Troubleshooting

### Issue: "Python not found" or "Python not recognized"

**Solution:**
1. Install Python from https://www.python.org
2. During installation, **CHECK** "Add Python to PATH"
3. Restart your computer
4. Try again

### Issue: Port 8050 is already in use

**Solution:** Edit `dashboard.py`, find this line:
```python
app.run_server(debug=True, host="127.0.0.1", port=8050)
```

Change `8050` to any other number (e.g., `8051`, `8080`):
```python
app.run_server(debug=True, host="127.0.0.1", port=8051)
```

Then access: `http://127.0.0.1:8051`

### Issue: "ModuleNotFoundError: No module named 'dash'"

**Solution:**
Make sure you installed dependencies:
```bash
pip install -r requirements.txt
```

If still failing, try upgrading pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: CSV file not found

**Solution:**
Generate the dataset:
```bash
python generate_dataset.py
```

Or download/place the CSV file in the project folder.

### Issue: Dashboard loads but charts are blank

**Solution:**
1. Check browser console (F12 → Console tab) for errors
2. Try clearing cache: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
3. Refresh page: F5 or Ctrl+R
4. Ensure `web_server_logs.csv` has data:
   ```bash
   python -c "import pandas as pd; df=pd.read_csv('web_server_logs.csv'); print(f'Rows: {len(df)}')"
   ```

---

## Next Steps

### For Development
1. Modify charts and layouts in `dashboard.py`
2. Add new visualizations by copying existing chart code
3. Customize colors and themes at the top of the file
4. All changes take effect when you save and refresh the browser

### For Production Deployment
1. Set `debug=False` in `dashboard.py`
2. Use Gunicorn: `gunicorn --bind 0.0.0.0:8050 dashboard:app`
3. Run behind Nginx or Apache
4. Use systemd or Docker for process management
5. Set up SSL/HTTPS certificates

### For Sharing with Team
1. Host on a shared server
2. Users access via browser (no local installation needed)
3. All data is centralized and real-time
4. Works on any device with web browser

---

## File Reference

| File | Purpose |
|------|---------|
| `dashboard.py` | Main Dash application - THE DASHBOARD |
| `generate_dataset.py` | Creates synthetic web server logs |
| `analyse_logs.py` | Static analysis with matplotlib (alternative) |
| `web_server_logs.csv` | The actual dataset (500 records) |
| `requirements.txt` | Python package dependencies |
| `README.md` | Main documentation |
| `SETUP.md` | This file - step-by-step guide |
| `run_dashboard.bat` | Windows launcher script |
| `run_dashboard.sh` | Mac/Linux launcher script |

---

## Performance Tips

1. **For large datasets (>100K rows):**
   - Filter data server-side before displaying
   - Use data aggregation (hourly instead of minute-level)
   - Consider caching or data warehouse

2. **For better responsiveness:**
   - Reduce number of charts displayed
   - Use fewer data points in time-series charts
   - Optimize CSV file size (remove unnecessary columns)

3. **For production use:**
   - Deploy to cloud (AWS, Azure, Heroku)
   - Use CDN for static assets
   - Enable browser caching
   - Monitor server performance

---

## Getting Help

**Issues? Questions?**

1. Check the `README.md` file - comprehensive documentation
2. Review `dashboard.py` comments - code is well-documented
3. Check Dash documentation: https://dash.plotly.com
4. Check Plotly documentation: https://plotly.com/python

---

**Ready to explore your data? Let's go! 🚀**

Open your browser and navigate to: **http://127.0.0.1:8050**
