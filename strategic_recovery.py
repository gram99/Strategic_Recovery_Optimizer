import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Citi Strategic Recovery & Capital Optimizer", layout="wide")

# 2. DATA ENGINE
@st.cache_data
def get_master_data():
    # Peer Benchmarking
    peers = pd.DataFrame({
        'Bank': ['JPM Chase', 'Amex', 'Capital One', 'BofA', 'Citi (2026 Target)'],
        'ROTCE (%)': [22.0, 30.0, 15.2, 14.5, 10.5],
        'CET1 Ratio (%)': [15.1, 10.2, 13.2, 11.8, 12.3]
    }).sort_values('ROTCE (%)', ascending=False)
    
    # Stress Projections
    quarters = [f"Q{i} 2024" if i < 3 else f"Q{i-2} 2025" for i in range(1, 10)]
    nco_severe = [2.4, 3.8, 5.2, 7.1, 8.4, 7.9, 6.5, 5.1, 4.2] 
    stress_df = pd.DataFrame({'Quarter': quarters, 'Severely Adverse (9Q)': nco_severe})
    
    # Vendor Data
    vendor_df = pd.DataFrame({
        'Vendor': ['Agency Alpha', 'Agency Beta', 'Agency Gamma'],
        'Efficiency %': [92, 84, 68],
        'L3 Exceptions': [0, 0, 1],
        'Capital Drag (bps)': [1.2, 4.5, 11.8]
    })
    
    # Regulatory Timeline Data
    timeline_data = pd.DataFrame([
        dict(Event="2020 Consent Order Issued", Date="2020-10-07", Type="Regulatory Action", Status="Ongoing"),
        dict(Event="OCC Resource Review Amendment", Date="2024-07-10", Type="Enhancement", Status="Completed"),
        dict(Event="Termination of OCC Amendment", Date="2025-12-15", Type="Milestone", Status="Success"),
        dict(Event="CA ADMT Compliance Deadline", Date="2026-01-01", Type="Compliance", Status="Active"),
        dict(Event="Target ROTCE (11-12%) Waypoint", Date="2026-12-31", Type="Strategic", Status="Target"),
    ])
    
    return peers, stress_df, vendor_df, timeline_data

peer_df, stress_df, vend_df, timeline_df = get_master_data()

# 3. GLOBAL SIDEBAR
with st.sidebar:
    st.image("https://www.citigroup.com", width=80)
    st.header("Executive Controls")
    scenario = st.selectbox("Strategic Mode", ["Standard Operations", "DFAST Stress Test"])
    st.divider()
    st.success("🟢 CET1 Ratio: 12.3%") 
    st.info("2026 ROTCE Target: 10-11%")
    st.markdown("[🔗 Citi Investor Relations](https://www.citigroup.com)")

# 4. MULTI-TAB INTERFACE
tabs = st.tabs(["Executive Risk", "Peer & Stress", "Vendor Governance", "Regulatory Heatmap", "User Guide", "LEAVE-BEHIND"])

# --- TAB 1: EXECUTIVE RISK ---
with tabs[0]:
    st.header("Portfolio Risk & Economic Profit")
    c1, c2, c3 = st.columns(3)
    c1.metric("WARR % Change", "+0.45%", "Risk Migration", delta_color="inverse")
    c2.metric("Economic Profit (EP)", "$1.2B", "+5.2% YoY")
    c3.metric("RWA Optimization", "$165M", "Net Recovery Impact")

# --- TAB 2: PEER & STRESS ANALYSIS ---
with tabs[1]:
    col_p, col_s = st.columns(2)
    with col_p:
        st.subheader("ROTCE Peer Benchmarking")
        st.plotly_chart(px.bar(peer_df, x='Bank', y='ROTCE (%)', color='Bank'), width='stretch')
    with col_s:
        st.subheader("9Q Severely Adverse NCO Projection")
        st.plotly_chart(px.line(stress_df, x='Quarter', y='Severely Adverse (9Q)'), width='stretch')

# --- TAB 3: VENDOR GOVERNANCE ---
with tabs[2]:
    st.header("Vendor Efficiency & Capital Adequacy Overlay")
    st.dataframe(vend_df.style.highlight_max(subset=['Capital Drag (bps)'], color='#ff4b4b'))

# --- TAB 4: REGULATORY HEATMAP & RISK MATRIX ---
with tabs[3]:
    st.header("Jurisdictional Exceptions & Risk Matrix")
    geo_df = pd.DataFrame({'State': ['NY', 'CA', 'TX', 'FL'], 'Exceptions': [2, 14, 5, 21]})
    st.plotly_chart(px.choropleth(geo_df, locations='State', locationmode="USA-states", color='Exceptions', scope="usa", color_continuous_scale="Reds"), width='stretch')
    
    st.subheader("📍 Jurisdictional Compliance Matrix")
    risk_matrix = {
        "Jurisdiction": ["Federal (OCC/Fed)", "California", "Florida"],
        "Focus": ["Data/Risk Controls", "Privacy/ADMT", "Debt Collection"],
        "Risk": ["🟡 Moderate", "🔴 High", "🔴 Elevated"],
        "Mitigation": ["Remediation Active", "Audit Pending", "Enhanced Monitoring"],
        "Update": ["OCC terminated Resource Review Dec 2025.", "New CPPA regs active Jan 2026.", "L2 audit scheduled Q2 2026."]
    }
    st.table(pd.DataFrame(risk_matrix))

# --- TAB 5: STRATEGIC USER GUIDE & TIMELINE ---
with tabs[4]:
    st.header("📖 Strategic User Guide & Regulatory Timeline")
    st.markdown("### **Transformation Roadmap**")
    
    # NEW: Regulatory Timeline Visualization
    fig_time = px.timeline(timeline_df, x_start="Date", x_end="Date", y="Event", color="Status",
                          title="Key Regulatory & Strategic Milestones (2020-2026)")
    fig_time.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown("""
    ### **Purpose**
    To quantify the impact of recovery yield on Citi’s **CET1 Ratio** and **ROTCE Waypoints**.
    
    ### **Executive Insights**
    * **Dec 2025:** Significant OCC milestone achieved; resource amendment terminated [3].
    * **Jan 2026:** Focused shift to **Automated Decision-Making (ADMT)** compliance in CA [4].
    """)

# --- TAB 6: EXECUTIVE LEAVE-BEHIND ---
with tabs[5]:
    st.header("🖨️ Executive Leave-Behind Summary")
    st.markdown("#### **Strategic Positioning (Q1 2026)**")
    st.write("* **Regulatory Milestone:** Dec 2025 OCC termination confirms transformation progress.")
    st.write("* **Capital Adequacy:** 12.3% CET1 provides headroom for 2026 growth.")
    
    components.html("""
    <script>function print_summary() { window.print(); }</script>
    <button onclick="print_summary()" style="background-color:#007bff; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
        Download Summary as PDF
    </button>""", height=50)