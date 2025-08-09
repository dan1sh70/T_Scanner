import json
import easyocr
import numpy as np
from PIL import Image
import io
import requests
from app.scorer import score_ingredients

# Path to the risk DB
RISK_DB_PATH = "app/risk_db.json"

# Initialize OCR reader
reader = easyocr.Reader(['en'], gpu=False)

def fetch_from_open_food_facts(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("status") == 1:
            product = data.get("product", {})
            raw_ingredients = product.get("ingredients", [])

            # Try structured ingredients list first
            ingredients_list = []
            for item in raw_ingredients:
                name = item.get("text")
                if name:
                    ingredients_list.append(name.strip().lower())

            # Fallback to plain ingredients text if list is empty
            if not ingredients_list and product.get("ingredients_text"):
                ingredients_list = [
                    i.strip().lower()
                    for i in product["ingredients_text"].split(",") if i.strip()
                ]

            name = (
                product.get("product_name") or
                product.get("product_name_en") or
                product.get("generic_name") or
                "Unknown"
            ).strip()

            return {
                "ingredients": ingredients_list,
                "brand": product.get("brands", "Unknown").strip(),
                "product_name": name,
                "source": "open_food_facts"
            }

    return None


def process_barcode(barcode: str):
    # Load local DB
    with open(RISK_DB_PATH, "r") as f:
        risk_db = json.load(f)

    if barcode in risk_db:
        product_data = risk_db[barcode]
    else:
        # Fetch from Open Food Facts if not in local DB
        product_data = fetch_from_open_food_facts(barcode)
        if not product_data:
            return {"error": "Product not found in database"}

        # Save new product to local DB
        risk_db[barcode] = product_data
        with open(RISK_DB_PATH, "w") as f:
            json.dump(risk_db, f, indent=2)

    ingredients = product_data.get("ingredients", [])
    scored = score_ingredients(ingredients)

    return {
        "tscore": scored["tscore"],
        "riskLevel": scored["riskLevel"],
        "badIngredients": scored["badIngredients"],
        "product_name": product_data.get("product_name", ""),
        "brand": product_data.get("brand", ""),
        "source": product_data.get("source", "")
    }

async def process_image(image_file):
    image_bytes = await image_file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Run OCR on image
    result = reader.readtext(np.array(image), detail=0)
    extracted_text = " ".join(result).lower()

    # Load risk ingredients from local DB
    with open(RISK_DB_PATH) as f:
        risk_db = json.load(f)

    # Flatten all risk ingredients
    all_risk_ingredients = set()
    for product in risk_db.values():
        all_risk_ingredients.update(map(str.lower, product.get("ingredients", [])))

    # Match ingredients from OCR output
    matched_ingredients = []
    for ingredient in all_risk_ingredients:
        if ingredient in extracted_text:
            matched_ingredients.append(ingredient)

    scored = score_ingredients(matched_ingredients)

    return {
        "tscore": scored["tscore"],
        "riskLevel": scored["riskLevel"],
        "badIngredients": scored["badIngredients"],
        "source": "ocr_scan"
    }
