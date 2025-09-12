import joblib
from pathlib import Path

def test_bundle_ok():
    b = joblib.load(Path("artifacts/loan_default_xgb.joblib"))
    # Ensuring the model bundle contains the expected keys
    assert {"model", "threshold", "features"} <= b.keys()
    
