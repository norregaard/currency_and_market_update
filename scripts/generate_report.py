# Load local .env file for development only (ignored in production)
from dotenv import load_dotenv
load_dotenv()

import requests
import yfinance as yf
import os
import shutil

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

# ---------------------- HTML REPORT ----------------------
def build_report_table_html(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk, blob_storage_base_url):
    rows = f"""
        <tr><td>1 USD</td><td>{usd_to_dkk:.4f} DKK</td></tr>
        <tr><td>1 GBP</td><td>{gbp_to_dkk:.4f} DKK</td></tr>
        <tr><td>1 XAU (Gold)</td><td>{f"{xau_dkk:.2f} DKK" if xau_dkk else "N/A"}</td></tr>
        <tr><td>1 XAG (Silver)</td><td>{f"{xag_dkk:.2f} DKK" if xag_dkk else "N/A"}</td></tr>
        <tr><td>Accenture (ACN)</td><td>{f"{acn_usd:.2f} USD / {acn_dkk:.2f} DKK" if acn_usd and acn_dkk else "N/A"}</td></tr>
    """

    html = f"""
    <html>
    <head>
        <title>Monthly Currency & Market Report</title>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <img src="{blob_storage_base_url}/Logo_jfn_github.png" alt="Logo" style="width:200px; height:auto; display:block; margin-bottom:20px;">
        <h2>💱 Monthly Currency & Market Report</h2>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; min-width: 300px;">
            <thead style="background-color: #f2f2f2;">
                <tr><th>Asset</th><th>Value</th></tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        <p style="font-size: 12px; color: #999;">Generated automatically by GitHub Actions.</p>
    </body>
    </html>
    """
    return html

# ---------------------- SAVE HTML AND LOGO ----------------------
def save_report_files(html_content, logo_path, output_dir="dist"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save HTML report
    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ Saved HTML report to {html_path}")

    # Copy logo to output directory
    dest_logo_path = os.path.join(output_dir, "Logo_jfn_github.png")
    shutil.copyfile(logo_path, dest_logo_path)
    print(f"✅ Copied logo to {dest_logo_path}")

# ---------------------- MAIN EXECUTION ----------------------
if __name__ == "__main__":
    print("📡 Fetching market data...")

    usd_to_dkk, _, gbp_to_dkk = get_exchange_rates()
    xau_dkk, xag_dkk = get_xau_xag_to_dkk()
    acn_usd, acn_dkk = get_accenture_stock_price(usd_to_dkk)

    # Azure Blob Storage base URL for logo
    blob_storage_base_url = os.getenv("BLOB_STORAGE_BASE_URL", "https://stcurrencyreportjfn003.z16.web.core.windows.net")

    # Generate HTML report
    html_output = build_report_table_html(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk, blob_storage_base_url)
    print("📧 Preview:\n", html_output)  # Optional for debugging

    # Save HTML and logo to dist/ directory
    save_report_files(html_output, "assets/Logo_jfn_github.png")