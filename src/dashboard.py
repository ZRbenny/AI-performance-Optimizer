# src/dashboard.py
import streamlit as st
import pandas as pd
from collector import load_history, collect_metrics, save_metrics
from analyzer import analyze_metrics, forecast_usage
from streamlit_autorefresh import st_autorefresh

# === Page Setup ===
st.set_page_config(page_title="AI Performance Optimizer", layout="wide")
st.title("🖥️ AI Performance Optimizer Dashboard")

# === Sidebar Controls ===
st.sidebar.header("⚙️ Settings")

# Refresh interval slider
refresh_rate = st.sidebar.slider("Auto-refresh interval (seconds)", 5, 60, 5)

# Remember auto_record across refreshes
if "auto_record" not in st.session_state:
    st.session_state.auto_record = True  # default ON

st.session_state.auto_record = st.sidebar.checkbox(
    "Enable Auto Recording", value=st.session_state.auto_record
)

# Auto-refresh only if enabled
if st.session_state.auto_record:
    st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")

# === Collect and Save Metrics ===
metrics = collect_metrics()
if st.session_state.auto_record:
    save_metrics(metrics, silent=True)

# === Live Metrics ===
st.header("Live System Metrics")
col1, col2, col3, col4 = st.columns(4)
col5, col6 = st.columns(2)

# CPU Progress Bar
col1.subheader("CPU Usage")
col1.progress(int(metrics['cpu_percent']))
col1.write(f"{metrics['cpu_percent']}%")

# Memory Progress Bar
col2.subheader("Memory Usage")
col2.progress(int(metrics['memory']['percent']))
col2.write(f"{metrics['memory']['percent']}% ({metrics['memory']['used'] // (1024**3)} GB / {metrics['memory']['total'] // (1024**3)} GB)")

# Disk Progress Bar
col3.subheader("Disk Usage")
col3.progress(int(metrics['disk']['percent']))
col3.write(f"{metrics['disk']['percent']}% ({metrics['disk']['used'] // (1024**3)} GB / {metrics['disk']['total'] // (1024**3)} GB)")

col4.metric("Network Sent", f"{metrics['network']['bytes_sent'] // (1024**2)} MB")
col5.metric("Network Recv", f"{metrics['network']['bytes_recv'] // (1024**2)} MB")
col6.metric(
    "System Uptime",
    f"{metrics['uptime'] // 3600}h {(metrics['uptime'] % 3600) // 60}m",
)

# Disk I/O
st.subheader("Disk I/O")
st.write(f"📖 Read: {metrics['disk_io']['read_mb']} MB | ✍️ Write: {metrics['disk_io']['write_mb']} MB")

# GPU
if "gpu" in metrics:
    st.subheader("GPU Usage")
    gpu = metrics["gpu"]
    st.metric("GPU Load", f"{gpu['load']:.1f}%")
    st.metric("GPU Memory", f"{gpu['memory_used']}MB / {gpu['memory_total']}MB")

# Top Processes
st.subheader("Top 5 Processes by CPU Usage")
proc_df = pd.DataFrame(metrics["top_processes"])
st.table(proc_df[["pid", "name", "cpu_percent", "memory_percent"]])

# === Issues ===
issues = analyze_metrics(metrics)
st.subheader("Issues Detected")
if issues:
    for issue in issues:
        st.error(issue)
else:
    st.success("No issues detected")

# === Forecasts ===
st.subheader("Forecasts")
forecasts = forecast_usage()
if forecasts:
    for f in forecasts:
        st.warning(f)
else:
    st.info("Not enough history for forecasts")

# === Historical Trends ===
st.header("Historical Trends")
history = load_history(limit=50)
if history:
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
