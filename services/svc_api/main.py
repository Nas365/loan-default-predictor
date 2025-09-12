from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib, pandas as pd, pathlib

app = FastAPI(title="Loan Default API", version="1.0")

BUNDLE = joblib.load(pathlib.Path(__file__).parents[2] / "artifacts" / "loan_default_xgb.joblib")
MODEL = BUNDLE["model"]
THRESH = float(BUNDLE["threshold"])
FEATURES = BUNDLE["features"]

class LoanInput(BaseModel):
    Credit_Utilization_Ratio: float = Field(..., ge=0)
    Debt_to_Income_Ratio: float = Field(..., ge=0)
    Monthly_Income: float = Field(..., ge=0)
    Borrower_Age: int = Field(..., ge=18, le=120)
    Open_Loans_Count: int = Field(..., ge=0)
    RealEstate_Loans_Count: int = Field(..., ge=0)
    Times_30_59DaysLate: int = Field(..., ge=0)
    Times_60_89DaysLate: int = Field(..., ge=0)
    Times_90DaysLate: int = Field(..., ge=0)
    Number_of_Dependents: int = Field(..., ge=0, le=20)

@app.get("/healthz")
def healthz():
    return {"status":"ok"}

@app.post("/predict")
def predict(x: LoanInput):
    row = {k: getattr(x, k) for k in FEATURES}
    X = pd.DataFrame([row])
    p = float(MODEL.predict_proba(X)[:,1][0])
    decision = "HIGH_RISK" if p >= THRESH else "LOW_RISK"
    return {"prob_default": p, "decision": decision, "threshold": THRESH}
