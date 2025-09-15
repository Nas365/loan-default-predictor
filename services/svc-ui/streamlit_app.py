import base64, pathlib
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Loan Default Predictor (UK)", page_icon="💳", layout="wide")

def set_background(image_path: str):
    p = pathlib.Path(image_path)
    if p.exists():
        b64 = base64.b64encode(p.read_bytes()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
              background: url("data:image/jpg;base64,{b64}") no-repeat center center fixed;
              background-size: cover;
              color:#e6eeff;
              font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            }}
            .card {{
              background: rgba(0,0,0,0.60);
              border: 1px solid rgba(255,255,255,0.08);
              border-radius: 18px;
              padding: 18px;
              box-shadow: 0 8px 24px rgba(0,0,0,.35);
            }}
            .feature-card {{
              background: rgba(0,0,0,0.55);
              border-radius: 12px;
              padding: 14px;
              margin-bottom: 12px;
              font-size: 0.92rem;
              line-height: 1.35rem;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

# this path is inside your repo
set_background("services/svc-ui/assets/bg.jpg")

@st.cache_resource(show_spinner=False)
def load_bundle():
    path = pathlib.Path("artifacts/loan_default_xgb.joblib")
    return joblib.load(path)

try:
    BUNDLE = load_bundle()
    MODEL = BUNDLE["model"]
    THRESH = float(BUNDLE["threshold"])
    FEATURES = BUNDLE["features"]
except Exception as e:
    st.error(f"Failed to load model bundle: {e}")
    st.stop()

st.title("💳 Loan Default Predictor")

left, right = st.columns([1.35, 0.9])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        age = st.number_input("Borrower Age (years)", 18, 100, 35)
        open_loans = st.number_input("Open Loans / Credit Lines", 0, 60, 6)
        re_loans = st.number_input("Real Estate Loans / Mortgages", 0, 30, 1)
        deps = st.number_input("Number of Dependents", 0, 15, 1)
    with c2:
        income = st.number_input("Monthly Income (GBP)", 0.0, 50000.0, 2500.0, step=50.0)
        dti = st.number_input("Debt-to-Income Ratio", 0.0, 10000.0, 0.35, step=0.01)
        util = st.number_input("Credit Utilization Ratio", 0.0, 10000.0, 0.25, step=0.01)
    with c3:
        late_30 = st.number_input("Times 30–59 Days Late (2 yrs)", 0, 100, 0)
        late_60 = st.number_input("Times 60–89 Days Late (2 yrs)", 0, 100, 0)
        late_90 = st.number_input("Times 90+ Days Late (2 yrs)", 0, 100, 0)

    if st.button("Predict risk", use_container_width=True, type="primary"):
        row = {
            "Credit_Utilization_Ratio": float(util),
            "Debt_to_Income_Ratio": float(dti),
            "Monthly_Income": float(income),
            "Borrower_Age": int(age),
            "Open_Loans_Count": int(open_loans),
            "RealEstate_Loans_Count": int(re_loans),
            "Times_30_59DaysLate": int(late_30),
            "Times_60_89DaysLate": int(late_60),
            "Times_90DaysLate": int(late_90),
            "Number_of_Dependents": int(deps),
        }
        X = pd.DataFrame([row])[FEATURES]
        p = float(MODEL.predict_proba(X)[:, 1][0])
        decision = "HIGH_RISK" if p >= THRESH else "LOW_RISK"
        st.metric("Probability of Default", f"{p:.2%}")
        if decision == "HIGH_RISK":
            st.error(f"Decision: {decision} • Threshold: {THRESH:.3f}")
        else:
            st.success(f"Decision: {decision} • Threshold: {THRESH:.3f}")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Feature guide")
    st.markdown('<div class="feature-card">Debt-to-Income (DTI) = total monthly debt payments ÷ monthly gross income.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">Credit Utilization = total credit used ÷ total credit limit.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">Late payments = how many times you were 30/60/90+ days late in the last 24 months.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">Open Loans / Credit Lines = number of active credit accounts.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">Real Estate Loans = number of mortgages or property loans.</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">Dependents = people you support financially (e.g., children).</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
