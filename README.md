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
