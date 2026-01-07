# Energy Valuation Engine (Python)

**A dynamic, scenario-based valuation platform for the Energy Sector.**
*Built by Liam Egan (Chemical Engineering / MSBA)*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Live%20%26%20Dynamic-success)]()

---

### 1. Executive Summary
This project bridges **Chemical Engineering physics** with **Investment Banking valuation**. Unlike standard models that assume perpetual GDP-level growth for fossil fuel assets, this engine quantifies the impact of the **Energy Transition** on long-term equity value.

**The Core Thesis: "Managed Decline"**
* **Traditional View:** Assumes +2-3% terminal growth for Oil Majors.
* **Engineered View:** Models a **-1.5% terminal growth rate** for fossil assets to reflect reservoir depletion and secular demand shifts, while modeling secular growth for Renewable portfolios (NextEra).

---

### 2. Key Findings (ExxonMobil Case Study)
The model stress-tested **ExxonMobil (XOM)** against three oil price scenarios.

* **Base Case ($85 Oil):** **Undervalued.** The model implies ~13% upside, suggesting the market is pricing in a faster transition than data supports.
* **Bear Case ($60 Oil):** **$64/share.** This highlights the massive "Commodity Beta" inherent in the stock—margins compress significantly due to high fixed operating costs.
* **Verdict:** XOM is a "Cash Cow" play. The cash flows in the next decade justify the valuation, even if the long-term terminal value is challenged.

*(Note: Run `notebooks/01_analysis.ipynb` to generate the latest sensitivity chart)*
![Valuation Sensitivity](figures/sensitivity_chart.png)

---

### 3. System Architecture
The project is architected to ensure **Model Governance** and **Scalability**. It separates Assumptions, Logic, and Data.

| Module | File | Purpose |
| :--- | :--- | :--- |
| **The Brain** | `config/settings.py` | Centralized assumptions database. Stores WACC parameters, Growth Curves, and Oil Scenarios. ensures no "hardcoded numbers." |
| **The Ingress** | `src/data_fetchers.py` | Live data pipeline connecting to **Yahoo Finance** for real-time pricing and share counts. |
| **Risk Engine** | `src/models/wacc.py` | **CAPM Calculator.** Differentiates risk by sector (e.g., Upstream Beta `1.25` vs. Utility Beta `0.95`). |
| **Valuation** | `src/models/dcf.py` | **Physics-Based DCF.** Uses an energy proxy for FCF (`EBITDA - Tax - CAPEX`) to isolate capital intensity. |
| **Stress Test** | `src/models/sensitivity.py` | **Scenario Loop.** Iterates through oil prices ($60/$85/$110) to quantify downside risk. |

---

### 4. How to Run
This model is plug-and-play. You can switch the active ticker in the notebook to value any of the 7 companies in the universe (`XOM`, `CVX`, `SHEL`, `TTE`, `BP`, `COP`, `NEE`).

1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/eganl2024-sudo/Energy-Valuation-Analysis.git](https://github.com/eganl2024-sudo/Energy-Valuation-Analysis.git)
    cd Energy-Valuation-Analysis
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Master Analysis:**
    Open `notebooks/01_analysis.ipynb` in Jupyter Lab/Notebook.
    * *Change `ticker = "NEE"` to see how the WACC and Valuation update instantly for a renewable utility.*

---

### 5. Methodology & Assumptions
* **WACC:** Derived using sector-specific Betas and credit-rating-based Cost of Debt.
* **Tax Rate:** Standardized to **24%** (Statutory US Rate + State) for asset comparability.
* **Terminal Value:** Gordon Growth Method with differentiated $g$ parameters (-1.5% to +2.5%).
* **Oil Scenarios:** Modeled via linear EBITDA margin expansion/compression based on a $85/bbl baseline.

---

**Contact:** Liam Egan | [LinkedIn](https://www.linkedin.com/in/liam-egan-/) | [Email](mailto:ljegan01@gmail.com)
