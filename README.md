# 🔧 HVAC O&M Maturity Diagnostic Tool

This is an interactive Streamlit web app designed to help facilities and operations teams assess and improve the maturity of their HVAC Operations & Maintenance (O&M) practices.

## 🚀 Features

- 📊 Self-assess across 5 key capability dimensions:
  - Governance
  - Outcome Alignment
  - Fault Detection
  - Knowledge Capture
  - Process Structure
- 🧩 Select maturity level (Reactive to Pioneering)
- 📌 Get dynamic, forward-looking recommendations
- 🤖 Learn how Polaris Co-Pilot supports each area
- 📈 View score summaries and maturity insights
- ✅ Clean, mobile-friendly interface via Streamlit

## 📂 App Structure

- **`hvac_maturity_app_level_descriptions_visible.py`**  
  The main app file with visible level definitions for user clarity.

## 🛠 How to Use

1. Visit the live app (hosted on Streamlit Cloud) or run it locally.
2. For each dimension, view the level definitions using the dropdown.
3. Select your current maturity level (1–4).
4. Review your average score and maturity summary.
5. Apply the recommendations and see how Polaris can support your transition.

## ▶️ Running Locally

```bash
pip install streamlit
streamlit run hvac_maturity_app_level_descriptions_visible.py
