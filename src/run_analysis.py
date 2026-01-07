import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add project root to path so we can import from src
sys.path.append(os.path.abspath('.'))

from src.data_fetchers import DataFetcher
from src.models.wacc import WACCCalculator
from src.models.dcf import DCFModel
from src.models.sensitivity import SensitivityAnalysis
from config.settings import COMPANIES, SECTOR_ASSUMPTIONS, OIL_SCENARIOS, COMPANY_FINANCIALS

# Initialize Fetcher
fetcher = DataFetcher()

# Analyze ExxonMobil (XOM) - The Showcase Company
ticker = "XOM"
print(f"📡 Fetching data for {ticker}...")

current_price = fetcher.get_current_price(ticker)
print(f"   Current Price: ${current_price:.2f}")

# Get Financials from Database
financials = COMPANY_FINANCIALS[ticker]
latest_revenue = financials["revenue"]
net_debt = financials["net_debt"]
shares_out = financials["shares"]

print(f"   Base Revenue: ${latest_revenue/1e9:.1f}B")
print(f"   Net Debt:     ${net_debt/1e9:.1f}B")
print(f"   Shares Out:   {shares_out/1e9:.1f}B")

# Calculate WACC
print(f"🧮 Calculating Risk Premium for {ticker}...")
wacc_calc = WACCCalculator(ticker)
wacc_result = wacc_calc.calculate_wacc()

print(f"   WACC: {wacc_result['wacc']:.2%}")

# DCF Model
sector = COMPANIES[ticker]['type']
assumptions = SECTOR_ASSUMPTIONS[sector]

dcf = DCFModel(
    ticker=ticker,
    wacc=wacc_result['wacc'],
    terminal_growth_rate=assumptions['terminal_growth']
)

projected_fcf = []
current_rev = latest_revenue

for i in range(5):
    growth_rate = assumptions['revenue_growth'][i]
    current_rev = current_rev * (1 + growth_rate)
    
    fcf = dcf.calculate_fcf(
        revenue=current_rev,
        ebitda_margin=assumptions['ebitda_margin_base'],
        tax_rate=assumptions['tax_rate'],
        capex_percent_revenue=assumptions['capex_percent_revenue']
    )
    projected_fcf.append(fcf)

# Terminal Value & Valuation
tv = dcf.calculate_terminal_value(projected_fcf[-1])
valuation = dcf.discount_cash_flows(projected_fcf, tv)

# Implied Share Price
equity_value = valuation['enterprise_value'] - net_debt
implied_share_price = equity_value / shares_out
upside = (implied_share_price - current_price) / current_price

print(f"\n⚖️ VALUATION VERDICT for {ticker}")
print(f"   Current Market Price:   ${current_price:.2f}")
print(f"   DCF Implied Value:      ${implied_share_price:.2f}")
print(f"   Upside / (Downside):    {upside:.1%}")

# Sensitivity Analysis
print("\n🌪️ RUNNING STRESS TEST...")
sens = SensitivityAnalysis(ticker, wacc_result['wacc'], assumptions['terminal_growth'])
sens_results = sens.run_oil_price_sensitivity(
    base_revenue=latest_revenue, 
    tax_rate=assumptions['tax_rate'], 
    capex_percent=assumptions['capex_percent_revenue'],
    net_debt=net_debt,
    shares=shares_out
)

# --- GENERATE & SAVE CHART ---
print("\n📊 Generating Sensitivity Chart...")
scenarios = list(sens_results.keys())
prices = list(sens_results.values())
colors = ['firebrick', 'steelblue', 'forestgreen'] # Bear, Base, Bull

plt.figure(figsize=(10, 6))
bars = plt.bar(scenarios, [max(0, p) for p in prices], color=colors, alpha=0.8)
plt.axhline(y=current_price, color='black', linestyle='--', linewidth=2, label=f'Current Market Price (${current_price:.2f})')

plt.title(f'ExxonMobil (XOM) Valuation Sensitivity', fontsize=14)
plt.ylabel('Implied Share Price ($)', fontsize=12)
plt.xlabel('Oil Price Scenario', fontsize=12)
plt.legend()

for i, bar in enumerate(bars):
    height = prices[i]
    label = f'${height:.2f}' if height >= 0 else 'Distressed'
    plt.text(bar.get_x() + bar.get_width()/2., max(0, height),
             label, ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
# Save to figures directory for README display
fig_path = os.path.join('figures', 'sensitivity_chart.png')
plt.savefig(fig_path)
print(f"✅ Chart saved to {fig_path}")
