import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Set Page Configuration
st.set_page_config(page_title="ISO-QA AI Analytics", layout="wide")

# Title and Description base sa Capstone project ninyo
st.title("🤖 ISO-QA AI: Isang Sistemang Organisasyon for Quality Assurance")
st.subheader("Classification & Regression Analytics Dashboard")
st.write("This application demonstrates the core AI capabilities of the system for ISO compliance management.")

# Load Trained Models safely
@st.cache_resource
def load_models():
    try:
        class_model = joblib.load('iso_clause_model.pkl')
        vectorizer = joblib.load('tfidf_vectorizer.pkl')
        reg_model = joblib.load('audit_risk_model.pkl')
        return class_model, vectorizer, reg_model
    except FileNotFoundError:
        st.error("Error: Model files (.pkl) not found. Please ensure 'iso_clause_model.pkl', 'tfidf_vectorizer.pkl', and 'audit_risk_model.pkl' are in the same directory as app.py.")
        return None, None, None

class_model, vectorizer, reg_model = load_models()

# Create Tabs for the Lab 5.0 Requirements
tab1, tab2 = st.tabs(["📄 ISO Document Classification (Classification)", "📈 Audit Findings Forecasting (Regression)"])

# ----------------------------------------------------
# TAB 1: CLASSIFICATION (Document Clause Categorization)
# ----------------------------------------------------
with tab1:
    st.header("AI-Assisted Document Classification Module")
    st.write("Automatically categorizes uploaded text or documents into their corresponding ISO Clauses.")
    
    # Text input field for document sample
    doc_input = st.text_area(
        "Enter excerpt or title of the ISO Document (SOP, Manual, or Report):",
        placeholder="e.g., Standard operating procedure for risk management assessment and hazard mitigation plans.",
        height=150
    )
    
    if st.button("Analyze & Classify Document"):
        if doc_input.strip() == "":
            st.warning("Please enter some document text or content to classify.")
        elif class_model and vectorizer:
            # Vectorize the input text and make a prediction
            vectorized_text = vectorizer.transform([doc_input])
            prediction = class_model.predict(vectorized_text)[0]
            
            st.success(f"### **Predicted Category:** {prediction}")
            st.info("The system automatically mapped this content based on patterns learned during historical document analysis.")
        else:
            st.error("Classification models are missing or failed to load.")

# ----------------------------------------------------
# TAB 2: REGRESSION (Predicting Potential Audit Issues)
# ----------------------------------------------------
with tab2:
    st.header("Predictive Analytics: Future Audit Risk Forecasting")
    st.write("Estimates the total number of potential non-conformities or findings in the next audit cycle based on historical performance data.")
    
    # Layout using columns for structured data entry
    col1, col2, col3 = st.columns(3)
    
    with col1:
        past_gaps = st.number_input("Number of Past Audit Gaps Logged:", min_value=0, max_value=100, value=5, step=1)
    with col2:
        unresolved_tasks = st.number_input("Current Unresolved Corrective Actions (CAP):", min_value=0, max_value=100, value=2, step=1)
    with col3:
        personnel_count = st.number_input("Total Active Personnel in the Office/Unit:", min_value=1, max_value=500, value=12, step=1)

    if st.button("Run Predictive Model"):
        if reg_model:
            # Map input features to a 2D array for the scikit-learn regression model
            input_features = np.array([[past_gaps, unresolved_tasks, personnel_count]])
            prediction_reg = reg_model.predict(input_features)[0]
            
            # Format and round the predicted continuous numerical value
            final_pred = max(0, round(prediction_reg, 1))
            
            st.write("---")
            st.metric(label="Predicted Potential Audit Issues / Findings", value=f"{final_pred} findings")
            
            # Contextual feedback based on risk level
            if final_pred > 5:
                st.error("⚠️ **High Risk Warning:** The model forecasts a significant amount of potential audit findings. It is highly recommended to prioritize and resolve pending Corrective Action Plans (CAP) immediately.")
            else:
                st.success("✅ **Low Risk Status:** The office performance indicates a well-maintained operational posture. Continue regular standard compliance monitoring.")
        else:
            st.error("Regression model is missing or failed to load.")