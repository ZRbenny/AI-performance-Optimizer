import argparse
from collector import collect_metrics, save_metrics, load_history
from analyzer import analyze_metrics, forecast_usage
from prettytable import PrettyTable

def display_metrics(metrics):
    table = PrettyTable()
    table.field_names = ["Metric", "Value"]

    # CPU
    table.add_row(["CPU Usage", f"{metrics['cpu_percent']}%"])

    # Memory
    mem = metrics["memory"]
    table.add_row([
        "Memory Usage",
        f"{mem['percent']}% ({mem['used'] // (1024**3)} GB / {mem['total'] // (1024**3)} GB)"
    ])

    # Disk
    disk = metrics["disk"]
    table.add_row([
        "Disk Usage",
        f"{disk['percent']}% ({disk['used'] // (1024**3)} GB / {disk['total'] // (1024**3)} GB)"
    ])

    # Network
    net = metrics["network"]
    table.add_row(["Network Sent", f"{net['bytes_sent'] // (1024**2)} MB"])
    table.add_row(["Network Recv", f"{net['bytes_recv'] // (1024**2)} MB"])

    print(table)

def display_issues(issues):
    print("\n=== Issues Detected ===")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues detected")

def display_history(limit=5):
    history = load_history(limit)
    if not history:
        print("No history found.")
        return

    table = PrettyTable()
    table.field_names = ["Timestamp", "CPU %", "Memory %", "Disk %"]

    for entry in history:
        table.add_row([
            entry["timestamp"],
            entry["cpu_percent"],
            entry["memory"]["percent"],
            entry["disk"]["percent"],
        ])

    print("\n=== Recent History ===")
    print(table)

def main():
    parser = argparse.ArgumentParser(description="AI Performance Optimizer CLI")
    parser.add_argument("command", choices=["monitor", "record", "history"], help="Command to run")
    parser.add_argument("--limit", type=int, default=5, help="How many history records to show")
    args = parser.parse_args()

    if args.command in ["monitor", "record"]:
        metrics = collect_metrics()
        print("\n=== System Metrics ===")
        display_metrics(metrics)

        issues = analyze_metrics(metrics)
        display_issues(issues)

        forecasts = forecast_usage()
        if forecasts:
            print("\n=== Forecasts ===")
            for f in forecasts:
                print("-", f)

        if args.command == "record":
            save_metrics(metrics)
            print("\n[INFO] Metrics saved to data/metrics_history.json")

    elif args.command == "history":
        display_history(limit=args.limit)

if __name__ == "__main__":
    main()
