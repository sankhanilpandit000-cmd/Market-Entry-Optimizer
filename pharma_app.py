"""
Market Entry Optimization - Simple One-Page Version
Easy-to-use pharmaceutical market entry intelligence
"""

import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

# ============================================================================
# PAGE SETUP
# ============================================================================
st.set_page_config(
    page_title="Market Entry Optimization",
    page_icon="🚀",
    layout="wide"
)

# ============================================================================
# SIMPLE CSS
# ============================================================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #111827 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .header {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(124, 58, 237, 0.15));
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
    }
    
    .header h1 {
        color: #06b6d4;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .header p {
        color: #94a3b8;
        margin: 5px 0 0 0;
    }
    
    .section {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .section h2 {
        color: #06b6d4;
        margin: 0 0 15px 0;
        font-size: 1.3rem;
    }
    
    .kpi {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
    }
    
    .kpi-label {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-bottom: 5px;
    }
    
    .kpi-value {
        color: #f1f5f9;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .success { color: #10b981; }
    .warning { color: #f59e0b; }
    .danger { color: #ef4444; }
    .info { color: #06b6d4; }
    
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 25px rgba(6, 182, 212, 0.3) !important;
    }
    
    input, textarea, select {
        background: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(6, 182, 212, 0.2) !important;
        color: #f1f5f9 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="header">
    <h1>🚀 Market Entry Optimization</h1>
    <p>Fast pharmaceutical market analysis for quick market entry decisions</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# INPUT SECTION
# ============================================================================
st.markdown('<div class="section"><h2>📝 Product Information</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    api_key = st.text_input("🔐 API Key", type="password", placeholder="Enter your Google AI API Key")
    product_name = st.text_input("Product Name", placeholder="e.g., Atorvastatin")
    therapeutic_area = st.selectbox("Therapeutic Area", 
        ["Cardiology", "Oncology", "Immunology", "Infectious Disease", "Neurology", "Other"])

with col2:
    dosage_form = st.selectbox("Dosage Form", 
        ["Oral Tablet", "Injectable", "Inhalation", "Topical", "Other"])
    markets = st.multiselect("Target Markets", 
        ["USA", "Europe", "APAC", "LATAM"], default=["USA", "Europe", "APAC"])
    
    product_details = st.text_area("Product Details", 
        placeholder="Briefly describe your product...", height=80)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# GENERATE BUTTON
# ============================================================================
if st.button("🚀 ANALYZE MARKET", use_container_width=True):
    
    # Validation
    if not api_key:
        st.error("❌ Please enter API Key")
        st.stop()
    if not product_name:
        st.error("❌ Please enter Product Name")
        st.stop()
    if not product_details:
        st.error("❌ Please enter Product Details")
        st.stop()
    
    # Configure API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except:
        st.error("❌ Invalid API Key")
        st.stop()
    
    # Simple prompt
    prompt = f"""
    Give me a quick pharmaceutical market analysis for {product_name} ({therapeutic_area}).
    Return ONLY valid JSON with these exact fields:
    {{
        "go_decision": "GO / NO-GO / CONDITIONAL",
        "confidence": 85,
        "best_market": "USA",
        "best_market_size": "$2.1B",
        "launch_timeline": "Q2 2025",
        "reimbursement_chance": 82,
        "optimal_price": "$2400",
        "top_competitors": ["Competitor A", "Competitor B"],
        "key_risks": ["Market saturation", "Pricing pressure"],
        "key_opportunities": ["Patent protection", "Growing patient population"],
        "recommended_actions": ["Start regulatory process", "Finalize partnerships", "Plan marketing"]
    }}
    """
    
    with st.spinner("⏳ Analyzing market..."):
        try:
            response = model.generate_content(prompt)
            data = json.loads(response.text)
            
            # ========================================================
            # RESULTS ON ONE PAGE
            # ========================================================
            
            # DECISION
            st.markdown('<div class="section"><h2>✅ DECISION</h2>', unsafe_allow_html=True)
            
            decision = data.get("go_decision", "CONDITIONAL")
            decision_color = "success" if "GO" in decision else "danger" if "NO" in decision else "warning"
            confidence = data.get("confidence", 0)
            timeline = data.get("launch_timeline", "TBD")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Go/No-Go</div><div class="kpi-value {decision_color}">{decision}</div></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Confidence</div><div class="kpi-value info">{confidence}%</div></div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Launch Timeline</div><div class="kpi-value info">{timeline}</div></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # MARKET ANALYSIS
            st.markdown('<div class="section"><h2>📊 MARKET ANALYSIS</h2>', unsafe_allow_html=True)
            
            best_market = data.get("best_market", "N/A")
            market_size = data.get("best_market_size", "N/A")
            reimbursement = data.get("reimbursement_chance", 0)
            optimal_price = data.get("optimal_price", "N/A")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Best Market</div><div class="kpi-value info">{best_market}</div></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Market Size</div><div class="kpi-value info">{market_size}</div></div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Reimbursement</div><div class="kpi-value success">{reimbursement}%</div></div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown(f'<div class="kpi"><div class="kpi-label">Optimal Price</div><div class="kpi-value info">{optimal_price}</div></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # COMPETITIVE LANDSCAPE
            st.markdown('<div class="section"><h2>🏆 COMPETITIVE LANDSCAPE</h2>', unsafe_allow_html=True)
            
            competitors = data.get("top_competitors", [])
            
            st.write("**Top Competitors:**")
            for idx, comp in enumerate(competitors, 1):
                st.write(f"{idx}. {comp}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # RISKS & OPPORTUNITIES
            st.markdown('<div class="section">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<h2 style="color: #06b6d4;">⚠️ RISKS</h2>', unsafe_allow_html=True)
                risks = data.get("key_risks", [])
                for risk in risks:
                    st.markdown(f'<div style="color: #fbbf24; margin: 8px 0;">• {risk}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<h2 style="color: #06b6d4;">💡 OPPORTUNITIES</h2>', unsafe_allow_html=True)
                opportunities = data.get("key_opportunities", [])
                for opp in opportunities:
                    st.markdown(f'<div style="color: #10b981; margin: 8px 0;">✓ {opp}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # RECOMMENDED ACTIONS
            st.markdown('<div class="section"><h2>📋 RECOMMENDED ACTIONS</h2>', unsafe_allow_html=True)
            
            actions = data.get("recommended_actions", [])
            for idx, action in enumerate(actions, 1):
                st.markdown(f'<div style="background: rgba(30, 41, 59, 0.9); border-left: 3px solid #06b6d4; padding: 12px; margin: 8px 0; border-radius: 4px;"><strong>{idx}.</strong> {action}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # DOWNLOAD
            st.markdown('<div class="section"><h2>📥 EXPORT RESULTS</h2>', unsafe_allow_html=True)
            
            report_json = json.dumps(data, indent=2)
            st.download_button(
                label="📊 Download Report",
                data=report_json,
                file_name=f"Market_Entry_{product_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.success("✅ Analysis Complete!")
            
        except json.JSONDecodeError:
            st.error("❌ API response error. Try again.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown('<div style="text-align: center; color: #64748b; font-size: 0.8rem;"><strong>Market Entry Optimization</strong> | © 2025</div>', unsafe_allow_html=True)
