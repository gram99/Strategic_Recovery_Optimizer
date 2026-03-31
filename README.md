**🏛️ Strategic Recovery & Capital Optimizer (PoC)**

The Strategic Recovery & Capital Optimizer is an executive-grade decision-support portal designed for banking leadership and risk committees. It provides a unified view of recovery strategies, capital adequacy (CET1), and vendor performance, specifically tailored for the Basel III / Basel IV regulatory landscape.


📈 **Business Value Proposition**

In a shifting macro environment, managing "Capital Drag" is as critical as managing losses. This tool demonstrates how recovery performance directly impacts shareholder value by:

**Optimizing CET1 Ratios**: Simulating how recovery yield lifts reduce Risk-Weighted Assets (RWA).

**Visualizing ROTCE Impact**: Tracking the path toward 2026 Return on Tangible Common Equity targets.

**Benchmarking Resilience**: Stress-testing Net Charge-Off (NCO) projections against "Severely Adverse" macro scenarios.

🛠️ **Key ModulesCapital Report & WARR Analysis**: Dynamic modeling of Weighted Average Recovery Rates (WARR) across Branded Cards and Retail segments, featuring automated YoY variance tracking.

**Dynamic Stress Testing**: A 9-quarter NCO projection engine that overlays peer benchmarking (JPM, Amex, etc.) against custom macro-economic severity sliders.

**Vendor Governance & Placement Simulator**:

  **Sunburst Analytics**: Visualizing the relationship between Tiered vendors, placement volume, and "Capital Drag" (bps).

  **Swap Simulator**: A "what-if" tool to calculate the net recovery gain of shifting inventory between agencies.

  **Jurisdictional Heatmap**: A Choropleth-based regulatory tracker for monitoring state-level exceptions and audit updates (e.g., CPPA audits in CA).


💻 **Technical ArchitectureUI/UX**: Streamlit with a custom CSS-in-Python "Executive Gateway" login.

**Data Visualization**: High-fidelity interactive charts using Plotly Express and Plotly Graph Objects.

**Performance**: Implements @st.cache_data for lightning-fast simulation of complex financial dataframes.

**Calculations**: Custom financial logic for CET1 basis point (bps) impact and yield premium analysis.


**🔐 Access Credentials**

This PoC is protected by an executive gateway:

Access Code: Recovery2026


**📊 KPI Glossary:** Understanding the Financial EngineTo provide context for the metrics calculated within this PoC, the following definitions align with standard banking and recovery operations:

**Capital & Profitability Metrics**

**CET1 (Common Equity Tier 1) Ratio**: The primary measure of a bank's financial strength. In this app, we simulate how increasing Recovery Lift reduces Risk-Weighted Assets (RWA), effectively "freeing up" capital.

**ROTCE (Return on Tangible Common Equity)**: A key performance metric for shareholders. The dashboard tracks the 10.5% target, showing how recovery efficiency contributes to the bottom line.

**Economic Profit**: The profit remaining after subtracting the cost of capital. The tool calculates a 5.2% YoY increase based on optimized recovery strategies.

**Recovery & Risk Metrics**

**WARR (Weighted Average Recovery Rate)**: The primary KPI for the Recovery department. It measures the percentage of charged-off principal that is successfully recovered through collections or legal action.

**NCO (Net Charge-Off) Projection**: The estimated percentage of loans unlikely to be recovered. The Stress Simulator projects this over a 9-quarter horizon to test resilience against "Severely Adverse" economic shifts.

**Capital Drag (bps)**: Measured in basis points. This represents the "cost of carry" for inventory. For example, legal-track inventory (Tier 2) has a higher capital drag due to longer liquidation timelines but often yields a higher recovery premium.

**Operational MetricsPlacement Volume**: The total dollar amount of debt assigned to a specific vendor (NRG, Apex, etc.).

**Efficiency (%)**: The vendor's success rate in hitting recovery targets relative to their peers in the same Tier.

**Yield Premium**: The additional recovery percentage gained by using higher-cost legal channels versus standard collection agencies.


**Disclaimer**: _All data presented in this PoC is synthetic and intended for architectural demonstration purposes only._
