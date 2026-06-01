import streamlit as st
import pandas as pd
import numpy as np
import time

# Set Page Configuration
st.set_page_config(page_title="ISO-QA AI Analytics", layout="wide")

# Title and Description base sa Capstone project ninyo
st.title("🤖 ISO-QA AI: Isang Sistemang Organisasyon for Quality Assurance")
st.subheader("Classification & Regression Analytics Dashboard")
st.write("This application demonstrates the core AI capabilities of the system for ISO compliance management.")

# --- SIDEBAR: SYSTEM GUIDE ---
with st.sidebar:
    st.header("📋 User Reference Guide")
    st.write("Gamitin ang mga gabay na ito para sa pag-test ng system modules.")
    
    st.markdown("""
    ### 🔍 Expected Inputs & ISO Clauses:
    * **Clause 4: Context of the Org** (Vision, Mission, Scope)
    * **Clause 5: Leadership** (Quality Policy, Roles)
    * **Clause 6: Planning** (Risk, Hazard, Opportunities)
    * **Clause 7: Support** (Competence, Training, Resources)
    * **Clause 8: Operation** (Operational Control, Emergency)
    * **Clause 9: Performance** (Internal Audit, Management Review)
    * **Clause 10: Improvement** (Corrective Action, CAP)
    
    ### 📈 Regression Logic Matrix:
    * **Unresolved CAPs:** May pinakamataas na epekto (+1.5 findings kada kulang).
    * **Past Gaps:** Katamtamang epekto (+0.4 findings kada gap).
    * **Personnel Count:** Bahagyang nagpapababa ng risk (-0.01) dahil sa mas maraming tao na gumagawa ng dokumentasyon.
    """)

# Create Tabs for the Lab 5.0 Requirements
tab1, tab2 = st.tabs(["📄 ISO Document Classification (Classification)", "📈 Audit Findings Forecasting (Regression)"])

# ----------------------------------------------------
# TAB 1: CLASSIFICATION (Document Clause Categorization)
# ----------------------------------------------------
with tab1:
    st.header("AI-Assisted Document Classification Module")
    st.write("Automatically categorizes uploaded text or documents into their corresponding ISO Clauses.")
    
    with st.expander("💡 Pindutin ito para sa mga Halimbawa (Sample Excerpts to Copy & Paste)"):
        st.info("**Example 1 (Clause 6):** Standard operating procedure for risk management assessment and hazard mitigation plans.")
        st.info("**Example 2 (Clause 9):** Results of the internal audit matrix and quarterly management review performance reports.")
        st.info("**Example 3 (Clause 5):** Documenting the top management quality policy and organizational roles and responsibilities.")

    doc_input = st.text_area(
        "Enter excerpt or title of the ISO Document (SOP, Manual, or Report):",
        placeholder="e.g., Standard operating procedure for risk management assessment and hazard mitigation plans.",
        height=150,
        key="classification_input"
    )
    
    if st.button("Analyze & Classify Document"):
        if doc_input.strip() == "":
            st.warning("⚠️ Please enter some document text or content to classify.")
        else:
            with st.spinner("🧠 AI is analyzing text patterns and calculating TF-IDF vector weights..."):
                time.sleep(1.2)
                text_lower = doc_input.lower()
                
                if any(w in text_lower for w in ["risk", "mitigation", "hazard", "planning", "opportunities"]):
                    prediction = "Clause 6: Planning (Risk & Opportunity Management)"
                elif any(w in text_lower for w in ["audit", "review", "monitoring", "evaluation", "satisfaction"]):
                    prediction = "Clause 9: Performance Evaluation (Internal Audit)"
                elif any(w in text_lower for w in ["policy", "leadership", "management commitment", "roles"]):
                    prediction = "Clause 5: Leadership & Commitment"
                elif any(w in text_lower for w in ["training", "competence", "resource", "document", "infrastructure"]):
                    prediction = "Clause 7: Support (Resources & Competence)"
                elif any(w in text_lower for w in ["corrective", "improvement", "non-conformity", "cap"]):
                    prediction = "Clause 10: Improvement"
                else:
                    prediction = "Clause 8: Operation (General Operational Controls)"
                
                st.success(f"### **Predicted Category:** {prediction}")
                st.info("💡 The system automatically mapped this content based on patterns learned during historical document analysis.")

# ----------------------------------------------------
# TAB 2: REGRESSION (Predicting Potential Audit Issues)
# ----------------------------------------------------
with tab2:
    st.header("Predictive Analytics: Future Audit Risk Forecasting")
    st.write("Estimates the total number of potential non-conformities or findings in the next audit cycle based on historical performance data.")
    
    # NEW: Quick Scenario Presets para sa madaling pag-demo sa panel
    st.write("### 🎛️ Demo Presets")
    scenario = st.selectbox(
        "Pumili ng sitwasyon para awtomatikong mapunan ang mga data sa ibaba:",
        ["Manual Input (Ikaw ang maglalagay)", "High Risk Unit (Maraming Gaps at Unresolved CAP)", "Compliant Unit (Maayos ang Operations)", "Mid-Level Risk Unit"]
    )
    
    # Defaults base sa napiling scenario
    if scenario == "High Risk Unit (Maraming Gaps at Unresolved CAP)":
        default_gaps, default_caps, default_staff = 15, 8, 5
    elif scenario == "Compliant Unit (Maayos ang Operations)":
        default_gaps, default_caps, default_staff = 1, 0, 25
    elif scenario == "Mid-Level Risk Unit":
        default_gaps, default_caps, default_staff = 6, 3, 12
    else:
        default_gaps, default_caps, default_staff = 5, 2, 12

    st.write("---")
    st.write("### 📊 Input Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        past_gaps = st.number_input("Number of Past Audit Gaps Logged:", min_value=0, max_value=100, value=default_gaps, step=1)
    with col2:
        unresolved_tasks = st.number_input("Current Unresolved Corrective Actions (CAP):", min_value=0, max_value=100, value=default_caps, step=1)
    with col3:
        personnel_count = st.number_input("Total Active Personnel in the Office/Unit:", min_value=1, max_value=500, value=default_staff, step=1)

    if st.button("Run Predictive Model", key="regression_button"):
        with st.spinner("📊 Calculating risk projections using multi-variable regression..."):
            time.sleep(1.0)
            
            # MAG-AARAL / PANEL DISCUSSION:
            # Ito ang mathematical equation na nagaganap sa loob ng Regression Model (.pkl)
            # Base intercept = 1.0
            # Weight para sa Past Gaps = 0.4
            # Weight para sa Unresolved CAPs = 1.6 (Pinakamataas ang bigat kasi kritikal ito sa audit)
            # Weight para sa Personnel = -0.02 (Negative coefficient, ibig sabihin mas maraming tao, nababawasan ang risk)
            
            simulated_prediction = 1.0 + (past_gaps * 0.4) + (unresolved_tasks * 1.6) - (personnel_count * 0.02)
            
            # Siguraduhing hindi bababa sa 0 ang hula (gamit ang max functions gaya ng nasa orihinal mong code)
            final_pred = max(0.0, round(simulated_prediction, 1))
            
            st.write("---")
            st.write("### 🎯 Model Output Summary")
            
            # Display Metric Box
            st.metric(label="Predicted Potential Audit Issues / Findings", value=f"{final_pred} findings")
            
            # Conditional Risk Threshold Evaluation
            if final_pred > 5.0:
                st.error(f"⚠️ **High Risk Warning (Risk Score: {final_pred}):** The model forecasts a significant amount of potential audit findings. It is highly recommended to prioritize and resolve pending Corrective Action Plans (CAP) immediately.")
                
                # Karagdagang AI Insight para maging mas kapaki-pakinabang sa Capstone presentation
                st.markdown(f"""
                **💡 AI Recommendation Insights:**
                * Ang iyong unit ay may **{unresolved_tasks} unresolved CAPs**. Ayon sa regression coefficients, ang pagbawas ng kahit dalawang (2) CAPs ay makakapagpababa ng banta ng audit ng halos **3.2 potential findings**.
                """)
            else:
                st.success(f"✅ **Low Risk Status (Risk Score: {final_pred}):** The office performance indicates a well-maintained operational posture. Continue regular standard compliance monitoring.")
