import streamlit as st
from PIL import Image
import pytesseract
import re

# Page Configuration
st.set_page_config(
    page_title="TradeLens AI - Regional Trade & Tariff Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚢 TradeLens AI: Customs & Tariff Engine")
st.markdown("Deterministic trade compliance, AfCFTA duty savings, dynamic document ingestion, and secure settlement.")
st.markdown("---")

# Initialize Session State Variables
if "exw_price" not in st.session_state:
    st.session_state["exw_price"] = 50000.0
if "freight_cost" not in st.session_state:
    st.session_state["freight_cost"] = 3500.0
if "vnom_value" not in st.session_state:
    st.session_state["vnom_value"] = 15000.0
if "hs_code" not in st.session_state:
    st.session_state["hs_code"] = "0901.11"
if "extra_variables" not in st.session_state:
    st.session_state["extra_variables"] = {}

# ==========================================
# SIDEBAR: DOCUMENT UPLOADER & PAYMENT GATEWAY
# ==========================================
st.sidebar.header("📥 Document Ingestion (OCR)")
uploaded_file = st.sidebar.file_uploader("Upload Invoice / Trade Document (PNG/JPG)", type=["png", "jpg", "jpeg"])

def parse_document_text(raw_text):
    exw_match = re.search(r"(?:exw|price|invoice value)\s*[:=]?\s*[\$]?\s*([\d,]+\.?\d*)", raw_text, re.IGNORECASE)
    freight_match = re.search(r"(?:freight|shipping|cif)\s*[:=]?\s*[\$]?\s*([\d,]+\.?\d*)", raw_text, re.IGNORECASE)
    vnom_match = re.search(r"(?:vnom|non-originating|foreign input)\s*[:=]?\s*[\$]?\s*([\d,]+\.?\d*)", raw_text, re.IGNORECASE)
    hs_match = re.search(r"(?:hs code|tariff)\s*[:=]?\s*([\d\.]+)", raw_text, re.IGNORECASE)

    if exw_match:
        st.session_state["exw_price"] = float(exw_match.group(1).replace(",", ""))
    if freight_match:
        st.session_state["freight_cost"] = float(freight_match.group(1).replace(",", ""))
    if vnom_match:
        st.session_state["vnom_value"] = float(vnom_match.group(1).replace(",", ""))
    if hs_match:
        st.session_state["hs_code"] = str(hs_match.group(1))

    lines = raw_text.split("\n")
    for line in lines:
        if ":" in line:
            parts = line.split(":")
            key, val = parts[0].strip(), parts[1].strip()
            if key and val and not any(k in key.lower() for k in ["exw", "freight", "vnom", "hs code"]):
                st.session_state["extra_variables"][key] = val

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Invoice", use_column_width=True)
    try:
        extracted_text = pytesseract.image_to_string(image)
        parse_document_text(extracted_text)
    except Exception:
        pass

# --- PAYMENT METHOD INTEGRATION IN SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.header("💳 Payment & Settlement Options")
payment_method = st.sidebar.selectbox(
    "Select Payment/Transfer Provider", 
    ["Telebirr", "Commercial Bank of Ethiopia (CBE)", "Sendwave (International)", "Remitly"]
)
st.sidebar.caption(f"Selected Gateway: **{payment_method}** ready for certification fee settlement.")
if st.sidebar.button("Process Fee & Unlock Official Stamp"):
    st.sidebar.success(f"Payment request initiated via {payment_method}!")

# ==========================================
# MAIN SECTION: VARIABLES & CALCULATIONS
# ==========================================
st.header("⚙️ 1. Core Trade Variables & Dynamic Expansion")

col1, col2, col3, col4 = st.columns(4)
with col1:
    hs_code = st.text_input("HS Code", value=st.session_state["hs_code"])
with col2:
    exw_price = st.number_input("Ex-Works Price ($)", min_value=0.0, value=st.session_state["exw_price"], step=500.0)
with col3:
    freight_cost = st.number_input("Freight & Insurance ($)", min_value=0.0, value=st.session_state["freight_cost"], step=100.0)
with col4:
    vnom_value = st.number_input("Non-Originating Materials (VNOM $)", min_value=0.0, value=st.session_state["vnom_value"], step=500.0)

# Dynamic Catch-All Extra Fields
if st.session_state["extra_variables"]:
    st.subheader("➕ Automatically Detected Extra Document Fields")
    for key, val in st.session_state["extra_variables"].items():
        st.text_input(f"Extra Variable: {key}", value=val, key=f"dyn_{key}")

# ==========================================
# DETERMINISTIC CALCULATIONS & KPIS
# ==========================================
st.markdown("---")
st.header("📊 2. Deterministic KPI Calculations")

standard_duty_rate = 0.15 
afcfta_duty_rate = 0.00    

cif_valuation = exw_price + freight_cost
standard_duty_payable = cif_valuation * standard_duty_rate
afcfta_duty_payable = cif_valuation * afcfta_duty_rate
total_duty_savings = standard_duty_payable - afcfta_duty_payable

if exw_price > 0:
    origin_compliance_score = max(0.0, (1.0 - (vnom_value / exw_price)) * 100.0)
else:
    origin_compliance_score = 0.0

is_compliant = origin_compliance_score >= 40.0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="CIF Total Valuation", value=f"${cif_valuation:,.2f}")
with kpi2:
    st.metric(label="AfCFTA Duty Savings", value=f"${total_duty_savings:,.2f}", delta="Saved")
with kpi3:
    st.metric(label="Rules of Origin Compliance", value=f"{origin_compliance_score:.1f}%")
with kpi4:
    status_label = "QUALIFIED" if is_compliant else "REVIEW REQUIRED"
    st.metric(label="AfCFTA Eligibility Status", value=status_label)

# ==========================================
# REPORT FORMAT & DOWNLOADABLE FILE
# ==========================================
st.markdown("---")
st.header("📥 3. Official Report Format & Download")

report_content = f"""
==================================================
TRADELENS AI - OFFICIAL TARIFF & COMPLIANCE REPORT
==================================================
1. CORE TRADE VARIABLES:
- HS Code: {hs_code}
- Ex-Works Price: ${exw_price:,.2f}
- Freight & Insurance: ${freight_cost:,.2f}
- Non-Originating Materials (VNOM): ${vnom_value:,.2f}

2. CALCULATED KPIs & COMPLIANCE:
- CIF Total Valuation: ${cif_valuation:,.2f}
- Standard Duty Payable: ${standard_duty_payable:,.2f}
- AfCFTA Preferential Duty: ${afcfta_duty_payable:,.2f}
- Total Estimated Duty Savings: ${total_duty_savings:,.2f}
- Rules of Origin Compliance Score: {origin_compliance_score:.1f}%
- AfCFTA Eligibility Status: {status_label}
- Selected Settlement Gateway: {payment_method}
==================================================
Generated via TradeLens AI Intelligence Engine
"""

st.text_area("Report Preview", value=report_content, height=200)

st.download_button(
    label="📥 Download Official Compliance Report (.txt)",
    data=report_content,
    file_name="tradelens_official_report.txt",
    mime="text/plain"
)
