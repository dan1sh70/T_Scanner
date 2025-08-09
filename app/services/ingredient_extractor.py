import os
import json
import requests
import easyocr
import re
import numpy as np
from PIL import Image
from io import BytesIO
from difflib import get_close_matches

# Load risk data
risk_db_path = os.path.join(os.path.dirname(__file__), "../models/risk_db.json")
with open(risk_db_path) as f:
    RISK_DATA = json.load(f)

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# 🧠 Risk Scoring Logic
def evaluate_risk(ingredients):
    score = 100
    bad_ingredients = []

    for ingredient in ingredients:
        found = False
        for risk in RISK_DATA:
            candidates = [risk["name"].lower()] + [a.lower() for a in risk.get("aliases", [])]
            match = get_close_matches(ingredient.lower(), candidates, n=1, cutoff=0.8)
            if match:
                score -= risk["penalty"]
                bad_ingredients.append({
                    "name": risk["name"],
                    "category": risk["category"],
                    "penalty": risk["penalty"]
                })
                found = True
                break

    score = max(0, score)

    if score >= 94:
        risk_level = "Testosterone Safe"
    elif score >= 80:
        risk_level = "Low Risk"
    elif score >= 60:
        risk_level = "Moderate Risk"
    elif score >= 40:
        risk_level = "Hormone Disruptive"
    else:
        risk_level = "High Risk"

    return score, risk_level, bad_ingredients

# 📦 Mock DB for offline barcode fallback
mock_db = {
    "5449000000996": {
        "ingredients": ["refined sugar", "soy lecithin", "triclosan"],
        "name": "Coca-Cola Zero"
    },
    "8000500024082": {
        "ingredients": ["refined sugar", "soy lecithin"],
        "name": "Nutella"
    }
}

# 🔍 Barcode Ingredient Extractor
def extract_ingredients_from_barcode(barcode: str):
    try:
        res = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json", timeout=5)
        data = res.json()
        ingredients = []
        product_name = "Unknown Product"

        if res.status_code == 200 and data.get("status") == 1:
            product = data["product"]
            product_name = product.get("product_name", "Unknown Product")
            ingredients_text = product.get("ingredients_text", "")
            ingredients = [
                i.strip().lower()
                for i in ingredients_text.replace(".", "")
                                         .replace(":", "")
                                         .replace(";", ",")
                                         .split(",") if i.strip()
            ]
        else:
            raise Exception("Product not found")

    except Exception as e:
        print(f"⚠️ Barcode fallback used: {e}")
        fallback = mock_db.get(barcode, {"ingredients": [], "name": "Unknown Product"})
        ingredients = fallback["ingredients"]
        product_name = fallback["name"]

    score, risk_level, bad_ingredients = evaluate_risk(ingredients)

    return {
        "productName": product_name,
        "tscore": score,
        "riskLevel": risk_level,
        "badIngredients": bad_ingredients
    }

# 🖼️ Image OCR Ingredient Extractor
def extract_ingredients_from_image(image_file):
    try:
        image_bytes = image_file.file.read()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_np = np.array(image)

        result = reader.readtext(image_np)
        text = " ".join([d[1] for d in result])
        print("🧾 OCR Extracted:", text)

        # Clean and normalize OCR text
        extracted = text.lower()
        extracted = re.sub(r"(ingredients|contains)", "", extracted)
        extracted = extracted.replace(";", ",").replace(".", ",")
        extracted = re.sub(r"[^a-zA-Z0-9,\s]", "", extracted)

        ingredients = [
            i.strip().lower()
            for i in extracted.split(",") if i.strip()
        ]

        score, risk_level, bad_ingredients = evaluate_risk(ingredients)

        return {
            "productName": "Scanned Image",
            "tscore": score,
            "riskLevel": risk_level,
            "badIngredients": bad_ingredients
        }

    except Exception as e:
        print(f"❌ Failed to process image: {e}")
        raise ValueError(f"Failed to process image: {str(e)}")







# @from app.utils.barcode_lookup import get_ingredients_by_barcode
# from app.utils.ocr_engine import perform_easyocr

# def extract_ingredients_from_barcode(barcode: str) -> str:
#     return get_ingredients_by_barcode(barcode)

# def extract_ingredients_from_image(image_file) -> str:
#     return perform_easyocr(image_file)

# print("🔎 Ingredients fetched from API:", ingredients)









# import os
# import re
# import easyocr

# # Initialize the EasyOCR reader once
# reader = easyocr.Reader(['en'], gpu=False)

# # Set of keywords for filtering relevant OCR lines
# KEYWORDS = ["ingredient", "contains", "composition", "includes"]

# def extract_ingredients_from_image(image_path):
#     result = reader.readtext(image_path, detail=0)
#     text = " ".join(result).lower()

#     # Extract lines with potential ingredient content
#     lines = text.splitlines()
#     ingredients_text = " ".join(
#         line for line in lines if any(keyword in line for keyword in KEYWORDS)
#     )

#     # Use regex to extract ingredients
#     match = re.search(r"(ingredients?|contains?)[:\- ]*(.*)", ingredients_text)
#     if match:
#         raw_ingredients = match.group(2)
#     else:
#         raw_ingredients = ingredients_text

#     # Split and clean
#     ingredients = [
#         ing.strip().lower()
#         for ing in re.split(r"[,;]", raw_ingredients)
#         if ing.strip()
#     ]

#     return ingredients


# def extract_ingredients_from_barcode(barcode):
#     # Mock barcode-to-ingredients database
#     barcode_db = {
#         "5449000000996": ["refined sugar", "soy lecithin", "triclosan"],
#         "0123456789123": ["paraben", "lavender oil", "caffeine"],
#         "1111111111111": ["bpa", "phosphoric acid", "msg"],
#         "2222222222222": ["artificial sweetener", "lead", "cadmium"]
#     }
#     return barcode_db.get(barcode, [])

