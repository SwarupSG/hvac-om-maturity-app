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

# Maturity level definitions
maturity_definitions = {
    "Reactive": "Operations and maintenance are driven by complaints and breakdowns. There are no structured processes for tracking faults or validating corrective actions. Visibility is limited, and decisions are made reactively without long-term planning or root cause consideration.",
    "Self Aware": "The organization has some awareness of recurring issues and begins using basic tools like checklists or logs. Faults are reported inconsistently, and manual processes dominate. Data may exist, but there is no framework to ensure follow-through, collaboration, or governance.",
    "Forward Thinking": "O&M activities are aligned with operational priorities. Faults are systematically tracked and verified, and workflows are defined for teams and vendors. Decisions are increasingly based on structured data and process discipline. Governance mechanisms are emerging, improving visibility and accountability.",
    "Pioneering": "O&M is proactive, collaborative, and continuously improving. Fault resolution is structured, trackable, and integrated across stakeholders. Data—automated or manual—is leveraged holistically to detect, resolve, and prevent faults. Governance is embedded in daily operations, enabling high performance and future readiness."
}

# Maturity Descriptions for Each Dimension and Level
descriptions = {
    "Governance": [
        "Service providers self-govern with no oversight or accountability.",
        "SLAs exist but are inconsistently tracked. Reporting is vendor-defined and not linked to business outcomes.",
        "Governance is reinforced with shared dashboards, task-level tracking, and structured review mechanisms.",
        "Governance is embedded in workflows with verified responsibilities and full accountability across critical tasks."
    ],
    "Outcome Alignment": [
        "O&M tasks are disconnected from building performance or business goals.",
        "Metrics are reported but not actioned; decisions are reactive and outcome linkage is missing.",
        "KPIs guide prioritization; operational decisions are increasingly data-driven and outcome-aligned.",
        "All workflows are designed to deliver measurable outcomes aligned to evolving business priorities."
    ],
    "Fault Detection": [
        "Faults are addressed only after complaints or breakdowns occur.",
        "Visibility is limited to basic inspections and uncoordinated alerts.",
        "Automated detection exists but is siloed; no unified triage or root-cause validation.",
        "Manual and automated detection methods are integrated; root-cause workflows and escalation paths are included."
    ],
    "Knowledge Capture": [
        "No documentation of operational knowledge; reliance on individual experience.",
        "Knowledge is captured informally and not reused consistently across the team.",
        "Knowledge is captured during fieldwork and reused to speed up resolution and train technicians.",
        "Captured insights improve decision-making and continuously evolve workflows and technician readiness."
    ],
    "Process Structure": [
        "No defined workflows; tasks are handled reactively based on individual decisions.",
        "Workflows exist but are inconsistently applied or enforced across teams.",
        "Tasks are digitized, tracked, and standardized through mobile apps and workflows.",
        "Workflows are adaptive and continuously improved using analytics, technician feedback, and fault data."
    ]
}

# Recommendations to Advance Maturity Levels
recommendations = {
    "Governance": [
        "Identify critical preventive and fault resolution tasks and assign verification roles.",
        "Align SLAs with business outcomes and establish routine oversight.",
        "Digitally track all critical O&M tasks and automate compliance checks.",
        "Use governance data to inform predictive risk mitigation and continuous improvement."
    ],
    "Outcome Alignment": [
        "Define business-aligned O&M goals and map top-priority actions.",
        "Use tracked metrics to support decision-making and focus on outcomes.",
        "Link operational KPIs to resource allocation and project planning.",
        "Continuously optimize O&M strategies using AI and evolving performance targets."
    ],
    "Fault Detection": [
        "Introduce fault reporting culture; log issues manually and via inspections.",
        "Consolidate inspection logs and alerts into a unified view.",
        "Combine FDD and manual detection with root-cause validation workflows.",
        "Use detection trends to drive long-term improvements and escalation management."
    ],
    "Knowledge Capture": [
        "Start capturing resolution notes with standard templates.",
        "Use logs to brief new staff and standardize informal knowledge.",
        "Link capture to digital workflows and reuse to improve performance.",
        "Continuously evolve technician guidance through structured learning systems."
    ],
    "Process Structure": [
        "Create checklists and SOPs for key O&M tasks.",
        "Map out workflows and assign ownership for each process step.",
        "Digitize all tasks and support consistency through mobile-first tools.",
        "Refine workflows with predictive fault modeling and technician insights."
    ]
}

# How Polaris Supports Each Dimension at All Levels
polaris_support = {
    "Governance": [
        "Polaris introduces a structured O&M framework tied to business priorities, replacing ad hoc oversight.",
        "Polaris automates SLA tracking and escalations linked to outcome-driven verification.",
        "Polaris drives real-time governance via dashboards, task logs, and accountability loops.",
        "Polaris supports predictive governance through insights into task trends, risk areas, and compliance."
    ],
    "Outcome Alignment": [
        "Polaris maps HVAC tasks to business outcomes using visual dashboards.",
        "Polaris connects O&M actions to tracked KPIs, guiding smarter prioritization.",
        "Polaris analyzes KPI trends and informs operational alignment in real-time.",
        "Polaris adapts task and team focus dynamically using AI-driven goal matching."
    ],
    "Fault Detection": [
        "Polaris enables inspection-based fault logging via mobile, even without BMS data.",
        "Polaris integrates basic and automated alerts into a structured triage platform.",
        "Polaris unifies FDD and manual detection with root-cause validation workflows.",
        "Polaris drives fault lifecycle workflows, assigning causes and tracking escalations."
    ],
    "Knowledge Capture": [
        "Polaris captures knowledge during fault resolution using guided mobile workflows.",
        "Polaris centralizes resolution logs and shares them across users and teams.",
        "Polaris reuses insights to speed up diagnosis and improve technician readiness.",
        "Polaris builds an evolving knowledge base that improves workflows and training."
    ],
    "Process Structure": [
        "Polaris provides templates and checklists to structure routine O&M actions.",
        "Polaris enables consistent workflow execution across teams using mobile guidance.",
        "Polaris digitizes workflows and adapts them using process feedback loops.",
        "Polaris evolves task management dynamically through analytics and technician inputs."
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

# Set up PDF
doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
doc.addPageTemplates([
    PageTemplate(id='WithLogo', frames=frame, onPage=add_product_logo)
])

elements = []

# Cover Page
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
elements.append(Spacer(1, 8))
elements.append(Spacer(1, 12))
elements.append(Spacer(1, 12))
elements.append(Paragraph("<b>Maturity Level Overview</b>", bold_style))
elements.append(Spacer(1, 6))
for level in ["Reactive", "Self Aware", "Forward Thinking", "Pioneering"]:
    elements.append(Paragraph(f"<b>{level}:</b> {maturity_definitions[level]}", normal_style))
    elements.append(Spacer(1, 4))
elements.append(NextPageTemplate('WithLogo'))
elements.append(PageBreak())

# Executive Summary Page
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
