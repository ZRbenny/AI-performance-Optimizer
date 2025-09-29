import argparse
from collector import collect_metrics
from analyzer import analyze_metrics
from prettytable import PrettyTable

def display_metrics(metrics):
    table = PrettyTable()
    table.field_names = ["Metric", "Value"]

    # CPU
    table.add_row(["CPU Usage", f"{metrics['cpu_percent']}%"])

    # Memory
    mem = metrics["memory"]
    table.add_row(["Memory Usage", f"{mem['percent']}% ({mem['used'] // (1024**3)} GB / {mem['total'] // (1024**3)} GB)"])

    # Disk
    disk = metrics["disk"]
    table.add_row(["Disk Usage", f"{disk['percent']}% ({disk['used'] // (1024**3)} GB / {disk['total'] // (1024**3)} GB)"])

    # Network
    net = metrics["network"]
    table.add_row(["Network Sent", f"{net['bytes_sent'] // (1024**2)} MB"])
    table.add_row(["Network Recv", f"{net['bytes_recv'] // (1024**2)} MB"])

    print("\n=== System Metrics ===")
    print(table)

def display_issues(issues):
    print("\n=== Issues Detected ===")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No issues detected")

def main():
    parser = argparse.ArgumentParser(description="AI Performance Optimizer CLI")
    parser.add_argument("command", choices=["monitor"], help="Command to run")
    args = parser.parse_args()

    if args.command == "monitor":
        metrics = collect_metrics()
        display_metrics(metrics)
        issues = analyze_metrics(metrics)
        display_issues(issues)

if __name__ == "__main__":
    main()
