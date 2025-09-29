# src/dashboard.py
import streamlit as st
import pandas as pd
from collector import load_history, collect_metrics
from analyzer import analyze_metrics, forecast_usage

st.set_page_config(page_title="AI Performance Optimizer", layout="wide")

st.title("🖥️ AI Performance Optimizer Dashboard")

# Live metrics section
st.header("Live System Metrics")
metrics = collect_metrics()

col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Usage", f"{metrics['cpu_percent']}%")
col2.metric("Memory Usage", f"{metrics['memory']['percent']}%")
col3.metric("Disk Usage", f"{metrics['disk']['percent']}%")
col4.metric("Network Sent", f"{metrics['network']['bytes_sent'] // (1024**2)} MB")

# Issues
issues = analyze_metrics(metrics)
st.subheader("Issues Detected")
if issues:
    for issue in issues:
        st.error(issue)
else:
    st.success("No issues detected")

# Forecasts
st.subheader("Forecasts")
forecasts = forecast_usage()
if forecasts:
    for f in forecasts:
        st.warning(f)
else:
    st.info("Not enough history for forecasts")

# Historical trends
st.header("Historical Trends")
history = load_history(limit=50)
if history:
    # Flatten history into a clean DataFrame
    clean_data = []
    for entry in history:
        clean_data.append({
            "timestamp": entry["timestamp"],
            "cpu_percent": entry["cpu_percent"],
            "memory_percent": entry["memory"]["percent"],
            "disk_percent": entry["disk"]["percent"]
        })

    df = pd.DataFrame(clean_data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    st.line_chart(df[["cpu_percent", "memory_percent", "disk_percent"]])
else:
    st.info("No history data available yet.")
