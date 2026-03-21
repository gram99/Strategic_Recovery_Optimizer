import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Citi Strategic Recovery & Capital Optimizer", layout="wide")

# 2. DATA ENGINE
@st.cache_data
def get_master_data():
    # Peer Benchmarking
    peers = pd.DataFrame({
        'Bank': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
        'CET1 Ratio (%)': [15.1, 10.2, 13.2, 11.8, 12.3]
    }).sort_values('ROTCE (%)', ascending=False)
    
    # 9Q DFAST Stress
    quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
    nco_severe = [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2] 
    stress_df = pd.DataFrame({'Quarter': quarters, 'Severely Adverse (9Q)': nco_severe})
    
    # Strategic Vendor List
    today = datetime.now().date()
    vendor_data = pd.DataFrame({
        'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
        'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
        'Core Segment': ['Mass Market Card', 'Retail Services', 'High-FICO Litigation', 'High-Balance Tail', 'Commercial/SME'],
        'Efficiency %': [92, 85, 74, 68, 81],
        'Capital Drag (bps)': [1.2, 2.4, 6.8, 8.2, 3.1],
        'Placement ($M)': [450, 320, 180, 140, 95],
        'Renewal Date': [today + timedelta(days=x) for x in [365, 180, 25, 90, 400]]
    })
    
    # Jurisdictional Data for Interactive Map
    juris_dict = {
        'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Shift to AI reporting noted Feb 2026.'},
        'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'New CPPA regs active Jan 2026; audit pending.'},
        'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned with national standards.'},
        'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 audit scheduled Q2 2026 due to vendor drift.'},
        'Federal': {'Risk': '🟡 Moderate', 'Focus': 'Data Controls', 'Update': 'OCC terminated Resource Review Dec 2025.'}
    }
    
    geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [12, 45, 8, 38]})
    
    # Regulatory Timeline
    timeline_df = pd.DataFrame([
        dict(Event="2020 Consent Order Issued", Start="2020-10-07", End="2020-10-08", Status="Ongoing"),
        dict(Event="OCC Resource Review Amendment", Start="2024-07-10", End="2024-07-11", Status="Completed"),
        dict(Event="Termination of OCC Amendment", Start="2025-12-15", End="2025-12-16", Status="Success"),
        dict(Event="CA ADMT Compliance Deadline", Start="2026-01-01", End="2026-01-02", Status="Active"),
    ])
    
    return peers, stress_df, vendor_data, juris_dict, geo_df, timeline_df

peers, stress_df, vend_df, juris_dict, geo_df, timeline_df = get_master_data()

# 3. GLOBAL SIDEBAR
with st.sidebar:
    st.image("https://www.citigroup.com", width=80)
    st.header("Executive Dashboard")
    scenario = st.selectbox("Strategic Mode", ["Standard Operations", "DFAST Stress Test"])
    st.divider()
    st.success("🟢 CET1 Ratio: 12.3%") 
    st.info("2026 ROTCE Target: 10.5%")
    st.markdown("[🔗 Citi Investor Relations](https://www.citigroup.com)")

# 4. MULTI-TAB INTERFACE
# Defined as individual variables to avoid index errors
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Risk", "Peer & Stress", "Vendor Management", "Regulatory Heatmap", "User Guide", "LEAVE-BEHIND"
])

# --- TAB 1: EXECUTIVE RISK ---
with tab1:
    st.header("Portfolio Risk & Economic Profit")
    c1, c2, c3 = st.columns(3)
    c1.metric("WARR % Change", "+0.45%", "Risk Migration", delta_color="inverse")
    c2.metric("Economic Profit (EP)", "$1.2B", "+5.2% YoY")
    c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")

# --- TAB 2: PEER & STRESS ANALYSIS ---
with tab2:
    col_p, col_s = st.columns(2)
    with col_p:
        st.plotly_chart(px.bar(peers, x='Bank', y='ROTCE (%)', color='Bank', title="ROTCE Peer Benchmarking"), use_container_width=True)
    with col_s:
        st.plotly_chart(px.line(stress_df, x='Quarter', y='Severely Adverse (9Q)', title="9Q Severe NCO Projection"), use_container_width=True)

# --- TAB 3: VENDOR MANAGEMENT ---
with tab3:
    st.header("🏢 Vendor Performance & Capital Optimizer")
    def color_renewals(val):
        color = 'red' if val < (datetime.now().date() + timedelta(days=30)) else 'black'
        return f'color: {color}; font-weight: bold' if color == 'red' else ''
    
    st.dataframe(vend_df.style.applymap(color_renewals, subset=['Renewal Date'])
                .background_gradient(subset=['Efficiency %'], cmap='YlGn'))
    
    st.divider()
    st.subheader("🔄 Strategic Placement Swap Simulator")
    sim_c1, sim_c2, sim_c3 = st.columns(3)
    with sim_c1: source_v = st.selectbox("From:", vend_df['Vendor Name'], index=3)
    with sim_c2: target_v = st.selectbox("To:", vend_df['Vendor Name'], index=2)
    
    s_eff = vend_df[vend_df['Vendor Name'] == source_v]['Efficiency %'].values[0]
    t_eff = vend_df[vend_df['Vendor Name'] == target_v]['Efficiency %'].values[0]
    eff_gain = (t_eff - s_eff) * 0.1
    
    with sim_c3:
        st.metric("Net Recovery Gain/Loss", f"${eff_gain:.2f}M", delta=f"{t_eff-s_eff}% Efficiency Delta")

# --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
with tab4:
    st.header("Jurisdictional Exceptions Map")
    st.markdown("👇 **Click a state on the map** to drill down into specific regulatory risks.")

    fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", 
                           color='Exceptions', scope="usa", color_continuous_scale="Reds")
    
    # Capture selection with rerun trigger
    selected_state = st.plotly_chart(fig_map, on_select="rerun")

    # Determine selection logic (Defaults to Federal overview)
    current_selection = "Federal"
    if selected_state and "selection" in selected_state and selected_state["selection"]["points"]:
        # Extract location from the clicked point
        current_selection = selected_state["selection"]["points"][0]["location"]

    st.divider()
    st.subheader(f"📍 Risk Detail: {current_selection}")
    
    detail = juris_dict.get(current_selection, juris_dict["Federal"])
    risk_display = pd.DataFrame({
        "Category": ["Jurisdiction", "Risk Level", "Primary Focus", "Recent Update"],
        "Details": [current_selection, detail['Risk'], detail['Focus'], detail['Update']]
    })

    def color_risk_text(val):
        if '🔴' in str(val): return 'color: red; font-weight: bold'
        if '🟡' in str(val): return 'color: orange; font-weight: bold'
        if '🟢' in str(val): return 'color: green; font-weight: bold'
        return ''

    st.table(risk_display.style.applymap(color_risk_text))

# --- TAB 5: USER GUIDE & TIMELINE ---
with tab5:
    st.header("📖 Strategic User Guide & Timeline")
    # Fixed timeline visualization with Start/End keys
    fig_time = px.timeline(timeline_df, x_start="Start", x_end="End", y="Event", color="Status")
    fig_time.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_time, use_container_width=True)

# --- TAB 6: LEAVE-BEHIND ---
with tab6:
    st.header("🖨️ Executive Leave-Behind Summary")
    st.markdown("#### **Strategic Positioning (Q1 2026)**")
    st.write("* **Vendor Strategy:** Lexington Legal identified as primary growth partner for High-FICO tail.")
    st.write("* **Risk Milestone:** Dec 2025 OCC termination confirms transformation stability.")
    components.html("""
    <script>function print_summary() { window.print(); }</script>
    <button onclick="print_summary()" style="background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
        Download PDF Summary
    </button>
    """, height=100)
