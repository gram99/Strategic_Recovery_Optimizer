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
    if "password_correct" not in st.session_state:
        st.title("🏦 Citi Recovery Strategy Gateway")
        st.markdown("### **Executive Access Required**")
        st.text_input("Enter Access Code:", type="password", key="password_input")
        if st.button("Login"):
            if st.session_state["password_input"] == "Optimizer2026":
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
            'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
            'Current_NCO': [1.5, 1.9, 4.8, 2.1, 2.4]
        })
        
        # Vendor Data (Story-Driven Tiers)
        today = datetime.now().date()
        vendor_data = pd.DataFrame({
            'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
            'Tier': ['Tier 1', 'Tier 1', 'Tier 2', 'Tier 2', 'Tier 3'],
            'Efficiency (%)': [92, 88, 74, 68, 81],
            'YTD Spend ($M)': [120, 95, 45, 38, 22],
            'Placement ($M)': [850, 720, 310, 290, 115],
            'Renewal Date': [today + timedelta(days=x) for x in [120, 45, 15, 200, 365]]
        })
        
        # Jurisdictional Details
        juris_dict = {
            'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data remediation Dec 2025.'},
            'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.'},
            'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned.'},
            'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 drift remediation ongoing.'},
            'Federal': {'Risk': '🟡 Moderate', 'Focus': 'OCC Oversight', 'Update': 'Resource Review terminated Dec 2025.'}
        }
        geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [12, 45, 5, 38]})
        
        return warr_history, peers, vendor_data, juris_dict, geo_df

    warr_df, peer_df, vend_df, juris_dict, geo_df = get_master_data()

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
        st.markdown("> **Strategic Context:** Recovery yield optimization acts as a capital engine. Use the simulator below to see how increasing our yield 'unlocks' CET1 basis points.")
        
        # Capital Lift Simulator
        recovery_lift = st.slider("Target Yield Optimization Lift (%)", 0, 10, 2)
        rwa_relief = 165 * (1 + (recovery_lift/100))
        cet1_impact_bps = (rwa_relief / 13500) * 100 # Scaling against $1.35T RWA
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CET1 Capital Ratio", "13.2%", f"+{cet1_impact_bps:.2f} bps")
        c2.metric("2026 ROTCE Target", "10.5%", "On Track")
        c3.metric("RWA Relief ($M)", f"${rwa_relief:.1f}M", f"{recovery_lift}% Opt")
        c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
        
        st.divider()
        st.subheader("Historical WARR Risk Migration (2023 - 2026)")
        fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                          color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
        st.plotly_chart(fig_warr, use_container_width=True)

    # --- TAB 2: PEER STRATEGY & STRESS ---
    with tab2:
        st.header("Competitive Resilience & Stress Strategy")
        st.markdown("> **The Story:** Simulate a macro shock to see Citi's resilience gap compared to consumer-heavy lenders.")
        
        ctrl, chart = st.columns([1, 2])
        with ctrl:
            stress = st.select_slider("Recession Severity", options=["Mild", "Moderate", "Severely Adverse"])
            peer = st.selectbox("Compare Against:", peer_df['Bank'].unique(), index=2) # Cap One
            
            multi = {"Mild": 1.4, "Moderate": 1.8, "Severely Adverse": 2.8}[stress]
            citi_stressed = 2.4 * multi
            peer_stressed = peer_df[peer_df['Bank']==peer]['Current_NCO'].values[0] * multi
            
            st.metric("Resilience Gap", f"{peer_stressed-citi_stressed:.1f}%", delta="Lower is Better", delta_color="inverse")
        
        with chart:
            quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
            nco_curve = [2.4 * (1 + (i*0.08)*multi) for i in range(len(quarters))]
            st.plotly_chart(px.line(x=quarters, y=nco_curve, title=f"9Q NCO Projection: {stress}"), use_container_width=True)

    # --- TAB 3: VENDOR MANAGEMENT & SWAP ---
    with tab3:
        st.header("Vendor Performance & Budget Capacity")
        
        total_budget = 500 
        ytd_spend = vend_df['YTD Spend ($M)'].sum()
        
        b1, b2 = st.columns([1, 1.5])
        with b1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = ytd_spend,
                gauge = {'axis': {'range': [None, total_budget]}, 'bar': {'color': "#007bff"}}))
            fig_gauge.update_layout(height=250)
            st.plotly_chart(fig_gauge, use_container_width=True)
        with b2:
            # CLEAN TABLE: Hiding the index column
            st.dataframe(vend_df, hide_index=True, use_container_width=True)

        st.divider()
        st.subheader("Placement Swap Simulator")
        s1, s2, s3 = st.columns(3)
        with s1: src = st.selectbox("From:", vend_df['Vendor Name'], index=3)
        with s2: tgt = st.selectbox("To:", vend_df['Vendor Name'], index=2)
        
        gain = (vend_df[vend_df['Vendor Name']==tgt]['Efficiency (%)'].values[0] - 
                vend_df[vend_df['Vendor Name']==src]['Efficiency (%)'].values[0]) * 0.1
        with s3:
            st.metric("Recovery Gain/Loss", f"${gain:.2f}M", delta="on $10M shift")

    # --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
    with tab4:
        st.header("Jurisdictional Governance")
        st.markdown("**Click a state** to drill down into localized risk remediation.")
        
        fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
        # RERUN on select to update the table below
        sel = st.plotly_chart(fig_map, on_select="rerun")
        
        # Robust Selection Logic
        state = "Federal"
        try:
            if sel and "selection" in sel and sel["selection"]["points"]:
                state = sel["selection"]["points"][0]["location"]
        except (KeyError, IndexError):
            state = "Federal"
        
        st.divider()
        st.subheader(f"Detailed Risk Matrix: {state}")
        info = juris_dict.get(state, juris_dict["Federal"])
        
        # CLEAN TABLE: Hiding the index column
        risk_tbl = pd.DataFrame({
            "Category": ["Jurisdiction", "Risk Level", "Focus Area", "Latest Update"],
            "Detail": [state, info['Risk'], info['Focus'], info['Update']]
        })
        st.table(risk_tbl.style.hide(axis="index"))

    # --- TAB 5: LEAVE-BEHIND ---
    with tab5:
        st.header("Executive Leave-Behind")
        st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
        st.write(f"- **Yield-to-Capital:** Current lift simulation adds **{cet1_impact_bps:.2f} bps** to CET1 headroom.")
        st.write("- **Portfolio Health:** WARR stabilizes at 1.22 after 2024 optimization.")
        st.divider()
        st.warning("**MRM Disclosure:** Synthetic metrics anchored in public 2024-2025 Citi disclosures.")
        components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)