import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Strategic Recovery & Capital Optimizer", layout="wide")

# 2. DATA ENGINE (Anchored to March 2026 Strategic Context)
@st.cache_data
def get_master_data():
    # Peer Benchmarking - Story: Path to 11% ROTCE
    peers = pd.DataFrame({
        'Bank': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026 Target)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
        'CET1 Ratio (%)': [15.1, 10.2, 13.2, 11.8, 12.3]
    }).sort_values('ROTCE (%)', ascending=False)
    
    # 9Q DFAST Stress - Story: Resilience under 10% Unemployment
    quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
    nco_severe = [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2] 
    stress_df = pd.DataFrame({
        'Quarter': quarters, 
        'Severely Adverse (9Q)': nco_severe,
        'Macro Impact': ['Hypothetical 10% Peak Unemployment & 40% CRE decline' for _ in range(9)]
    })
    
    # Strategic Vendor List
    today = datetime.now().date()
    vendor_data = pd.DataFrame({
        'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
        'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
        'Core Segment': ['Mass Market Card', 'Retail Services', 'High-FICO Litigation', 'High-Balance Tail', 'Commercial/SME'],
        'Efficiency (%)':,
        'Capital Drag (bps)': [1.2, 2.4, 6.8, 8.2, 3.1],
        'Placement ($M)':,
        'Renewal Date': [today + timedelta(days=x) for x in]
    })
    
    # Jurisdictional Data for Interactive Map
    juris_dict = {
        'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'AML reporting shift noted Feb 2026.'},
        'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA compliance audit active.'},
        'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned with national standards.'},
        'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 audit scheduled Q2 2026 due to vendor drift.'},
        'Federal': {'Risk': '🟡 Moderate', 'Focus': 'Data Controls', 'Update': 'OCC terminated Resource Review Dec 2025.'}
    }
    geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions':})
    
    return peers, stress_df, vendor_data, juris_dict, geo_df

peers, stress_df, vend_df, juris_dict, geo_df = get_master_data()

# 3. GLOBAL SIDEBAR
with st.sidebar:
    st.image("https://www.citigroup.com", width=80)
    st.header("Executive Dashboard")
    scenario = st.selectbox("Strategic Mode", ["Standard Operations", "DFAST Stress Test"])
    st.divider()
    st.info("**2026 ROTCE Target:** 10.5%")
    st.success("**CET1 Buffer:** +130bps vs Req")
    st.markdown("[🔗 Citi IR: Financial Earnings](https://www.citigroup.com)")

# 4. MULTI-TAB INTERFACE
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Capital Report", "Peer Strategy & Stress", "Vendor Management", "Regulatory Heatmap", "LEAVE-BEHIND"
])

# --- TAB 1: EXECUTIVE CAPITAL REPORT ---
with tab1:
    st.header("Executive Capital & Shareholder Value Report")
    st.markdown("""
    > **Strategic Context:** Recovery Operations is a **Capital Engine**. Every $100M in recovered 'long-tail' yield directly lowers 
    Risk-Weighted Assets (RWA), providing the capital headroom necessary to hit our **11% ROTCE target** by year-end 2026.
    """)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CET1 Capital Ratio", "13.2%", "+160bps Buffer")
    c2.metric("2026 ROTCE Target", "10.5%", "On Track")
    c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
    c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
    
    st.divider()
    st.subheader("WARR Risk Migration by Segment")
    w_data = pd.DataFrame({'Segment': ['Branded Cards', 'Retail Services'], 'WARR': [1.2, 6.1]})
    st.bar_chart(w_data.set_index('Segment'))

# --- TAB 2: PEER STRATEGY & STRESS ---
with tab2:
    st.header("The Competitive Advantage: Peer & Stress Strategy")
    st.markdown("""
    > **Strategic Context:** While industry rivals face rising delinquency, Citi’s High-FICO tail strategy maintains resilience. 
    Even under the **Severely Adverse** (10% unemployment) scenario, our litigation yield significantly outperforms asset liquidation.
    """)
    
    col_p, col_s = st.columns(2)
    with col_p:
        st.plotly_chart(px.bar(peers, x='Bank', y='ROTCE (%)', color='Bank', title="Competitive ROTCE Benchmarking"), use_container_width=True)
    with col_s:
        # Hover-over description integrated
        fig_stress = px.line(stress_df, x='Quarter', y='Severely Adverse (9Q)', 
                             title="9-Quarter Severe NCO Projection (DFAST)",
                             hover_data={'Macro Impact': True})
        st.plotly_chart(fig_stress, use_container_width=True)

# --- TAB 3: VENDOR MANAGEMENT ---
with tab3:
    st.header("Vendor Performance & Capital Optimizer")
    st.markdown("""
    > **Strategic Context:** We reallocate funds from high-drag mass agencies to high-yield legal partners. 
    **Red Renewal Dates** indicate imminent contract risks requiring MD approval for Q2 placement continuity.
    """)

    def color_renewals(val):
        color = 'red' if val < (datetime.now().date() + timedelta(days=30)) else 'black'
        return f'color: {color}; font-weight: bold' if color == 'red' else ''
    
    # Hide index for clean executive table
    st.dataframe(vend_df.style.applymap(color_renewals, subset=['Renewal Date'])
                .background_gradient(subset=['Efficiency (%)'], cmap='YlGn'),
                hide_index=True, use_container_width=True)
    
    st.divider()
    st.subheader("Strategic Placement Swap Simulator")
    sim1, sim2 = st.columns(2)
    with sim1: source = st.selectbox("From (Source):", vend_df['Vendor Name'], index=3)
    with sim2: target = st.selectbox("To (Target):", vend_df['Vendor Name'], index=2)
    
    gain = (vend_df[vend_df['Vendor Name']==target]['Efficiency (%)'].values - 
            vend_df[vend_df['Vendor Name']==source]['Efficiency (%)'].values) * 0.1
    st.metric("Net Recovery Gain/Loss ($M)", f"${gain:.2f}M")

# --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
with tab4:
    st.header("Jurisdictional Exceptions Map")
    st.markdown("""
    > **Strategic Context:** Transformation progress is tracked by **Red-to-Green migration**. 
    **Click a state** to drill down into 2026 compliance hurdles, such as CA ADMT or NY Fair Lending.
    """)

    fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", 
                           color='Exceptions', scope="usa", color_continuous_scale="Reds")
    sel = st.plotly_chart(fig_map, on_select="rerun")

    state = "Federal"
    if sel and "selection" in sel and sel["selection"]["points"]:
        state = sel["selection"]["points"]["location"]

    st.subheader(f"Detailed Risk Matrix: {state}")
    risk_info = juris_dict.get(state, juris_dict["Federal"])
    
    # Clean table with explicit headers and hidden index
    risk_tbl = pd.DataFrame({
        "Strategic Category": ["Jurisdiction", "Risk Level", "Primary Focus", "Recent Update"],
        "Operational Detail": [state, risk_info['Risk'], risk_info['Focus'], risk_info['Update']]
    })
    st.table(risk_tbl.style.hide(axis="index"))

# --- TAB 5: LEAVE-BEHIND ---
with tab5:
    st.header("Executive Leave-Behind Summary")
    st.markdown("#### **Strategic Positioning (March 2026)**")
    st.write("* **ROTCE Catalyst:** Long-tail recovery yield is a primary driver for the **10.5% waypoint**.")
    st.write("* **Capital Strength:** **13.2% CET1 ratio** confirms successful RWA optimization efforts.")
    st.write("* **Regulatory Milestone:** Dec 2025 OCC termination signals risk control stability.")
    components.html("""
    <script>function print_summary() { window.print(); }</script>
    <button onclick="print_summary()" style="background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
        Download PDF Summary
    </button>""", height=100)