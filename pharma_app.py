🏥 Ultimate Pharmaceutical Market Entry Intelligence Platform

I'll completely rewrite this code to create an industry-ready, comprehensive dashboard with all the advanced KPIs you've requested. This is a full enterprise-grade solution:

python
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

============================================================================
PAGE CONFIGURATION
============================================================================
st.setpageconfig(
    page_title="PharmIntel Pro™ | Market Entry Intelligence",
    page_icon="🧬",
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
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #111827 50%, #0a0e1a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    / Hide Streamlit Branding /
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    / Main Header /
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
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
    }
    
    / Section Headers /
    .section-header {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.2), transparent);
        border-left: 4px solid #06b6d4;
        padding: 15px 20px;
        margin: 30px 0 20px 0;
        border-radius: 0 12px 12px 0;
    }
    
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 5px;
    }
    
    / KPI Cards /
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 25px;
    }
    
    .kpi-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
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
    
    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 10px;
    }
    
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
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .kpi-change.up { color: #10b981; }
    .kpi-change.down { color: #ef4444; }
    .kpi-change.neutral { color: #64748b; }
    
    / Data Tables /
    .data-table {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .table-header {
        background: linear-gradient(90deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
        padding: 15px 20px;
        border-bottom: 1px solid rgba(100, 116, 139, 0.3);
    }
    
    .table-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    / Score Badges /
    .score-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .score-high { background: rgba(16, 185, 129, 0.2); color: #10b981; }
    .score-medium { background: rgba(245, 158, 11, 0.2); color: #f59e0b; }
    .score-low { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    
    / Progress Bars /
    .progress-container {
        background: rgba(30, 41, 59, 0.8);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin-top: 8px;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .progress-cyan { background: linear-gradient(90deg, #06b6d4, #22d3ee); }
    .progress-purple { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .progress-green { background: linear-gradient(90deg, #10b981, #34d399); }
    .progress-orange { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    
    / Info Cards /
    .info-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .info-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }
    
    .info-card-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    / Alert Boxes /
    .alert-box {
        padding: 16px 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
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
    
    / Sidebar Styling /
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(100, 116, 139, 0.3);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    / Custom Tabs /
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
    
    / Metric Cards for Rankings /
    .rank-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .rank-number {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.1rem;
    }
    
    .rank-1 { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #1e293b; }
    .rank-2 { background: linear-gradient(135deg, #94a3b8, #64748b); color: #1e293b; }
    .rank-3 { background: linear-gradient(135deg, #cd7f32, #b87333); color: #1e293b; }
    .rank-other { background: rgba(100, 116, 139, 0.3); color: #94a3b8; }
    
    .rank-content {
        flex: 1;
    }
    
    .rank-title {
        font-size: 1rem;
        font-weight: 600;
        color: #f1f5f9;
    }
    
    .rank-subtitle {
        font-size: 0.8rem;
        color: #64748b;
    }
    
    .rank-score {
        text-align: right;
    }
    
    .rank-score-value {
        font-size: 1.3rem;
        font-weight: 800;
        color: #06b6d4;
    }
    
    .rank-score-label {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
    }
</style>
""", unsafeallowhtml=True)

============================================================================
DATA GENERATION FUNCTIONS
============================================================================

@st.cache_data(ttl=3600)
def generatemarketreadiness_data():
    """Generate Market Readiness Index for Top Priority Countries"""
    countries = [
        {"country": "Germany", "flag": "🇩🇪", "region": "Europe", 
         "regulatoryspeed": 92, "pricingfavorability": 85, "patient_population": 4.2,
         "marketsize": "$48.2B", "approvaltime": "180 days"},
        {"country": "Japan", "flag": "🇯🇵", "region": "APAC",
         "regulatoryspeed": 88, "pricingfavorability": 78, "patient_population": 6.8,
         "marketsize": "$86.4B", "approvaltime": "270 days"},
        {"country": "United Kingdom", "flag": "🇬🇧", "region": "Europe",
         "regulatoryspeed": 90, "pricingfavorability": 72, "patient_population": 3.1,
         "marketsize": "$32.1B", "approvaltime": "210 days"},
        {"country": "Canada", "flag": "🇨🇦", "region": "North America",
         "regulatoryspeed": 85, "pricingfavorability": 80, "patient_population": 2.4,
         "marketsize": "$24.8B", "approvaltime": "240 days"},
        {"country": "Australia", "flag": "🇦🇺", "region": "APAC",
         "regulatory_
