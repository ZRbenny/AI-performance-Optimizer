# src/analyzer.py
def analyze_metrics(metrics):
    issues = []

    if metrics["cpu_percent"] > 85:
        issues.append("High CPU usage detected")

    if metrics["memory"]["percent"] > 85:
        issues.append("High memory usage detected")

    if metrics["disk"]["percent"] > 90:
        issues.append("Disk space running low")

    return issues
