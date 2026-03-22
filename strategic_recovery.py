import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Strategic Recovery & Capital Optimizer", layout="wide")

# 2. DATA ENGINE
@st.cache_data
def get_master_data():
    # Historical WARR Migration (Story: 2023 -> 2026 Evolution)
    warr_history = pd.DataFrame({
        'Year': ['2023-24', '2023-24', '2024-25', '2024-25', '2025-26 (Current)', '2025-26 (Current)'],
        'Segment': ['Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services'],
        'WARR': [1.05, 5.20, 1.18, 5.95, 1.22, 6.10]
    })
    
    # Peer Benchmarking (2026 Waypoints)
    peers = pd.DataFrame({
        'Bank': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026 Target)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
        'CET1 Ratio (%)': [15.1, 10.2, 13.2, 11.8, 12.3]
    }).sort_values('ROTCE (%)', ascending=False)
    
    # 9Q DFAST Stress (Severely Adverse)
    quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
    nco_severe = [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2] 
    stress_df = pd.DataFrame({'Quarter': quarters, 'Severely Adverse (9Q)': nco_severe})
    
    # Vendor & Budget Data
    vendor_data = pd.DataFrame({
        'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
        'Efficiency %':,
        'YTD Spend ($M)':,
        'Capacity ($M)':,
        'Renewal Date': [datetime.now().date() + timedelta(days=x) for x in]
    })
    
    # Jurisdictional Map
    juris_dict = {
        'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data controls remediation Dec 2025.'},
        'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.'},
        'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 drift remediation ongoing.'},
        'Federal': {'Risk': '🟡 Moderate', 'Focus': 'OCC/Fed Oversight', 'Update': 'Resource Review terminated Dec 2025.'}
    }
    geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions':})
    
    return warr_history, peers, stress_df, vendor_data, juris_dict, geo_df

warr_df, peer_df, stress_df, vend_df, juris_dict, geo_df = get_master_data()

# 3. GLOBAL SIDEBAR
with st.sidebar:
    st.image("https://www.citigroup.com", width=80)
    st.header("Executive Dashboard")
    st.divider()
    st.info("**2026 ROTCE Target:** 10.5%")
    st.success("**CET1 Ratio:** 13.2% (+160bps)")
    st.markdown("[🔗 Citi Investor Relations](https://www.citigroup.com)")

# 4. MULTI-TAB INTERFACE
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Capital Report", "Peer Strategy & Stress", "Vendor & Budget Management", "Regulatory Heatmap", "LEAVE-BEHIND"
])

# --- TAB 1: EXECUTIVE CAPITAL REPORT (WARR MIGRATION) ---
with tab1:
    st.header("Executive Capital & Shareholder Value Report")
    st.markdown("> **Strategic Context:** Recovery yield optimization acts as a capital engine, fueling our path to an **11% ROTCE**. This report tracks how our **WARR (Weighted Average Risk Rating)** has evolved as we transitioned from post-pandemic stability to inflationary optimization.")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CET1 Capital Ratio", "13.2%", "+160bps Buffer")
    c2.metric("2026 ROTCE Target", "10.5%", "On Track")
    c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
    c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
    
    st.divider()
    st.subheader("Historical WARR Risk Migration (2023 - 2026)")
    # Visualizing how risk has moved over the requested timeframe
    fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                      title="WARR Evolution by Portfolio Segment",
                      color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
    st.plotly_chart(fig_warr, use_container_width=True)

# --- TAB 2: PEER STRATEGY & STRESS ---
with tab2:
    st.header("The Competitive Advantage: Peer & Stress Strategy")
    col_p, col_s = st.columns(2)
    with col_p:
        st.plotly_chart(px.bar(peer_df, x='Bank', y='ROTCE (%)', color='Bank', title="Competitive ROTCE Benchmarking"), use_container_width=True)
    with col_s:
        fig_stress = px.line(stress_df, x='Quarter', y='Severely Adverse (9Q)', title="9Q Severe NCO Projection (DFAST)")
        st.plotly_chart(fig_stress, use_container_width=True)

# --- TAB 3: VENDOR & BUDGET MANAGEMENT ---
with tab3:
    st.header("Vendor Performance & Budget Capacity")
    
    # BUDGET GAUGE
    total_budget = 500 # $500M fictional budget
    ytd_spend = vend_df['YTD Spend ($M)'].sum()
    
    b_col1, b_col2 = st.columns([1, 2])
    with b_col1:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = ytd_spend,
            title = {'text': "Recovery OpEx Budget ($M)"},
            delta = {'reference': total_budget, 'increasing': {'color': "red"}},
            gauge = {'axis': {'range': [None, total_budget]},
                     'steps' : [{'range': [0, 400], 'color': "lightgray"},
                                {'range': [400, 500], 'color': "gray"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 450}}))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with b_col2:
        st.subheader("Active Vendor Network & Contract Status")
        st.dataframe(vend_df, hide_index=True, use_container_width=True)
        st.info(f"**Budget Utilization:** {ytd_spend/total_budget*100:.1f}% used. Projected to finish year within +/- 2% of guidance.")

# --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
with tab4:
    st.header("Jurisdictional Governance")
    fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
    sel = st.plotly_chart(fig_map, on_select="rerun")
    
    state = "Federal"
    if sel and "selection" in sel and sel["selection"]["points"]:
        state = sel["selection"]["points"]["location"]
    
    risk_info = juris_dict.get(state, juris_dict["Federal"])
    st.table(pd.DataFrame({"Category": ["Jurisdiction", "Risk", "Update"], "Detail": [state, risk_info['Risk'], risk_info['Update']]}).style.hide(axis="index"))

# --- TAB 5: LEAVE-BEHIND ---
with tab5:
    st.header("🖨️ Executive Leave-Behind")
    st.markdown("#### **Strategic Positioning (March 2026)**")
    st.write(f"- **Budget Discipline:** OpEx spend currently at ${ytd_spend}M ({(ytd_spend/total_budget)*100:.1f}% capacity).")
    st.write("- **Risk Stability:** WARR migration into 2026 shows stabilizing credit quality in Branded Cards.")
    components.html("<script>function print_summary() { window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=100)