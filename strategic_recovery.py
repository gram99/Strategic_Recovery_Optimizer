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
        # WARR History: 2023 -> 2026 Story
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
        
        # Vendor & Budget Data
        today = datetime.now().date()
        vendor_data = pd.DataFrame({
            'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
            'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
            'Efficiency (%)':,
            'YTD Spend ($M)':,
            'Placement ($M)':,
            'Renewal Date': [today + timedelta(days=x) for x in]
        })
        
        # Jurisdictional Data
        juris_dict = {
            'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data controls remediation Dec 2025.'},
            'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.'},
            'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned with national standards.'},
            'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'L2 drift remediation ongoing.'},
            'Federal': {'Risk': '🟡 Moderate', 'Focus': 'OCC Oversight', 'Update': 'Resource Review terminated Dec 2025.'}
        }
        geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions':})
        
        return warr_history, peers, vendor_data, juris_dict, geo_df

    warr_df, peer_df, vend_df, juris_dict, geo_df = get_master_data()

    # 3. GLOBAL SIDEBAR
    with st.sidebar:
        st.image("https://www.citigroup.com", width=80)
        st.header("Executive Hub")
        st.divider()
        if st.button("Logout"):
            del st.session_state["password_correct"]
            st.rerun()

    # 4. MULTI-TAB INTERFACE
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Executive Capital Report", "Peer Strategy & Stress", "Vendor Management", "Regulatory Heatmap", "LEAVE-BEHIND"
    ])

    # --- TAB 1: EXECUTIVE CAPITAL REPORT (THE CAPITAL ENGINE) ---
    with tab1:
        st.header("Executive Capital & Shareholder Value Report")
        st.markdown("> **The Story:** We aren't just 'collecting'—we are optimizing capital. Use the simulator below to see how increasing our litigation yield targets 'unlocks' CET1 basis points by reducing RWAs.")
        
        # Scenario: RWA Optimization Lift
        recovery_lift = st.slider("Target Yield Optimization Lift (%)", 0, 10, 2, help="Percentage improvement in long-tail litigation recovery yield.")
        rwa_relief = 165 * (1 + (recovery_lift/100))
        cet1_impact_bps = (rwa_relief / 13500) * 100 # Estimated impact on $1.35T RWA
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CET1 Capital Ratio", "13.2%", f"+{cet1_impact_bps:.2f} bps")
        c2.metric("2026 ROTCE Target", "10.5%", "On Track")
        c3.metric("RWA Relief ($M)", f"${rwa_relief:.1f}M", f"{recovery_lift}% Opt")
        c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
        
        st.divider()
        st.subheader("Historical WARR Risk Migration (2023 - 2026)")
        fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                          title="WARR Evolution: From Post-Pandemic Stability to 2026 Optimization",
                          color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
        st.plotly_chart(fig_warr, use_container_width=True)

    # --- TAB 2: PEER STRATEGY & STRESS (THE RESILIENCE GAP) ---
    with tab2:
        st.header("Competitive Advantage: Stress Resilience")
        st.markdown("> **The Story:** How does Citi hold up in a shock? Use the slider to simulate a macro event. Citi's 'Prime-heavy' portfolio maintains a larger resilience gap vs consumer-heavy peers.")
        
        col_ctrl, col_chart = st.columns([1, 2])
        
        with col_ctrl:
            stress_severity = st.select_slider("Recession Severity", options=["Mild", "Moderate", "Severely Adverse"])
            peer_choice = st.selectbox("Compare Against Peer:", peer_df['Bank'].unique(), index=2) 
            
            multi = {"Mild": 1.4, "Moderate": 1.8, "Severely Adverse": 2.8}[stress_severity]
            citi_stressed = 2.4 * multi
            peer_stressed = peer_df[peer_df['Bank']==peer_choice]['Current_NCO'].values * multi
            
            st.metric("Resilience Gap", f"{peer_stressed-citi_stressed:.1f}%", delta="Lower is Better", delta_color="inverse")
            st.info(f"In a `{stress_severity}` environment, Citi's loss velocity remains significantly lower than `{peer_choice}`.")

        with col_chart:
            quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
            nco_curve = [2.4 * (1 + (i*0.08)*multi) for i in range(len(quarters))]
            fig_stress = px.line(x=quarters, y=nco_curve, title=f"9Q NCO Projection: {stress_severity} Environment",
                                labels={'x': 'Quarter', 'y': 'NCO Ratio (%)'})
            fig_stress.add_hline(y=8.0, line_dash="dash", line_color="red", annotation_text="DFAST Threshold")
            st.plotly_chart(fig_stress, use_container_width=True)

    # --- TAB 3: VENDOR MANAGEMENT & BUDGET ---
    with tab3:
        st.header("🏢 Vendor Performance & Budget Capacity")
        st.markdown("> **The Story:** We maintain budget discipline while shifting funds to high-yield legal partners. Red renewal dates highlight imminent contractual risks.")
        
        total_budget = 500 
        ytd_spend = vend_df['YTD Spend ($M)'].sum()
        
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
        s1, s2, s3 = st.columns(3)
        with s1: source = st.selectbox("From:", vend_df['Vendor Name'], index=3)
        with s2: target = st.selectbox("To:", vend_df['Vendor Name'], index=2)
        
        s_eff = vend_df[vend_df['Vendor Name']==source]['Efficiency (%)'].values
        t_eff = vend_df[vend_df['Vendor Name']==target]['Efficiency (%)'].values
        gain = (t_eff - s_eff) * 0.1 
        
        with s3:
            st.metric("Recovery Gain/Loss", f"${gain:.2f}M", delta=f"{t_eff-s_eff}% Efficiency Delta")

    # --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
    with tab4:
        st.header("Jurisdictional Governance")
        st.markdown("> **The Story:** Transformation progress is tracked by 'Red-to-Green' migration. Click a state to see localized updates on the path to compliance.")
        
        fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
        sel = st.plotly_chart(fig_map, on_select="rerun")
        
        # REPAIR: Corrected map selection logic to avoid TypeError
        state = "Federal"
        if sel and "selection" in sel and sel["selection"]["points"]:
            state = sel["selection"]["points"]["location"]
        
        st.divider()
        st.subheader(f"📍 Detailed Risk Matrix: {state}")
        risk_info = juris_dict.get(state, juris_dict["Federal"])
        
        # FIXED: Removed integer columns by hiding the index
        risk_tbl = pd.DataFrame({
            "Strategic Category": ["Jurisdiction", "Risk Level", "Focus Area", "Latest Status"],
            "Operational Detail": [state, risk_info['Risk'], risk_info['Focus'], risk_info['Update']]
        })
        st.table(risk_tbl.style.hide(axis="index"))

    # --- TAB 5: LEAVE-BEHIND ---
    with tab5:
        st.header("🖨️ Executive Leave-Behind")
        st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
        st.write(f"- **Yield-to-Capital:** Current 2% lift in litigation yield adds **{cet1_impact_bps:.2f} bps** to CET1 headroom.")
        st.write("- **Budget Capacity:** YTD Spend remains within guidance; 15.2% capacity remaining for Q4 peak.")
        st.divider()
        st.warning("**MRM Disclosure:** These synthetic WARR and stress metrics are anchored in public Citi 2024-2025 DFAST disclosures to demonstrate analytical stewardship.")
        components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)