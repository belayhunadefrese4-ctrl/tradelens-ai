import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="TradeLens AI - Regional Trade & Tariff Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚢 TradeLens AI: Customs & Tariff Engine")
st.markdown("Deterministic trade compliance, AfCFTA duty savings, dynamic variable entry, and secure settlement.")
st.markdown("---")

# ==========================================
# SIDEBAR: SETTLEMENT & GATEWAY
# ==========================================
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
    hs_code = st.text_input("HS Code", value="0901.11")
with col2:
    exw_price = st.number_input("Ex-Works Price ($)", min_value=0.0, value=50000.0, step=500.0)
with col3:
    freight_cost = st.number_input("Freight & Insurance ($)", min_value=0.0, value=3500.0, step=100.0)
with col4:
    vnom_value = st.number_input("Non-Originating Materials (VNOM $)", min_value=0.0, value=15000.0, step=500.0)

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
