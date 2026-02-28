import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import numpy as np

# --- 1. PAGE SETUP & CUSTOM CSS ---
st.set_page_config(page_title="Market Entry Optimizer", page_icon="📊", layout="wide")

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }
    
    /* Animated background */
    @keyframes pulse {
        0%, 100% { opacity: 0.1; }
        50% { opacity: 0.3; }
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
        filter: blur(80px);
        animation: pulse 4s ease-in-out infinite;
    }
    
    .circle-1 { 
        width: 300px; 
        height: 300px; 
        top: -150px; 
        right: -150px; 
        background: radial-gradient(circle, #06b6d4 0%, transparent 70%);
    }
    
    .circle-2 { 
        width: 300px; 
        height: 300px; 
        bottom: -150px; 
        left: -150px; 
        background: radial-gradient(circle, #ec4899 0%, transparent 70%);
        animation-delay: 1s;
    }
    
    .circle-3 { 
        width: 400px; 
        height: 400px; 
        top: 50%; 
        left: 50%; 
        background: radial-gradient(circle, #8b5cf6 0%, transparent 70%);
        animation-delay: 2s;
    }
    
    /* Glass morphism card */
    .glass-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        background: rgba(30, 41, 59, 0.95);
        border-color: rgba(148, 163, 184, 0.4);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.5);
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #06b6d4 0%, #0ea5e9 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    /* Title styles */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #06b6d4, #0ea5e9, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        text-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #f1f5f9;
        margin-bottom: 24px;
        font-weight: 500;
    }
    
    /* Metric cards */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(139, 92, 246, 0.15));
        border: 2px solid;
        border-radius: 24px;
        padding: 28px;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .metric-card-high {
        border-color: rgba(16, 185, 129, 0.5);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
    }
    
    .metric-card-high:hover {
        box-shadow: 0 0 50px rgba(16, 185, 129, 0.4);
        transform: translateY(-5px);
    }
    
    .metric-card-medium {
        border-color: rgba(245, 158, 11, 0.5);
        box-shadow: 0 0 30px rgba(245, 158, 11, 0.2);
    }
    
    .metric-card-medium:hover {
        box-shadow: 0 0 50px rgba(245, 158, 11, 0.4);
        transform: translateY(-5px);
    }
    
    .metric-card-low {
        border-color: rgba(236, 72, 153, 0.5);
        box-shadow: 0 0 30px rgba(236, 72, 153, 0.2);
    }
    
    .metric-card-low:hover {
        box-shadow: 0 0 50px rgba(236, 72, 153, 0.4);
        transform: translateY(-5px);
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: linear-gradient(135deg, #06b6d4, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
    }
    
    .metric-value {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 16px;
        font-family: 'Courier New', monospace;
    }
    
    .metric-value-high { color: #10b981; }
    .metric-value-medium { color: #f59e0b; }
    .metric-value-low { color: #ec4899; }
    
    .metric-bar {
        width: 100%;
        height: 6px;
        background: rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 12px;
    }
    
    .metric-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1.2s ease-out;
    }
    
    .metric-bar-fill-high { background: linear-gradient(90deg, #10b981, #14b8a6); }
    .metric-bar-fill-medium { background: linear-gradient(90deg, #f59e0b, #ea580c); }
    .metric-bar-fill-low { background: linear-gradient(90deg, #ec4899, #f43f5e); }
    
    .metric-desc {
        font-size: 0.8rem;
        color: #f1f5f9;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 32px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(6, 182, 212, 0.5);
    }
    
    /* Factor item */
    .factor-item {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    
    .factor-item:hover {
        border-color: rgba(6, 182, 212, 0.6);
        background: rgba(15, 23, 42, 0.8);
    }
    
    .factor-name {
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
    }
    
    .factor-score {
        font-size: 0.85rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        font-family: monospace;
    }
    
    .factor-score-high { background: rgba(16, 185, 129, 0.3); color: #6ee7b7; font-weight: 800; }
    .factor-score-medium { background: rgba(245, 158, 11, 0.3); color: #fbbf24; font-weight: 800; }
    .factor-score-low { background: rgba(236, 72, 153, 0.3); color: #f472b6; font-weight: 800; }
    
    .factor-desc {
        font-size: 0.8rem;
        color: #f1f5f9;
        line-height: 1.4;
    }
    
    /* Badge styles */
    .badge-container {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .badge {
        font-size: 0.7rem;
        font-weight: 800;
        padding: 6px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-high { background: rgba(236, 72, 153, 0.4); color: #f472b6; }
    .badge-medium { background: rgba(245, 158, 11, 0.4); color: #fbbf24; }
    .badge-low { background: rgba(16, 185, 129, 0.4); color: #6ee7b7; }
    .badge-blue { background: rgba(6, 182, 212, 0.4); color: #67e8f9; }
    
    /* Gap list */
    .gap-item {
        display: flex;
        gap: 12px;
        margin-bottom: 12px;
        padding: 12px;
        background: rgba(15, 23, 42, 0.4);
        border-radius: 8px;
        border-left: 3px solid #06b6d4;
    }
    
    .gap-dot {
        width: 8px;
        height: 8px;
        background: linear-gradient(135deg, #06b6d4, #0ea5e9);
        border-radius: 50%;
        margin-top: 6px;
        flex-shrink: 0;
    }
    
    .gap-text {
        color: #f1f5f9;
        font-size: 0.95rem;
        line-height: 1.5;
        font-weight: 500;
    }
    
    /* Competitor item */
    .competitor-item {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    .competitor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    
    .competitor-name {
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .competitor-threat {
        font-size: 0.75rem;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 12px;
        text-transform: uppercase;
    }
    
    .competitor-threat-high {
        background: rgba(236, 72, 153, 0.4);
        color: #f472b6;
    }
    
    .competitor-threat-medium {
        background: rgba(245, 158, 11, 0.4);
        color: #fbbf24;
    }
    
    .competitor-threat-low {
        background: rgba(16, 185, 129, 0.4);
        color: #6ee7b7;
    }
    
    .competitor-desc {
        font-size: 0.85rem;
        color: #cbd5e1;
        line-height: 1.5;
    }
    
    /* Innovation grid */
    .innovation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 16px;
        margin-bottom: 30px;
    }
    
    .innovation-card {
        background: linear-gradient(135deg, rgba(217, 119, 6, 0.1), rgba(236, 72, 153, 0.1));
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .innovation-card:hover {
        border-color: rgba(251, 191, 36, 0.6);
        background: linear-gradient(135deg, rgba(217, 119, 6, 0.2), rgba(236, 72, 153, 0.2));
        transform: translateY(-5px);
    }
    
    .innovation-title {
        font-weight: 800;
        color: #fbbf24;
        margin-bottom: 8px;
    }
    
    .innovation-desc {
        font-size: 0.9rem;
        color: #f1f5f9;
        line-height: 1.5;
    }
    
    /* Recommendation grid */
    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 16px;
    }
    
    .recommendation-item {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 12px;
        padding: 16px;
        display: flex;
        gap: 12px;
    }
    
    .recommendation-number {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10b981, #14b8a6);
        color: #0f172a;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .recommendation-text {
        color: #f1f5f9;
        line-height: 1.5;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* Input styling */
    input[type="text"], input[type="password"] {
        background: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #0ea5e9) !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 12px 32px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 30px rgba(6, 182, 212, 0.6) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: #06b6d4 !important;
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

st.markdown('<h1 class="main-title">📊 Market Entry Optimizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Determine the exact optimal moment to launch your product</p>', unsafe_allow_html=True)
st.write("")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Configuration")
    api_key = st.text_input("Enter Google AI Studio API Key:", type="password")

# --- 3. SEARCH & LOGIC ---
query = st.text_input("Describe your product and target market (e.g., 'Paracetamol'):", placeholder="Type here...")

def get_score_level(score):
    if score >= 75:
        return 'high'
    elif score >= 50:
        return 'medium'
    else:
        return 'low'

def get_threat_level(threat_text):
    threat_text = threat_text.lower()
    if 'high' in threat_text:
        return 'high'
    elif 'medium' in threat_text or 'med' in threat_text:
        return 'medium'
    else:
        return 'low'

if st.button("Analyze ➔", type="primary"):
    if not api_key:
        st.error("Please enter your Google AI Studio API Key in the sidebar.")
    elif not query:
        st.warning("Please enter a product description.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"response_mime_type": "application/json"})
        
        prompt = f"""
        Analyze market entry for: '{query}'. Return ONLY valid JSON:
        {{
            "readinessScore": 85,
            "successProbability": 75,
            "optimalWindow": "Q4 2024",
            "windowReason": "Peak market demand with minimal regulatory barriers",
            "factors": [
                {{"name": "Regulatory Compliance", "score": 95, "desc": "All major certifications achievable within 4 months"}},
                {{"name": "Market Demand", "score": 88, "desc": "Growing segment with CAGR of 12% annually"}},
                {{"name": "Price Sensitivity", "score": 72, "desc": "Moderate price elasticity in target demographic"}}
            ],
            "gaps": ["Gap 1: Limited local distribution networks", "Gap 2: Need for regional partnerships", "Gap 3: Supply chain vulnerabilities"],
            "competitors": [
                {{"name": "Competitor A", "threat": "HIGH", "desc": "Established brand with 40% market share and aggressive pricing"}},
                {{"name": "Competitor B", "threat": "MEDIUM", "desc": "Growing player focusing on premium segment"}}
            ],
            "innovations": [
                {{"title": "Advanced Formulation", "impact": "HIGH", "desc": "Unique delivery mechanism improving absorption by 35%"}},
                {{"title": "Sustainable Packaging", "impact": "MEDIUM", "desc": "Eco-friendly materials reducing environmental impact"}}
            ],
            "recs": ["Build strategic partnerships with major distributors", "Invest in targeted digital marketing", "Secure early regulatory approvals"]
        }}
        """
        
        with st.spinner(f"Processing '{query}' with Market Intelligence AI..."):
            try:
                response = model.generate_content(prompt)
                data = json.loads(response.text)
                
                # --- ROW 1: TOP METRICS ---
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    level = get_score_level(data['readinessScore'])
                    st.markdown(f"""
                    <div class="metric-card metric-card-{level}">
                        <div class="metric-label">📈 Market Readiness</div>
                        <div class="metric-value metric-value-{level}">{data['readinessScore']}</div>
                        <div class="metric-bar">
                            <div class="metric-bar-fill metric-bar-fill-{level}" style="width: {data['readinessScore']}%"></div>
                        </div>
                        <div class="metric-desc">Overall market readiness score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    level = get_score_level(data['successProbability'])
                    st.markdown(f"""
                    <div class="metric-card metric-card-{level}">
                        <div class="metric-label">🎯 Success Rate</div>
                        <div class="metric-value metric-value-{level}">{data['successProbability']}%</div>
                        <div class="metric-bar">
                            <div class="metric-bar-fill metric-bar-fill-{level}" style="width: {data['successProbability']}%"></div>
                        </div>
                        <div class="metric-desc">Est. probability of successful launch</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card metric-card-high">
                        <div class="metric-label">📅 Optimal Window</div>
                        <div class="metric-value metric-value-high" style="font-size: 2.5rem;">{data['optimalWindow']}</div>
                        <div class="metric-desc">{data['windowReason']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
                
                # --- ROW 2: FACTORS & CHART ---
                st.markdown('<h2 class="section-title">⚡ Key Market Factors</h2>', unsafe_allow_html=True)
                
                col_factors = st.columns(1)[0]
                with col_factors:
                    for factor in data.get('factors', []):
                        level = get_score_level(factor['score'])
                        st.markdown(f"""
                        <div class="factor-item">
                            <div class="factor-name">
                                <span>{factor['name']}</span>
                                <span class="factor-score factor-score-{level}">{factor['score']}/100</span>
                            </div>
                            <div class="factor-desc">{factor['desc']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.write("")
                
                # --- ROW 3: GAPS & COMPETITORS ---
                col_gaps, col_comp = st.columns(2)
                
                with col_gaps:
                    st.markdown('<h2 class="section-title">🔍 Market Gaps</h2>', unsafe_allow_html=True)
                    for gap in data.get('gaps', []):
                        st.markdown(f"""
                        <div class="gap-item">
                            <div class="gap-dot"></div>
                            <div class="gap-text">{gap}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col_comp:
                    st.markdown('<h2 class="section-title">🏢 Competitor Landscape</h2>', unsafe_allow_html=True)
                    for competitor in data.get('competitors', []):
                        threat_level = get_threat_level(competitor['threat'])
                        st.markdown(f"""
                        <div class="competitor-item">
                            <div class="competitor-header">
                                <div class="competitor-name">{competitor['name']}</div>
                                <div class="competitor-threat competitor-threat-{threat_level}">{competitor['threat']}</div>
                            </div>
                            <div class="competitor-desc">{competitor['desc']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.write("")
                
                # --- ROW 4: INNOVATIONS ---
                st.markdown('<h2 class="section-title">💡 Recommended Innovations</h2>', unsafe_allow_html=True)
                st.markdown('<div class="innovation-grid">', unsafe_allow_html=True)
                
                for innovation in data.get('innovations', []):
                    st.markdown(f"""
                    <div class="innovation-card">
                        <div class="badge-container">
                            <span class="badge badge-blue">{innovation['impact']} IMPACT</span>
                        </div>
                        <div class="innovation-title">{innovation['title']}</div>
                        <div class="innovation-desc">{innovation['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")
                
                # --- ROW 5: RECOMMENDATIONS ---
                st.markdown('<h2 class="section-title">✅ Strategic Recommendations</h2>', unsafe_allow_html=True)
                st.markdown('<div class="recommendation-grid">', unsafe_allow_html=True)
                
                for idx, rec in enumerate(data.get('recs', []), 1):
                    st.markdown(f"""
                    <div class="recommendation-item">
                        <div class="recommendation-number">{idx}</div>
                        <div class="recommendation-text">{rec}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except json.JSONDecodeError as e:
                st.error(f"Error parsing AI response. Please try again. Error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
