from fastapi import FastAPI
from backend.routers import reconcile, validate

app = FastAPI()

app.include_router(reconcile.router)
app.include_router(validate.router)

@app.get("/")
def read_root():
    return {"Test": "TestValue"}






