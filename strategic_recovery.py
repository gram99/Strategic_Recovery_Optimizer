import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Citi Strategic Recovery & Capital Optimizer", layout="wide")

# --- LOGIN GATEWAY ---
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🏦 Citi Recovery Strategy Gateway")
        st.text_input("Enter Executive Access Code:", type="password", key="password_input")
        if st.button("Login"):
            if st.session_state["password_input"] == "Citi2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect Access Code.")
        return False
    return True

if check_password():
    # 2. DATA ENGINE
    @st.cache_data
    def get_master_data():
        # Historical WARR Migration
        warr_history = pd.DataFrame({
            'Year': ['2023-24', '2023-24', '2024-25', '2024-25', '2025-26', '2025-26'],
            'Segment': ['Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services'],
            'WARR': [1.05, 5.20, 1.35, 6.45, 1.22, 6.10]
        })
        
        # Peer Benchmarking
        peers = pd.DataFrame({
            'Bank': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026)'],
            'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5]
        }).sort_values('ROTCE (%)', ascending=False)
        
        # 9Q DFAST Stress
        quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
        stress_df = pd.DataFrame({
            'Quarter': quarters, 
            'Severely Adverse (9Q)': [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2],
            'Macro Impact': ['10% Peak Unemployment' for _ in range(9)]
        })
        
        # Vendor Data (Fixed Syntax)
        today = datetime.now().date()
        vendor_data = pd.DataFrame({
            'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
            'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
            'Efficiency %': [92, 85, 78, 68, 88],
            'YTD Spend ($M)': [120, 95, 45, 82, 35],
            'Placement ($M)': [1200, 950, 450, 820, 350],
            'Renewal Date': [today + timedelta(days=x) for x in [30, 90, 15, 120, 200]]
        })
        
        # Jurisdictional Data
        juris_dict = {
            'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data controls remediation Dec 2025.'},
            'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.'},
            'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned.'},
            'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 drift remediation ongoing.'},
            'Federal': {'Risk': '🟡 Moderate', 'Focus': 'OCC Oversight', 'Update': 'Resource Review terminated Dec 2025.'}
        }
        geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [12, 45, 8, 31]})
        
        return warr_history, peers, stress_df, vendor_data, juris_dict, geo_df

    warr_df, peer_df, stress_df, vend_df, juris_dict, geo_df = get_master_data()

    # 3. GLOBAL SIDEBAR
    with st.sidebar:
        st.image("https://www.citigroup.com", width=80)
        st.header("Executive Dashboard")
        st.divider()
        if st.button("Logout"):
            del st.session_state["password_correct"]
            st.rerun()

    # 4. MULTI-TAB INTERFACE
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Executive Capital Report", "Peer Strategy & Stress", "Vendor Management", "Regulatory Heatmap", "LEAVE-BEHIND"
    ])

    # --- TAB 1: EXECUTIVE CAPITAL REPORT ---
    with tab1:
        st.header("Executive Capital & Shareholder Value Report")
        # FIXED: Added integer '4' to st.columns
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CET1 Capital Ratio", "13.2%", "+160bps Buffer")
        c2.metric("2026 ROTCE Target", "10.5%", "On Track")
        c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
        c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
        
        st.divider()
        st.subheader("Historical WARR Risk Migration (2023 - 2026)")
        fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                          title="WARR Evolution: Post-Pandemic to 2026 Optimization",
                          color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
        st.plotly_chart(fig_warr, use_container_width=True)

    # --- TAB 2: PEER & STRESS ANALYSIS ---
    with tab2:
        st.header("The Competitive Advantage: Peer & Stress Strategy")
        # FIXED: Added integer '2' to st.columns
        col_p, col_s = st.columns(2)
        with col_p:
            st.plotly_chart(px.bar(peer_df, x='Bank', y='ROTCE (%)', color='Bank', title="Competitive ROTCE Benchmarking"), use_container_width=True)
        with col_s:
            fig_stress = px.line(stress_df, x='Quarter', y='Severely Adverse (9Q)', 
                                 title="9-Quarter Severe NCO Projection (DFAST)",
                                 hover_data={'Macro Impact': True})
            st.plotly_chart(fig_stress, use_container_width=True)

    # --- TAB 3: VENDOR MANAGEMENT ---
    with tab3:
        st.header("🏢 Vendor Performance & Budget Capacity")
        total_budget = 500 
        ytd_spend = vend_df['YTD Spend ($M)'].sum()
        
        # FIXED: Added integer '2' to st.columns
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = ytd_spend,
                title = {'text': "OpEx Budget Utilization ($M)"},
                gauge = {'axis': {'range': [None, total_budget]}, 'bar': {'color': "#007bff"},
                         'threshold' : {'line': {'color': "red", 'width': 4}, 'value': 450}}))
            st.plotly_chart(fig_gauge, use_container_width=True)
        with b_col2:
            st.dataframe(vend_df, hide_index=True, use_container_width=True)

        st.divider()
        st.subheader("🔄 Strategic Placement Swap Simulator")
        # FIXED: Added integer '3' to st.columns
        s1, s2, s3 = st.columns(3)
        with s1: source = st.selectbox("From:", vend_df['Vendor Name'], index=3)
        with s2: target = st.selectbox("To:", vend_df['Vendor Name'], index=2)
        
        s_eff = vend_df[vend_df['Vendor Name']==source]['Efficiency %'].values[0]
        t_eff = vend_df[vend_df['Vendor Name']==target]['Efficiency %'].values[0]
        gain = (t_eff - s_eff) * 0.1 
        
        with s3:
            st.metric("Recovery Gain/Loss", f"${gain:.2f}M", delta=f"{t_eff-s_eff}% Efficiency Delta")

    # --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
    with tab4:
        st.header("Jurisdictional Governance")
        fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
        sel = st.plotly_chart(fig_map, on_select="rerun")
        
        state = "Federal"
        if sel and "selection" in sel and sel["selection"]["points"]:
            # FIXED: Added index [0] to the points list
            state = sel["selection"]["points"][0]["location"]
        
        st.divider()
        st.subheader(f"📍 Detailed Risk Matrix: {state}")
        risk_info = juris_dict.get(state, juris_dict["Federal"])
        risk_tbl = pd.DataFrame({"Category": ["Jurisdiction", "Risk", "Focus"], "Detail": [state, risk_info['Risk'], risk_info['Focus']]})
        st.table(risk_tbl.style.hide(axis="index"))

    # --- TAB 5: LEAVE-BEHIND ---
    with tab5:
        st.header("🖨️ Executive Leave-Behind")
        st.markdown("#### **Strategic Positioning (Q1 2026)**")
        st.write(f"- **Budget Performance:** YTD Spend at ${ytd_spend}M vs ${total_budget}M cap.")
        st.write("- **Portfolio Health:** WARR stabilizes at 1.22 after 2024 optimization.")
        components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)