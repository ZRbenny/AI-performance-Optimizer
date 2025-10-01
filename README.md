AI Performance Optimizer

This project is an AI-powered tool for monitoring and analyzing computer performance.
It collects data on CPU, memory, disk, and network usage, then uses OpenAI’s GPT-4o-mini to generate insights and recommendations.

📌 Features

System Metrics Collection: CPU, memory, disk, network.

Issue Detection: Highlights anomalies (e.g., high memory or low disk).

AI-Driven Reports: GPT-4o-mini provides human-readable performance insights.

Command-Line Interface (CLI): Monitor, record, and view history.

Dashboard: Streamlit app for live metrics, trends, and AI analysis.

🚀 Getting Started
1. Clone the Repo
git clone https://github.com/ZRbenny/AI-performance-Optimizer.git
cd AI-performance-Optimizer

2. Install Dependencies
pip install -r requirements.txt

3. Set Up OpenAI API Key

Create a file named .env in the project root and add your key:

OPENAI_API_KEY=sk-proj-yourkeyhere

👉 Tip: Copy `.env.example` to `.env` and paste your API key inside.

⚠️ Do not commit this file to GitHub (it’s in .gitignore).

If you don’t have an API key yet:

Go to platform.openai.com

Create a new key under View API Keys

Add a payment method (API usage is billed separately from ChatGPT Plus).

This project uses gpt-4o-mini, which costs less than $1/month for typical use.

📊 Usage
Run CLI
python src/cli.py monitor
python src/cli.py record
python src/cli.py history

Run Dashboard commends:
python -m streamlit run src/dashboard.py

The dashboard shows:

Live system metrics

Detected issues

Forecasts of resource usage

🤖 AI Performance Report (GPT-4o-mini powered)


📜 License:

MIT License