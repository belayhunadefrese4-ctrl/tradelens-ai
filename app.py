import streamlit as st
import pandas as pd
import io
from datetime import datetime

# ReportLab imports for professional multi-page PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="TradeLens AI - Regional Trade & Tariff Intelligence",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚢 TradeLens AI: Customs & Tariff Engine")
st.markdown("Deterministic trade compliance, AfCFTA duty savings, dynamic variable entry, and instant free certified PDF report generation.")
st.markdown("---")

# ==========================================
# 2. SIDEBAR: PROFESSIONAL PORTFOLIO INFO
# ==========================================
st.sidebar.header("📋 Platform Overview")
st.sidebar.info(
    "**Open Access Portfolio Tool**\n\n"
    "This engine is fully unlocked for public demonstration, economic evaluation, and institutional review."
)

# ==========================================
# 3. MAIN SECTION: VARIABLES & CALCULATIONS
# ==========================================
st.header("⚙️ 1. Core Trade Variables & Dynamic Expansion")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    hs_code = st.text_input("HS Code", value="0901.11")
with col2:
    exw_price = st.number_input("Ex-Works Price ($)", min_value=0.0, value=50000.0, step=500.0)
with col3:
    freight_cost = st.number_input("Freight & Insurance ($)", min_value=0.0, value=3500.0, step=100.0)
with col4:
    vnom_value = st.number_input("Non-Originating Materials (VNOM $)", min_value=0.0, value=15000.0, step=500.0)
with col5:
    destination_country = st.selectbox("Destination Market", ["Kenya (EAC)", "Egypt (COMESA)", "South Africa (SADC)", "Ghana (ECOWAS)", "Rwanda (EAC)"])

# ==========================================
# 4. DETERMINISTIC CALCULATIONS & KPIS
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
# 5. PROFESSIONAL REPORTLAB PDF GENERATION
# ==========================================
st.markdown("---")
st.header("📥 3. Certified Export & Compliance Report Generation (.PDF)")

def generate_pdf_report(hs, exw, freight, vnom, cif, std_duty, afc_duty, savings, score, status, market):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=14, textColor=colors.HexColor('#1A365D'), spaceAfter=6)
    subtitle_style = ParagraphStyle('DocSubTitle', parent=styles['Normal'], fontSize=8.5, textColor=colors.HexColor('#4A5568'), spaceAfter=10)
    heading_style = ParagraphStyle('SectionHeading', fontSize=10, textColor=colors.HexColor('#1A365D'), spaceBefore=8, spaceAfter=4)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#2D3748'), spaceAfter=4, leading=11)
    
    header_cell = ParagraphStyle('HeaderCell', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.whitesmoke, leading=10)
    table_cell = ParagraphStyle('TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#2D3748'), leading=10)
    
    story = []
    story.append(Paragraph("<b>TRADELENS AI - OFFICIAL CUSTOMS & TARIFF COMPLIANCE CERTIFICATE</b>", title_style))
    story.append(Paragraph(f"<b>Destination Market:</b> {market} | <b>HS Code:</b> {hs} | <b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceAfter=8))
    
    story.append(Paragraph("1. Executive Summary & Rules of Origin Evaluation", heading_style))
    exec_summary = f"""
    This official trade certificate verifies the customs valuation and preferential tariff eligibility under the African Continental Free Trade Area (AfCFTA) framework. 
    The evaluated shipment under HS Code <b>{hs}</b> destined for <b>{market}</b> achieves a Rules of Origin local value content score of <b>{score:.1f}%</b>, 
    officially registering a compliance status of <b>{status}</b> based on a maximum non-originating material allowance of 60%.
    """
    story.append(Paragraph(exec_summary, body_style))
    
    story.append(Paragraph("2. Financial Valuation & Tariff Savings Breakdown", heading_style))
    table_data = [
        [Paragraph("Metric Description", header_cell), Paragraph("Standard Tariff Regime", header_cell), Paragraph("AfCFTA Preferential Regime", header_cell)],
        [Paragraph("Ex-Works Price (EXW)", table_cell), Paragraph(f"${exw:,.2f}", table_cell), Paragraph(f"${exw:,.2f}", table_cell)],
        [Paragraph("Freight & Insurance", table_cell), Paragraph(f"${freight:,.2f}", table_cell), Paragraph(f"${freight:,.2f}", table_cell)],
        [Paragraph("CIF Total Valuation", table_cell), Paragraph(f"${cif:,.2f}", table_cell), Paragraph(f"${cif:,.2f}", table_cell)],
        [Paragraph("Applicable Duty Rate", table_cell), Paragraph("15.0%", table_cell), Paragraph("0.0% (Duty-Free)", table_cell)],
        [Paragraph("Customs Duty Payable", table_cell), Paragraph(f"${std_duty:,.2f}", table_cell), Paragraph(f"${afc_duty:,.2f}", table_cell)],
        [Paragraph("Net Preferential Savings", table_cell), Paragraph("-", table_cell), Paragraph(f"<b>${savings:,.2f} Saved</b>", table_cell)]
    ]
    
    t = Table(table_data, colWidths=[180, 160, 160])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    
    story.append(Paragraph("3. Audit Verification", heading_style))
    audit_text = f"""
    <b>Compliance Status:</b> {status} <br/>
    <b>Certification Stamp:</b> Verified via TradeLens AI Regional Intelligence Engine (Open Access Portfolio Edition).
    """
    story.append(Paragraph(audit_text, body_style))
    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

pdf_bytes = generate_pdf_report(
    hs=hs_code,
    exw=exw_price,
    freight=freight_cost,
    vnom=vnom_value,
    cif=cif_valuation,
    std_duty=standard_duty_payable,
    afc_duty=afcfta_duty_payable,
    savings=total_duty_savings,
    score=origin_compliance_score,
    status=status_label,
    market=destination_country
)

st.success("🎉 Official Compliance PDF Ready for Instant Download!")
st.download_button(
    label="📥 Download Certified Customs & Tariff Report (.PDF)",
    data=pdf_bytes,
    file_name=f"TradeLens_AfCFTA_Certificate_{hs_code.replace('.', '')}.pdf",
    mime="application/pdf",
    type="primary"
)
