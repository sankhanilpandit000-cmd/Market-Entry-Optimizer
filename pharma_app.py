"""
================================================================================
MARKET ENTRY OPTIMIZATION
Enterprise Pharmaceutical Market Entry Intelligence Platform
Clean, Minimalist Design
================================================================================
"""

import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import numpy as np
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
try:
    st.set_page_config(
        page_title="Market Entry Optimization",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception as e:
    print(f"Page config error: {e}")

# ============================================================================
# CSS STYLING - MINIMALIST & CLEAN
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0f1419 100%);
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* API SLIDER BUTTON */
    .api-slider-btn {
        position: fixed;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        color: white;
        border: none;
        padding: 12px 8px;
        border-radius: 0 8px 8px 0;
        cursor: pointer;
        z-index: 999;
        font-weight: 700;
        transition: all 0.3s ease;
        writing-mode: vertical-rl;
        text-orientation: mixed;
    }
    
    .api-slider-btn:hover {
        padding-left: 15px;
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.3);
    }
    
    /* MAIN HEADER */
    .main-header {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(124, 58, 237, 0.1));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 30px;
        text-align: center;
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1rem;
    }
    
    /* SECTION HEADER */
    .section-header {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.1), transparent);
        border-left: 3px solid #06b6d4;
        padding: 15px 20px;
        margin: 25px 0 15px 0;
        border-radius: 0 8px 8px 0;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 800;
        color: #f1f5f9;
        margin: 0;
    }
    
    /* KPI CARD */
    .kpi-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: rgba(6, 182, 212, 0.4);
        box-shadow: 0 8px 20px rgba(6, 182, 212, 0.1);
        transform: translateY(-2px);
    }
    
    .kpi-label {
        font-size: 0.7rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 900;
        color: #f1f5f9;
        margin-bottom: 8px;
    }
    
    .kpi-subtext {
        font-size: 0.8rem;
        color: #cbd5e1;
    }
    
    /* RANK CARD */
    .rank-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }
    
    /* ALERTS */
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 3px solid #10b981;
        color: #6ee7b7;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    .alert-error {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 3px solid #ef4444;
        color: #fca5a5;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 3px solid #f59e0b;
        color: #fbbf24;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    /* BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 25px rgba(6, 182, 212, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* INPUT */
    input[type="text"], input[type="password"], textarea {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1419 0%, #1a202c 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# API KEY SLIDER STATE
# ============================================================================
if "api_key_modal" not in st.session_state:
    st.session_state.api_key_modal = False

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="main-header">
    <div class="header-title">🚀 Market Entry Optimization</div>
    <div class="header-subtitle">Enterprise Pharmaceutical Market Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# API KEY SLIDER BUTTON & MODAL
# ============================================================================
col1, col2, col3 = st.columns([0.1, 2, 0.1])

with col2:
    if st.button("🔐 API KEY", key="api_btn", use_container_width=False):
        st.session_state.api_key_modal = not st.session_state.api_key_modal

if st.session_state.api_key_modal:
    st.markdown('<div class="section-header"><div class="section-title">🔐 API Configuration</div></div>', unsafe_allow_html=True)
    
    api_key = st.text_input(
        "Google AI API Key",
        type="password",
        placeholder="sk-ant-...",
        key="api_key_input"
    )
    
    if api_key:
        st.success("✅ API Key Connected")
    else:
        st.warning("⚠️ Enter API Key to proceed")
    
    st.markdown("---")
else:
    # Store API key from sidebar if exists
    with st.sidebar:
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            key="sidebar_api_key"
        )

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown('<div class="section-header"><div class="section-title">📝 Analysis Input</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    product_name = st.text_input(
        "Product Name",
        placeholder="e.g., Atorvastatin",
        value=""
    )
    
    product_details = st.text_area(
        "Product Details",
        placeholder="Describe your product...",
        height=100,
        value=""
    )

with col2:
    therapeutic_area = st.selectbox(
        "Therapeutic Area",
        ["Cardiology", "Oncology", "Immunology", "Infectious Disease", 
         "Neurology", "Gastroenterology", "Other"]
    )
    
    dosage_form = st.selectbox(
        "Dosage Form",
        ["Oral Tablet", "Injectable", "Inhalation", "Other"]
    )
    
    primary_markets = st.multiselect(
        "Markets",
        ["USA", "Europe", "APAC", "LATAM"],
        default=["USA", "Europe", "APAC"]
    )

st.markdown("---")

# ============================================================================
# GENERATE REPORT
# ============================================================================
if st.button("🚀 Generate Report", use_container_width=True, type="primary"):
    
    # Get API key
    if st.session_state.api_key_modal:
        api_key_to_use = api_key
    else:
        api_key_to_use = api_key if 'api_key' in locals() else None
    
    # Validation
    if not api_key_to_use:
        st.error("❌ API Key is required. Click 🔐 API KEY button to enter it.")
        st.stop()
    
    if not product_name:
        st.error("❌ Product name is required")
        st.stop()
    
    if not product_details:
        st.error("❌ Product details are required")
        st.stop()
    
    # API Configuration
    try:
        genai.configure(api_key=api_key_to_use)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        st.stop()
    
    # Prompt
    prompt = f"""
    Generate pharmaceutical market entry analysis for {product_name}.
    
    PRODUCT: {product_name}
    THERAPEUTIC AREA: {therapeutic_area}
    DOSAGE FORM: {dosage_form}
    MARKETS: {', '.join(primary_markets)}
    CONTEXT: {product_details}
    
    Return valid JSON:
    {{
        "executiveSummary": {{
            "productName": "{product_name}",
            "overallRecommendation": "GO",
            "confidenceScore": 85,
            "launchTimeline": "Q2 2025"
        }},
        
        "marketReadiness": {{
            "topMarkets": [
                {{"rank": 1, "country": "USA", "readinessScore": 92, "marketSizeUSD": 1200000000}},
                {{"rank": 2, "country": "Germany", "readinessScore": 88, "marketSizeUSD": 950000000}},
                {{"rank": 3, "country": "Japan", "readinessScore": 85, "marketSizeUSD": 1500000000}},
                {{"rank": 4, "country": "Canada", "readinessScore": 82, "marketSizeUSD": 450000000}},
                {{"rank": 5, "country": "Australia", "readinessScore": 78, "marketSizeUSD": 350000000}}
            ]
        }},
        
        "emergingMarkets": {{
            "opportunities": [
                {{"region": "Southeast Asia", "country": "Vietnam", "diseaseBurdenGrowth": 18.5, "marketSizeUSD": 450000000}},
                {{"region": "Latin America", "country": "Brazil", "diseaseBurdenGrowth": 22.3, "marketSizeUSD": 650000000}}
            ]
        }},
        
        "financial": {{
            "reimbursementProbabilityPercent": 82,
            "optimalLaunchPrice": "$2400",
            "fiveYearROIPercent": 185,
            "peakAnnualRevenueUSD": 850000000
        }},
        
        "supplyChain": {{
            "apiVulnerabilityScore": 42,
            "manufacturingScalabilityScore": 88,
            "criticalRisks": ["Regulatory delays", "Supply constraints"]
        }},
        
        "competitors": [
            {{"competitorName": "Competitor A", "marketSharePercent": 28, "threatLevel": "HIGH"}},
            {{"competitorName": "Competitor B", "marketSharePercent": 18, "threatLevel": "MEDIUM"}}
        ],
        
        "recommendations": {{
            "goNoGoDecision": "GO",
            "keySuccessFactors": ["Strong patent protection", "Clear regulatory pathway"],
            "criticalRisks": ["Market saturation", "Pricing pressure"],
            "immediateActionItems": ["Initiate regulatory discussions", "Finalize manufacturing partnerships"]
        }}
    }}
    """
    
    # Execute
    with st.spinner("🔍 Analyzing market..."):
        try:
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                st.error("❌ Empty response from API")
                st.stop()
            
            # Parse JSON
            data = json.loads(response.text)
            
            # ============================================================
            # EXECUTIVE SUMMARY
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">📊 Executive Summary</div></div>', unsafe_allow_html=True)
            
            exec_summary = data.get("executiveSummary", {})
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                recommendation = exec_summary.get("overallRecommendation", "N/A")
                rec_color = "#10b981" if "GO" in recommendation else "#ef4444" if "NO" in recommendation else "#f59e0b"
                
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Decision</div>
                    <div class="kpi-value" style="color: {rec_color}; font-size: 1.6rem;">{recommendation}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                confidence = exec_summary.get("confidenceScore", 0)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Confidence</div>
                    <div class="kpi-value">{confidence}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                timeline = exec_summary.get("launchTimeline", "TBD")
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Launch</div>
                    <div class="kpi-value" style="font-size: 1.4rem;">{timeline}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Product</div>
                    <div class="kpi-value" style="font-size: 1rem;">{product_name}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # MARKET READINESS
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">🌍 Market Readiness</div></div>', unsafe_allow_html=True)
            
            market_readiness = data.get("marketReadiness", {})
            top_markets = market_readiness.get("topMarkets", [])
            
            if top_markets:
                for market in top_markets:
                    rank = market.get("rank", 0)
                    country = market.get("country", "N/A")
                    score = market.get("readinessScore", 0)
                    size = market.get("marketSizeUSD", 0)
                    
                    st.markdown(f"""
                    <div class="rank-card">
                        <strong>#{rank} {country}</strong> | Score: {score}% | Market: ${size/1e9:.2f}B
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # EMERGING MARKETS
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">📈 Emerging Markets</div></div>', unsafe_allow_html=True)
            
            emerging = data.get("emergingMarkets", {})
            opportunities = emerging.get("opportunities", [])
            
            if opportunities:
                cols = st.columns(2)
                for idx, opp in enumerate(opportunities):
                    with cols[idx % 2]:
                        region = opp.get("region", "N/A")
                        country = opp.get("country", "N/A")
                        growth = opp.get("diseaseBurdenGrowth", 0)
                        size = opp.get("marketSizeUSD", 0)
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">{region} • {country}</div>
                            <div class="kpi-value" style="font-size: 1.8rem;">{growth}%</div>
                            <div class="kpi-subtext">Growth | Market: ${size/1e9:.2f}B</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # FINANCIAL
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">💰 Financial Analysis</div></div>', unsafe_allow_html=True)
            
            financial = data.get("financial", {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                reimbursement = financial.get("reimbursementProbabilityPercent", 0)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Reimbursement</div>
                    <div class="kpi-value">{reimbursement}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                price = financial.get("optimalLaunchPrice", "N/A")
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Launch Price</div>
                    <div class="kpi-value" style="font-size: 1.6rem;">{price}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                roi = financial.get("fiveYearROIPercent", 0)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">5-Year ROI</div>
                    <div class="kpi-value">{roi}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # SUPPLY CHAIN
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">⚙️ Supply Chain</div></div>', unsafe_allow_html=True)
            
            supply = data.get("supplyChain", {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                api_risk = supply.get("apiVulnerabilityScore", 0)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">API Vulnerability</div>
                    <div class="kpi-value">{api_risk}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                scalability = supply.get("manufacturingScalabilityScore", 0)
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-label">Scalability</div>
                    <div class="kpi-value">{scalability}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            risks = supply.get("criticalRisks", [])
            if risks:
                for risk in risks:
                    st.markdown(f'<div class="alert-warning">⚠️ {risk}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # COMPETITORS
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">🏆 Competitors</div></div>', unsafe_allow_html=True)
            
            competitors = data.get("competitors", [])
            
            if competitors:
                for comp in competitors:
                    name = comp.get("competitorName", "N/A")
                    share = comp.get("marketSharePercent", 0)
                    threat = comp.get("threatLevel", "N/A")
                    threat_color = "#ef4444" if "HIGH" in threat else "#f59e0b" if "MEDIUM" in threat else "#10b981"
                    
                    st.markdown(f"""
                    <div class="rank-card">
                        <strong>{name}</strong> | Share: {share}% | <span style="color: {threat_color};">Threat: {threat}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # RECOMMENDATIONS
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">📋 Recommendations</div></div>', unsafe_allow_html=True)
            
            recs = data.get("recommendations", {})
            
            decision = recs.get("goNoGoDecision", "CONDITIONAL")
            dec_color = "#10b981" if "GO" in decision else "#ef4444" if "NO" in decision else "#f59e0b"
            
            st.markdown(f"""
            <div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); 
                        border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                <strong style="color: {dec_color};">Decision: {decision}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            success = recs.get("keySuccessFactors", [])
            if success:
                for factor in success:
                    st.markdown(f'<div class="alert-success">✓ {factor}</div>', unsafe_allow_html=True)
            
            risks = recs.get("criticalRisks", [])
            if risks:
                for risk in risks:
                    st.markdown(f'<div class="alert-error">🚨 {risk}</div>', unsafe_allow_html=True)
            
            actions = recs.get("immediateActionItems", [])
            if actions:
                st.markdown("**Actions:**")
                for idx, action in enumerate(actions, 1):
                    st.markdown(f"""
                    <div class="rank-card">
                        <strong>{idx}. {action}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # ============================================================
            # EXPORT
            # ============================================================
            st.markdown('<div class="section-header"><div class="section-title">📥 Export</div></div>', unsafe_allow_html=True)
            
            report_json = json.dumps(data, indent=2)
            st.download_button(
                label="📊 Download Report",
                data=report_json,
                file_name=f"Market_Entry_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.success("✅ Analysis Complete!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 20px;">
    <strong>Market Entry Optimization</strong> | Enterprise Intelligence Platform | © 2025
</div>
""", unsafe_allow_html=True)
