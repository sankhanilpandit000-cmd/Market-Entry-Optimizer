import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Pharmaceutical Market Entry Intelligence Platform",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM STYLING ---
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
        font-family: 'Inter', 'Segoe UI', sans-serif;
        min-height: 100vh;
    }
    
    /* Animated background */
    @keyframes pulse {
        0%, 100% { opacity: 0.05; }
        50% { opacity: 0.15; }
    }
    
    .pulse-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        pointer-events: none;
    }
    
    .pulse-circle {
        position: absolute;
        border-radius: 50%;
        filter: blur(100px);
        animation: pulse 6s ease-in-out infinite;
    }
    
    .circle-1 { 
        width: 500px; 
        height: 500px; 
        top: -250px; 
        right: -250px; 
        background: radial-gradient(circle, #00d9ff 0%, transparent 70%);
    }
    
    .circle-2 { 
        width: 500px; 
        height: 500px; 
        bottom: -250px; 
        left: -250px; 
        background: radial-gradient(circle, #7c3aed 0%, transparent 70%);
        animation-delay: 2s;
    }
    
    .circle-3 { 
        width: 600px; 
        height: 600px; 
        top: 50%; 
        left: 50%; 
        background: radial-gradient(circle, #06b6d4 0%, transparent 70%);
        animation-delay: 4s;
    }
    
    /* Header Styling */
    .header-main {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(124, 58, 237, 0.1));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 24px;
        padding: 40px;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d9ff, #06b6d4, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: #cbd5e1;
        font-weight: 500;
    }
    
    .header-meta {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 12px;
    }
    
    /* KPI Grid Styling */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 16px;
        margin-bottom: 30px;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d9ff, #7c3aed);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 217, 255, 0.15);
    }
    
    .kpi-card:hover::before {
        opacity: 1;
    }
    
    .kpi-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #00d9ff;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 900;
        color: #f1f5f9;
        margin-bottom: 8px;
        font-family: 'Courier New', monospace;
    }
    
    .kpi-subtext {
        font-size: 0.8rem;
        color: #cbd5e1;
        line-height: 1.4;
    }
    
    .kpi-trend {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        margin-top: 8px;
    }
    
    .trend-positive { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; }
    .trend-negative { background: rgba(239, 68, 68, 0.2); color: #fca5a5; }
    .trend-neutral { background: rgba(100, 116, 139, 0.2); color: #cbd5e1; }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d9ff, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(0, 217, 255, 0.3);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Infographic Container */
    .infographic-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.7), rgba(30, 41, 59, 0.7));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .infographic-card:hover {
        border-color: rgba(0, 217, 255, 0.4);
        box-shadow: 0 15px 40px rgba(0, 217, 255, 0.1);
    }
    
    /* Matrix/Table Styling */
    .matrix-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        overflow-x: auto;
    }
    
    .matrix-header {
        font-weight: 700;
        color: #00d9ff;
        padding: 12px;
        border-bottom: 2px solid rgba(0, 217, 255, 0.3);
    }
    
    .matrix-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
        padding: 12px 0;
        border-bottom: 1px solid rgba(0, 217, 255, 0.1);
    }
    
    .matrix-cell {
        padding: 12px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 8px;
        color: #cbd5e1;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }
    
    .matrix-cell:hover {
        background: rgba(30, 41, 59, 0.8);
        color: #f1f5f9;
    }
    
    .matrix-highlight {
        background: rgba(0, 217, 255, 0.15);
        border-left: 3px solid #00d9ff;
        color: #00d9ff;
        font-weight: 600;
    }
    
    /* Alert Boxes */
    .alert-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #fca5a5;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #6ee7b7;
    }
    
    .warning-box {
        background: rgba(251, 191, 36, 0.1);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-left: 4px solid #fbbf24;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        color: #fde047;
    }
    
    /* Report Container */
    .report-section {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 217, 255, 0.15);
        border-radius: 16px;
        padding: 28px;
        margin: 20px 0;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 16px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid rgba(0, 217, 255, 0.15);
    }
    
    /* Ranking List */
    .ranking-item {
        background: rgba(30, 41, 59, 0.5);
        border-left: 3px solid #00d9ff;
        padding: 16px;
        margin: 12px 0;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.2s ease;
    }
    
    .ranking-item:hover {
        background: rgba(30, 41, 59, 0.8);
        border-left-color: #06b6d4;
    }
    
    .ranking-badge {
        background: linear-gradient(135deg, #00d9ff, #06b6d4);
        color: #0a0e27;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        flex-shrink: 0;
    }
    
    .ranking-content {
        flex: 1;
    }
    
    .ranking-title {
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 4px;
    }
    
    .ranking-subtitle {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    
    .ranking-score {
        background: rgba(0, 217, 255, 0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        color: #00d9ff;
        font-size: 0.85rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d9ff, #06b6d4) !important;
        color: #0a0e27 !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 14px 32px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 20px rgba(0, 217, 255, 0.3) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 12px 30px rgba(0, 217, 255, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Input Styling */
    input[type="text"], input[type="password"], textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    input[type="text"]:focus, input[type="password"]:focus, textarea:focus {
        border-color: #00d9ff !important;
        box-shadow: 0 0 0 3px rgba(0, 217, 255, 0.1) !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1), rgba(124, 58, 237, 0.1));
        border-radius: 8px;
        border: 1px solid rgba(0, 217, 255, 0.2);
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 217, 255, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Add animated background
st.markdown("""
<div class="pulse-bg">
    <div class="pulse-circle circle-1"></div>
    <div class="pulse-circle circle-2"></div>
    <div class="pulse-circle circle-3"></div>
</div>
""", unsafe_allow_html=True)

# --- MAIN HEADER ---
st.markdown("""
<div class="header-main">
    <div class="header-title">💊 Pharmaceutical Market Entry Intelligence Platform</div>
    <div class="header-subtitle">AI-Powered Global Launch Strategy & Risk Analysis</div>
    <div class="header-meta">📊 Report Generated: """ + datetime.now().strftime("%B %d, %Y • %I:%M %p") + """</div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    api_key = st.text_input("Google AI API Key", type="password", help="Get your key from aistudio.google.com")
    
    st.markdown("---")
    st.subheader("Analysis Parameters")
    
    product_name = st.text_input(
        "Product Name",
        placeholder="e.g., Paracetamol, Atorvastatin",
        help="Brand or generic name"
    )
    
    therapeutic_area = st.selectbox(
        "Therapeutic Area",
        ["Cardiology", "Oncology", "Immunology", "Infectious Disease", "Neurology", "Dermatology", "Gastroenterology", "Other"]
    )
    
    primary_markets = st.multiselect(
        "Primary Target Markets",
        ["USA", "EU", "APAC", "LATAM", "MENA", "Africa"],
        default=["USA", "EU", "APAC"]
    )
    
    dosage_form = st.selectbox(
        "Dosage Form",
        ["Oral Tablet", "Oral Liquid", "Intravenous", "Injectable", "Transdermal", "Other"]
    )
    
    st.markdown("---")
    st.subheader("Report Options")
    
    include_sections = st.multiselect(
        "Include Sections",
        [
            "Executive Summary",
            "Global Market Expansion Analysis",
            "Drug Lifecycle & Innovation",
            "Financial & Reimbursement Analysis",
            "Supply Chain & Operational Risk",
            "Competitive Landscape",
            "Recommendations & Action Items"
        ],
        default=[
            "Executive Summary",
            "Global Market Expansion Analysis",
            "Drug Lifecycle & Innovation",
            "Financial & Reimbursement Analysis",
            "Competitive Landscape",
            "Recommendations & Action Items"
        ]
    )

# --- MAIN CONTENT ---
st.markdown('<div class="section-header">📋 Analysis Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_area(
        "Product Details & Market Context",
        placeholder="""Provide detailed information about your product:
- Current indication(s) and mechanism of action
- Target patient population
- Competitive landscape
- Manufacturing capabilities
- Regulatory status
- Any specific market concerns""",
        height=120
    )

with col2:
    st.markdown("**Analysis Status**")
    st.info("📌 Ready to analyze\nClick 'Generate Report' to start")

st.markdown("---")

# --- ANALYSIS BUTTON ---
if st.button("🚀 Generate Comprehensive Report", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Please enter your Google AI API Key in the sidebar")
    elif not product_name:
        st.error("❌ Please enter a product name")
    elif not query:
        st.error("❌ Please provide product details and market context")
    else:
        # Configure API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Enhanced Prompt with all KPIs
        comprehensive_prompt = f"""
        Generate a comprehensive pharmaceutical market entry analysis for: {product_name}
        
        Product Context:
        - Therapeutic Area: {therapeutic_area}
        - Dosage Form: {dosage_form}
        - Target Markets: {', '.join(primary_markets)}
        - Details: {query}
        
        Return ONLY a valid JSON object with this exact structure:
        {{
            "executiveSummary": {{
                "productName": "string",
                "therapeuticArea": "string",
                "overallRecommendation": "string (RECOMMENDED / CONDITIONAL / NOT RECOMMENDED)",
                "confidenceScore": number (0-100),
                "recommendedLaunchTimeframe": "string (e.g., Q1 2025)"
            }},
            
            "globalExpansion": {{
                "topPriorityMarkets": [
                    {{
                        "rank": number,
                        "country": "string",
                        "marketReadinessScore": number (0-100),
                        "regulatoryApprovalTimeline": "string",
                        "targetPatientPopulation": number,
                        "competitorSaturation": number (0-100),
                        "pricingStrategy": "string",
                        "marketSize": "string (e.g., $1.2B)"
                    }}
                ],
                "emergingMarketOpportunities": [
                    {{
                        "region": "string",
                        "growthRate": "string (e.g., 12% CAGR)",
                        "competitorPresence": "string (HIGH/MEDIUM/LOW)",
                        "entryRisk": "string (LOW/MEDIUM/HIGH)",
                        "potentialMarketSize": "string"
                    }}
                ],
                "competitorBlindSpots": [
                    {{
                        "location": "string",
                        "opportunity": "string",
                        "timeWindow": "string (e.g., 6-12 months)"
                    }}
                ]
            }},
            
            "lifecycleInnovation": {{
                "drugRepurposingScore": number (0-100),
                "repurposingOpportunities": [
                    {{
                        "indication": "string",
                        "viabilityScore": number (0-100),
                        "clinicalEvidence": "string",
                        "marketPotential": "string"
                    }}
                ],
                "formulationGaps": [
                    {{
                        "currentFormulation": "string",
                        "marketSaturation": number (0-100),
                        "newFormulationOpportunity": "string",
                        "developmentTimeline": "string",
                        "estimatedAdditionalMarket": "string"
                    }}
                ],
                "innovationPipeline": "string"
            }},
            
            "financialViability": {{
                "reimbursementProbability": number (0-100),
                "estimatedNegotiationDifficulty": "string (LOW/MEDIUM/HIGH)",
                "optimalPriceRange": {{
                    "minimumViablePrice": "string (e.g., $50/unit)",
                    "maxWillingnessToPayPrice": "string (e.g., $200/unit)",
                    "recommendedLaunchPrice": "string (e.g., $120/unit)"
                }},
                "timeToPeakSalesForecast": "string (e.g., 18-24 months)",
                "projectedPeakMarketShare": number (0-100),
                "genericErosionTimeline": "string (e.g., 8-10 years post-patent)",
                "roi5YearProjection": "string (e.g., 180-220%)"
            }},
            
            "supplyChainRisk": {{
                "apiVulnerabilityScore": number (0-100),
                "criticalIngredientDependencies": [
                    {{
                        "ingredient": "string",
                        "suppliers": number,
                        "geopoliticalRisk": "string (LOW/MEDIUM/HIGH)",
                        "alternativeSourcesAvailable": "string (YES/NO/LIMITED)"
                    }}
                ],
                "manufacturingScalabilityIndex": number (0-100),
                "currentCapacity": "string (e.g., 100M units/year)",
                "projectedDemandCapacity": "string (e.g., 150M units/year)",
                "capacityGap": "string (e.g., 50% surplus or 30% shortfall)",
                "recommendedCMOPartners": ["string"],
                "supplyChainRisks": ["string"]
            }},
            
            "competitiveLandscape": {{
                "directCompetitors": [
                    {{
                        "name": "string",
                        "marketShare": number (0-100),
                        "strengths": ["string"],
                        "weaknesses": ["string"],
                        "threatLevel": "string (HIGH/MEDIUM/LOW)"
                    }}
                ],
                "competitiveAdvantage": ["string"],
                "marketDifferentiation": "string"
            }},
            
            "recommendations": {{
                "goNoGoDecision": "string (GO / CONDITIONAL GO / NO-GO)",
                "keySuccessFactors": ["string"],
                "criticalRisks": ["string"],
                "mitigationStrategies": ["string"],
                "nextStepsActionItems": ["string"],
                "timelineMilestones": ["string"]
            }},
            
            "reportMetadata": {{
                "analysisDate": "string",
                "confidenceLevel": "string (HIGH/MEDIUM/LOW)",
                "dataQuality": "string",
                "disclaimers": "string"
            }}
        }}
        """
        
        with st.spinner("🔍 Analyzing pharmaceutical market landscape..."):
            try:
                response = model.generate_content(comprehensive_prompt)
                data = json.loads(response.text)
                
                # --- EXECUTIVE SUMMARY SECTION ---
                if "Executive Summary" in include_sections:
                    st.markdown('<div class="section-header">📊 Executive Summary</div>', unsafe_allow_html=True)
                    
                    exec_summary = data.get("executiveSummary", {})
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Go/No-Go Decision</div>
                            <div class="kpi-value" style="color: {'#10b981' if exec_summary.get('overallRecommendation') == 'RECOMMENDED' else '#ef4444' if exec_summary.get('overallRecommendation') == 'NOT RECOMMENDED' else '#fbbf24'}">{exec_summary.get('overallRecommendation', 'N/A')}</div>
                            <div class="kpi-subtext">Strategic recommendation based on comprehensive analysis</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Confidence Score</div>
                            <div class="kpi-value">{exec_summary.get('confidenceScore', 0)}%</div>
                            <div class="kpi-subtext">Reliability of analysis based on data quality</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Recommended Launch</div>
                            <div class="kpi-value" style="font-size: 1.8rem;">{exec_summary.get('recommendedLaunchTimeframe', 'TBD')}</div>
                            <div class="kpi-subtext">Optimal market entry window</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Product Name</div>
                            <div class="kpi-value" style="font-size: 1.5rem;">{exec_summary.get('productName', 'N/A')}</div>
                            <div class="kpi-subtext">{therapeutic_area}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # --- GLOBAL EXPANSION SECTION ---
                if "Global Market Expansion Analysis" in include_sections:
                    st.markdown('<div class="section-header">🌍 Global Market Expansion & Penetration</div>', unsafe_allow_html=True)
                    
                    global_exp = data.get("globalExpansion", {})
                    
                    # Top Priority Markets
                    st.markdown("### 🎯 Top 5 Priority Entry Markets")
                    
                    top_markets = global_exp.get("topPriorityMarkets", [])
                    for market in sorted(top_markets, key=lambda x: x.get('marketReadinessScore', 0), reverse=True)[:5]:
                        col1, col2 = st.columns([1, 4])
                        
                        with col1:
                            rank = market.get('rank', 0)
                            score = market.get('marketReadinessScore', 0)
                            st.markdown(f"""
                            <div class="ranking-badge">{rank}</div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="ranking-item">
                                <div class="ranking-content">
                                    <div class="ranking-title">{market.get('country', 'N/A')}</div>
                                    <div class="ranking-subtitle">
                                        📋 Readiness: {score}/100 | 
                                        👥 Patients: {market.get('targetPatientPopulation', 'N/A')} | 
                                        💰 Market Size: {market.get('marketSize', 'N/A')} | 
                                        ⏱️ Approval: {market.get('regulatoryApprovalTimeline', 'N/A')}
                                    </div>
                                </div>
                                <span class="ranking-score">{score}%</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Emerging Market Opportunities
                    st.markdown("### 📈 Emerging Market Growth Opportunities")
                    
                    emerging = global_exp.get("emergingMarketOpportunities", [])
                    
                    if emerging:
                        cols = st.columns(len(emerging[:3]))
                        for idx, market in enumerate(emerging[:3]):
                            with cols[idx]:
                                growth = market.get('growthRate', '0%')
                                color = '#10b981' if 'HIGH' in market.get('competitorPresence', '').upper() else '#fbbf24'
                                
                                st.markdown(f"""
                                <div class="kpi-card">
                                    <div class="kpi-label">{market.get('region', 'N/A')}</div>
                                    <div class="kpi-value" style="font-size: 1.8rem; color: {color};">{growth}</div>
                                    <div class="kpi-subtext">
                                        Growth Rate<br>
                                        Competitor: {market.get('competitorPresence', 'N/A')}<br>
                                        Risk: {market.get('entryRisk', 'N/A')}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                    
                    # Competitor Blind Spots
                    blind_spots = global_exp.get("competitorBlindSpots", [])
                    if blind_spots:
                        st.markdown("### 🎪 Competitor Blind Spot Opportunities")
                        for spot in blind_spots:
                            st.markdown(f"""
                            <div class="success-box">
                                <strong>📍 {spot.get('location', 'N/A')}</strong><br>
                                💡 {spot.get('opportunity', 'N/A')}<br>
                                ⏳ Time Window: {spot.get('timeWindow', 'N/A')}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # --- LIFECYCLE & INNOVATION SECTION ---
                if "Drug Lifecycle & Innovation" in include_sections:
                    st.markdown('<div class="section-header">🧬 Drug Lifecycle & Innovation Strategy</div>', unsafe_allow_html=True)
                    
                    lifecycle = data.get("lifecycleInnovation", {})
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 🔄 Drug Repurposing Potential")
                        
                        repur_score = lifecycle.get('drugRepurposingScore', 0)
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Repurposing Viability</div>
                            <div class="kpi-value">{repur_score}%</div>
                            <div class="kpi-subtext">Potential to enter secondary indications</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        opps = lifecycle.get('repurposingOpportunities', [])
                        for opp in opps:
                            st.markdown(f"""
                            <div class="ranking-item">
                                <div class="ranking-content">
                                    <div class="ranking-title">{opp.get('indication', 'N/A')}</div>
                                    <div class="ranking-subtitle">Evidence: {opp.get('clinicalEvidence', 'N/A')}</div>
                                </div>
                                <span class="ranking-score">{opp.get('viabilityScore', 0)}%</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("### 🔬 Formulation Innovation Gaps")
                        
                        gaps = lifecycle.get('formulationGaps', [])
                        for gap in gaps:
                            current_sat = gap.get('marketSaturation', 0)
                            color = '#ef4444' if current_sat > 80 else '#fbbf24' if current_sat > 50 else '#10b981'
                            
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-label">Formulation Opportunity</div>
                                <div style="font-weight: 700; color: #f1f5f9; margin-bottom: 8px;">{gap.get('currentFormulation', 'N/A')} → {gap.get('newFormulationOpportunity', 'N/A')}</div>
                                <div class="kpi-subtext">
                                    Current Saturation: <span style="color: {color}; font-weight: 700;">{current_sat}%</span><br>
                                    Timeline: {gap.get('developmentTimeline', 'N/A')}<br>
                                    Market Potential: {gap.get('estimatedAdditionalMarket', 'N/A')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # --- FINANCIAL & REIMBURSEMENT SECTION ---
                if "Financial & Reimbursement Analysis" in include_sections:
                    st.markdown('<div class="section-header">💰 Financial & Access Viability</div>', unsafe_allow_html=True)
                    
                    financial = data.get("financialViability", {})
                    
                    # KPI Row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        reimburst = financial.get('reimbursementProbability', 0)
                        color = '#10b981' if reimburst > 70 else '#fbbf24' if reimburst > 40 else '#ef4444'
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Reimbursement Probability</div>
                            <div class="kpi-value" style="color: {color};">{reimburst}%</div>
                            <div class="kpi-subtext">Coverage likelihood by major payers</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        peak_time = financial.get('timeToPeakSalesForecast', 'N/A')
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Time to Peak Sales</div>
                            <div class="kpi-value" style="font-size: 1.8rem;">{peak_time}</div>
                            <div class="kpi-subtext">Post-launch ramp to maximum market share</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        peak_share = financial.get('projectedPeakMarketShare', 0)
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Peak Market Share</div>
                            <div class="kpi-value">{peak_share}%</div>
                            <div class="kpi-subtext">Maximum market penetration forecast</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        roi = financial.get('roi5YearProjection', 'N/A')
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">5-Year ROI Projection</div>
                            <div class="kpi-value" style="font-size: 1.8rem;">{roi}</div>
                            <div class="kpi-subtext">Return on investment estimate</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Pricing Strategy
                    st.markdown("### 💵 Optimal Price Corridor Analysis")
                    
                    pricing = financial.get('optimalPriceRange', {})
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Minimum Viable Price</div>
                            <div class="kpi-value" style="font-size: 2rem; color: #ef4444;">{pricing.get('minimumViablePrice', 'N/A')}</div>
                            <div class="kpi-subtext">Floor price for profitability</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Recommended Launch Price</div>
                            <div class="kpi-value" style="font-size: 2rem; color: #00d9ff;">{pricing.get('recommendedLaunchPrice', 'N/A')}</div>
                            <div class="kpi-subtext">Optimal entry point</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Max Willingness to Pay</div>
                            <div class="kpi-value" style="font-size: 2rem; color: #10b981;">{pricing.get('maxWillingnessToPayPrice', 'N/A')}</div>
                            <div class="kpi-subtext">Ceiling before pushback</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # --- SUPPLY CHAIN RISK SECTION ---
                if "Supply Chain & Operational Risk" in include_sections:
                    st.markdown('<div class="section-header">⚙️ Supply Chain & Operational Risk Assessment</div>', unsafe_allow_html=True)
                    
                    supply = data.get("supplyChainRisk", {})
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        api_risk = supply.get('apiVulnerabilityScore', 0)
                        color = '#ef4444' if api_risk > 70 else '#fbbf24' if api_risk > 40 else '#10b981'
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">API Vulnerability Score</div>
                            <div class="kpi-value" style="color: {color};">{api_risk}%</div>
                            <div class="kpi-subtext">Geopolitical supply risk for active ingredients</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        scalability = supply.get('manufacturingScalabilityIndex', 0)
                        color = '#10b981' if scalability > 70 else '#fbbf24' if scalability > 40 else '#ef4444'
                        
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Manufacturing Scalability</div>
                            <div class="kpi-value" style="color: {color};">{scalability}%</div>
                            <div class="kpi-subtext">Capacity to meet peak demand</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        capacity_gap = supply.get('capacityGap', 'N/A')
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-label">Capacity Status</div>
                            <div class="kpi-value" style="font-size: 1.8rem; color: #fbbf24;">{capacity_gap}</div>
                            <div class="kpi-subtext">Current vs. projected demand</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # API Dependencies
                    st.markdown("### 🔗 Critical Ingredient Dependencies")
                    
                    dependencies = supply.get('criticalIngredientDependencies', [])
                    
                    for dep in dependencies:
                        geopolitical_color = '#ef4444' if 'HIGH' in dep.get('geopoliticalRisk', '').upper() else '#fbbf24' if 'MEDIUM' in dep.get('geopoliticalRisk', '').upper() else '#10b981'
                        
                        st.markdown(f"""
                        <div class="ranking-item">
                            <div class="ranking-content">
                                <div class="ranking-title">{dep.get('ingredient', 'N/A')}</div>
                                <div class="ranking-subtitle">
                                    Suppliers: {dep.get('suppliers', 'N/A')} | 
                                    Risk: <span style="color: {geopolitical_color}; font-weight: 700;">{dep.get('geopoliticalRisk', 'N/A')}</span> | 
                                    Alternatives: {dep.get('alternativeSourcesAvailable', 'N/A')}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Supply Chain Risks
                    risks = supply.get('supplyChainRisks', [])
                    if risks:
                        st.markdown("### ⚠️ Supply Chain Risk Flags")
                        for risk in risks:
                            st.markdown(f"""
                            <div class="alert-box">
                                🚨 {risk}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # --- COMPETITIVE LANDSCAPE SECTION ---
                if "Competitive Landscape" in include_sections:
                    st.markdown('<div class="section-header">🏆 Competitive Landscape Analysis</div>', unsafe_allow_html=True)
                    
                    competitive = data.get("competitiveLandscape", {})
                    
                    st.markdown("### 🎯 Direct Competitors")
                    
                    competitors = competitive.get("directCompetitors", [])
                    
                    for comp in competitors:
                        threat_color = '#ef4444' if 'HIGH' in comp.get('threatLevel', '').upper() else '#fbbf24' if 'MEDIUM' in comp.get('threatLevel', '').upper() else '#10b981'
                        
                        with st.expander(f"📊 {comp.get('name', 'N/A')} | Market Share: {comp.get('marketShare', 0)}%", expanded=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Strengths:**")
                                for strength in comp.get('strengths', []):
                                    st.success(f"✓ {strength}")
                            
                            with col2:
                                st.markdown("**Weaknesses:**")
                                for weakness in comp.get('weaknesses', []):
                                    st.warning(f"✗ {weakness}")
                            
                            st.markdown(f"**Threat Level:** <span style='color: {threat_color}; font-weight: 700;'>{comp.get('threatLevel', 'N/A')}</span>", unsafe_allow_html=True)
                    
                    # Competitive Advantage
                    st.markdown("### 💪 Your Competitive Advantages")
                    
                    advantages = competitive.get("competitiveAdvantage", [])
                    cols = st.columns(len(advantages[:3]))
                    
                    for idx, advantage in enumerate(advantages[:3]):
                        with cols[idx]:
                            st.markdown(f"""
                            <div class="success-box">
                                ✨ {advantage}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                
                # --- RECOMMENDATIONS SECTION ---
                if "Recommendations & Action Items" in include_sections:
                    st.markdown('<div class="section-header">📋 Strategic Recommendations & Action Plan</div>', unsafe_allow_html=True)
                    
                    recs = data.get("recommendations", {})
                    
                    # Go/No-Go Decision
                    go_decision = recs.get('goNoGoDecision', 'CONDITIONAL GO')
                    go_color = '#10b981' if 'GO' in go_decision.upper() and 'NO' not in go_decision.upper() else '#fbbf24' if 'CONDITIONAL' in go_decision.upper() else '#ef4444'
                    
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Final Go/No-Go Decision</div>
                        <div class="kpi-value" style="color: {go_color};">{go_decision}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Key Success Factors
                    st.markdown("### 🎯 Key Success Factors")
                    
                    success_factors = recs.get('keySuccessFactors', [])
                    cols = st.columns(3)
                    
                    for idx, factor in enumerate(success_factors):
                        with cols[idx % 3]:
                            st.markdown(f"""
                            <div class="success-box">
                                ✓ {factor}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Critical Risks
                    st.markdown("### ⚠️ Critical Risks to Monitor")
                    
                    critical_risks = recs.get('criticalRisks', [])
                    for risk in critical_risks:
                        st.markdown(f"""
                        <div class="alert-box">
                            🚨 {risk}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Mitigation Strategies
                    st.markdown("### 🛡️ Risk Mitigation Strategies")
                    
                    mitigations = recs.get('mitigationStrategies', [])
                    for idx, mitigation in enumerate(mitigations, 1):
                        st.markdown(f"""
                        <div class="warning-box">
                            {idx}. {mitigation}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Action Items
                    st.markdown("### 🚀 Next Steps & Action Items")
                    
                    actions = recs.get('nextStepsActionItems', [])
                    
                    for idx, action in enumerate(actions, 1):
                        st.markdown(f"""
                        <div class="ranking-item">
                            <div class="ranking-badge">{idx}</div>
                            <div class="ranking-content">
                                <div class="ranking-title">{action}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Timeline Milestones
                    st.markdown("### 📅 Recommended Timeline & Milestones")
                    
                    milestones = recs.get('timelineMilestones', [])
                    for milestone in milestones:
                        st.markdown(f"""
                        <div class="ranking-item">
                            <div class="gap-dot" style="width: 12px; height: 12px;"></div>
                            <div class="ranking-content">
                                <div class="ranking-title">{milestone}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # --- REPORT METADATA ---
                st.markdown("---")
                st.markdown('<div class="section-header">📄 Report Information</div>', unsafe_allow_html=True)
                
                metadata = data.get("reportMetadata", {})
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Analysis Date</div>
                        <div class="kpi-value" style="font-size: 1.2rem;">{metadata.get('analysisDate', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    confidence = metadata.get('confidenceLevel', 'MEDIUM')
                    conf_color = '#10b981' if 'HIGH' in confidence else '#fbbf24' if 'MEDIUM' in confidence else '#ef4444'
                    
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Confidence Level</div>
                        <div class="kpi-value" style="font-size: 1.8rem; color: {conf_color};">{confidence}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-label">Data Quality</div>
                        <div class="kpi-value" style="font-size: 1.2rem;">{metadata.get('dataQuality', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Disclaimers
                with st.expander("📋 Report Disclaimers & Methodology", expanded=False):
                    st.markdown(f"""
                    {metadata.get('disclaimers', 'N/A')}
                    
                    **Important Notes:**
                    - This analysis is AI-generated and should be reviewed by qualified pharmaceutical professionals
                    - All projections and forecasts are estimates based on available data
                    - Market conditions and regulatory environments are subject to rapid change
                    - Recommend validation with primary market research and expert consultation
                    """)
                
                # Export Option
                st.markdown("---")
                st.markdown("### 📥 Export Report")
                
                report_json = json.dumps(data, indent=2)
                st.download_button(
                    label="📊 Download Full Report (JSON)",
                    data=report_json,
                    file_name=f"Pharma_Market_Analysis_{product_name}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
                
            except json.JSONDecodeError as e:
                st.error(f"❌ Error parsing AI response: {str(e)}")
                st.info("💡 The API may have returned malformed JSON. Please try again with a simpler query.")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please check your API key and try again.")
