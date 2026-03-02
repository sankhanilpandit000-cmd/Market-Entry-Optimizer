import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="PharmIntel Pro | Market Entry Intelligence",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS STYLING
# ============================================================================
st.markdown("""
<style>
    * {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0a0e1a 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(124, 58, 237, 0.15));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
    }
    
    .section-header {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.2), transparent);
        border-left: 4px solid #06b6d4;
        padding: 15px 20px;
        margin: 30px 0 20px 0;
        border-radius: 0 12px 12px 0;
    }
    
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 15px 40px rgba(6, 182, 212, 0.15);
    }
    
    .kpi-card.positive { border-top: 3px solid #10b981; }
    .kpi-card.warning { border-top: 3px solid #f59e0b; }
    .kpi-card.negative { border-top: 3px solid #ef4444; }
    .kpi-card.info { border-top: 3px solid #06b6d4; }
    
    .kpi-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f1f5f9;
        line-height: 1.2;
    }
    
    .kpi-change {
        font-size: 0.8rem;
        margin-top: 8px;
    }
    
    .kpi-change.up { color: #10b981; }
    .kpi-change.down { color: #ef4444; }
    
    .alert-box {
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #f59e0b;
    }
    
    .alert-danger {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #ef4444;
    }
    
    .rank-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .score-high { color: #10b981; }
    .score-medium { color: #f59e0b; }
    .score-low { color: #ef4444; }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_score_color(score):
    if score >= 75:
        return "score-high"
    elif score >= 50:
        return "score-medium"
    else:
        return "score-low"

def get_card_class(score):
    if score >= 75:
        return "positive"
    elif score >= 50:
        return "warning"
    else:
        return "negative"

# ============================================================================
# MAIN APP
# ============================================================================

st.markdown("""
<div class="main-header">
    <div class="header-title">💊 PharmIntel Pro</div>
    <div class="header-subtitle">Pharmaceutical Market Entry Intelligence Platform v3.0</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    api_key = st.text_input(
        "Google AI API Key",
        type="password",
        help="Get your API key from aistudio.google.com/app/apikey"
    )
    
    st.markdown("---")
    st.subheader("📋 Product Details")
    
    product_name = st.text_input(
        "Product Name",
        placeholder="e.g., Atorvastatin, Lisinopril",
        help="Brand or generic pharmaceutical name"
    )
    
    therapeutic_area = st.selectbox(
        "Therapeutic Area",
        ["Cardiology", "Oncology", "Immunology", "Infectious Disease", 
         "Neurology", "Dermatology", "Gastroenterology", "Endocrinology", "Other"]
    )
    
    dosage_form = st.selectbox(
        "Dosage Form",
        ["Oral Tablet", "Oral Liquid", "Intravenous", "Injectable", 
         "Transdermal", "Inhaler", "Other"]
    )
    
    primary_markets = st.multiselect(
        "Target Markets",
        ["USA", "EU", "APAC", "LATAM", "MENA", "Africa"],
        default=["USA", "EU", "APAC"]
    )
    
    st.markdown("---")
    st.subheader("📊 Report Options")
    
    include_sections = st.multiselect(
        "Sections to Include",
        [
            "Executive Summary",
            "Market Readiness Index",
            "Emerging Markets Analysis",
            "Competitor Blind Spots",
            "Drug Repurposing Analysis",
            "Formulation Gaps",
            "Financial Viability",
            "Supply Chain Risk",
            "Competitive Landscape",
            "Recommendations"
        ],
        default=[
            "Executive Summary",
            "Market Readiness Index",
            "Financial Viability",
            "Recommendations"
        ]
    )

# ============================================================================
# MAIN CONTENT
# ============================================================================

st.markdown('<div class="section-header"><div class="section-title">📝 Analysis Input</div></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    product_details = st.text_area(
        "Product Context & Market Information",
        placeholder="""Provide details about your pharmaceutical product:
• Current indication(s) and mechanism of action
• Target patient population and disease prevalence
• Current competitive landscape
• Manufacturing capabilities
• Regulatory status (IND, NDA, approved, etc.)
• Pricing strategy and reimbursement considerations
• Any specific market concerns or opportunities""",
        height=150
    )

with col2:
    st.info("""
    **Analysis Ready** ✓
    
    Click 'Generate Report' to receive:
    
    ✓ 15+ KPIs
    ✓ Global Insights
    ✓ Risk Assessment
    ✓ Action Items
    """)

st.markdown("---")

# ============================================================================
# ANALYSIS EXECUTION
# ============================================================================

if st.button("🚀 Generate Comprehensive Report", use_container_width=True, type="primary"):
    
    # Validation
    if not api_key:
        st.error("❌ Please enter your Google AI API Key in the sidebar")
        st.stop()
    
    if not product_name:
        st.error("❌ Please enter a product name")
        st.stop()
    
    if not product_details:
        st.error("❌ Please provide product context and market information")
        st.stop()
    
    # Configure API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
    except Exception as e:
        st.error(f"❌ API Configuration Error: {str(e)}")
        st.stop()
    
    # Enhanced Prompt
    prompt = f"""
    Generate a comprehensive pharmaceutical market entry analysis for:
    
    PRODUCT: {product_name}
    THERAPEUTIC AREA: {therapeutic_area}
    DOSAGE FORM: {dosage_form}
    TARGET MARKETS: {', '.join(primary_markets)}
    
    CONTEXT:
    {product_details}
    
    Return a valid JSON object with this exact structure:
    {{
        "executiveSummary": {{
            "productName": "string",
            "overallRecommendation": "GO / CONDITIONAL / NO-GO",
            "confidenceScore": number,
            "launchTimeline": "string (e.g., Q2 2025)"
        }},
        "marketReadiness": {{
            "topMarkets": [
                {{
                    "rank": 1,
                    "country": "string",
                    "score": number (0-100),
                    "approvalTime": "string",
                    "marketSize": "string"
                }}
            ]
        }},
        "emergingMarkets": {{
            "opportunities": [
                {{
                    "region": "string",
                    "growthRate": number,
                    "competitorPresence": "HIGH/MEDIUM/LOW",
                    "entryRisk": "LOW/MEDIUM/HIGH"
                }}
            ]
        }},
        "competitorBlindSpots": [
            {{
                "location": "string",
                "opportunity": "string",
                "timeWindow": "string"
            }}
        ],
        "drugRepurposing": {{
            "score": number (0-100),
            "opportunities": [
                {{
                    "indication": "string",
                    "viability": number (0-100),
                    "marketPotential": "string"
                }}
            ]
        }},
        "formulationGaps": [
            {{
                "currentFormulation": "string",
                "newOpportunity": "string",
                "saturation": number,
                "marketPotential": "string"
            }}
        ],
        "financial": {{
            "reimbursementProbability": number (0-100),
            "optimalPrice": "string",
            "timeToPeakSales": "string",
            "peakMarketShare": number (0-100),
            "fiveYearROI": "string"
        }},
        "supplyChain": {{
            "apiVulnerability": number (0-100),
            "manufacturingScalability": number (0-100),
            "criticalRisks": ["string"]
        }},
        "competitors": [
            {{
                "name": "string",
                "marketShare": number,
                "threatLevel": "HIGH/MEDIUM/LOW"
            }}
        ],
        "recommendations": {{
            "keySuccessFactors": ["string"],
            "criticalRisks": ["string"],
            "nextSteps": ["string"]
        }}
    }}
    """
    
    # Execute Analysis
    with st.spinner("🔍 Analyzing pharmaceutical market landscape..."):
        try:
            response = model.generate_content(prompt)
            data = json.loads(response.text)
            
            # ============================================================
            # EXECUTIVE SUMMARY
            # ============================================================
            if "Executive Summary" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">📊 Executive Summary</div></div>', unsafe_allow_html=True)
                
                exec_summary = data.get("executiveSummary", {})
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    recommendation = exec_summary.get("overallRecommendation", "N/A")
                    rec_color = "#10b981" if "GO" in recommendation and "NO" not in recommendation else "#f59e0b" if "CONDITIONAL" in recommendation else "#ef4444"
                    
                    st.markdown(f"""
                    <div class="kpi-card {get_card_class(75 if 'GO' in recommendation else 50 if 'CONDITIONAL' in recommendation else 25)}">
                        <div class="kpi-label">Go/No-Go Decision</div>
                        <div class="kpi-value" style="color: {rec_color}; font-size: 1.4rem;">{recommendation}</div>
                        <div class="kpi-change">Strategic recommendation</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    confidence = exec_summary.get("confidenceScore", 0)
                    st.markdown(f"""
                    <div class="kpi-card info">
                        <div class="kpi-label">Confidence Score</div>
                        <div class="kpi-value">{confidence}%</div>
                        <div class="kpi-change">Analysis reliability</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    timeline = exec_summary.get("launchTimeline", "TBD")
                    st.markdown(f"""
                    <div class="kpi-card info">
                        <div class="kpi-label">Recommended Launch</div>
                        <div class="kpi-value" style="font-size: 1.4rem;">{timeline}</div>
                        <div class="kpi-change">Target entry window</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    product = exec_summary.get("productName", product_name)
                    st.markdown(f"""
                    <div class="kpi-card info">
                        <div class="kpi-label">Product</div>
                        <div class="kpi-value" style="font-size: 1.3rem;">{product}</div>
                        <div class="kpi-change">{therapeutic_area}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # MARKET READINESS INDEX
            # ============================================================
            if "Market Readiness Index" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">🌍 Market Readiness Index - Top Priority Countries</div></div>', unsafe_allow_html=True)
                
                market_readiness = data.get("marketReadiness", {})
                top_markets = market_readiness.get("topMarkets", [])
                
                if top_markets:
                    for market in top_markets:
                        rank = market.get("rank", 0)
                        country = market.get("country", "N/A")
                        score = market.get("score", 0)
                        approval = market.get("approvalTime", "N/A")
                        size = market.get("marketSize", "N/A")
                        
                        st.markdown(f"""
                        <div class="rank-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <strong style="font-size: 1.1rem; color: #f1f5f9;">#{rank} {country}</strong><br>
                                    <span style="font-size: 0.85rem; color: #94a3b8;">
                                        ⏱️ Approval: {approval} | 💰 Market: {size}
                                    </span>
                                </div>
                                <div class="kpi-value" style="font-size: 2rem; color: {'#10b981' if score >= 75 else '#f59e0b' if score >= 50 else '#ef4444'};">{score}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # EMERGING MARKETS
            # ============================================================
            if "Emerging Markets Analysis" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">📈 Emerging Market Opportunities</div></div>', unsafe_allow_html=True)
                
                emerging = data.get("emergingMarkets", {})
                opportunities = emerging.get("opportunities", [])
                
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
                
                for idx, opp in enumerate(opportunities[:3]):
                    with cols[idx % 3]:
                        region = opp.get("region", "N/A")
                        growth = opp.get("growthRate", 0)
                        competitor = opp.get("competitorPresence", "N/A")
                        risk = opp.get("entryRisk", "N/A")
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">{region}</div>
                            <div class="kpi-value" style="font-size: 2rem; color: #06b6d4;">{growth}%</div>
                            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">
                                Growth Rate<br>
                                Competitor: {competitor}<br>
                                Risk: {risk}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # COMPETITOR BLIND SPOTS
            # ============================================================
            if "Competitor Blind Spots" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">🎪 Competitor Blind Spot Opportunities</div></div>', unsafe_allow_html=True)
                
                blind_spots = data.get("competitorBlindSpots", [])
                
                for spot in blind_spots:
                    location = spot.get("location", "N/A")
                    opportunity = spot.get("opportunity", "N/A")
                    window = spot.get("timeWindow", "N/A")
                    
                    st.markdown(f"""
                    <div class="alert-box alert-success">
                        <strong>📍 {location}</strong><br>
                        💡 {opportunity}<br>
                        ⏳ Time Window: {window}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # DRUG REPURPOSING
            # ============================================================
            if "Drug Repurposing Analysis" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">🔄 Drug Repurposing Viability</div></div>', unsafe_allow_html=True)
                
                repurposing = data.get("drugRepurposing", {})
                score = repurposing.get("score", 0)
                opportunities = repurposing.get("opportunities", [])
                
                st.markdown(f"""
                <div class="kpi-card {get_card_class(score)}">
                    <div class="kpi-label">Overall Repurposing Score</div>
                    <div class="kpi-value" style="color: {'#10b981' if score >= 75 else '#f59e0b' if score >= 50 else '#ef4444'};">{score}%</div>
                    <div class="kpi-change">Potential to enter secondary indications</div>
                </div>
                """, unsafe_allow_html=True)
                
                if opportunities:
                    st.markdown("**Specific Repurposing Opportunities:**")
                    for opp in opportunities:
                        indication = opp.get("indication", "N/A")
                        viability = opp.get("viability", 0)
                        potential = opp.get("marketPotential", "N/A")
                        
                        st.markdown(f"""
                        <div class="rank-card">
                            <strong>{indication}</strong><br>
                            <span style="font-size: 0.85rem; color: #94a3b8;">
                                Viability: <span class="{get_score_color(viability)}">{viability}%</span> | 
                                Market Potential: {potential}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # FORMULATION GAPS
            # ============================================================
            if "Formulation Gaps" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">🧪 Formulation Innovation Gaps</div></div>', unsafe_allow_html=True)
                
                gaps = data.get("formulationGaps", [])
                
                if gaps:
                    for gap in gaps:
                        current = gap.get("currentFormulation", "N/A")
                        new = gap.get("newOpportunity", "N/A")
                        saturation = gap.get("saturation", 0)
                        potential = gap.get("marketPotential", "N/A")
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div style="margin-bottom: 12px;">
                                <strong style="color: #f1f5f9;">{current} → {new}</strong>
                            </div>
                            <div style="font-size: 0.85rem; color: #94a3b8;">
                                Current Saturation: <span class="{get_score_color(saturation)}">{saturation}%</span><br>
                                New Market Potential: {potential}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # FINANCIAL VIABILITY
            # ============================================================
            if "Financial Viability" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">💰 Financial & Reimbursement Analysis</div></div>', unsafe_allow_html=True)
                
                financial = data.get("financial", {})
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    reimbursement = financial.get("reimbursementProbability", 0)
                    st.markdown(f"""
                    <div class="kpi-card {get_card_class(reimbursement)}">
                        <div class="kpi-label">Reimbursement Probability</div>
                        <div class="kpi-value">{reimbursement}%</div>
                        <div class="kpi-change">Coverage likelihood by major payers</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    price = financial.get("optimalPrice", "N/A")
                    st.markdown(f"""
                    <div class="kpi-card info">
                        <div class="kpi-label">Optimal Launch Price</div>
                        <div class="kpi-value" style="font-size: 1.4rem;">{price}</div>
                        <div class="kpi-change">Recommended entry point</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    roi = financial.get("fiveYearROI", "N/A")
                    st.markdown(f"""
                    <div class="kpi-card positive">
                        <div class="kpi-label">5-Year ROI Projection</div>
                        <div class="kpi-value" style="font-size: 1.4rem;">{roi}</div>
                        <div class="kpi-change">Return on investment</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                timeline = financial.get("timeToPeakSales", "N/A")
                peak_share = financial.get("peakMarketShare", 0)
                
                st.markdown(f"""
                <div class="rank-card">
                    <strong>Sales Trajectory</strong><br>
                    <span style="font-size: 0.85rem; color: #94a3b8;">
                        Time to Peak: {timeline} | Peak Market Share: {peak_share}%
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # SUPPLY CHAIN RISK
            # ============================================================
            if "Supply Chain Risk" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">⚙️ Supply Chain & Operational Risk</div></div>', unsafe_allow_html=True)
                
                supply = data.get("supplyChain", {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    api_vuln = supply.get("apiVulnerability", 0)
                    st.markdown(f"""
                    <div class="kpi-card {get_card_class(100 - api_vuln)}">
                        <div class="kpi-label">API Vulnerability Score</div>
                        <div class="kpi-value">{api_vuln}%</div>
                        <div class="kpi-change">Geopolitical supply risk</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    scalability = supply.get("manufacturingScalability", 0)
                    st.markdown(f"""
                    <div class="kpi-card {get_card_class(scalability)}">
                        <div class="kpi-label">Manufacturing Scalability</div>
                        <div class="kpi-value">{scalability}%</div>
                        <div class="kpi-change">Capacity to meet demand</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                risks = supply.get("criticalRisks", [])
                if risks:
                    st.markdown("**Critical Supply Chain Risks:**")
                    for risk in risks:
                        st.markdown(f"""
                        <div class="alert-box alert-danger">
                            🚨 {risk}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # COMPETITIVE LANDSCAPE
            # ============================================================
            if "Competitive Landscape" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">🏆 Competitive Landscape</div></div>', unsafe_allow_html=True)
                
                competitors = data.get("competitors", [])
                
                for comp in competitors:
                    name = comp.get("name", "N/A")
                    share = comp.get("marketShare", 0)
                    threat = comp.get("threatLevel", "N/A")
                    threat_color = "#ef4444" if "HIGH" in threat else "#f59e0b" if "MEDIUM" in threat else "#10b981"
                    
                    st.markdown(f"""
                    <div class="rank-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="color: #f1f5f9;">{name}</strong><br>
                                <span style="font-size: 0.85rem; color: #94a3b8;">Market Share: {share}%</span>
                            </div>
                            <div style="color: {threat_color}; font-weight: 700;">{threat} THREAT</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
            
            # ============================================================
            # RECOMMENDATIONS
            # ============================================================
            if "Recommendations" in include_sections:
                st.markdown('<div class="section-header"><div class="section-title">📋 Strategic Recommendations & Action Plan</div></div>', unsafe_allow_html=True)
                
                recs = data.get("recommendations", {})
                
                success_factors = recs.get("keySuccessFactors", [])
                if success_factors:
                    st.markdown("**🎯 Key Success Factors:**")
                    for factor in success_factors:
                        st.markdown(f"""
                        <div class="alert-box alert-success">
                            ✓ {factor}
                        </div>
                        """, unsafe_allow_html=True)
                
                risks = recs.get("criticalRisks", [])
                if risks:
                    st.markdown("**⚠️ Critical Risks to Monitor:**")
                    for risk in risks:
                        st.markdown(f"""
                        <div class="alert-box alert-danger">
                            🚨 {risk}
                        </div>
                        """, unsafe_allow_html=True)
                
                next_steps = recs.get("nextSteps", [])
                if next_steps:
                    st.markdown("**🚀 Next Steps & Action Items:**")
                    for idx, step in enumerate(next_steps, 1):
                        st.markdown(f"""
                        <div class="rank-card">
                            <strong>{idx}. {step}</strong>
                        </div>
                        """, unsafe_allow_html=True)
            
            # ============================================================
            # EXPORT OPTIONS
            # ============================================================
            st.markdown("---")
            st.markdown('<div class="section-header"><div class="section-title">📥 Export & Download</div></div>', unsafe_allow_html=True)
            
            report_json = json.dumps(data, indent=2)
            st.download_button(
                label="📊 Download Full Report (JSON)",
                data=report_json,
                file_name=f"PharmIntel_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.success("✅ Analysis Complete! Report generated successfully.")
            
        except json.JSONDecodeError as e:
            st.error(f"❌ Error parsing AI response: {str(e)}")
            st.info("💡 The API returned invalid JSON. Please try again with a refined query.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("💡 Please check your API key and internet connection, then try again.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 20px;">
    <strong>PharmIntel Pro v3.0</strong> | Pharmaceutical Market Entry Intelligence Platform<br>
    Powered by Google Generative AI | © 2025 | For Professional Use Only
</div>
""", unsafe_allow_html=True)
