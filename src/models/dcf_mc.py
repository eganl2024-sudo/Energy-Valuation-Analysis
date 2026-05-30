"""
Private Oil Futures - Dynamic Monte Carlo DCF Simulator
Vectorized cash flow forecasting and discount engine mapping neural return shifts
and annualized EWMA volatility directly to corporate valuations.
"""

import numpy as np
import pandas as pd

class MonteCarloDCFModel:
    def __init__(self, ticker, base_wacc, base_terminal_growth, base_margin, 
                 revenue_growth_list, financials, expected_return_shift=0.0, ewma_vol=0.15):
        """
        Args:
            ticker (str): Company ticker
            base_wacc (float): CAPM-derived base WACC (discount rate)
            base_terminal_growth (float): Perpetual growth rate
            base_margin (float): Sector ebitda margin baseline
            revenue_growth_list (list/np.array): 5-year expected revenue growths
            financials (dict): Standardized balance sheet inputs:
                               { "revenue": float, "net_debt": float, "shares": float }
            expected_return_shift (float): Tier 1 Neural net WGAN-GP expected return shift
            ewma_vol (float): Tier 1 Annualized EWMA commodity volatility
        """
        self.ticker = ticker
        self.base_wacc = base_wacc
        self.base_terminal_growth = base_terminal_growth
        self.base_margin = base_margin
        self.revenue_growth_list = np.array(revenue_growth_list)
        self.financials = financials
        self.expected_return_shift = expected_return_shift
        self.ewma_vol = ewma_vol

    def run_simulation(self, num_trials=5000, current_price=100.0, tax_rate=0.21, capex_percent_revenue=0.08):
        """
        Runs a vectorized Monte Carlo simulation.
        Returns:
            dict: Simulation metrics and raw share price vector.
        """
        # 1. Random variable WACC & Terminal Growth draws
        # WACC_trial ~ Normal(base_wacc, 0.0075), clamped to [4%, 18%]
        wacc_trials = np.random.normal(self.base_wacc, 0.0075, size=num_trials)
        wacc_trials = np.clip(wacc_trials, 0.04, 0.18)
        
        # terminal_growth_trial ~ Normal(base_terminal_growth, 0.005), clamped to [-3%, 4%]
        g_trials = np.random.normal(self.base_terminal_growth, 0.005, size=num_trials)
        g_trials = np.clip(g_trials, -0.03, 0.04)
        
        # 2. EBITDA Margin standard deviation scaled by EWMA Volatility
        # If the commodity EWMA Volatility spikes, the company's operational margin uncertainty spikes.
        margin_std = 0.05 + 0.10 * self.ewma_vol
        margin_trials = np.random.normal(self.base_margin, margin_std, size=num_trials)
        margin_trials = np.clip(margin_trials, 0.05, 0.85)
        
        # 3. Revenue growth projections shocked by Neural projections & EWMA Volatility
        # Growth volatility scales with the commodity's EWMA Volatility
        growth_std = 0.02 + 0.05 * self.ewma_vol
        
        # Size: (num_trials, 5)
        growth_shocks = np.random.normal(self.expected_return_shift, growth_std, size=(num_trials, 5))
        
        # Base growth factors: (1, 5)
        base_growth = self.revenue_growth_list.reshape(1, 5)
        
        # Trial growth rates: (num_trials, 5)
        trial_growth_rates = base_growth + growth_shocks
        trial_growth_rates = np.clip(trial_growth_rates, -0.15, 0.25) # physical bounds: -15% to +25%
        
        # Compute revenues for 5 years
        # Size: (num_trials, 5)
        projected_revenues = np.zeros((num_trials, 5))
        current_revs = np.full(num_trials, self.financials["revenue"])
        
        for yr in range(5):
            current_revs = current_revs * (1.0 + trial_growth_rates[:, yr])
            projected_revenues[:, yr] = current_revs
            
        # 4. Project UFCFs: EBITDA - Taxes - Capex
        # ebitda = revenue * margin
        # ebit = ebitda - (revenue * capex_percent)
        # taxes = ebit * tax_rate
        # UFCF = ebitda - taxes - capex
        projected_ebitdas = projected_revenues * margin_trials.reshape(num_trials, 1)
        projected_capex = projected_revenues * capex_percent_revenue
        projected_ebits = projected_ebitdas - projected_capex
        projected_taxes = projected_ebits * tax_rate
        projected_ufcfs = projected_ebitdas - projected_taxes - projected_capex
        
        # 5. Gordon Growth Terminal Value
        # TV = (FCF_5 * (1 + g)) / (WACC - g)
        # Risk guard: If g >= WACC, cap g at WACC - 1.5%
        final_ufcf = projected_ufcfs[:, -1]
        
        # Vectorized guard: cap effective_g at wacc - 0.015
        effective_g = np.minimum(g_trials, wacc_trials - 0.015)
        
        terminal_values = (final_ufcf * (1.0 + effective_g)) / (wacc_trials - effective_g)
        
        # 6. Discounting to present value
        # PV of explicit UFCFs
        # Size: (num_trials, 5)
        pv_ufcfs = np.zeros((num_trials, 5))
        for yr in range(5):
            year = yr + 1
            discount_factor = 1.0 / ((1.0 + wacc_trials) ** year)
            pv_ufcfs[:, yr] = projected_ufcfs[:, yr] * discount_factor
            
        pv_explicit = np.sum(pv_ufcfs, axis=1)
        
        # PV of Terminal Value
        pv_tv = terminal_values / ((1.0 + wacc_trials) ** 5)
        
        # Enterprise Value
        enterprise_values = pv_explicit + pv_tv
        
        # 7. Implied Share Price
        # Equity Value = EV - Net Debt
        equity_values = enterprise_values - self.financials["net_debt"]
        implied_share_prices = equity_values / self.financials["shares"]
        
        # Safety clamp: share prices cannot fall below 0.0 (unlimited liability guard)
        implied_share_prices = np.clip(implied_share_prices, 0.0, None)
        
        # 8. Summary metrics
        p10 = float(np.percentile(implied_share_prices, 10))
        p50 = float(np.percentile(implied_share_prices, 50))
        p90 = float(np.percentile(implied_share_prices, 90))
        
        # Probability of Upside
        prob_upside = float(np.mean(implied_share_prices > current_price))
        
        # Margin of Safety (relative to median target)
        if p50 > 0:
            margin_of_safety = (p50 - current_price) / p50
        else:
            margin_of_safety = 0.0
            
        return {
            "implied_prices": implied_share_prices,
            "p10": p10,
            "p50": p50,
            "p90": p90,
            "prob_upside": prob_upside,
            "margin_of_safety": margin_of_safety,
            "mean_wacc": float(np.mean(wacc_trials)),
            "mean_g": float(np.mean(g_trials))
        }
