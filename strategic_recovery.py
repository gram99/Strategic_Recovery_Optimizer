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
        st.markdown("### **Executive Access Required**")
        st.text_input("Enter Access Code:", type="password", key="password_input")
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
        # WARR History: Story of 2024 Stress vs 2026 Stabilization
        warr_history = pd.DataFrame({
            'Year': ['2023-24', '2023-24', '2024-25', '2024-25', '2025-26', '2025-26'],
            'Segment': ['Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services'],
            'WARR': [1.05, 5.20, 1.35, 6.45, 1.22, 6.10]
        })
        
        # Peer Benchmarking - Path to 11% ROTCE
        peers = pd.DataFrame({
            'Bank': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026 Target)'],
            'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5]
        }).sort_values('ROTCE (%)', ascending=False)
        
        # 9Q DFAST Stress - Resilience under 10% Unemployment
        quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
        nco_severe = [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2] 
        stress_df = pd.DataFrame({
            'Quarter': quarters, 
            'Severely Adverse (9Q)': nco_severe,
            'Macro Impact': ['Hypothetical 10% Peak Unemployment & 40% CRE decline' for _ in range(9)]
        })
        
        # Strategic Vendor Data - REPAIRED: Populated all missing values
        today = datetime.now().date()
        vendor_data = pd.DataFrame({
            'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
            'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
            'Efficiency %': [92, 85, 78, 65, 88],
            'YTD Spend ($M)': [120, 85, 45, 60, 30],
            'Placement ($M)': [450, 320, 180, 240, 110],
            'Renewal Date': [today + timedelta(days=x) for x in [45, 90, 15, 120, 210]]
        })
        
        # Jurisdictional Data for Interactive Map
        juris_dict = {
            'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data controls remediation Dec 2025.'},
            'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.'},
            'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned with national standards.'},
            'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 drift remediation ongoing.'},
            'Federal': {'Risk': '🟡 Moderate', 'Focus': 'OCC Oversight', 'Update': 'Resource Review terminated Dec 2025.'}
        }
        # REPAIRED: Populated missing exceptions data
        geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [2, 14, 5, 21]})
        
        return warr_history, peers, stress_df, vendor_data, juris_dict, geo_df

    warr_df, peer_df, stress_df, vend_df, juris_dict, geo_df = get_master_data()

    # 3. GLOBAL SIDEBAR
    with st.sidebar:
        st.image("https://www.citigroup.com", width=80)
        st.header("Strategic Controls")
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
        st.markdown("> **Strategic Context:** Recovery yield optimization acts as a capital engine, fueling our path to an **11% ROTCE waypoint**.")
        
        # INTEGRATED TARGETS: Primary North Star Metrics
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

    # --- TAB 2: PEER STRATEGY & STRESS ---
    with tab2:
        st.header("Competitive Resilience & Stress Strategy")
        st.markdown("> **The Story:** While rivals face 4.8% NCOs, Citi's high-FICO tail strategy remains resilient. Even under 10% unemployment, our portfolio out-earns immediate asset sales.")
        
        col_p, col_s = st.columns(2)
        with col_p:
            st.plotly_chart(px.bar(peer_df, x='Bank', y='ROTCE (%)', color='Bank', title="Competitive ROTCE Benchmarking"), use_container_width=True)
        with col_s:
            # REPAIRED: Hover-over description integrated
            fig_stress = px.line(stress_df, x='Quarter', y='Severely Adverse (9Q)', 
                                 title="9-Quarter Severe NCO Projection (DFAST)",
                                 hover_data={'Macro Impact': True})
            st.plotly_chart(fig_stress, use_container_width=True)

    # --- TAB 3: VENDOR MANAGEMENT & SWAP SIMULATOR ---
    with tab3:
        st.header("🏢 Vendor Performance & Budget Capacity")
        
        total_budget = 500 # $500M 
        ytd_spend = vend_df['YTD Spend ($M)'].sum()
        
        b_col1, b_col2 = st.columns()
        with b_col1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = ytd_spend,
                title = {'text': "OpEx Budget Utilization ($M)"},
                gauge = {'axis': {'range': [None, total_budget]}, 'bar': {'color': "#007bff"},
                         'threshold' : {'line': {'color': "red", 'width': 4}, 'value': 450}}))
            st.plotly_chart(fig_gauge, use_container_width=True)
        with b_col2:
            st.subheader("📍 Active Vendor Network")
            st.dataframe(vend_df, hide_index=True, use_container_width=True)

        st.divider()

        # SWAP SIMULATOR: Monetary Gain/Loss
        st.subheader("🔄 Strategic Placement Swap Simulator")
        st.markdown("Assess the monetary impact of shifting **$10M** in placements between agencies.")
        s1, s2, s3 = st.columns(3)
        with s1: source = st.selectbox("From (Source Vendor):", vend_df['Vendor Name'], index=3)
        with s2: target = st.selectbox("To (Target Vendor):", vend_df['Vendor Name'], index=2)
        
        # Scalar calculation for delta
        s_eff = vend_df[vend_df['Vendor Name']==source]['Efficiency %'].values[0]
        t_eff = vend_df[vend_df['Vendor Name']==target]['Efficiency %'].values[0]
        gain = (t_eff - s_eff) * 0.1 # Monetary impact on $10M shift
        
        with s3:
            st.metric("Projected Recovery Gain/Loss", f"${gain:.2f}M", delta=f"{t_eff-s_eff}% Efficiency Delta")

    # --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
    with tab4:
        st.header("Jurisdictional Governance")
        st.markdown("👇 **Click a state** to drill down into localized risk remediation.")
        
        fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
        # REPAIRED: Capture selection with correct rerun trigger
        sel = st.plotly_chart(fig_map, on_select="rerun")
        
        state = "Federal"
        if sel and "selection" in sel and sel["selection"]["points"]:
            # REPAIRED: Fixed TypeError by indexing the list
            state = sel["selection"]["points"][0]["location"]
        
        st.divider()
        st.subheader(f"📍 Detailed Risk Matrix: {state}")
        risk_info = juris_dict.get(state, juris_dict["Federal"])
        
        risk_tbl = pd.DataFrame({
            "Category": ["Jurisdiction", "Risk Level", "Focus Area", "Latest Status"],
            "Detail": [state, risk_info['Risk'], risk_info['Focus'], risk_info['Update']]
        })
        st.table(risk_tbl.style.hide(axis="index"))

    # --- TAB 5: LEAVE-BEHIND & DISCLOSURE ---
    with tab5:
        st.header("🖨️ Executive Briefing")
        st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
        st.write(f"- **Budget Performance:** YTD Spend at ${ytd_spend}M vs ${total_budget}M cap.")
        st.write("- **Portfolio Health:** WARR stabilizes at 1.22 following 2024 optimization.")
        
        st.divider()
        st.subheader("⚠️ Model Risk Management (MRM) Disclosure")
        st.warning("""
        **Synthetic WARR Methodology:** Metrics are anchored in public Citi DFAST disclosures to demonstrate analytical stewardship. 
        Calculations assume a baseline cost of capital and utilize standardized RWA density profiles.
        """)
        
        components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)