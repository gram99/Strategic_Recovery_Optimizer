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
    st.stop()

# 2. DATA ENGINE
@st.cache_data
def get_master_data():
    # Historical Risk Data
    warr_history = pd.DataFrame({
        'Year': ['2023-24', '2023-24', '2024-25', '2024-25', '2025-26', '2025-26'],
        'Segment': ['Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services'],
        'WARR': [1.05, 5.20, 1.35, 6.45, 1.22, 6.10]
    })
    
    # Peer Metrics
    peers = pd.DataFrame({
        'Bank Indicator': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026 Target)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
        'Current NCO (%)': [1.5, 1.9, 4.8, 2.1, 2.4]
    })
    
    # Strategic Vendor Data
    today = datetime.now().date()
    vendor_data = pd.DataFrame({
        'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
        'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
        'Efficiency (%)': [94.2, 88.5, 76.1, 72.4, 84.8],
        'Capital Drag (bps)': [1.2, 2.4, 6.8, 8.2, 3.1],
        'YTD Spend ($M)': [142.5, 98.2, 64.1, 55.8, 28.4],
        'Placement ($M)': [220.0, 150.0, 45.0, 40.0, 45.0],
        'Renewal Date': [today + timedelta(days=x) for x in [12, 45, 8, 90, 120]]
    })
    
    # Jurisdictional Data
    juris_dict = {
        'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'Data remediation Dec 2025.', 'Vol': 8},
        'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA audit active.', 'Vol': 24},
        'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'Vendor remediation active.', 'Vol': 18},
        'TX': {'Risk': '🟢 Stable', 'Focus': 'National Standards', 'Update': 'Process aligned.', 'Vol': 4},
        'Federal': {'Risk': '🟡 Moderate', 'Focus': 'OCC Oversight', 'Update': 'Resource Review terminated Dec 2025.', 'Vol': 52}
    }
    geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [8, 24, 4, 18]})
    
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

# --- TAB 1: EXECUTIVE CAPITAL REPORT ---
with tab1:
    st.header("Executive Capital & Shareholder Value Report")
    recovery_lift = st.slider("Target Yield Optimization Lift (%)", 0, 10, 2)
    cet1_bps = ((165 * (1 + (recovery_lift/100))) / 13500) * 100
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CET1 Capital Ratio", "13.2%", f"+{cet1_bps:.2f} bps")
    c2.metric("2026 ROTCE Target", "10.5%", "On Track")
    c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
    c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
    
    st.divider()
    st.subheader("Historical WARR Risk Migration with Risk Trendlines")
    fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                      color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
    fig_warr.add_trace(go.Scatter(x=['2023-24', '2024-25', '2025-26'], y=[1.05, 1.35, 1.22], name="Branded Trend", line=dict(color="#007bff", dash='dot')))
    fig_warr.add_trace(go.Scatter(x=['2023-24', '2024-25', '2025-26'], y=[5.20, 6.45, 6.10], name="Retail Trend", line=dict(color="#ff4b4b", dash='dot')))
    st.plotly_chart(fig_warr, use_container_width=True)

    st.subheader("Historical Risk Data & YoY Variance")
    p_df = warr_df.pivot(index="Year", columns="Segment", values="WARR").reset_index()
    p_df['Branded YoY %'] = p_df['Branded Cards'].pct_change() * 100
    p_df['Retail YoY %'] = p_df['Retail Services'].pct_change() * 100
    # FIXED: Index Hidden
    st.table(p_df.style.format({"Branded YoY %": "{:+.2f}%", "Retail YoY %": "{:+.2f}%"}).hide(axis="index"))

# --- TAB 2: PEER STRATEGY & DYNAMIC STRESS ---
with tab2:
    st.header("Competitive Advantage & Dynamic Stress Resilience")
    stress_severity = st.select_slider("Select Macro Scenario Severity", options=["Baseline", "Mild", "Moderate", "Severely Adverse"])
    
    col_t, col_g = st.columns([1, 1.5])
    with col_t:
        st.subheader("Peer Benchmarking")
        # FIXED: Index Hidden
        st.dataframe(peer_df, hide_index=True, use_container_width=True)
    with col_g:
        m_val = {"Baseline": 0.2, "Mild": 0.5, "Moderate": 1.1, "Severely Adverse": 2.4}[stress_severity]
        quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
        curve = [2.4 * (1 + (i*0.09) * m_val) for i in range(len(quarters))]
        fig_stress = px.line(x=quarters, y=curve, title=f"9Q NCO Projection: {stress_severity} Impact")
        fig_stress.add_hline(y=8.0, line_dash="dash", line_color="red", annotation_text="DFAST Threshold")
        st.plotly_chart(fig_stress, use_container_width=True)

# --- TAB 3: VENDOR MANAGEMENT ---
with tab3:
    st.header("🏢 Vendor Performance & Capital Optimization")
    
    col_gauge, col_sun = st.columns([1, 1.2])
    with col_gauge:
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number+delta", value=vend_df['YTD Spend ($M)'].sum(), 
            title={'text': "OpEx Budget Utilization ($M)"}, delta={'reference': 500},
            gauge={'axis': {'range': [None, 500]}, 'bar': {'color': "#007bff"}, 'threshold': {'line': {'color': "red", 'width': 4}, 'value': 450}}))
        st.plotly_chart(fig_gauge, use_container_width=True)
    with col_sun:
        st.plotly_chart(px.sunburst(vend_df, path=['Tier', 'Vendor Name'], values='Placement ($M)', color='Capital Drag (bps)', 
                                    color_continuous_scale='RdYlGn_r', title="Placement Volume vs. Capital Drag"), use_container_width=True)

    st.info("**Strategic Insight:** Tier 2 Legal partners manage litigation-track inventory. Under Basel III 'Loss Given Default' (LGD) models, legal-track inventory requires higher capital reserves. This drag is a structural 'cost of carry' for a **3.4x yield premium**.")

    st.subheader("📍 Active Vendor Governance")
    # FIXED: Index Hidden
    st.dataframe(vend_df, hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("🔄 Strategic Placement Swap Simulator")
    s1, s2, s3 = st.columns(3)
    with s1: src = st.selectbox("From (Source):", vend_df['Vendor Name'], index=3)
    with s2: tgt = st.selectbox("To (Target):", vend_df['Vendor Name'], index=2)
    gain = (vend_df[vend_df['Vendor Name']==tgt]['Efficiency (%)'].iloc[0] - vend_df[vend_df['Vendor Name']==src]['Efficiency (%)'].iloc[0]) * 0.1
    with s3:
        st.metric("Net Recovery Gain/Loss", f"${gain:.2f}M", delta="on $10M shift")

# --- TAB 4: REGULATORY HEATMAP ---
with tab4:
    st.header("Jurisdictional Governance")
    fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
    sel = st.plotly_chart(fig_map, on_select="rerun")
    
    state = "Federal"
    if sel and "selection" in sel and sel["selection"]["points"]:
        state = sel["selection"]["points"][0]["location"]
    
    st.divider()
    st.subheader(f"📍 Risk Detail: {state}")
    info = juris_dict.get(state, juris_dict["Federal"])
    
    # ADDED: Exception Volume Row
    risk_tbl = pd.DataFrame({
        "Strategic Category": ["Jurisdiction", "Risk Level", "Focus Area", "Total Exception Volume", "Status"],
        "Detail": [state, info['Risk'], info['Focus'], f"{info['Vol']} Active Exceptions", info['Update']]
    })
    # FIXED: Index Hidden
    st.table(risk_tbl.style.hide(axis="index"))

# --- TAB 5: LEAVE-BEHIND ---
with tab5:
    st.header("🖨️ Executive Leave-Behind")
    st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
    st.write(f"- **Capital Impact:** Yield optimization adds **{cet1_bps:.2f} bps** to CET1 headroom.")
    st.write("- **Historical Context:** Proactive 2024 optimization stabilized risk velocity in Branded Cards.")
    components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)