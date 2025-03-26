import streamlit as st
import pandas as pd
import io
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Frame, PageTemplate, NextPageTemplate
from reportlab.lib.units import inch


# Page setup
st.set_page_config(page_title="HVAC O&M Maturity Diagnostic", layout="wide")
st.image("https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/app_logo.png", width=150)

st.markdown("""
# 🔧 HVAC O&M Maturity Diagnostic Tool Across Five Capability Dimensions  
# Governance | Outcome Alignment | Fault Detection | Knowledge Capture | Process Structure
""")

# Define dimensions and levels
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


def safe_text(text):
    return text.replace("–", "-").replace("•", "*").replace("“", "\"").replace("”", "\"").replace("’", "'")

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

# Calculate maturity
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
    report_data.append([
        dim,
        f"Level {i+1}",
        levels[i],
        descriptions[dim][i],
        recommendations[dim][i],
        descriptions[dim][3],
        polaris_support[dim][i]
    ])

# Generate PDF using ReportLab
st.markdown("### 📅 Download PDF Summary")

buffer = io.BytesIO()

# Define logos
company_logo_url = "https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/company_logo.png"
product_logo_url = "https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/app_logo.png"

# Page template with product logo in top right corner (excluding first page)
def add_product_logo(canvas, doc):
    if doc.page > 1:
        canvas.saveState()
        logo_width = 1.1 * inch
        logo_height = 0.37 * inch
        canvas.drawImage(product_logo_url, A4[0] - logo_width - 30, A4[1] - logo_height - 30,
                         width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
        canvas.restoreState()

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(name='TitleStyle', fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=20)
header_style = styles['Heading2']
normal_style = styles['BodyText']
bold_style = ParagraphStyle(name='BoldStyle', parent=normal_style, fontName='Helvetica-Bold')
dimension_title_style = ParagraphStyle(name='DimensionTitle', fontSize=14, leading=18, fontName='Helvetica-Bold')

# Set up the document and templates
doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
doc.addPageTemplates([
    PageTemplate(id='WithLogo', frames=frame, onPage=add_product_logo)
])

elements = []

# Cover page with company logo (scaled with aspect ratio preserved and capped size)
company_logo = Image(company_logo_url)
max_logo_height = 1.2 * inch
aspect = company_logo.imageWidth / float(company_logo.imageHeight)
company_logo.drawHeight = max_logo_height
company_logo.drawWidth = max_logo_height * aspect
company_logo.hAlign = 'CENTER'
elements.append(company_logo)
elements.append(Spacer(1, 12))
elements.append(Paragraph("<b>HVAC O&M Maturity Diagnostic Summary</b>", title_style))
elements.append(Spacer(1, 12))
elements.append(Paragraph(f"<b>Overall Maturity Level:</b> {maturity}", normal_style))
elements.append(Paragraph(f"<b>Average Score:</b> {average_score:.2f}", normal_style))
elements.append(NextPageTemplate('WithLogo'))
elements.append(PageBreak())

# Executive Summary Section with product logo auto-applied by template
elements.append(Paragraph("<b>Executive Summary</b>", title_style))
elements.append(Spacer(1, 10))

for row in report_data:
    elements.append(Paragraph(f"{row[0]} - {row[1]} ({row[2]})", dimension_title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(f"<b>{row[2]} Definition:</b> {safe_text(row[3])}", normal_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>Next Step:</b> " + safe_text(row[4]), normal_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>What could Pioneering (Level 4) look like?</b>", bold_style))
    elements.append(Paragraph(safe_text(row[5]), normal_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>How Polaris can support you?</b> " + safe_text(row[6]), normal_style))
    elements.append(Spacer(1, 10))

# Finalize PDF
doc.build(elements)
buffer.seek(0)
pdf_data = buffer.read()

pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
pdf_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="HVAC_O&M_Maturity_Report.pdf">📄 Download PDF Report</a>'
st.markdown(pdf_link, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.image("https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/company_logo.png", width=220)
st.caption("Built by Sustain Synergy Pte. Ltd.")
