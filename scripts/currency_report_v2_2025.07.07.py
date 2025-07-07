import requests
import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    api_key = os.getenv("METAL_API_KEY")
    if not api_key:
        print("❌ Missing METAL_API_KEY in environment.")
        return None, None

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
    except Exception:
        return None, None

# ---------------------- HTML EMAIL TABLE ----------------------

def build_report_table_html(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk):
    rows = f"""
        <tr><td>1 USD</td><td>{usd_to_dkk:.4f} DKK</td></tr>
        <tr><td>1 GBP</td><td>{gbp_to_dkk:.4f} DKK</td></tr>
        <tr><td>1 XAU (Gold)</td><td>{f"{xau_dkk:.2f} DKK" if xau_dkk else "N/A"}</td></tr>
        <tr><td>1 XAG (Silver)</td><td>{f"{xag_dkk:.2f} DKK" if xag_dkk else "N/A"}</td></tr>
        <tr><td>Accenture (ACN)</td><td>{f"{acn_usd:.2f} USD / {acn_dkk:.2f} DKK" if acn_usd and acn_dkk else "N/A"}</td></tr>
    """

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2>💱 Monthly Currency & Market Report</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; min-width: 300px;">
            <thead style="background-color: #f2f2f2;">
                <tr><th>Asset</th><th>Value</th></tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <p style="font-size: 12px; color: #999;">Sent automatically by GitHub Actions.</p>
    </body>
    </html>
    """
    return html

# ---------------------- EMAIL SENDING ----------------------

def send_email(subject, html_body, to_email, from_email, password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    part_html = MIMEText(html_body, "html")
    msg.attach(part_html)

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

    html_output = build_report_table_html(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk)
    print("📧 Preview:\n", html_output)  # Optional for debugging

    # Read email config from environment
    to_email = os.getenv("TO_EMAIL")
    from_email = os.getenv("FROM_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if to_email and from_email and password:
        send_email(
            subject="💱 Monthly Currency & Market Report",
            html_body=html_output,
            to_email=to_email,
            from_email=from_email,
            password=password
        )
    else:
        print("⚠️ Missing email credentials in environment.")
