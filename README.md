# 📊 Currency and Market Update

This repository automates the generation and deployment of two types of reports:

---

## 🗓️ Monthly Currency and Market Report

Automatically fetches currency exchange rates, metal prices, and stock prices — then emails (once per month) a clean, mobile-friendly market summary report.

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

- **Script:** [`scripts/currency_report_v2.py`](scripts/generate_report.py)
- **Output:** Github Actions sends output via email, .github/workflows/report.yml

## 📸 Sample Email Output

| Asset           | Value                    |
| --------------- | ------------------------ |
| 1 USD           | 6.3412 DKK               |
| 1 GBP           | 8.6512 DKK               |
| 1 XAU (Gold)    | 21126.82 DKK             |
| 1 XAG (Silver)  | 233.92 DKK               |
| Accenture (ACN) | 304.78 USD / 1932.67 DKK |

---

## 📅 Daily Currency Report

In addition to the monthly overview, the project now includes a **daily report** that uploads exchange rates and gold prices daily to a Azure blob storage static website.

- **Script:** [`scripts/generate_report.py`](scripts/generate_report.py)
- **Automation:** Deployed daily using [GitHub Actions workflow](.github/workflows/deploy-to-blob.yml)
- **Output:** Hosted via Azure Blob Storage Static Website

### 🔁 Workflow Highlights

- Runs once a day using a GitHub Actions cron schedule
- Fetches live exchange rates and gold prices
- Generates a lightweight HTML report
- Automatically uploads to Azure Blob Storage
- Report can be viewed as a web page

---

## 🚀 Getting Started

- Create a storage account in Azure and enable static website under Data Management section. Custom domain can be set under Networking section (separate sub tab)
- Create the required repository secrets in Github, e.g. METAL_API_KEY, TO_EMAIL, FROM_EMAIL, EMAIL_PASSWORD (look through the mentioned files to see all used)

### Dependencies

- Python 3.8+
- Required libraries are listed in `requirements.txt`

