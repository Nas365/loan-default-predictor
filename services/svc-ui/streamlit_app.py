import os
import base64
import pathlib
import requests
import streamlit as st
import pandas as pd  


st.set_page_config(page_title="Loan Default Predictor (UK)", page_icon="💳", layout="wide")
API_URL = os.getenv("API_URL", "http://localhost:8080")  



def set_background(image_path: str):
    try:
        img_bytes = pathlib.Path(image_path).read_bytes()
        b64 = base64.b64encode(img_bytes).decode()
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
              background: rgba(0,0,0,0.55);   /* glass overlay so text stays readable */
              border: 1px solid rgba(255,255,255,0.08);
              border-radius: 18px;
              padding: 18px;
              box-shadow: 0 8px 24px rgba(0,0,0,.35);
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        # Fallback: gradient if image missing
        st.markdown(
            """
            <style>
            .stApp {
              background: radial-gradient(1200px 600px at 10% -10%, #0e1a35 0%, #0a1024 35%, #070d1e 60%, #050a18 100%);
              color:#e6eeff;
              font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
            }
            .card {
              background: rgba(255,255,255,0.04);
              border: 1px solid rgba(255,255,255,0.08);
              border-radius: 18px;
              padding: 18px;
              box-shadow: 0 8px 24px rgba(0,0,0,.35);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )



set_background("services/svc-ui/assets/bg.jpg")



st.title("💳 Loan Default Predictor")
st.caption(f"API endpoint: {API_URL}")

left, right = st.columns([1.3, 1])



with st.sidebar:
    st.header("Feature guide")
    st.write("**Debt-to-Income (DTI)** = total **monthly debt payments** ÷ **monthly gross income**.")
    st.write("**Credit Utilization** = **total credit used** ÷ **total credit limit**.")
    st.write("**Late payments** = how many times you were **30/60/90+ days late** in the last **24 months**.")
    st.write("**Open Loans / Credit Lines** = number of active credit accounts.")
    st.write("**Real Estate Loans** = number of mortgages or property loans.")
    st.write("**Dependents** = people you support financially (e.g., children).")



with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input(
            "Borrower Age (years)", 18, 100, 35,
            help="Age of the borrower at application time (years)."
        )
        open_loans = st.number_input(
            "Open Loans / Credit Lines", 0, 60, 6,
            help="Count of currently open credit accounts (cards, loans, etc.)."
        )
        re_loans = st.number_input(
            "Real Estate Loans / Mortgages", 0, 30, 1,
            help="Number of mortgages or other property-related loans."
        )
        deps = st.number_input(
            "Number of Dependents", 0, 15, 1,
            help="People you support financially (children or others)."
        )

    with c2:
        income = st.number_input(
            "Monthly Income (GBP)", 0.0, 50000.0, 2500.0, step=50.0,
            help="Gross monthly income before taxes (in GBP)."
        )
        dti = st.number_input(
            "Debt-to-Income Ratio", 0.0, 10000.0, 0.35, step=0.01,
            help="Monthly debt payments ÷ monthly gross income. Example: £700/£2000 = 0.35."
        )
        util = st.number_input(
            "Credit Utilization Ratio", 0.0, 10000.0, 0.25, step=0.01,
            help="Total credit used ÷ total credit limit. Example: owe £1,250 on £5,000 limit → 0.25."
        )

    with c3:
        late_30 = st.number_input(
            "Times 30–59 Days Late (2 yrs)", 0, 100, 0,
            help="How many times in the last 24 months a payment was 30–59 days late."
        )
        late_60 = st.number_input(
            "Times 60–89 Days Late (2 yrs)", 0, 100, 0,
            help="How many times in the last 24 months a payment was 60–89 days late."
        )
        late_90 = st.number_input(
            "Times 90+ Days Late (2 yrs)", 0, 100, 0,
            help="How many times in the last 24 months a payment was 90+ days late."
        )

    # Predict button
    if st.button("Predict risk", use_container_width=True, type="primary"):
        payload = {
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

        try:
            r = requests.post(f"{API_URL}/predict", json=payload, timeout=15)
            r.raise_for_status()
            out = r.json()
            st.metric("Probability of Default", f"{out['prob_default']:.2%}")
            if out["decision"] == "HIGH_RISK":
                st.error(f"Decision: {out['decision']}  •  Threshold: {out['threshold']:.3f}")
            else:
                st.success(f"Decision: {out['decision']}  •  Threshold: {out['threshold']:.3f}")

            with st.expander("See raw response"):
                st.write(out)

        except requests.exceptions.RequestException as e:
            st.error(f"API error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)



with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("About the model")
    st.write("- XGBoost (tuned); primary metric **PR-AUC** for ~7% default rate.")
    st.write("- Threshold tuned to maximize F1 on validation.")
    st.write("- Top drivers: late payments, utilization, DTI, age.")
    st.markdown("</div>", unsafe_allow_html=True)


