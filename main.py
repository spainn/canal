import requests
import pprint

API_KEY = "DEMO_KEY"
BARCODE = 850126007120

def track(barcode):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&pageSize=10&api_key={API_KEY}"

    rawProductData = requests.get(url)
    pprint.pprint(rawProductData.json())

def main():
    track(BARCODE)


if __name__ == "__main__":
    main()
