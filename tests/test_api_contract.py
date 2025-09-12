import joblib
from pathlib import Path

def test_feature_list():
    b = joblib.load(Path("artifacts/loan_default_xgb.joblib"))
    feats = b["features"]
    assert len(feats) == 10
    assert feats[0] == "Credit_Utilization_Ratio"
