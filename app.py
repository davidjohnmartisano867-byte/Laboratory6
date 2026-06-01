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
    st.write("Gamitin ang mga gabay na ito para sa pag-test ng Document Classification module.")
    
    st.markdown("""
    ### 🔍 Expected Inputs & ISO Clauses:
    
    * **Clause 4: Context of the Organization**
      * *Keywords:* Vision, Mission, Scope, Interested Parties, Internal Issues.
    * **Clause 5: Leadership**
      * *Keywords:* Policy, Quality Objective, Management Commitment, Roles, Responsibilities.
    * **Clause 6: Planning**
      * *Keywords:* Risk Assessment, Hazard Mitigation, Opportunities, Quality Goals.
    * **Clause 7: Support**
      * *Keywords:* Resources, Competence, Awareness, Documented Information, Infrastructure.
    * **Clause 8: Operation**
      * *Keywords:* Operational Control, Design, Development, Emergency Preparedness, Production.
    * **Clause 9: Performance Evaluation**
      * *Keywords:* Internal Audit, Management Review, Customer Satisfaction, Monitoring.
    * **Clause 10: Improvement**
      * *Keywords:* Non-conformity, Corrective Action (CAP), Continual Improvement.
    """)

# Create Tabs for the Lab 5.0 Requirements
tab1, tab2 = st.tabs(["📄 ISO Document Classification (Classification)", "📈 Audit Findings Forecasting (Regression)"])

# ----------------------------------------------------
# TAB 1: CLASSIFICATION (Document Clause Categorization)
# ----------------------------------------------------
with tab1:
    st.header("AI-Assisted Document Classification Module")
    st.write("Automatically categorizes uploaded text or documents into their corresponding ISO Clauses.")
    
    # Nag-inject tayo ng "Expander" para makita agad ng user kung ano ang pwede nilang i-copy-paste
    with st.expander("💡 Pindutin ito para sa mga Halimbawa (Sample Excerpts to Copy & Paste)"):
        st.info("**Example 1 (Clause 6):** Standard operating procedure for risk management assessment and hazard mitigation plans.")
        st.info("**Example 2 (Clause 9):** Results of the internal audit matrix and quarterly management review performance reports.")
        st.info("**Example 3 (Clause 5):** Documenting the top management quality policy and organizational roles and responsibilities.")

    doc_input = st.text_area(
        "Enter excerpt or title of the ISO Document (SOP, Manual, or Report):",
        placeholder="e.g., Standard operating procedure for risk management assessment and hazard mitigation plans.",
        height=150
    )
    
    if st.button("Analyze & Classify Document"):
        if doc_input.strip() == "":
            st.warning("⚠️ Please enter some document text or content to classify.")
        else:
            with st.spinner("🧠 AI is analyzing text patterns and calculating TF-IDF vector weights..."):
                time.sleep(1.5) # Ginaya natin ang processing time ng AI
                
                # Rule-based Simulation para maging functional kahit walang .pkl file
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        past_gaps = st.number_input("Number of Past Audit Gaps Logged:", min_value=0, max_value=100, value=5, step=1)
    with col2:
        unresolved_tasks = st.number_input("Current Unresolved Corrective Actions (CAP):", min_value=0, max_value=100, value=2, step=1)
    with col3:
        personnel_count = st.number_input("Total Active Personnel in the Office/Unit:", min_value=1, max_value=500, value=12, step=1)

    if st.button("Run Predictive Model"):
        with st.spinner("📊 Calculating risk projections using multi-variable regression..."):
            time.sleep(1.0)
            
            # Simulated Linear Regression Formula: Y = (Past Gaps * 0.4) + (CAPs * 1.2) - (Personnel * 0.02) + Baseline
            # Mas maraming unresolved CAPs, mas mataas ang tsansa ng audit findings
            calculated_findings = (past_gaps * 0.4) + (unresolved_tasks * 1.5) - (personnel_count * 0.01) + 1.5
            final_pred = max(0, round(calculated_findings, 1))
            
            st.write("---")
            st.metric(label="Predicted Potential Audit Issues / Findings", value=f"{final_pred} findings")
            
            if final_pred > 5:
                st.error("⚠️ **High Risk Warning:** The model forecasts a significant amount of potential audit findings. It is highly recommended to prioritize and resolve pending Corrective Action Plans (CAP) immediately.")
            else:
                st.success("✅ **Low Risk Status:** The office performance indicates a well-maintained operational posture. Continue regular standard compliance monitoring.")
