
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import io

# Page setup
st.set_page_config(page_title="HVAC O&M Maturity Diagnostic", layout="wide")

# Show app logo at top left
st.image("https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/app_logo.png", width=150)

# App title and dimensions in same visual style
st.markdown("""
# 🔧 HVAC O&M Maturity Diagnostic Tool Across Five Capability Dimensions  
# Governance | Outcome Alignment | Fault Detection | Knowledge Capture | Process Structure
""")

# Safe text cleaner
def safe_text(text):
    return text.replace("–", "-").replace("•", "*").replace("“", """).replace("”", """).replace("’", "'")

# Define dimensions
dimensions = [
    "Governance",
    "Outcome Alignment",
    "Fault Detection",
    "Knowledge Capture",
    "Process Structure"
]

levels = ["1 - Reactive", "2 - Self Aware", "3 - Forward Thinking", "4 - Pioneering"]


# Define descriptions for each dimension and level
descriptions = {
    "Governance": [
        "Service providers self-govern with no oversight or accountability.",
        "SLAs and KPIs are defined but not consistently enforced; SLAs don’t clearly link with business priorities and outcomes desired; service providers largely self-govern with limited oversight or accountability.",
        "Accountability supported by real-time tracking and shared reporting.",
        "Fully transparent tracking of all preselected high-priority O&M activities, with a proven link to desired outcomes."
    ],
    "Outcome Alignment": [
        "No link between O&M activity and building performance goals.",
        "Metrics are tracked for reporting, but rarely used for action. There is no clear link between metrics and operational outcomes, and no prioritization of effort based on performance goals.",
        "Metrics are reviewed regularly and begin to inform decisions. There is an emerging link between operational KPIs and business outcomes, enabling prioritization and more consistent follow-through.",
        "O&M priorities and actions are selected based on desired business outcomes, then configured into an operating framework that drives governance, fault detection, and knowledge capture."
    ],
    "Fault Detection": [
        "Reactive only; faults noticed after complaints or breakdowns.",
        "Manual inspections and basic alerts provide partial visibility.",
        "FDD exists but limited by data gaps; manual inspections operate separately. No unified fault view.",
        "All detection methods (manual inspection & automated FDD engines) converge into one system; validation and escalation workflow included."
    ],
    "Knowledge Capture": [
        "No capture of building’s operational knowledge. Learning is individual and not retained or reused.",
        "Operational knowledge is captured informally, often by individuals or vendors. No structured method for reuse.",
        "Knowledge is captured during fault resolution and reused for similar cases. Reuse informs training and triage. Mobile interfaces support field capture and retrieval.",
        "Embedded in workflows. All resolutions and insights are systematically captured and reused to guide fault response, inform technician decisions, and continuously improve training."
    ],
    "Process Structure": [
        "No formal process; actions vary by person and urgency.",
        "Some processes exist but are inconsistently applied across teams.",
        "Digital workflows improve consistency, guided by mobile apps for reporting and resolution management.",
        "Intelligent, adaptive workflows—powered by mobile apps for guided fault resolution and technician optimization."
    ]
}

# Define forward-looking recommendations and Polaris support per level
recommendations = {
    "Governance": [
        "Start by defining most important Preventive Maintenance Activities & Faults based on business priorities. Introduce external verification and basic accountability across service providers.",
        "Align most important activities with business priorities. Establish oversight mechanisms and routine performance reviews.",
        "Digitally track assigned faults and resolution activities across all providers. Automate reporting and enforce governance policies.",
        "Maintain transparent, outcome-driven governance. Use data to drive predictive risk control and continuous improvement."
    ],
    "Outcome Alignment": [
        "Define O&M goals linked to business outcomes. Identify priority activities that influence performance.",
        "Prioritize actions using tracked metrics. Map O&M actions to specific business outcomes.",
        "Link KPIs with business decisions. Use outcome metrics to set goals.",
        "Continuously align operations with evolving business goals. Use AI or analytics to optimize priorities."
    ],
    "Fault Detection": [
        "Establish fault reporting culture. Implement manual logs and begin basic inspection routines.",
        "Integrate alerts and logs into one platform. Review fault patterns to plan upgrades.",
        "Unify automated FDD and manual detection with shared validation workflows and triage views.",
        "Continuously optimize detection accuracy and integrate escalations into long-term planning."
    ],
    "Knowledge Capture": [
        "Begin capturing operational knowledge. Introduce templates for resolution logs and review routines.",
        "Standardize structured logging across teams. Begin using logs to train and brief new technicians.",
        "Connect knowledge capture to mobile workflows. Reuse insights to improve resolution speed and training.",
        "Feed captured knowledge into continuous learning systems and advanced technician support tools."
    ],
    "Process Structure": [
        "Create standard O&M checklists and assign responsibilities to promote consistency.",
        "Document workflows. Introduce performance-linked reviews and improve task clarity.",
        "Automate standard processes and enable real-time guidance using mobile apps.",
        "Evolve workflows based on resolution analytics, technician input, and predictive fault models."
    ]
}

polaris_support = {
    "Governance": [
        "Polaris simplifies setup and introduces structured O&M Framework capturing priorities linked to business priorities and outcomes.",
        "Polaris links selected activities with outcomes and automates compliance reviews and escalation tracking.",
        "Polaris enforces compliance through live dashboards and automatic reporting to stakeholders.",
        "Polaris enables predictive governance by analyzing patterns across tasks, SLAs, and fault trends."
    ],
    "Outcome Alignment": [
        "Polaris helps map O&M actions to performance outcomes with visual dashboards and goal alignment.",
        "Polaris connects O&M activities with business priorities using performance-driven dashboards.",
        "Polaris translates KPI trends into actionable insights and aligns team focus with business outcomes.",
        "Polaris continuously aligns O&M tasks with strategic priorities using AI-driven recommendations."
    ],
    "Fault Detection": [
        "Polaris configures HVAC system into a fault framework and enable fault logging from inspections through mobile app."
        "Polaris enables fault logging from inspections through mobile app and automates first-level fault categorization.",
        "Polaris integrates all fault sources and prioritizes fault resolution through a unified triage interface.",
        "Polaris unifies automated and manual fault detection and assigns validated root-causes automatically.",
    ],
    "Knowledge Capture": [
        "Polaris mobile app work flow capture operational knowledge during daily tasks.",
        "Polaris captures and centralizes resolution notes for reuse and supports technician knowledge sharing.",
        "Polaris reuses captured resolutions to improve triage speed and optimize technician guidance.",
        "Polaris evolves its knowledge base with each resolution to enhance technician effectiveness."
    ],
    "Process Structure": [
        "Polaris provides guided workflows to standardize task execution.",
        "Polaris enables consistent workflows across teams via digital tracking and mobile task support.",
        "Polaris digitizes and adapts workflows dynamically based on fault data and process analytics.",
        "Polaris provides intelligent workflow automation and evolves task guidance based on performance feedback."
    ]
}
# Collect input
user_scores = {}
report_data = []

st.subheader("📊 Select Your Current Level for Each Capability")

for dim in dimensions:
    st.subheader(f"🔹 {dim} – What Each Level Means")
    with st.expander("Click to view level definitions"):
        for i in range(4):
            st.markdown(f"**Level {i+1}:** {descriptions[dim][i]}")
    level = st.selectbox(f"Select your level for {dim}", levels, key=dim)
    score = int(level.split(" - ")[0])
    user_scores[dim] = score

# Scoring and results
average_score = sum(user_scores.values()) / len(user_scores)

if average_score == 4:
    maturity = "Pioneering"
elif average_score >= 3:
    maturity = "Forward Thinking"
elif average_score >= 2:
    maturity = "Self Aware"
else:
    maturity = "Reactive"

st.markdown("---")
st.header("🔍 Your Maturity Summary")
st.metric("Average Score", f"{average_score:.2f}")
st.success(f"Overall Maturity Level: **{maturity}**")

st.markdown("---")
st.header("📌 Dimension-Specific Recommendations")

for dim in dimensions:
    i = user_scores[dim] - 1
    st.subheader(f"🔹 {dim}")
    st.write(f"**Next Step:** {recommendations[dim][i]}")
    st.write(f"**How Polaris Helps:** {polaris_support[dim][i]}")
    report_data.append([dim, f"Level {i+1}", recommendations[dim][i], polaris_support[dim][i]])

# Build PDF using Unicode-safe font
st.markdown("### 📥 Download PDF Summary")


pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_left_margin(15)
pdf.set_right_margin(15)

# Cover Page
pdf.add_page()
try:
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 24)
    pdf.cell(0, 80, "", ln=True)
    pdf.cell(0, 15, "HVAC O&M Maturity Diagnostic Report", ln=True, align="C")
    pdf.set_font("DejaVu", "", 14)
    pdf.ln(10)
    pdf.cell(0, 10, f"Overall Maturity Level: {maturity}", ln=True, align="C")
    pdf.cell(0, 10, f"Average Score: {average_score:.2f}", ln=True, align="C")
except Exception as e:
    st.error("⚠️ Unicode font 'DejaVuSans.ttf' not found or failed to load. Please upload it to your GitHub repo.")

# Logo page
pdf.add_page()
pdf.image("app_logo.png", x=165, y=10, w=30)  # Product logo top-right
pdf.set_font("DejaVu", "", 16)
pdf.ln(15)
pdf.cell(0, 10, "HVAC O&M Maturity Diagnostic Summary", ln=True)

pdf.set_font("DejaVu", "", 12)
pdf.ln(5)
pdf.cell(0, 10, f"Average Score: {average_score:.2f}", ln=True)
pdf.cell(0, 10, f"Overall Maturity Level: {maturity}", ln=True)
pdf.ln(10)

for row in report_data:
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 8, f"{row[0]} - {row[1]}", ln=True)
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 6, "Next Step:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 6, safe_text(row[2]))
    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 6, "Polaris Support:", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.multi_cell(0, 6, safe_text(row[3]))
    pdf.ln(4)

# Footer
pdf.set_y(-30)
pdf.set_font("DejaVu", "", 10)
pdf.cell(0, 10, "© 2025 Sustain Synergy Pte. Ltd. All rights reserved.", align="C")
pdf.image("company_logo.png", x=85, w=40)

pdf_output = io.BytesIO()
pdf.output(pdf_output)
base64_pdf = base64.b64encode(pdf_output.getvalue()).decode("utf-8")

# Display and download
st.markdown("### 📥 Download Your Professional PDF Report")
pdf_link = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="HVAC_O&M_Maturity_Report.pdf">📄 Download PDF Report</a>'
st.markdown(pdf_link, unsafe_allow_html=True)
st.markdown("### 👀 Preview PDF Below")
pdf_preview = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
st.markdown(pdf_preview, unsafe_allow_html=True)

pdf_output = io.BytesIO()
pdf.output(pdf_output)
base64_pdf = base64.b64encode(pdf_output.getvalue()).decode("utf-8")

st.markdown("### 📥 Download PDF Summary")
pdf_link = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="HVAC_O&M_Maturity_Summary.pdf">📄 Download PDF Report</a>'
st.markdown(pdf_link, unsafe_allow_html=True)


# Show PDF preview inline
#st.markdown("### 👀 Preview PDF Below")
#pdf_preview = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
#st.markdown(pdf_preview, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.image("https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/company_logo.png", width=220)
st.caption("Built by Sustain Synergy Pte. Ltd.")
