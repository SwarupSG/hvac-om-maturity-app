
import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="HVAC O&M Maturity Diagnostic", layout="wide")
st.title("🔧 HVAC O&M Maturity Diagnostic Tool")

# Define capability dimensions and options
dimensions = [
    "Governance",
    "Outcome Alignment",
    "Fault Detection",
    "Knowledge Capture",
    "Process Structure"
]

levels = ["1 - Reactive", "2 - Self Aware", "3 - Forward Thinking", "4 - Pioneering"]

# Define forward-looking recommendations and Polaris support per level
recommendations = {
    "Governance": [
        "Define key activities and introduce structured reporting.",
        "Align activities with business outcomes and establish review routines.",
        "Digitally track and enforce priorities across providers.",
        "Use data to drive predictive governance and continuous improvement."
    ],
    "Outcome Alignment": [
        "Define goals and identify priority activities.",
        "Use metrics to connect actions to business results.",
        "Align decisions and investments with performance trends.",
        "Enable continuous alignment with evolving business needs."
    ],
    "Fault Detection": [
        "Train staff to log faults and perform manual checks.",
        "Combine logs and alerts into structured reviews.",
        "Unify FDD and inspections through shared platforms.",
        "Optimize detection using validation, data, and escalation."
    ],
    "Knowledge Capture": [
        "Start documenting actions and learnings.",
        "Standardize how and when knowledge is captured.",
        "Link captured insights to workflows and reuse in training.",
        "Automate knowledge reuse for guidance and optimization."
    ],
    "Process Structure": [
        "Create checklists and assign responsibilities.",
        "Document workflows and ensure consistent execution.",
        "Digitize and guide processes with mobile tools.",
        "Adapt processes using analytics and technician input."
    ]
}

polaris_support = {
    "Governance": [
        "Polaris simplifies tracking and reporting of O&M priorities.",
        "Polaris aligns governance with outcomes using smart dashboards.",
        "Polaris enforces compliance through real-time reporting.",
        "Polaris supports predictive risk governance using trends and insights."
    ],
    "Outcome Alignment": [
        "Polaris maps O&M tasks to business goals.",
        "Polaris links metrics with decisions and actions.",
        "Polaris drives alignment through dashboards and alerts.",
        "Polaris continuously adjusts O&M actions based on evolving targets."
    ],
    "Fault Detection": [
        "Polaris enables logging and structured detection.",
        "Polaris centralizes inspection logs and alerts.",
        "Polaris unifies FDD and inspections with triage tools.",
        "Polaris automates detection optimization and escalations."
    ],
    "Knowledge Capture": [
        "Polaris helps log and reuse daily learnings.",
        "Polaris standardizes capture and makes insights reusable.",
        "Polaris links knowledge to training and technician guidance.",
        "Polaris evolves knowledge continuously for smarter resolution."
    ],
    "Process Structure": [
        "Polaris supports task execution with checklists.",
        "Polaris enforces workflows across all teams.",
        "Polaris digitizes processes using mobile interfaces.",
        "Polaris adapts workflows based on performance data."
    ]
}

# User input collection
user_scores = {}
st.subheader("📊 Select Your Current Level for Each Capability")

for dim in dimensions:
    level = st.selectbox(f"{dim}", levels, key=dim)
    score = int(level.split(" - ")[0])
    user_scores[dim] = score

# Calculate average score
average_score = sum(user_scores.values()) / len(user_scores)

# Determine maturity stage
if average_score == 4:
    maturity = "Pioneering"
elif average_score >= 3:
    maturity = "Forward Thinking"
elif average_score >= 2:
    maturity = "Self Aware"
else:
    maturity = "Reactive"

# Show results
st.markdown("---")
st.header("🔍 Your Maturity Summary")
st.metric("Average Score", f"{average_score:.2f}", help="Based on your selections")
st.success(f"Overall Maturity Level: **{maturity}**")

st.markdown("---")
st.header("📌 Dimension-Specific Recommendations")

for dim in dimensions:
    i = user_scores[dim] - 1
    st.subheader(f"🔹 {dim}")
    st.write(f"**Next Step:** {recommendations[dim][i]}")
    st.write(f"**How Polaris Helps:** {polaris_support[dim][i]}")
