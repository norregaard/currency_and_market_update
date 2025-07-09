# 💱 Currency & Market Update Email Reporter

Automatically fetches daily (or monthly) currency exchange rates, metal prices, and stock prices — then emails a clean, mobile-friendly market summary report. Perfect for keeping yourself or your team updated via GitHub Actions.

---

## ✨ Features

- 🔁 Automated via GitHub Actions (daily, weekly, or monthly)
- 📬 Sends an HTML-formatted email with:
  - USD and GBP exchange rates to DKK
  - Gold (XAU) and Silver (XAG) prices in DKK
  - Accenture (ACN) stock price in USD and DKK
- ✅ Secure: all secrets handled via GitHub Actions Secrets
- 📱 Optimized for email and mobile display
- 📦 Open source under the MIT license

---

## 📸 Sample Email Output

| Asset           | Value                    |
| --------------- | ------------------------ |
| 1 USD           | 6.3412 DKK               |
| 1 GBP           | 8.6512 DKK               |
| 1 XAU (Gold)    | 21126.82 DKK             |
| 1 XAG (Silver)  | 233.92 DKK               |
| Accenture (ACN) | 304.78 USD / 1932.67 DKK |


----

# 📊 Currency and Market Update

This repository automates the generation and deployment of two types of reports:

---

## 🗓️ Monthly Currency and Market Report

This script generates a **monthly market update** based on historical exchange rate data and visualizes it in an HTML report.

- **Script:** [`scripts/generate_report.py`](scripts/generate_report.py)
- **Output:** `dist/index.html`
- **Hosting:** Can be uploaded to Azure Blob Storage Static Website

---

## 📅 Daily Currency Snapshot Report (New!)

In addition to the monthly overview, the project now includes a **daily report** that shows up-to-date exchange rates and gold prices.

- **Script:** [`scripts/currency_report_v2.py`](scripts/currency_report_v2.py)
- **Automation:** Deployed daily using [GitHub Actions](.github/workflows/deploy-to-blob.yml)
- **Live URL:** Hosted via Azure Blob Storage Static Website

### 🔁 Workflow Highlights

- Runs once a day using a GitHub Actions cron schedule
- Fetches live exchange rates and gold prices
- Generates a lightweight HTML report
- Automatically uploads to Azure Blob Storage

---

## 🚀 Getting Started

### Dependencies

- Python 3.8+
- Required libraries are listed in `requirements.txt`

### Environment Variables

Both reports rely on external APIs, so you need to configure:

```bash
export API_KEY_EXCHANGE_RATES=your_key_here
export API_KEY_GOLD=your_key_here

