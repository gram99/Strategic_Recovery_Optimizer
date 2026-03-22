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
        st.title("Recovery Strategy Gateway")
        st.text_input("Enter Access Code:", type="password", key="password_input")
        if st.button("Login"):
            if st.session_state["password_input"] == "Recovery2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Access Code Incorrect.")
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
        
        # Peer Metrics Table
        peers = pd.DataFrame({
            'Bank Indicator': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026 Target)'],
            'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
            'Current NCO (%)': [1.5, 1.9, 4.8, 2.1, 2.4]
        })
        
        # Vendor & Budget Data
        today = datetime.now().date()
        vendor_data = pd.DataFrame({
            'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
            'Tier': ['Tier 1', 'Tier 1', 'Tier 2', 'Tier 2', 'Tier 3'],
            'Efficiency (%)':,
            'YTD Spend ($M)':,
            'Capacity ($M)':,
            'Renewal Date': [today + timedelta(days=x) for x in]
        })
        
        # Jurisdictional Data
        juris_dict = {
            'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data remediation Dec 2025.'},
            'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.'},
            'TX': {'Risk': '🟢 Stable', 'Focus': 'Documentation', 'Update': 'Process aligned.'},
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

    # --- TAB 1: EXECUTIVE CAPITAL REPORT (TRENDLINES & DATA TABLE) ---
    with tab1:
        st.header("Executive Capital & Shareholder Value Report")
        
        # Capital Simulation
        recovery_lift = st.slider("Target Yield Optimization Lift (%)", 0, 10, 2)
        cet1_bps = ((165 * (1 + (recovery_lift/100))) / 13500) * 100
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("CET1 Capital Ratio", "13.2%", f"+{cet1_bps:.2f} bps")
        c2.metric("2026 ROTCE Target", "10.5%", "On Track")
        c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
        c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
        
        st.divider()
        st.subheader("Historical WARR Migration with Risk Trendlines")
        
        # Creating Bar Chart with Trendlines
        fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                          color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
        
        # Adding Synthetic Trendlines for each segment
        fig_warr.add_trace(go.Scatter(x=['2023-24', '2024-25', '2025-26'], y=[1.05, 1.35, 1.22], name="Branded Trend", line=dict(color="#007bff", dash='dot')))
        fig_warr.add_trace(go.Scatter(x=['2023-24', '2024-25', '2025-26'], y=[5.20, 6.45, 6.10], name="Retail Trend", line=dict(color="#ff4b4b", dash='dot')))
        
        st.plotly_chart(fig_warr, use_container_width=True)

        st.subheader("Historical WARR Data Points")
        st.dataframe(warr_df.pivot(index="Year", columns="Segment", values="WARR"), use_container_width=True)

    # --- TAB 2: PEER STRATEGY & DYNAMIC STRESS ---
    with tab2:
        st.header("Competitive Advantage & Dynamic Stress Resilience")
        st.markdown("> **The Story:** Adjust the slider to see how Citi's 'long-tail' recovery yield protects us during a macro shock.")
        
        stress_severity = st.select_slider("Select Macro Scenario Severity", options=["Baseline", "Mild", "Moderate", "Severely Adverse"])
        
        col_table, col_graph = st.columns([1, 1.5])
        
        with col_table:
            st.subheader("Peer Benchmarking")
            st.dataframe(peer_df, hide_index=True, use_container_width=True)

        with col_graph:
            # Dynamic Stress Logic
            multi = {"Baseline": 1.0, "Mild": 1.3, "Moderate": 1.8, "Severely Adverse": 2.8}[stress_severity]
            quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
            
            # Curve calculation that actually reacts to the slider
            nco_base = 2.4
            curve = [nco_base * (1 + (i*0.1) * (multi-0.5)) for i in range(len(quarters))]
            
            fig_stress = px.line(x=quarters, y=curve, title=f"9Q NCO Projection: {stress_severity} Environment",
                                labels={'x': 'Quarter', 'y': 'NCO Ratio (%)'})
            fig_stress.add_hline(y=8.0, line_dash="dash", line_color="red", annotation_text="DFAST Threshold")
            st.plotly_chart(fig_stress, use_container_width=True)

    # --- TAB 3: VENDOR MANAGEMENT & SPEEDOMETER ---
    with tab3:
        st.header("Vendor Performance & Budget Capacity")
        
        total_budget = 500 
        ytd_spend = vend_df['YTD Spend ($M)'].sum()
        
        # Restored Full-Size Speedometer
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta", value = ytd_spend,
            title = {'text': "Recovery OpEx Budget Utilization ($M)"},
            delta = {'reference': total_budget, 'increasing': {'color': "red"}},
            gauge = {'axis': {'range': [None, total_budget]}, 
                     'bar': {'color': "#007bff"},
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 450}}))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.subheader("Active Vendor Network")
        st.dataframe(vend_df, hide_index=True, use_container_width=True)

        st.divider()
        st.subheader("Strategic Placement Swap Simulator")
        s1, s2, s3 = st.columns(3)
        with s1: src = st.selectbox("From (Source):", vend_df['Vendor Name'], index=3)
        with s2: tgt = st.selectbox("To (Target):", vend_df['Vendor Name'], index=2)
        
        gain = (vend_df[vend_df['Vendor Name']==tgt]['Efficiency (%)'].values - 
                vend_df[vend_df['Vendor Name']==src]['Efficiency (%)'].values) * 0.1
        with s3:
            st.metric("Net Recovery Gain/Loss", f"${gain:.2f}M", delta="on $10M shift")

    # --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
    with tab4:
        st.header("Jurisdictional Governance")
        fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
        sel = st.plotly_chart(fig_map, on_select="rerun")
        
        state = "Federal"
        if sel and "selection" in sel and sel["selection"]["points"]:
            state = sel["selection"]["points"]["location"]
        
        st.divider()
        st.subheader(f"Detailed Risk Matrix: {state}")
        info = juris_dict.get(state, juris_dict["Federal"])
        
        # Hiding row index
        risk_tbl = pd.DataFrame({
            "Category": ["Jurisdiction", "Risk Level", "Focus Area", "Latest Status"],
            "Detail": [state, info['Risk'], info['Focus'], info['Update']]
        })
        st.table(risk_tbl.style.hide(axis="index"))

    # --- TAB 5: LEAVE-BEHIND ---
    with tab5:
        st.header("🖨️ Executive Leave-Behind")
        st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
        st.write(f"- **Capital Impact:** Current lift simulation adds **{cet1_bps:.2f} bps** to CET1 headroom.")
        st.write(f"- **Budget Control:** YTD Spend at ${ytd_spend}M ({(ytd_spend/total_budget)*100:.1f}% capacity).")
        components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)



