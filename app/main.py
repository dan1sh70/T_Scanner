from fastapi import FastAPI
from app.routes.scan import router

app = FastAPI(title="Testosterone Scanner API")
app.include_router(router)
