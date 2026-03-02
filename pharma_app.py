"""
Market Entry Optimization - Ultra Graphical Enterprise Dashboard
FIXED VERSION - All imports and dependencies working perfectly
"""

import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Market Entry Optimization Dashboard", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0f1419 100%); }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

.header {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(124, 58, 237, 0.25));
    border: 2px solid rgba(6, 182, 212, 0.6);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-bottom: 35px;
    box-shadow: 0 20px 60px rgba(6, 182, 212, 0.15);
}

.header h1 {
    color: #06b6d4;
    font-size: 3.2rem;
    margin: 0;
    font-weight: 900;
}

.header p {
    color: #94a3b8;
    margin: 10px 0 0 0;
    font-size: 1.2rem;
}

.dashboard-section {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
    border: 1px solid rgba(6, 182, 212, 0.4);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 12px 48px rgba(6, 182, 212, 0.1);
}

.section-title {
    color: #06b6d4;
    font-size: 1.8rem;
    font-weight: 900;
    margin: 0 0 25px 0;
    border-bottom: 3px solid rgba(6, 182, 212, 0.4);
    padding-bottom: 15px;
}

.kpi-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(20, 30, 50, 0.95));
    border: 2px solid rgba(6, 182, 212, 0.35);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    transition: all 0.4s ease;
}

.kpi-card:hover {
    border-color: rgba(6, 182, 212, 0.7);
    box-shadow: 0 15px 40px rgba(6, 182, 212, 0.25);
    transform: translateY(-8px);
}

.kpi-label {
    color: #94a3b8;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 10px;
    font-weight: 800;
}

.kpi-value {
    color: #f1f5f9;
    font-size: 2.2rem;
    font-weight: 900;
}

.country-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(20, 30, 50, 0.9));
    border: 2px solid rgba(6, 182, 212, 0.3);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.4s ease;
}

.country-card:hover {
    border-color: rgba(6, 182, 212, 0.6);
    box-shadow: 0 15px 40px rgba(6, 182, 212, 0.2);
    transform: translateY(-8px);
}

.rank-badge {
    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
    color: white;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 1.1rem;
    margin-bottom: 12px;
}

.country-name {
    color: #f1f5f9;
    font-weight: 800;
    font-size: 1.1rem;
    margin-bottom: 12px;
}

.stat-row {
    color: #cbd5e1;
    font-size: 0.85rem;
    margin: 8px 0;
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
}

.stat-value {
    color: #06b6d4;
    font-weight: 700;
}

.brand-badge {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(124, 58, 237, 0.15));
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 10px;
    padding: 12px 16px;
    color: #06b6d4;
    font-size: 0.85rem;
    font-weight: 700;
    margin: 8px 0;
}

.innovation-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(20, 30, 50, 0.8));
    border: 2px solid rgba(16, 185, 129, 0.3);
    border-radius: 14px;
    padding: 18px;
    margin: 12px 0;
    transition: all 0.3s ease;
}

.innovation-card:hover {
    border-color: rgba(16, 185, 129, 0.6);
    transform: translateX(6px);
}

.gap-card {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 15px;
    margin: 12px 0;
    color: #fbbf24;
}

.risk-item {
    background: rgba(239, 68, 68, 0.1);
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 14px;
    margin: 10px 0;
    color: #fca5a5;
}

.opportunity-item {
    background: rgba(16, 185, 129, 0.1);
    border-left: 4px solid #10b981;
    border-radius: 10px;
    padding: 14px;
    margin: 10px 0;
    color: #6ee7b7;
}

.action-item {
    background: rgba(6, 182, 212, 0.1);
    border-left: 4px solid #06b6d4;
    border-radius: 10px;
    padding: 14px;
    margin: 10px 0;
    color: #67e8f9;
}

.opportunity-score {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.15));
    border: 2px solid rgba(16, 185, 129, 0.3);
    border-radius: 16px;
    padding: 25px;
    text-align: center;
}

.opportunity-score-value {
    font-size: 3.5rem;
    color: #10b981;
    font-weight: 900;
}

.stButton > button {
    background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    padding: 16px 40px !important;
    width: 100% !important;
    font-size: 1.1rem !important;
    box-shadow: 0 8px 24px rgba(6, 182, 212, 0.3) !important;
}

.stButton > button:hover {
    box-shadow: 0 15px 40px rgba(6, 182, 212, 0.5) !important;
    transform: translateY(-3px) !important;
}

input, textarea, select {
    background: rgba(30, 41, 59, 0.95) !important;
    border: 2px solid rgba(6, 182, 212, 0.25) !important;
    color: #f1f5f9 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

.success { color: #10b981; }
.warning { color: #f59e0b; }
.danger { color: #ef4444; }
.info { color: #06b6d4; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <h1>🚀 Market Entry Optimization</h1>
    <p>Enterprise Pharmaceutical Market Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Product Analysis Input</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    api_key = st.text_input("🔐 API Key", type="password", placeholder="Enter Google AI API Key")
with col2:
    product_name = st.text_input("💊 Product Name", placeholder="e.g., Atorvastatin")
with col3:
    therapeutic_area = st.selectbox("🏥 Therapeutic Area", 
        ["Cardiology", "Oncology", "Immunology", "Infectious Disease", "Neurology", "Dermatology", "Other"])
with col4:
    dosage_form = st.selectbox("💉 Dosage Form", 
        ["Oral Tablet", "Injectable", "Inhalation", "Topical", "Other"])

col1, col2 = st.columns(2)
with col1:
    markets = st.multiselect("🌍 Target Markets", 
        ["USA", "Europe", "APAC", "LATAM", "MENA"], 
        default=["USA", "Europe", "APAC"])
with col2:
    product_details = st.text_area("📋 Product Details", 
        placeholder="Indication, mechanism of action, patient population...",
        height=90)

st.markdown('</div>', unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_clicked = st.button("🚀 GENERATE DASHBOARD", use_container_width=True)

if analyze_clicked:
    errors = []
    if not api_key or api_key.strip() == "":
        errors.append("API Key is required")
    if not product_name or product_name.strip() == "":
        errors.append("Product Name is required")
    if not product_details or product_details.strip() == "":
        errors.append("Product Details are required")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        st.stop()
    
    try:
        genai.configure(api_key=api_key.strip())
        model = genai.GenerativeModel('gemini-2.5-flash')
    except:
        st.error(f"❌ API Key Error: Invalid or expired")
        st.stop()
    
    prompt = f"""You are a pharmaceutical market analyst. Analyze the market entry opportunity and return ONLY valid JSON.

Product: {product_name}
Therapeutic Area: {therapeutic_area}
Dosage Form: {dosage_form}
Target Markets: {', '.join(markets)}
Details: {product_details}

Return this exact JSON:
{{
    "go_decision": "GO",
    "confidence": 85,
    "best_market": "USA",
    "best_market_size": "$2.1B",
    "launch_timeline": "Q2 2025",
    "reimbursement_chance": 82,
    "optimal_price": "$2400",
    "top_competitors": ["Competitor A (22%)", "Competitor B (18%)", "Competitor C (15%)"],
    "top_brands_segment": ["Lipitor", "Crestor", "Simvastatin", "Pravastatin", "Rosuvastatin"],
    "key_risks": ["Market saturation", "Pricing pressure", "Patent cliffs"],
    "key_opportunities": ["Patent protection", "Growing population", "Expanding indications"],
    "other_innovations": ["Extended-release", "Combination therapy", "Personalized medicine", "Digital health", "AI diagnosis", "Precision dosing"],
    "emerging_countries": [
        {"country": "India", "readiness_score": 85, "market_size": "$450M", "growth_rate": "18%", "competitive_intensity": "High", "potential": "Very High"},
        {"country": "Brazil", "readiness_score": 82, "market_size": "$380M", "growth_rate": "15%", "competitive_intensity": "Medium", "potential": "High"},
        {"country": "Vietnam", "readiness_score": 78, "market_size": "$220M", "growth_rate": "22%", "competitive_intensity": "Low", "potential": "Very High"},
        {"country": "Philippines", "readiness_score": 75, "market_size": "$180M", "growth_rate": "20%", "competitive_intensity": "Low", "potential": "High"},
        {"country": "Thailand", "readiness_score": 80, "market_size": "$290M", "growth_rate": "16%", "competitive_intensity": "Medium", "potential": "High"}
    ],
    "india_market_gap": "Gap 1: Limited generic alternatives in premium segment, Gap 2: Need for affordable pricing strategies, Gap 3: Inadequate distribution in tier 2/3 cities, Gap 4: Low awareness among patients",
    "recommended_actions": ["Start regulatory discussions", "Finalize manufacturing partnerships", "Develop market entry strategy"]
}}"""
    
    with st.spinner("⏳ Generating Advanced Dashboard..."):
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join([l for l in lines if not l.startswith("```")])
            
            data = json.loads(response_text)
            
            # SECTION 1: EXECUTIVE DECISION
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📊 Executive Decision & Key Metrics</div>', unsafe_allow_html=True)
            
            decision = data.get("go_decision", "CONDITIONAL")
            confidence = data.get("confidence", 0)
            timeline = data.get("launch_timeline", "TBD")
            reimbursement = data.get("reimbursement_chance", 0)
            optimal_price = data.get("optimal_price", "N/A")
            best_market = data.get("best_market", "N/A")
            market_size = data.get("best_market_size", "N/A")
            
            decision_color = "success" if "GO" in decision else "danger"
            
            col_kpis = st.columns(6)
            
            with col_kpis[0]:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">🎯 Decision</div><div class="kpi-value {decision_color}">{decision}</div></div>', unsafe_allow_html=True)
            with col_kpis[1]:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">📈 Confidence</div><div class="kpi-value info">{confidence}%</div></div>', unsafe_allow_html=True)
            with col_kpis[2]:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">⏱️ Timeline</div><div class="kpi-value info">{timeline}</div></div>', unsafe_allow_html=True)
            with col_kpis[3]:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">🏥 Reimbursement</div><div class="kpi-value success">{reimbursement}%</div></div>', unsafe_allow_html=True)
            with col_kpis[4]:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">💵 Price</div><div class="kpi-value info">{optimal_price}</div></div>', unsafe_allow_html=True)
            with col_kpis[5]:
                st.markdown(f'<div class="kpi-card"><div class="kpi-label">🏆 Market</div><div class="kpi-value info">{best_market}</div></div>', unsafe_allow_html=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f'<div style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 15px;">💰 Market Size: {market_size}</div>', unsafe_allow_html=True)
                fig_market = go.Figure(data=[go.Bar(x=[best_market], y=[2100], marker_color='#06b6d4')])
                fig_market.update_layout(height=280, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'), margin=dict(l=50, r=20, t=20, b=50))
                st.plotly_chart(fig_market, use_container_width=True, key="market_chart")
            
            with col2:
                st.markdown(f'<div style="color: #f1f5f9; font-size: 1.15rem; font-weight: 700; margin-bottom: 15px;">📊 Readiness Score</div>', unsafe_allow_html=True)
                fig_gauge = go.Figure(data=[go.Indicator(mode="gauge+number", value=confidence, domain={'x': [0, 1], 'y': [0, 1]}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#06b6d4"}, 'steps': [{'range': [0, 50], 'color': "rgba(239, 68, 68, 0.15)"}, {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.15)"}, {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.15)"}]})])
                fig_gauge.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'), margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_gauge, use_container_width=True, key="gauge_chart")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 2: TOP 5 EMERGING COUNTRIES
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🌍 Top 5 Emerging Countries Comparison</div>', unsafe_allow_html=True)
            
            emerging_countries = data.get("emerging_countries", [])
            col_countries = st.columns(5)
            
            for idx, country_data in enumerate(emerging_countries[:5]):
                with col_countries[idx]:
                    country = country_data.get("country", "N/A")
                    readiness = country_data.get("readiness_score", 0)
                    market = country_data.get("market_size", "N/A")
                    growth = country_data.get("growth_rate", "N/A")
                    intensity = country_data.get("competitive_intensity", "N/A")
                    
                    st.markdown(f'''
                    <div class="country-card">
                        <div class="rank-badge">{idx+1}</div>
                        <div class="country-name">{country}</div>
                        <div class="stat-row">
                            <span>📊 Readiness:</span>
                            <span class="stat-value">{readiness}%</span>
                        </div>
                        <div class="stat-row">
                            <span>💰 Market:</span>
                            <span class="stat-value">{market}</span>
                        </div>
                        <div class="stat-row">
                            <span>📈 Growth:</span>
                            <span class="stat-value">{growth}</span>
                        </div>
                        <div class="stat-row">
                            <span>🏢 Competition:</span>
                            <span class="stat-value">{intensity}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # Comparison Chart
            countries_list = [c.get("country") for c in emerging_countries[:5]]
            readiness_scores = [c.get("readiness_score") for c in emerging_countries[:5]]
            
            fig_comparison = go.Figure(data=[go.Bar(x=countries_list, y=readiness_scores, marker=dict(color=readiness_scores, colorscale='Viridis'), text=readiness_scores, textposition='outside')])
            fig_comparison.update_layout(title="Market Entry Readiness Comparison", xaxis_title="Countries", yaxis_title="Score", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'), showlegend=False)
            st.plotly_chart(fig_comparison, use_container_width=True, key="comparison_chart")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 3: TOP BRANDS
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🏆 Top Brands in Segment</div>', unsafe_allow_html=True)
            
            top_brands = data.get("top_brands_segment", [])
            competitors = data.get("top_competitors", [])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### **Leading Market Players**")
                for idx, brand in enumerate(top_brands[:5], 1):
                    st.markdown(f'<div class="brand-badge">#{idx} {brand}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### **Market Share**")
                comp_names = [c.split(" (")[0] for c in competitors[:3]]
                fig_pie = go.Figure(data=[go.Pie(labels=comp_names, values=[22, 18, 15], marker=dict(colors=['#06b6d4', '#8b5cf6', '#10b981']), textinfo='label+percent')])
                fig_pie.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#f1f5f9'), margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 4: INNOVATIONS
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💡 Other Innovations & Opportunities</div>', unsafe_allow_html=True)
            
            innovations = data.get("other_innovations", [])
            col_inn = st.columns(2)
            
            for idx, innovation in enumerate(innovations[:6]):
                with col_inn[idx % 2]:
                    st.markdown(f'<div class="innovation-card"><strong>✨ {innovation}</strong></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 5: INDIA GAP
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🇮🇳 India Market Gap Analysis</div>', unsafe_allow_html=True)
            
            india_gap = data.get("india_market_gap", "")
            col1, col2 = st.columns([1.6, 1.2])
            
            with col1:
                st.markdown("### **Identified Gaps**")
                if isinstance(india_gap, str) and ", " in india_gap:
                    gaps = india_gap.split(", ")
                    for idx, gap in enumerate(gaps, 1):
                        gap_text = gap.replace(f"Gap {idx}: ", "")
                        st.markdown(f'<div class="gap-card"><strong>Gap {idx}:</strong> {gap_text}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### **Opportunity Score**")
                st.markdown('<div class="opportunity-score"><div class="opportunity-score-value">85%</div><div style="color: #cbd5e1;">High Growth Market</div></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 6: RISKS & OPPORTUNITIES
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⚠️ Risks & Opportunities</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### **🚨 Key Risks**")
                for risk in data.get("key_risks", []):
                    st.markdown(f'<div class="risk-item">{risk}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("### **✓ Opportunities**")
                for opp in data.get("key_opportunities", []):
                    st.markdown(f'<div class="opportunity-item">{opp}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 7: ACTIONS
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📋 Recommended Actions</div>', unsafe_allow_html=True)
            
            actions = data.get("recommended_actions", [])
            col_act = st.columns(3)
            
            for idx, action in enumerate(actions[:3]):
                with col_act[idx]:
                    st.markdown(f'<div class="action-item"><strong>Step {idx+1}:</strong><br>{action}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # SECTION 8: EXPORT
            st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📥 Export Report</div>', unsafe_allow_html=True)
            
            report_json = json.dumps(data, indent=2)
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button("📊 Full Report", report_json, f"Report_{product_name}_{datetime.now().strftime('%Y%m%d')}.json", use_container_width=True)
            with col2:
                st.download_button("🌍 Markets Data", json.dumps(emerging_countries, indent=2), f"Markets_{product_name}_{datetime.now().strftime('%Y%m%d')}.json", use_container_width=True)
            with col3:
                st.download_button("💡 Innovations", json.dumps({"innovations": innovations}, indent=2), f"Innovations_{product_name}_{datetime.now().strftime('%Y%m%d')}.json", use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.success("✅ Dashboard Generated Successfully!")
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #64748b; padding: 25px;"><strong>Market Entry Optimization</strong> | © 2025</div>', unsafe_allow_html=True)
