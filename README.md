🏛️ **Strategic Recovery & Capital Optimizer (PoC)
**
The Strategic Recovery & Capital Optimizer is an executive-grade decision-support portal designed for banking leadership and risk committees. It provides a unified view of recovery strategies, capital adequacy (CET1), and vendor performance, specifically tailored for the Basel III / Basel IV regulatory landscape.

📈 **Business Value Proposition**

In a shifting macro environment, managing "Capital Drag" is as critical as managing losses. This tool demonstrates how recovery performance directly impacts shareholder value by:

**Optimizing CET1 Ratios**: Simulating how recovery yield lifts reduce Risk-Weighted Assets (RWA).

**Visualizing ROTCE Impact**: Tracking the path toward 2026 Return on Tangible Common Equity targets.

**Benchmarking Resilience**: Stress-testing Net Charge-Off (NCO) projections against "Severely Adverse" macro scenarios.

🛠️ **Key ModulesCapital Report & WARR Analysis**: Dynamic modeling of Weighted Average Recovery Rates (WARR) across Branded Cards and Retail segments, featuring automated YoY variance tracking.

**Dynamic Stress Testing**: A 9-quarter NCO projection engine that overlays peer benchmarking (JPM, Amex, etc.) against custom macro-economic severity sliders.

**Vendor Governance & Placement Simulator**:Sunburst Analytics: Visualizing the relationship between Tiered vendors, placement volume, and "Capital Drag" (bps).

**Swap Simulator**: A "what-if" tool to calculate the net recovery gain of shifting inventory between agencies.

**Jurisdictional Heatmap**: A Choropleth-based regulatory tracker for monitoring state-level exceptions and audit updates (e.g., CPPA audits in CA).

💻 **Technical ArchitectureUI/UX**: Streamlit with a custom CSS-in-Python "Executive Gateway" login.

**Data Visualization**: High-fidelity interactive charts using Plotly Express and Plotly Graph Objects.

**Performance**: Implements @st.cache_data for lightning-fast simulation of complex financial dataframes.

**Calculations**: Custom financial logic for CET1 basis point (bps) impact and yield premium analysis.

🔐 **Access Credentials
**
This PoC is protected by an executive gateway:

Access Code: Recovery2026
