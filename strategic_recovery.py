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

# 2. DATA ENGINE (Anchored to March 2026 Context)
@st.cache_data
def get_master_data():
    # Historical WARR Migration (2023 -> 2026 Story)
    warr_history = pd.DataFrame({
        'Year': ['2023-24', '2023-24', '2024-25', '2024-25', '2025-26', '2025-26'],
        'Segment': ['Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services', 'Branded Cards', 'Retail Services'],
        'WARR': [1.05, 5.20, 1.35, 6.45, 1.22, 6.10]
    })
    
    # Peer Benchmarking Table
    peers = pd.DataFrame({
        'Bank Indicator': ['JPM Chase', 'Amex', 'Cap One', 'BofA', 'Citi (2026 Target)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
        'Current NCO (%)': [1.5, 1.9, 4.8, 2.1, 2.4]
    }).sort_values('ROTCE (%)', ascending=False)
    
    # Strategic Vendor List (Full Data Integration)
    today = datetime.now().date()
    vendor_data = pd.DataFrame({
        'Vendor Name': ['NRG (National)', 'Apex Collections', 'Lexington Legal', 'Sterling Assets', 'Summit SME'],
        'Tier': ['Tier 1', 'Tier 1', 'Tier 2 (Legal)', 'Tier 2 (Legal)', 'Tier 3'],
        'Core Segment': ['Mass Market Card', 'Retail Services', 'High-FICO Litigation', 'High-Balance Tail', 'Commercial/SME'],
        'Efficiency (%)': [94.2, 88.5, 76.1, 72.4, 84.8],
        'Capital Drag (bps)': [1.2, 2.4, 6.8, 8.2, 3.1],
        'YTD Spend ($M)': [85, 92, 45, 38, 22],
        'Placement ($M)': [420, 310, 125, 95, 55],
        'Renewal Date': [today + timedelta(days=x) for x in [120, 45, 15, 210, 300]]
    })
    
    # Jurisdictional Data for Interactive Map
    juris_dict = {
        'NY': {'Risk': '🟡 Moderate', 'Focus': 'Fair Lending', 'Update': 'AML reporting shift noted.'},
        'CA': {'Risk': '🔴 High', 'Focus': 'Privacy/ADMT', 'Update': 'Jan 2026 CPPA compliance audit active.'},
        'FL': {'Risk': '🔴 Elevated', 'Focus': 'Debt Collection', 'Update': 'Vendor drift remediation ongoing.'},
        'TX': {'Risk': '🟢 Stable', 'Focus': 'National Preemption', 'Update': 'Lending standards aligned.'},
        'Federal': {'Risk': '🟡 Moderate', 'Focus': 'Data Controls', 'Update': 'OCC terminated Resource Review Dec 2025.'}
    }
    geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [4, 18, 2, 24]})
    
    return warr_history, peers, vendor_data, juris_dict, geo_df

warr_df, peer_df, vend_df, juris_dict, geo_df = get_master_data()

# 3. GLOBAL SIDEBAR
with st.sidebar:
    st.image("https://www.citigroup.com", width=80)
    st.header("Executive Hub")
    st.success("🟢 CET1 Ratio: 13.2%") 
    st.info("2026 ROTCE Target: 10.5%")
    if st.button("Logout"):
        del st.session_state["password_correct"]
        st.rerun()

# 4. MULTI-TAB INTERFACE
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Capital Report", "Peer Strategy & Stress", "Vendor Management", "Regulatory Heatmap", "LEAVE-BEHIND"
])

# --- TAB 1: EXECUTIVE CAPITAL REPORT (TRENDLINES & PIVOT TABLE) ---
with tab1:
    st.header("Executive Capital & Shareholder Value Report")
    st.markdown("> **The Story:** This report tracks how our **WARR (Weighted Average Risk Rating)** migrated through the 2024 stress period and our successful stabilization into 2026.")
    
    # Capital Lift Simulator
    recovery_lift = st.slider("Target Yield Optimization Lift (%)", 0, 10, 2)
    cet1_bps = ((165 * (1 + (recovery_lift/100))) / 13500) * 100
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CET1 Capital Ratio", "13.2%", f"+{cet1_bps:.2f} bps")
    c2.metric("2026 ROTCE Target", "10.5%", "On Track")
    c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")
    c4.metric("Economic Profit", "$1.2B", "+5.2% YoY")
    
    st.divider()
    st.subheader("Historical WARR Migration with Risk Trendlines")
    
    # Bar Chart with Trendlines
    fig_warr = px.bar(warr_df, x="Year", y="WARR", color="Segment", barmode="group",
                      color_discrete_map={'Branded Cards': '#007bff', 'Retail Services': '#ff4b4b'})
    
    # Adding Dual Trendlines
    fig_warr.add_trace(go.Scatter(x=['2023-24', '2024-25', '2025-26'], y=[1.05, 1.35, 1.22], name="Branded Trend", line=dict(color="#007bff", dash='dot')))
    fig_warr.add_trace(go.Scatter(x=['2023-24', '2024-25', '2025-26'], y=[5.20, 6.45, 6.10], name="Retail Trend", line=dict(color="#ff4b4b", dash='dot')))
    st.plotly_chart(fig_warr, use_container_width=True)

    st.subheader("Historical Risk Data (Actual Values)")
    warr_pivot = warr_df.pivot(index="Year", columns="Segment", values="WARR").reset_index()
    # Hiding index to remove unlabeled integers
    st.table(warr_pivot.style.hide(axis="index"))

# --- TAB 2: PEER STRATEGY & DYNAMIC STRESS ---
with tab2:
    st.header("Competitive Advantage & Dynamic Stress Resilience")
    st.markdown("> **The Story:** Adjust the slider to see how Citi's 'long-tail' recovery yield acts as a shock absorber during macro shocks.")
    
    stress_severity = st.select_slider("Select Macro Scenario Severity", options=["Baseline", "Mild", "Moderate", "Severely Adverse"])
    
    col_table, col_graph = st.columns([1, 1.5])
    
    with col_table:
        st.subheader("Peer Comparison Table")
        st.dataframe(peer_df, hide_index=True, use_container_width=True)

    with col_graph:
        # Dynamic Curve Logic that reacts to the slider
        multipliers = {"Baseline": 0.2, "Mild": 0.5, "Moderate": 1.1, "Severely Adverse": 2.4}
        m = multipliers[stress_severity]
        quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
        
        nco_base = 2.4
        curve = [nco_base * (1 + (i*0.09) * m) for i in range(len(quarters))]
        
        fig_stress = px.line(x=quarters, y=curve, title=f"9Q NCO Projection: {stress_severity} Impact",
                            labels={'x': 'Quarter', 'y': 'NCO Ratio (%)'})
        fig_stress.add_hline(y=8.0, line_dash="dash", line_color="red", annotation_text="DFAST Threshold")
        st.plotly_chart(fig_stress, use_container_width=True)

# --- TAB 3: VENDOR MANAGEMENT (SUNBURST & SPEEDOMETER) ---
with tab3:
    st.header("🏢 Vendor Performance & Capital Optimization")
    st.markdown("> **The Story:** Restoring budget discipline while shifting funds to high-yield legal partners. Red dates indicate imminent contract risks.")

    # RESTORED BUDGET GAUGE & SUNBURST
    total_budget = 500
    ytd_spend = vend_df['YTD Spend ($M)'].sum()
    
    col_gauge, col_sunburst = st.columns([1, 1.2])
    
    with col_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta", value = ytd_spend,
            title = {'text': "Recovery OpEx Budget Utilization ($M)"},
            delta = {'reference': total_budget, 'increasing': {'color': "red"}},
            gauge = {'axis': {'range': [None, total_budget]}, 'bar': {'color': "#007bff"},
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 450}}))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_sunburst:
        fig_sun = px.sunburst(vend_df, path=['Tier', 'Vendor Name'], values='Placement ($M)',
                              color='Capital Drag (bps)', color_continuous_scale='RdYlGn_r',
                              title="Portfolio Mix: Volume vs. Capital Drag")
        st.plotly_chart(fig_sun, use_container_width=True)

    st.subheader("📍 Active Vendor Governance")
    def color_renewals(val):
        return 'color: red; font-weight: bold' if val < (datetime.now().date() + timedelta(days=30)) else ''
    
    # Hide index for clean look
    st.dataframe(vend_df.style.applymap(color_renewals, subset=['Renewal Date']), 
                 hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("🔄 Strategic Placement Swap Simulator")
    s1, s2, s3 = st.columns(3)
    with s1: src = st.selectbox("From (Source):", vend_df['Vendor Name'], index=3)
    with s2: tgt = st.selectbox("To (Target):", vend_df['Vendor Name'], index=2)
    
    gain = (vend_df[vend_df['Vendor Name']==tgt]['Efficiency (%)'].iloc[0] - 
            vend_df[vend_df['Vendor Name']==src]['Efficiency (%)'].iloc[0]) * 0.1
    with s3:
        st.metric("Net Recovery Gain/Loss", f"${gain:.2f}M", delta="on $10M shift")

# --- TAB 4: INTERACTIVE REGULATORY HEATMAP ---
with tab4:
    st.header("Jurisdictional Governance")
    st.markdown("👇 **Click a state on the map** to drill down into localized risk remediation.")
    
    fig_map = px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds")
    # Capture selection
    sel = st.plotly_chart(fig_map, on_select="rerun")
    
    state = "Federal"
    if sel and "selection" in sel and sel["selection"]["points"]:
        state = sel["selection"]["points"][0]["location"]
    
    st.divider()
    st.subheader(f"📍 Detailed Risk Matrix: {state}")
    info = juris_dict.get(state, juris_dict["Federal"])
    
    risk_tbl = pd.DataFrame({
        "Category": ["Jurisdiction", "Risk Level", "Focus Area", "Latest Status"],
        "Detail": [state, info['Risk'], info['Focus'], info['Update']]
    })
    # Hiding the integer column index
    st.table(risk_tbl.style.hide(axis="index"))

# --- TAB 5: LEAVE-BEHIND ---
with tab5:
    st.header("🖨️ Executive Leave-Behind")
    st.markdown("#### **Strategic Positioning Summary (Q1 2026)**")
    st.write(f"- **Capital Impact:** Current yield simulation adds **{cet1_bps:.2f} bps** to CET1 headroom.")
    st.write(f"- **Budget Performance:** Spend at ${ytd_spend}M vs ${total_budget}M cap.")
    st.divider()
    st.warning("**Model Risk Management:** These synthetic metrics are anchored in public 2024-2025 Citi disclosures to demonstrate analytical stewardship.")
    components.html("<script>function print_summary(){ window.print(); }</script><button onclick='print_summary()' style='background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;'>Download PDF Summary</button>", height=80)