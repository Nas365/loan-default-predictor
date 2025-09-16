# 💳 Loan Default Predictor

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)  
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-orange.svg)](https://streamlit.io/)  
[![Docker](https://img.shields.io/badge/Docker-Containerization-blue.svg)](https://www.docker.com/)  
[![Heroku](https://img.shields.io/badge/Heroku-Deployed-purple.svg)](https://www.heroku.com/)  
[![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub%20Actions-green.svg)](https://github.com/features/actions)

A machine learning project to predict the probability that a borrower will default on their loan within 90 days.  
This project demonstrates **end-to-end Data Science and MLOps**: data preprocessing, model training, feature engineering, evaluation, containerization, and deployment with CI/CD.



##  Dataset
The dataset was imported from [Kaggle / Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit) and preprocessed in **Google Colab**.  
It contains anonymized borrower records with features such as:

- **Credit Utilization Ratio** (how much credit is used relative to the limit)  
- **Debt-to-Income Ratio (DTI)** (total monthly debt ÷ monthly income)  
- **Monthly Income** (GBP)  
- **Borrower Age**  
- **Open Loans / Credit Lines**  
- **Real Estate Loans / Mortgages**  
- **Late Payments (30, 60, 90+ days in past 2 yrs)**  
- **Number of Dependents**

Target variable:  
- `Default_90Days` (1 = default, 0 = no default)



##  Algorithms
The following algorithms were tested and compared:
- Logistic Regression  
- Random Forest  
- AdaBoost  
- **XGBoost (final selected model)**  

Evaluation metrics:
- **ROC AUC**: 0.869  
- **PR AUC**: 0.406  
- Threshold tuning based on best F1-score

XGBoost was chosen as the production model due to its superior balance of recall and precision.



##  Deployment Journey
Initially, the plan was to split the project into:
- **FastAPI** backend for inference (deployed on AWS App Runner)  
- **Streamlit** frontend (UI)

After facing App Runner integration challenges, the final deployment was simplified to:  
- **Streamlit-only app**  
- Containerized with **Docker**  
- Deployed to **Heroku (Container Stack)**  
- Automated with **GitHub Actions** for CI/CD

Every push to `main` triggers a workflow that rebuilds and redeploys the container automatically.



##  Live Demo
👉 [Loan Default Predictor App](https://loan-default-predictor-45986ae9d37b.herokuapp.com/)  



##  Features (App Guide)
- **User Inputs**: Borrower age, income, debt-to-income ratio, utilization ratio, open loans, late payments, etc.  
- **Model Output**:  
  - **Probability of Default** (e.g. *35% chance of default*)  
  - **Decision** (HIGH_RISK vs. LOW_RISK, based on tuned threshold)

The app also explains each feature in plain terms for better user understanding.



##  Tech Stack
- **Python 3.11**  
- **pandas**, **scikit-learn**, **xgboost**, **joblib**  
- **Streamlit** for the UI  
- **Docker** for containerization  
- **Heroku (container stack)** for hosting  
- **GitHub Actions** for CI/CD automation  



##  Next Steps
- Explore feature importance (XGBoost gain-based)  
- Improve precision by incorporating additional credit bureau features  
- Consider scaling to AWS ECS/ECR for production-grade deployments  



##  Author
Nasir Abubakar  
- 📧 [nasirdansabo10@gmail.com](mailto:nasirdansabo10@gmail.com)  
- 🌐 [LinkedIn](https://linkedin.com/in/nasirdansabo)  
- 💻 [GitHub](https://github.com/Nas365)  


