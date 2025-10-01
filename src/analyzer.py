# src/analyzer.py
from collector import load_history
from datetime import datetime
from dateutil import parser  # install via pip install python-dateutil

def analyze_metrics(metrics, history_limit=20):
    issues = []
    history = load_history(limit=history_limit)

    if history:
        avg_cpu = sum(h["cpu_percent"] for h in history) / len(history)
        avg_mem = sum(h["memory"]["percent"] for h in history) / len(history)
        avg_disk = sum(h["disk"]["percent"] for h in history) / len(history)
    else:
        avg_cpu, avg_mem, avg_disk = 0, 0, 0

    # CPU
    if metrics["cpu_percent"] > 85:
        issues.append("High CPU usage detected")
    elif history and metrics["cpu_percent"] > avg_cpu * 1.5:
        issues.append(f"Unusual CPU spike: {metrics['cpu_percent']}% (avg ~{avg_cpu:.1f}%)")

    # Memory
    if metrics["memory"]["percent"] > 85:
        issues.append("High memory usage detected")
    elif history and metrics["memory"]["percent"] > avg_mem * 1.5:
        issues.append(f"Unusual memory usage: {metrics['memory']['percent']}% (avg ~{avg_mem:.1f}%)")

    # Disk
    if metrics["disk"]["percent"] > 90:
        issues.append("Disk space running low")
    elif history and metrics["disk"]["percent"] > avg_disk * 1.2:
        issues.append(f"Disk usage above normal: {metrics['disk']['percent']}% (avg ~{avg_disk:.1f}%)")

    return issues


def forecast_usage(history_limit=20):
    """Predicts future CPU, memory, and disk issues based on recent growth trends."""
    history = load_history(limit=history_limit)
    if len(history) < 2:
        return ["Not enough history for forecasting"]

    forecasts = []

    # First and last entries for growth calculation
    first = history[0]
    last = history[-1]

    t0 = parser.parse(first["timestamp"])
    t1 = parser.parse(last["timestamp"])
    hours = (t1 - t0).total_seconds() / 3600

    if hours <= 0:
        return ["Invalid time window for forecasting"]

    # --- Disk growth rate ---
    disk_growth = (last["disk"]["percent"] - first["disk"]["percent"]) / hours
    if disk_growth > 0:
        remaining = 100 - last["disk"]["percent"]
        hours_left = remaining / disk_growth
        forecasts.append(f"Disk will be full in ~{hours_left:.1f} hours")
    else:
        forecasts.append("Disk usage stable (no growth detected)")

    # --- Memory growth rate ---
    mem_growth = (last["memory"]["percent"] - first["memory"]["percent"]) / hours
    if mem_growth > 0:
        remaining = 100 - last["memory"]["percent"]
        hours_left = remaining / mem_growth
        forecasts.append(f"Memory will hit 100% in ~{hours_left:.1f} hours")
    else:
        forecasts.append("Memory usage stable (no growth detected)")

    # --- CPU trend ---
    cpu_growth = (last["cpu_percent"] - first["cpu_percent"]) / hours
    if cpu_growth > 0:
        predicted_cpu = last["cpu_percent"] + (cpu_growth * 1)  # 1 hour projection
        forecasts.append(f"CPU usage trending upward → may reach ~{predicted_cpu:.1f}% in 1 hour")
    else:
        forecasts.append("CPU usage stable (no growth detected)")

    return forecasts
