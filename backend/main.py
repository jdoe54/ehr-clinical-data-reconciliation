from fastapi import FastAPI
from backend.routers import reconcile, validate, patient, medication, allergies, conditions, labs
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(reconcile.router)
app.include_router(validate.router)
app.include_router(patient.router)
app.include_router(medication.router)

app.include_router(allergies.router)
app.include_router(conditions.router)
app.include_router(labs.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Test": "TestValue"}






