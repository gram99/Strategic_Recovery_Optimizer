# 🏛️ Strategic Recovery & Capital Optimizer (PoC)
**Author:** Gram99  
**Target Stakeholders:** Chief Risk Officers (CRO), CFOs, & Basel IV Steering Committees

---

## 📊 Executive Summary
The **Strategic Recovery & Capital Optimizer** is an executive-grade decision-support portal designed to navigate the complexities of the modern regulatory landscape. By unifying recovery operations with capital adequacy metrics (CET1), this platform demonstrates how high-performance recovery strategies directly mitigate **Capital Drag** and drive shareholder value.

### Strategic Business Value:
*   **CET1 Ratio Optimization:** Simulates the reduction of Risk-Weighted Assets (RWA) through increased recovery yields, effectively "freeing up" Tier 1 capital for reinvestment.
*   **ROTCE Pathfinding:** Provides a direct line of sight toward **Return on Tangible Common Equity (ROTCE)** targets (e.g., 11% by 2026), proving that recovery efficiency is a primary driver of bottom-line profitability.
*   **Macro-Resilience:** Stress-tests Net Charge-Off (NCO) projections across a 9-quarter horizon against "Severely Adverse" economic scenarios.

---

## 🚀 Strategic Modules & Executive UX
The portal features a "Human-in-the-Loop" architecture, protected by an **Executive Gateway** for secure leadership review.

### 1. Capital Report & WARR Analysis
*   **Goal:** Track the yield health of Branded Cards and Retail segments.
*   **Analytics:** Dynamic modeling of **Weighted Average Recovery Rates (WARR)** with automated Year-over-Year (YoY) variance tracking to identify performance leakage and its impact on CET1 ratios.

### 2. Dynamic Stress Testing (9-Quarter Engine)
*   **Goal:** Benchmark institutional resilience against peer institutions (e.g., JPM, Amex).
*   **Simulation:** An NCO projection engine that overlays macro-economic severity sliders (Unemployment, GDP), allowing leaders to visualize capital requirements in recessionary environments.

### 3. Vendor Governance & Placement Simulator
*   **Sunburst Analytics:** Visualizes the relationship between Tiered vendors and **Capital Drag (bps)**.
*   **Inventory Swap Simulator:** A "what-if" tool to calculate the net recovery gain of shifting inventory between agencies or moving to legal-track recovery.
*   **Jurisdictional Heatmap:** A Choropleth-based tracker monitoring state-level regulatory exceptions and audit updates (e.g., CPPA audits in CA).

---

## 🛠️ Technical Architecture
This project demonstrates proficiency in financial engineering, high-fidelity data visualization, and secure web deployment.

| Layer | Technical Implementation |
| :--- | :--- |
| **UI/UX Framework** | `Streamlit` with custom CSS-in-Python styling for an "Executive Gateway" interface. |
| **Financial Engine** | High-performance `@st.cache_data` logic for simulating CET1 basis point (bps) impacts across multi-million row dataframes. |
| **Visualizations** | `Plotly Graph Objects` for financial curves and `Plotly Express` for sunburst/geospatial analytics. |

---

## 📊 Strategic KPI Glossary
Key metrics calculated within the PoC are aligned with standard banking and recovery operations:

*   **CET1 Ratio:** The primary measure of a bank's financial strength; recovery lifts reduce RWA to boost this ratio.
*   **ROTCE:** Return on Tangible Common Equity; the ultimate yardstick for shareholder value and profitability.
*   **Capital Drag (bps):** The "cost of carry" for inventory measured in basis points, reflecting capital tied up during long liquidation timelines.
*   **Yield Premium:** The additional recovery percentage gained by utilizing higher-cost legal channels over standard collections.

---

## 💻 Installation & Usage
To launch the decision engine locally:

1. **Clone the repository:**  
   `git clone https://github.com/your-username/strategic-recovery-optimizer.git`
2. **Install dependencies:**  
   `pip install -r requirements.txt`
3. **Run the application:**  
   `streamlit run app.py`

**Executive Gateway Access Code:** `Recovery2026`

---

## 📁 Repository Strategy
This repository serves as a **Narrative of Authority**, shifting the focus from simple operations to institutional capital management.

| Operational Focus (Old) | Capital Strategy Focus (New) |
| :--- | :--- |
| Lists "Vendor Placement" as a feature. | Frames it as "Managing Capital Drag (bps)" for the CFO. |
