import streamlit as st
import google.generativeai as genai
import json
import pandas as pd

# --- 1. PAGE SETUP & CUSTOM CSS ---
st.set_page_config(page_title="Market Entry Optimizer", page_icon="📊", layout="wide")

# This CSS mimics the Tailwind styles from your React reference file
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    .ui-card { background: white; border-radius: 16px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; height: 100%; margin-bottom: 15px;}
    .ui-title { color: #64748b; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;}
    .metric-value-high { color: #059669; font-size: 48px; font-weight: 300; line-height: 1; }
    .metric-value-med { color: #d97706; font-size: 48px; font-weight: 300; line-height: 1; }
    .metric-value-low { color: #e11d48; font-size: 48px; font-weight: 300; line-height: 1; }
    .badge-high { background-color: #fef2f2; color: #e11d48; border: 1px solid #fecdd3; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .badge-med { background-color: #fffbeb; color: #d97706; border: 1px solid #fde68a; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .badge-low { background-color: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .badge-blue { background-color: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; padding: 3px 10px; border-radius: 9999px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .text-sm { font-size: 14px; color: #475569; line-height: 1.5;}
    .text-xs { font-size: 12px; color: #64748b; margin-top: 4px;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Market Entry Optimizer")
st.markdown("### Determine the exact optimal moment to launch.")
st.markdown("<p style='color:#64748b; max-width:800px;'>Stop relying on static spreadsheets. Our AI continuously ingests real-time data to find the most profitable launch windows for your product.</p>", unsafe_allow_html=True)
st.write("")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Configuration")
    api_key = st.text_input("Enter Google AI Studio API Key:", type="password")

# --- 3. SEARCH & LOGIC ---
query = st.text_input("Describe your product and target market (e.g., 'Paracetamol'):", placeholder="Type here...")

# Helper functions for dynamic styling based on your React file logic
def get_color(score):
    if score >= 75: return "metric-value-high"
    elif score >= 50: return "metric-value-med"
    else: return "metric-value-low"

def get_badge(level):
    level = level.lower()
    if 'high' in level: return "badge-high"
    elif 'medium' in level or 'med' in level: return "badge-med"
    else: return "badge-low"

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
            "successProbability": 35,
            "optimalWindow": "Q4 2024",
            "windowReason": "Brief reason...",
            "factors": [
                {{"name": "Regulatory Compliance", "score": 95, "desc": "Description..."}},
                {{"name": "Price Sensitivity", "score": 90, "desc": "Description..."}}
            ],
            "gaps": ["Gap 1", "Gap 2"],
            "competitors": [
                {{"name": "GSK (Panadol)", "threat": "HIGH", "desc": "Description..."}}
            ],
            "innovations": [
                {{"title": "Nanoparticle Absorption", "impact": "HIGH", "desc": "Description..."}}
            ],
            "recs": ["Rec 1", "Rec 2", "Rec 3"]
        }}
        """
        
        with st.spinner(f"Processing '{query}' with Market Intelligence AI..."):
            try:
                response = model.generate_content(prompt)
                data = json.loads(response.text)
                
                # --- ROW 1: TOP METRICS ---
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"""
                <div class="ui-card">
                    <div class="ui-title">📈 MARKET READINESS</div>
                    <div class="{get_color(data['readinessScore'])}">{data['readinessScore']}<span style="font-size:16px; color:#94a3b8;">/100</span></div>
                </div>""", unsafe_allow_html=True)
                
                c2.markdown(f"""
                <div class="ui-card">
                    <div class="ui-title">🎯 EST. SUCCESS RATE</div>
                    <div class="{get_color(data['successProbability'])}">{data['successProbability']}%</div>
                </div>""", unsafe_allow_html=True)
                
                c3.markdown(f"""
                <div class="ui-card">
                    <div class="ui-title">📅 OPTIMAL WINDOW</div>
                    <div style="font-size: 32px; font-weight: 600; color: #0f172a; margin-bottom:8px;">{data['optimalWindow']}</div>
                    <div class="text-xs">{data['windowReason']}</div>
                </div>""", unsafe_allow_html=True)

                st.write("")

                # --- ROW 2: CHART AND FACTORS ---
                c_chart, c_factors = st.columns([2, 1])
                with c_chart:
                    st.markdown('<div class="ui-card"><div class="ui-title">📊 12-MONTH PROJECTION</div>', unsafe_allow_html=True)
                    chart_data = pd.DataFrame({"Projection":}, index=[f"M{i}" for i in range(1, 13)])
                    st.area_chart(chart_data, color="#3b82f6", height=280)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with c_factors:
                    factors_html = '<div class="ui-card" style="overflow-y:auto; max-height:380px;"><div class="ui-title">⚠️ KEY FACTORS</div>'
                    for f in data.get('factors', []):
                        color_class = get_color(f['score']).replace('metric-value', 'text')
                        factors_html += f"""
                        <div style="padding:12px; background:#f8fafc; border-radius:8px; margin-bottom:10px; border:1px solid #f1f5f9;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                                <strong style="font-size:13px; color:#0f172a;">{f['name']}</strong>
                                <span style="font-size:12px; font-weight:600;" class="{color_class}">{f['score']}/100</span>
                            </div>
                            <div class="text-xs">{f['desc']}</div>
                        </div>"""
                    factors_html += '</div>'
                    st.markdown(factors_html, unsafe_allow_html=True)

                st.write("")

                # --- ROW 3: GAPS & COMPETITORS ---
                c_gaps, c_comp = st.columns(2)
                gaps_html = '<div class="ui-card"><div class="ui-title">🔍 MARKET GAPS</div><ul style="padding-left: 20px;">'
                for gap in data.get('gaps', []): gaps_html += f'<li class="text-sm" style="margin-bottom:8px;">{gap}</li>'
                c_gaps.markdown(gaps_html + '</ul></div>', unsafe_allow_html=True)

                comp_html = '<div class="ui-card"><div class="ui-title">🏢 COMPETITOR LANDSCAPE</div>'
                for comp in data.get('competitors', []):
                    comp_html += f"""
                    <div style="padding:12px; background:#f8fafc; border-radius:8px; margin-bottom:10px; border:1px solid #f1f5f9;">
                        <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
                            <strong style="font-size:14px; color:#0f172a;">{comp['name']}</strong>
                            <span class="{get_badge(comp['threat'])}">{comp['threat']} THREAT</span>
                        </div>
                        <div class="text-xs">{comp['desc']}</div>
                    </div>"""
                c_comp.markdown(comp_html + '</div>', unsafe_allow_html=True)

                st.write("")

                # --- ROW 4: INNOVATIONS ---
                st.markdown('<div class="ui-title">💡 RECOMMENDED INNOVATIONS</div>', unsafe_allow_html=True)
                inn_cols = st.columns(3)
                for i, inn in enumerate(data.get('innovations', [])[:3]):
                    with inn_cols[i % 3]:
                        st.markdown(f"""
                        <div class="ui-card">
                            <div style="margin-bottom:12px;"><span class="badge-blue">{inn['impact']} IMPACT</span></div>
                            <strong style="font-size:14px; color:#0f172a; display:block; margin-bottom:8px;">{inn['title']}</strong>
                            <div class="text-xs">{inn['desc']}</div>
                        </div>""", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")


