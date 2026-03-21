from fastapi import FastAPI
from backend.routers import reconcile

app = FastAPI()

app.include_router(reconcile.router)
#app.include_router(validate.router)

@app.get("/")
def read_root():
    return {"Test": "TestValue"}





"""

@app.post("/api/validate/data-quality")
def validate_data():
    return {"validate": "data-quality"}

"""
