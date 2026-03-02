Ultimate Pharmaceutical Market Entry Intelligence Platform

I'll fix the syntax error and provide the complete, industry-ready code:

python
============================================================================
PHARMINTEL PRO - ULTIMATE PHARMACEUTICAL MARKET ENTRY INTELLIGENCE PLATFORM
============================================================================
Version: 3.0 Enterprise Edition
Industry-Ready Dashboard with Advanced KPIs
============================================================================

import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import random
import time

============================================================================
PAGE CONFIGURATION
============================================================================
st.setpageconfig(
    page_title="PharmIntel Pro | Market Entry Intelligence",
    page_icon="💊",
    layout="wide",
    initialsidebarstate="expanded"
)

============================================================================
PREMIUM CSS STYLING
============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
     {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0a0e1a 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #06b6d4, #8b5cf6, #ec4899);
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
    
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 5px;
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
    .kpi-card.purple { border-top: 3px solid #8b5cf6; }
    
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
    
    .info-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .info-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 15px;
    }
    
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
    
    .alert-info {
        background: rgba(6, 182, 212, 0.15);
        border: 1px solid rgba(6, 182, 212, 0.3);
        color: #06b6d4;
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
    
    .metric-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 5px;
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        color: white;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    .executive-summary {
        background: linear-gradient(145deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.1));
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
    }
    
    .recommendation-card {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .risk-card {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.1), rgba(245, 158, 11, 0.1));
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafeallowhtml=True)

============================================================================
DATA GENERATION FUNCTIONS
============================================================================

@st.cache_data(ttl=3600)
def generatemarketreadinessdata(drugclass):
    """Generate Market Readiness Index for Top Priority Countries"""
    np.random.seed(hash(drug_class) % 100)
    
    countries_data = [
        {"country": "Germany", "flag": "DE", "region": "Europe", "iso": "DEU"},
        {"country": "Japan", "flag": "JP", "region": "APAC", "iso": "JPN"},
        {"country": "United Kingdom", "flag": "GB", "region": "Europe", "iso": "GBR"},
        {"country": "Canada", "flag": "CA", "region": "North America", "iso": "CAN"},
        {"country": "Australia", "flag": "AU", "region": "APAC", "iso": "AUS"},
        {"country": "France", "flag": "FR", "region": "Europe", "iso": "FRA"},
        {"country": "South Korea", "flag": "KR", "region": "APAC", "iso": "KOR"},
        {"country": "Brazil", "flag": "BR", "region": "LATAM", "iso": "BRA"},
        {"country": "Mexico", "flag": "MX", "region": "LATAM", "iso": "MEX"},
        {"country": "India", "flag": "IN", "region": "APAC", "iso": "IND"},
    ]
    
    results = []
    for c in countries_data:
        regulatory_speed = np.random.randint(65, 98)
        pricing_favorability = np.random.randint(55, 95)
        patient_population = round(np.random.uniform(1.5, 12.0), 1)
        market_size = round(np.random.uniform(8, 95), 1)
        approval_time = np.random.randint(120, 400)
        
        # Calculate composite score
        compositescore = (regulatoryspeed  0.35 + pricing_favorability  0.35 + 
                         min(patient_population  5, 30) + np.random.randint(0, 10))
        
        results.append({
            c,
            "regulatoryspeed": regulatoryspeed,
            "pricingfavorability": pricingfavorability,
            "patientpopulationm": patient_population,
            "marketsizeb": market_size,
            "approvaltimedays": approval_time,
            "compositescore": min(round(compositescore, 1), 98)
        })
    
    return sorted(results, key=lambda x: x["composite_score"], reverse=True)[:5]

@st.cache_data(ttl=3600)
def generateemergingmarketsdata(drugclass):
    """Generate Emerging Market Growth Rate Data"""
    np.random.seed(hash(drug_class + "emerging") % 100)
    
    emerging_markets = [
        {"country": "Vietnam", "region": "APAC", "current_penetration": 12},
        {"country": "Indonesia", "region": "APAC", "current_penetration": 8},
        {"country": "Colombia", "region": "LATAM", "current_penetration": 15},
        {"country": "Philippines", "region": "APAC", "current_penetration": 11},
        {"country": "Egypt", "region": "MEA", "current_penetration": 7},
        {"country": "Nigeria", "region": "MEA", "current_penetration": 5},
        {"country": "Thailand", "region": "APAC", "current_penetration": 18},
        {"country": "Argentina", "region": "LATAM", "current_penetration": 14},
        {"country": "Saudi Arabia", "region": "MEA", "current_penetration": 22},
        {"country": "Malaysia", "region": "APAC", "current_penetration": 20},
    ]
    
    results = []
    for m in emerging_markets:
        diseaseburdengrowth = round(np.random.uniform(8, 28), 1)
        competitor_saturation = np.random.randint(5, 45)
        healthcarespendinggrowth = round(np.random.uniform(5, 18), 1)
        population_growth = round(np.random.uniform(0.8, 3.5), 1)
        
        # Opportunity score
        opportunityscore = (diseaseburdengrowth  2 + (100 - competitorsaturation)  0.5 + 
                           healthcarespendinggrowth + np.random.randint(0, 15))
        
        results.append({
            m,
            "diseaseburdengrowth": diseaseburdengrowth,
            "competitorsaturation": competitorsaturation,
            "healthcarespendinggrowth": healthcarespendinggrowth,
            "populationgrowth": populationgrowth,
            "opportunityscore": min(round(opportunityscore, 1), 95)
        })
    
    return sorted(results, key=lambda x: x["opportunity_score"], reverse=True)[:5]

@st.cache_data(ttl=3600)
def generatecompetitorblindspots(drug_class):
    """Generate Competitor Blind Spot Analysis"""
    np.random.seed(hash(drug_class + "blindspot") % 100)
    
    blindspots = [
        {
            "region": "
