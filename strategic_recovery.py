import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. PAGE CONFIG
st.set_page_config(page_title="Citi Strategic Recovery Suite", layout="wide")

# 2. DATA ENGINE
@st.cache_data
def get_master_data():
    # Peer Benchmarking
    peers = pd.DataFrame({
        'Bank': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5]
    })
    
    # Detailed Jurisdictional Data for Drill-Down
    juris_data = {
        'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Shift to AI reporting noted Feb 2026.'},
        'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'New CPPA regs active Jan 2026; audit pending.'},
        'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned with national standards.'},
        'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 audit scheduled Q2 2026 due to vendor drift.'},
        'Federal': {'Risk': '🟡 Moderate', 'Focus': 'Data Controls', 'Update': 'OCC terminated Resource Review Dec 2025.'}
    }
    
    # Map Data
    geo_df = pd.DataFrame({
        'State': ['NY', 'CA', 'TX', 'FL'],
        'Exceptions': [2, 14, 5, 21]
    })
    
    return peers, juris_data, geo_df

peers, juris_dict, geo_df = get_master_data()

# 3. SIDEBAR
with st.sidebar:
    st.header("Executive Dashboard")
    st.success("🟢 CET1 Ratio: 12.3%")
    st.info("2026 ROTCE Target: 10.5%")

# 4. TABS
tab1, tab2 = st.tabs(["Executive Overview", "Interactive Regulatory Map"])

with tab1:
    st.header("ROTCE Peer Benchmarking")
    st.plotly_chart(px.bar(peers, x='Bank', y='ROTCE (%)', color='Bank'))

# --- TAB 2: INTERACTIVE MAP & DRILL-DOWN ---
with tab2:
    st.header("Jurisdictional Exceptions Map")
    st.markdown("👇 **Click a state on the map** to drill down into specific regulatory risks.")

    # Interactive Map
    fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", 
                           color='Exceptions', scope="usa", color_continuous_scale="Reds")
    
    # Capture selection
    selected_state = st.plotly_chart(fig_map, on_select="rerun", selection_mode="points")

    # Determine which state to show (Default to Federal if nothing clicked)
    current_selection = "Federal"
    if selected_state and selected_state["selection"]["points"]:
        # Get the 'location' (State Code) from the clicked point
        current_selection = selected_state["selection"]["points"][0]["location"]

    st.divider()
    
    # DRILL-DOWN MATRIX
    st.subheader(f"📍 Risk Detail: {current_selection}")
    
    detail = juris_dict.get(current_selection, juris_dict["Federal"])
    
    # Create the display table
    risk_display = pd.DataFrame({
        "Category": ["Jurisdiction", "Risk Level", "Primary Focus", "Recent Update"],
        "Details": [current_selection, detail['Risk'], detail['Focus'], detail['Update']]
    })

    def color_risk(val):
        if '🔴' in str(val): return 'color: red; font-weight: bold'
        if '🟡' in str(val): return 'color: orange; font-weight: bold'
        if '🟢' in str(val): return 'color: green; font-weight: bold'
        return ''

    st.table(risk_display.style.applymap(color_risk))

    if "🔴" in detail['Risk']:
        st.error(f"**MD Alert:** {current_selection} requires immediate remediation focus to prevent further RWA erosion.")