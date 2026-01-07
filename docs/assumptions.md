# Energy Sector Valuation Assumptions & Methodology

## 1. EXECUTIVE SUMMARY
**Project Goal:** Valuation of 7 global energy companies across three strategic segments (Integrated Majors, Upstream Pure-Play, Renewables) to quantify the impact of energy transition headwinds on long-term terminal value.

**Key Insight:** Traditional valuation models often overstate the terminal value of fossil fuel assets by assuming GDP-level growth (3-4%). This model utilizes a **sector-specific managed decline rate (1.5%)** for traditional O&G assets vs. a **growth rate (2.5-3.0%)** for renewable portfolios.

## 2. COMPANY SEGMENTATION & UNIVERSE

### Integrated Majors (XOM, CVX, SHEL)
* **Business Model:** Vertically integrated (Upstream Extraction + Downstream Refining + Chemical Trading).
* **Valuation Thesis:** High free cash flow generation enables aggressive share buybacks, but "size" acts as a drag on rapid pivoting.
* **Key Driver:** Blended margins. Upstream profits (high margin) hedge downstream volatility (low margin).

### European Transition Leaders (TTE, BP)
* **Business Model:** Traditional O&G Cash Cow funding a rapid Renewable Energy pivot.
* **Valuation Thesis:** The market currently applies a "conglomerate discount" due to the uncertainty of renewable returns.
* **Key Driver:** The pace of CAPEX redeployment from hydrocarbons to electrons.

### Upstream Pure Play (COP)
* **Business Model:** Exploration & Production (E&P) only. No refining hedge.
* **Valuation Thesis:** Highest "Beta" to oil prices. Most efficient capital deployers but most exposed to commodity cycles.
* **Key Driver:** Breakeven price per barrel (approx. $40/bbl).

### Renewables (NEE)
* **Business Model:** Regulated Utility + Renewable Generation (Wind/Solar).
* **Valuation Thesis:** "Bond-like" equity with stable cash flows backed by long-term Power Purchase Agreements (PPAs).
* **Key Driver:** Interest rates (Cost of Capital) rather than Oil Price.

---

## 3. VALUATION SCENARIOS (SENSITIVITY)

Energy valuations are non-linear relative to commodity pricing. We model three explicit states to test EBITDA margin resilience.

| Scenario | Oil Price (Brent) | Thesis | Margin Impact |
| :--- | :--- | :--- | :--- |
| **Recession (Bear)** | **$60/bbl** | Demand destruction, oversupply. | **-10% (Compression)** |
| **Base Case** | **$85/bbl** | Balanced market, OPEC discipline. | **0% (Baseline)** |
| **Supply Shock (Bull)** | **$110/bbl** | Geopolitical disruption, scarcity. | **+10% (Expansion)** |

*Note: NextEra Energy (NEE) is modeled as price-neutral to oil fluctuations due to fixed-price PPAs.*

---

## 4. DCF MODELING ASSUMPTIONS

### A. Revenue Growth & Decline Curves
We reject "perpetual growth" for fossil assets.
* **Integrated Majors:** +2.0% (Yr 1) declining to -1.5% (Yr 5).
* **Upstream:** +2.0% (Yr 1) declining to -2.0% (Yr 5) due to natural reservoir depletion requiring constant reinvestment.
* **Renewables:** +5.0% flat (Yr 1-5) driven by secular demand shift.

### B. CAPEX Intensity (The "Spend to Stand Still" Ratio)
Energy is capital intensive. High CAPEX reduces Free Cash Flow (FCF).
* **Renewables (NEE):** **18-20%** of Revenue. High upfront growth CAPEX.
* **Upstream (COP):** **15-18%** of Revenue. Continuous drilling required to replace reserves.
* **Integrated (XOM):** **10-12%** of Revenue. Efficiencies of scale.

### C. Terminal Value (The "Forever" Assumption)
* **Fossil Fuel Assets:** **1.5%** (Below global GDP). Reflects long-term energy transition risk and potential stranded assets.
* **Renewable Assets:** **2.5%**. Reflects electrification of the grid and long-term utility demand.

---

## 5. COST OF CAPITAL (WACC)

We utilize a CAPM build-up method, differentiating risk (Beta) by business model.

* **Risk-Free Rate:** 4.5% (10Y US Treasury)
* **Market Risk Premium:** 6.5%

| Ticker | Beta ($\beta$) | Cost of Debt | WACC | Logic |
| :--- | :--- | :--- | :--- | :--- |
| **COP (Upstream)** | **1.25** | 4.50% | **~8.7%** | Highest risk; pure commodity exposure. |
| **XOM (Integrated)**| **1.15** | 4.25% | **~8.0%** | Diversified; strong balance sheet (AA-). |
| **NEE (Renewable)** | **0.95** | 4.00% | **~6.8%** | Lowest risk; regulated utility cash flows. |
