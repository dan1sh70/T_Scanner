import requests

def get_ingredients_by_barcode(barcode: str) -> str:
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return ""

    data = response.json()
    return data.get('product', {}).get('ingredients_text', '')
