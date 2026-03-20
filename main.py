from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Test": "TestValue"}


@app.post("/api/reconcile/medication")
def reconcile_medication():
    return {"reconcile": "medication"}


@app.post("/api/validate/data-quality")
def reconcile_medication():
    return {"validate": "data-quality"}

