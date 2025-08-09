# import re

# def clean_ingredients(raw_text):
#     raw_text = raw_text.lower()
#     raw_text = re.sub(r'[^a-zA-Z0-9, ]+', '', raw_text)
#     parts = [x.strip() for x in raw_text.split(",") if x.strip()]
#     return parts


import re

def clean_ingredients(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9,\s]', '', text)  # Remove unwanted symbols
    text = text.replace("ingredients", "")    # Remove 'ingredients' label if needed
    ingredients = re.split(r'[,\n]', text)    # Split by comma or newline
    return [i.strip() for i in ingredients if i.strip()]



# import re

# def clean_ingredients(text: str):
#     text = text.lower()
#     text = re.sub(r'[^a-z0-9,\s]', '', text)
#     return [i.strip() for i in text.split(',') if i.strip()]
