import requests
import yfinance as yf
from tabulate import tabulate

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

def display_results_table(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk):
    table = [
        ["1 USD", f"{usd_to_dkk:.4f} DKK"],
        ["1 GBP", f"{gbp_to_dkk:.4f} DKK"],
        ["1 XAU (Gold)", f"{xau_dkk:.2f} DKK" if xau_dkk else "N/A"],
        ["1 XAG (Silver)", f"{xag_dkk:.2f} DKK" if xag_dkk else "N/A"],
        ["Accenture (ACN)", f"{acn_usd:.2f} USD / {acn_dkk:.2f} DKK" if acn_usd and acn_dkk else "N/A"],
    ]

    print("\n📊 Currency and Market Summary\n")
    print(tabulate(table, headers=["Asset", "Value"], tablefmt="fancy_grid"))

# Run all
if __name__ == "__main__":
    print("Fetching data...")

    usd_to_dkk, _, gbp_to_dkk = get_exchange_rates()
    xau_dkk, xag_dkk = get_xau_xag_to_dkk()
    acn_usd, acn_dkk = get_accenture_stock_price(usd_to_dkk)

    display_results_table(usd_to_dkk, gbp_to_dkk, xau_dkk, xag_dkk, acn_usd, acn_dkk)
