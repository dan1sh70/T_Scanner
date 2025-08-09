import json

with open("app/risk_db.json") as f:
    RISK_DB = json.load(f)

# Normalize keys to lowercase for safe matching
RISK_DB_LOWER = {k.lower(): v for k, v in RISK_DB.items()}

def score_ingredients(found_ingredients):
    tscore = 100
    results = []

    for ing in found_ingredients:
        ing_lower = ing.lower()
        if ing_lower in RISK_DB_LOWER:
            data = RISK_DB_LOWER[ing_lower]
            category = data["category"]
            penalty = data["penalty"]
            tscore -= penalty
            results.append({
                "name": ing.title(),
                "category": category,
                "penalty": penalty
            })

    tscore = max(0, tscore)

    risk_level = (
        "Testosterone Safe" if tscore >= 94 else
        "Low Risk" if tscore >= 80 else
        "Moderate Risk" if tscore >= 60 else
        "Hormone Disruptive" if tscore >= 40 else
        "High Risk"
    )

    return {
        "tscore": tscore,
        "riskLevel": risk_level,
        "badIngredients": results
    }
