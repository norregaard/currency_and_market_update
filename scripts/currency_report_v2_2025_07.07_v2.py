import requests
import yfinance as yf
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
import os

# ---------------------- DATA FETCHING FUNCTIONS ----------------------

def get_exchange_rates():
    url = "https://api.frankfurter.app/latest"
    params = {"symbols": "USD,DKK,GBP"}

    response = requests.get(url, params=params)
    data = response.json()

    rates = data.get("rates", {})
    eur_to_usd = rates.get("USD")
    eur_to_dkk = rates.get("DKK")
    eur_to_gbp = rates.get("GBP")

    if eur_to_usd and eur_to_dkk and eur_to_gbp:
        usd_to_dkk = eur_to_dkk / eur_to_usd
        usd_to_gbp = eur_to_gbp / eur_to_usd
        gbp_to_dkk = eur_to_dkk / eur_to_gbp
        return usd_to_dkk, usd_to_gbp, gbp_to_dkk
    else:
        raise Exception("Failed to get required exchange rates.")

def get_xau_xag_to_dkk():
    api_key = "1ce53d09f679bf18cbb43af2ac7a0d92"
    url = "https://api.metalpriceapi.com/v1/latest"
    params = {
        "api_key": api_key,
        "base": "XAU",
        "currencies": "USD,DKK,XAG"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("success", False):
        return None, None

    rates = data.get("rates", {})
    xau_to_usd = rates.get("USD")
    xau_to_dkk = rates.get("DKK")
    xau_to_xag = rates.get("XAG")

    if xau_to_usd and xau_to_dkk and xau_to_xag:
        xag_to_dkk = xau_to_dkk / xau_to_xag
        return xau_to_dkk, xag_to_dkk
    else:
        return None, None

def get_accenture_stock_price(usd_to_dkk):
    try:
        ticker = yf.Ticker("ACN")
        price_usd = ticker.info["regularMarketPrice"]
        price_dkk = price_usd * usd_to_dkk
        return price_usd, price_dkk
    except Exception as e:
        return None, None

# ---------------------- OUTPUT & EMAIL FUNCTIONS ----------------------

def build_report_table(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk):
    lines = [
        "Asset            | Value",
        "-----------------|---------------------",
        f"1 USD            | {usd_to_dkk:.4f} DKK",
        f"1 GBP            | {gbp_to_dkk:.4f} DKK",
        f"1 XAU (Gold)     | {xau_dkk:.2f} DKK" if xau_dkk else "1 XAU (Gold)     | N/A",
        f"1 XAG (Silver)   | {xag_dkk:.2f} DKK" if xag_dkk else "1 XAG (Silver)   | N/A",
        f"Accenture (ACN)  | {acn_usd:.2f} USD / {acn_dkk:.2f} DKK" if acn_usd and acn_dkk else "Accenture (ACN)  | N/A",
    ]
    return "\n".join(lines)

def send_email(subject, body, to_email, from_email, password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, [to_email], msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ---------------------- MAIN EXECUTION ----------------------

if __name__ == "__main__":
    print("📡 Fetching market data...")

    usd_to_dkk, _, gbp_to_dkk = get_exchange_rates()
    xau_dkk, xag_dkk = get_xau_xag_to_dkk()
    acn_usd, acn_dkk = get_accenture_stock_price(usd_to_dkk)

    report = build_report_table(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk)
    print("\n📊 Monthly Currency & Market Report\n")
    print(report)

    # Get email credentials from environment (GitHub Secrets or locally)
    to_email = os.getenv("TO_EMAIL")
    from_email = os.getenv("FROM_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if to_email and from_email and password:
        send_email(
            subject="💱 Monthly Currency & Market Report",
            body=report,
            to_email=to_email,
            from_email=from_email,
            password=password
        )
    else:
        print("⚠️ Email not sent — missing environment variables.")
