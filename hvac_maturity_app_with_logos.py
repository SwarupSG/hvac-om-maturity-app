import streamlit as st
import pandas as pd
import io
import base64
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    FrameBreak,
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Frame, PageTemplate, NextPageTemplate
)


# Page setup
st.set_page_config(page_title="HVAC O&M Maturity Diagnostic", layout="wide")
st.image("https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/app_logo.png", width=150)

st.markdown("""
<h2>🔧 HVAC O&M Maturity Diagnostic Tool Across Five Capability Dimensions</h1>
<h4>Governance | Outcome Alignment | Fault Detection | Knowledge Capture | Process Structure</h4>
""", unsafe_allow_html=True)

# Define dimensions and levels
dimensions = [
    "Governance",
    "Outcome Alignment",
    "Fault Detection",
    "Knowledge Capture",
    "Process Structure"
]

levels = ["1 - Reactive", "2 - Self Aware", "3 - Forward Thinking", "4 - Pioneering"]

maturity_definitions = {
    "Reactive": (
        "Operations and maintenance are driven by complaints, equipment breakdowns, or ad-hoc inspections. "
        "There is no structured approach to fault resolution or verification. Faults may go unrecorded, "
        "and corrective actions are undocumented. Visibility is minimal, roles are unclear, and governance is absent."
    ),
    "Self Aware": (
        "Basic awareness of issues begins to take shape through checklists, logs, or manual inspections. "
        "Faults are captured inconsistently and often resolved without follow-up. Some data is available, "
        "but there is no system to link faults to root causes or outcomes. Oversight is informal, and coordination is limited."
    ),
    "Forward Thinking": (
        "O&M activities are linked to operational priorities such as energy efficiency, comfort, and cost control. "
        "Faults and corrective actions are consistently tracked. Workflows are defined across internal teams and vendors, "
        "enabling better collaboration and repeatability. Data is used for decisions, and governance structures begin to ensure accountability."
    ),
    "Pioneering": (
        "O&M is proactive, structured, and outcome-driven. All faults are captured and resolved through guided workflows, "
        "regardless of data availability. Manual and automated inputs converge into a unified resolution framework. "
        "Governance is embedded in daily operations through role-based accountability, real-time tracking, and predictive insights. "
        "Knowledge is captured, reused, and drives continuous improvement, making the building future-ready."
    )
}

# Define descriptions for each dimension and level
descriptions = {
    "Governance": [
        "Service providers operate independently with no formal oversight or tracking.",
        "SLAs exist but are weakly enforced; reporting is inconsistent and lacks connection to business priorities.",
        "Governance supported by role-based responsibilities, digital tracking, and shared dashboards.",
        "Governance is fully embedded across teams through live tracking, structured workflows, and outcome-based oversight."
    ],
    "Outcome Alignment": [
        "No alignment between O&M tasks and business outcomes like energy, comfort, or cost control.",
        "Metrics are reported but rarely drive decisions; priorities remain reactive.",
        "Performance data starts informing task selection and team priorities.",
        "O&M efforts are prioritized based on strategic business drivers—energy efficiency, tenant satisfaction, and operational cost savings."
    ],
    "Fault Detection": [
        "Faults are only addressed after breakdowns or complaints; no structured detection.",
        "Manual inspections exist but are fragmented; alerts are not consistently logged or followed through.",
        "Fault detection includes FDD and manual methods, but insights are siloed with no unified resolution path.",
        "All faults—manual or automated—are captured through a unified platform, with clear categorization and root-cause validation."
    ],
    "Knowledge Capture": [
        "No systematic capture of operational knowledge; problem-solving depends on individual expertise.",
        "Resolution notes are captured inconsistently and often lost with staff turnover.",
        "Knowledge is structured into fault categories and reused to guide future diagnostics and training.",
        "Knowledge is embedded in workflows and evolves dynamically—fueling AI, technician support, and continuous improvement."
    ],
    "Process Structure": [
        "No formal workflows; tasks vary by urgency or technician preference.",
        "Some standard checklists exist but are inconsistently applied across teams and vendors.",
        "Digital workflows and mobile tasking ensure consistency, accountability, and repeatability.",
        "Intelligent, adaptive workflows use real-time data and technician input to continuously improve execution."
    ]
}

# Define forward-looking recommendations and Polaris support per level
recommendations = {
    "Governance": [
        "Identify key O&M tasks tied to business priorities. Start tracking service provider actions independently.",
        "Map SLAs to performance outcomes and use mobile dashboards for oversight.",
        "Implement digital workflows for cross-team accountability and transparent reporting.",
        "Use data trends to predict governance gaps, improve coordination, and enforce proactive oversight."
    ],
    "Outcome Alignment": [
        "Define operational goals—energy, comfort, cost—and assign tasks that impact them.",
        "Use tracked metrics to prioritize work across internal teams and vendors.",
        "Regularly review outcomes and link KPIs to fault and maintenance workflows.",
        "Dynamically align task selection with business goals using analytics and predictive insights."
    ],
    "Fault Detection": [
        "Encourage fault logging culture—use inspections and manual observations to surface issues.",
        "Centralize all fault inputs into one system for tracking and pattern recognition.",
        "Unify BMS, IoT, and manual detection using a structured cause-based framework.",
        "Ensure all faults and root causes are validated, even when automated data is unavailable."
    ],
    "Knowledge Capture": [
        "Introduce resolution logs and guided fault templates to capture site-level insights.",
        "Structure captured knowledge into reusable categories; support onboarding and triage with real examples.",
        "Use captured data in mobile workflows to guide real-time decisions and optimize training.",
        "Leverage insights from every resolution to build AI-ready knowledge bases."
    ],
    "Process Structure": [
        "Standardize key tasks and responsibilities with simple workflows.",
        "Enable mobile execution and reporting for all teams and vendors.",
        "Digitize and monitor workflows in real time to improve reliability and speed.",
        "Continuously refine workflows based on analytics and field feedback."
    ]
}

# Define how Polaris supports each level of maturity
polaris_support = {
    "Governance": [
        "Polaris embeds governance into daily operations using real-time tracking and role-based workflows.",
        "Polaris links SLAs to outcomes and enables compliance tracking through mobile dashboards.",
        "Polaris enforces cross-party accountability with escalation alerts and structured workflows.",
        "Polaris provides predictive oversight through historical fault patterns and SLA performance trends."
    ],
    "Outcome Alignment": [
        "Polaris created an operating frameowork by mapping Maintenance tasks & Faults to key goals—energy savings, tenant comfort, cost efficiency.",
        "Polaris uses business KPIs to prioritize high-impact activities associated with Maintenance and Fault Resolution.",
        "Polaris tracks maintenance proof of work and resolution effectiveness and updates dashboards to reflect impact on performance.",
        "Polaris updated the operating framwork based on evolving business goals and updates Maintenance tasks & Faults priorities."
    ],
    "Fault Detection": [
        "Polaris supports fault detection even without BMS data through mobile inspections and structured guides.",
        "Polaris centralizes & merges manual and automated detection using a fault ontology.",
        "Polaris unifies triage workflows, ensuring all fault causes are captured and prioritized.",
        "Polaris drives root-cause verification through guided workflows and data-driven fault lifecycle tracking."
    ],
    "Knowledge Capture": [
        "Polaris structures building specific fault and resolution knowledge into its operating framework.",
        "Polaris enables centralized resolution tracking for future training and guidance.",
        "Polaris applies captured knowledge to improve triage and resolution speed across teams.",
        "Polaris builds an adaptive, building-specific knowledge base that grows with every resolution."
    ],
    "Process Structure": [
        "Polaris standardizes task execution with guided mobile workflows.",
        "Polaris digitizes and tracks task progress across workgroups and vendors.",
        "Polaris enables dynamic adaptation of workflows using fault data and technician feedback.",
        "Polaris powers intelligent process refinement for efficiency, accountability, and faster resolution on its mobile platform."
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

# Page templates
def cover_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColorRGB(0.7, 0.7, 0.7)
    canvas.setLineWidth(0.5)
    canvas.line(40, 35, A4[0] - 40, 35)
    canvas.setFont("Helvetica", 6)
    canvas.drawCentredString(A4[0] / 2, 25, "© Copyright Sustain Synergy Pte Ltd")
    canvas.restoreState()

def standard_footer_with_logo(canvas, doc):
    canvas.saveState()
    logo_width = 1.1 * inch
    logo_height = 0.37 * inch
    canvas.drawImage(product_logo_url, A4[0] - logo_width - 30, A4[1] - logo_height - 30,
                     width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
    canvas.setFont("Helvetica", 6)
    canvas.drawCentredString(A4[0] / 2, 20, "Confidential | Created by Sustain Synergy Pte Ltd, Singapore")
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
# Removed page templates; handled via build() below

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
elements.append(Spacer(1, 12))
elements.append(Paragraph("<b>Maturity Level Overview</b>", bold_style))
elements.append(Spacer(1, 6))
for level in ["Reactive", "Self Aware", "Forward Thinking", "Pioneering"]:
    elements.append(Paragraph(f"<b>{level}:</b> {maturity_definitions[level]}", normal_style))
    elements.append(Spacer(1, 4))
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
doc.build(elements, onFirstPage=cover_footer, onLaterPages=standard_footer_with_logo)
buffer.seek(0)
pdf_data = buffer.read()

pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
pdf_link = f'<a href="data:application/pdf;base64,{pdf_base64}" download="HVAC_O&M_Maturity_Report.pdf">📄 Download PDF Report</a>'
st.markdown(pdf_link, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.image("https://raw.githubusercontent.com/SwarupSG/hvac-om-maturity-app/main/company_logo.png", width=220)
st.caption("Built by Sustain Synergy Pte. Ltd.")

