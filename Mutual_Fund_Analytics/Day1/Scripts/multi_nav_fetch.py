import requests
import pandas as pd

# Scheme names and codes
schemes = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for scheme_name, scheme_code in schemes.items():

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # Convert only the raw NAV data to DataFrame
        df = pd.DataFrame(data["data"])

        # Save each scheme as its own CSV
        filename = f"{scheme_name}_raw.csv"
        df.to_csv(filename, index=False)

        print(f"Saved: {filename}")

    except Exception as e:
        print(f"Error fetching {scheme_name}: {e}")
