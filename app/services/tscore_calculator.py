import json
import os
from fuzzywuzzy import fuzz

# Fuzzy match function
def fuzzy_match(ingredient, risk_entry):
    all_names = [risk_entry["name"].lower()] + [a.lower() for a in risk_entry.get("aliases", [])]
    for alias in all_names:
        if fuzz.partial_ratio(ingredient.lower(), alias) > 75:  # 75% match threshold
            return True
    return False

# Main T-Score calculator
def calculate_t_score(ingredients):
    risk_db_path = os.path.join(os.path.dirname(__file__), "../models/risk_db.json")
    with open(risk_db_path) as f:
        risk_data = json.load(f)

    score = 100
    bad_ingredients = []

    for ingredient in ingredients:
        for risk in risk_data:
            if fuzzy_match(ingredient, risk):
                score -= risk["penalty"]
                bad_ingredients.append({
                    "name": risk["name"],
                    "category": risk["category"],
                    "penalty": risk["penalty"]
                })
                break

    score = max(0, score)
    risk_level = get_risk_level(score)

    return {
        "tscore": score,
        "riskLevel": risk_level,
        "badIngredients": bad_ingredients
    }

# Risk level categorization
def get_risk_level(score):
    if score >= 94:
        return "Testosterone Safe"
    elif score >= 80:
        return "Low Risk"
    elif score >= 60:
        return "Moderate Risk"
    elif score >= 40:
        return "Hormone Disruptive"
    else:
        return "High Risk"










# import json
# import os

# def calculate_t_score(ingredients):
#     risk_db_path = os.path.join(os.path.dirname(__file__), "../models/risk_db.json")
#     with open(risk_db_path) as f:
#         risk_data = json.load(f)

#     score = 100
#     bad_ingredients = []

#     for ingredient in ingredients:
#         for risk in risk_data:
#             if ingredient in [risk["name"]] + risk.get("aliases", []):
#                 score -= risk["penalty"]
#                 bad_ingredients.append({
#                     "name": risk["name"],
#                     "category": risk["category"],
#                     "penalty": risk["penalty"]
#                 })
#                 break

#     score = max(0, score)
#     risk_level = get_risk_level(score)

#     return {
#         "tscore": score,
#         "riskLevel": risk_level,
#         "badIngredients": bad_ingredients
#     }

# def get_risk_level(score):
#     if score >= 94: return "Testosterone Safe"
#     elif score >= 80: return "Low Risk"
#     elif score >= 60: return "Moderate Risk"
#     elif score >= 40: return "Hormone Disruptive"
#     else: return "High Risk"
