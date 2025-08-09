# from fastapi import APIRouter, UploadFile, File
# from app.services.ingredient_extractor import extract_ingredients_from_barcode, extract_ingredients_from_image
# from app.services.ingredient_cleaner import clean_ingredients
# from app.services.tscore_calculator import calculate_t_score

# router = APIRouter()  # ✅ THIS must exist!

# @router.post("/scan/barcode")
# async def scan_barcode(barcode: str):
#     raw_text = extract_ingredients_from_barcode(barcode)
#     ingredients = clean_ingredients(raw_text)
#     return calculate_t_score(ingredients)

# @router.post("/scan/image")
# async def scan_image(image: UploadFile = File(...)):
#     raw_text = extract_ingredients_from_image(image)
#     ingredients = clean_ingredients(raw_text)
#     return calculate_t_score(ingredients)


# from fastapi import APIRouter, UploadFile, File
# from app.services.ingredient_extractor import extract_ingredients_from_barcode, extract_ingredients_from_image

# router = APIRouter()  # ✅ Must exist

# @router.post("/scan/barcode")
# async def scan_barcode(barcode: str):
#     return extract_ingredients_from_barcode(barcode)

# @router.post("/scan/image")
# async def scan_image(image: UploadFile = File(...)):
#     return extract_ingredients_from_image(image)


from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingredient_extractor import extract_ingredients_from_barcode, extract_ingredients_from_image

router = APIRouter()  # ✅ Must exist

@router.post("/scan/barcode")
async def scan_barcode(barcode: str):
    try:
        result = extract_ingredients_from_barcode(barcode)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process barcode: {str(e)}")

@router.post("/scan/image")
async def scan_image(image: UploadFile = File(...)):
    try:
        result = extract_ingredients_from_image(image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")
