import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Strategic Recovery & Capital Optimizer", layout="wide")

# --- LOGIN GATEWAY ---
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "Recovery2026$": # Hypothetical password
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.title("Recovery Strategy Gateway")
        st.text_input("Please enter the Access Code:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.title("Recovery Strategy Gateway")
        st.text_input("Please enter the Access Code:", type="password", on_change=password_entered, key="password")
        st.error("Access Code incorrect. Please contact the Recovery Strategy Office.")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # 2. DATA ENGINE
    @st.cache_data
    def get_master_data():
        # WARR History: Story of 2024 Stress vs 2026 Stabilization
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
        nco_severe = [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2] 
        stress_df = pd.DataFrame({'Quarter': quarters, 'Severely Adverse (9Q)': nco_severe})
        
        # Strategic Vendor Data (FIXED: Populated missing values)
        today = datetime.now().date()
        vendor_data = pd.DataFrame({
            'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
            'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
            'Efficiency %': [92, 88, 74, 68, 81],
            'YTD Spend ($M)': [140, 110, 85, 45, 20],
            'Capacity ($M)': [200, 150, 100, 80, 40],
            'Renewal Date': [today + timedelta(days=x) for x in [45, 120, 15, 210, 90]]
        })
        
        # Jurisdictional Data
        juris_dict = {
            'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data remediation Dec 2025.'},
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
        st.header("Executive Hub")
        st.success("🟢 CET1 Ratio: 13.2%") 
        st.info("2026 ROTCE Target: 10.5%")
        if st.button("Logout"):
            st.session_state["password_correct"] = False
            st.rerun()

    # 4. MULTI-TAB INTERFACE
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Executive Capital Report", "Peer Strategy & Stress", "Vendor & Budget Management", "Regulatory Heatmap", "LEAVE-BEHIND"
    ])

    # --- TAB 1: EXECUTIVE CAPITAL REPORT & WARR STORY ---
    with tab1:
        st.header("Executive Capital & Shareholder Value Report")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CET1 Capital Ratio", "13.2%", "+160bps Buffer")
        c2.metric("2026 ROTCE Target", "10.5%", "On Track")
        c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
        c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
        
        st.divider()
        st.subheader("Historical WARR Risk Migration (2023 - 2026)")
        fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                          title="WARR Evolution: Tracking the 2024 Stress Peak to 2026 Stabilization",
                          color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
        st.plotly_chart(fig_warr, use_container_width=True)

        with st.expander("Analysis: Synthetic WARR Migration Methodology"):
            st.markdown("""
            **The Story Behind the Data:**
            - **2023-24 (Stabilization):** Reflects normalized post-pandemic delinquency rates.
            - **2024-25 (Stress Peak):** The 1.35 spike in Branded Cards captures the peak inflationary pressure on the US consumer.
            - **2025-26 (Optimization):** Current stabilization to 1.22 reflects successful litigation-heavy strategies in the 'long-tail' segment.
            """)

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
        
        total_budget = 500 # $500M 
        ytd_spend = vend_df['YTD Spend ($M)'].sum()
        
        b_col1, b_col2 = st.columns([1, 2])
        with b_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = ytd_spend,
                title = {'text': "OpEx Budget Utilization ($M)"},
                gauge = {'axis': {'range': [None, total_budget]}, 'bar': {'color': "#007bff"},
                         'threshold' : {'line': {'color': "red", 'width': 4}, 'value': 450}}))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with b_col2:
            st.dataframe(vend_df, hide_index=True, use_container_width=True)

    # --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
    with tab4:
        st.header("Jurisdictional Governance")
        fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
        sel = st.plotly_chart(fig_map, on_select="rerun")
        
        state = "Federal"
        if sel and "selection" in sel and sel["selection"]["points"]:
            state = sel["selection"]["points"]["location"]
        
        risk_info = juris_dict.get(state, juris_dict["Federal"])
        st.table(pd.DataFrame({"Category": ["Jurisdiction", "Risk Level", "Focus"], "Detail": [state, risk_info['Risk'], risk_info['Focus']]}).style.hide(axis="index"))

    # --- TAB 5: LEAVE-BEHIND & DISCLOSURE ---
    with tab5:
        st.header("Executive Briefing & Disclosures")
        st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
        st.write(f"- **Budget Performance:** YTD Spend at ${ytd_spend}M vs ${total_budget}M cap.")
        st.write("- **Portfolio Health:** WARR stabilizes at 1.22 following proactive 2024 optimization.")
        
        st.divider()
        st.subheader("Model Risk Management (MRM) Disclosure")
        st.warning("""
        **Synthetic Data Disclaimer:**
        All metrics provided herein (WARR, NCO Projections, Vendor Efficiency) are **synthetic representations** created for the purpose of demonstrating 
        analytical capabilities. They are anchored in public 2024-2025 Citigroup financial filings and DFAST disclosures but do not represent 
        actual non-public proprietary banking data.
        """)
        
        components.html("<script>function print_summary() { window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=100)