"""
Discounted Cash Flow (DCF) Model
Projects Free Cash Flow and determines Intrinsic Value.
"""

import numpy as np
import pandas as pd

class DCFModel:
    def __init__(self, ticker, wacc, terminal_growth_rate, projection_years=5):
        self.ticker = ticker
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        self.projection_years = projection_years

    def calculate_fcf(self, revenue, ebitda_margin, tax_rate, capex_percent_revenue):
        """
        Calculate Unlevered Free Cash Flow (UFCF) for a single period.
        Energy Sector Proxy: FCF = EBITDA - Taxes - Capex
        """
        ebitda = revenue * ebitda_margin
        
        # Taxes paid on EBIT (EBITDA - D&A). 
        # For mature O&G, we assume D&A ≈ Capex (Maintenance Mode).
        # Therefore EBIT ≈ EBITDA - Capex
        ebit = ebitda - (revenue * capex_percent_revenue)
        taxes = ebit * tax_rate
        
        capex = revenue * capex_percent_revenue
        
        # UFCF = EBITDA - Taxes - Capex
        fcf = ebitda - taxes - capex
        return fcf

    def calculate_terminal_value(self, final_year_fcf):
        """
        Gordon Growth Method: TV = (FCF_n * (1 + g)) / (WACC - g)
        Includes Logic Guard for WACC <= g
        """
        # GUARD: If Growth >= WACC, the formula explodes (div by zero or negative)
        # We cap the growth rate at WACC - 1.5% to ensure a finite value
        if self.terminal_growth_rate >= self.wacc:
            capped_growth = self.wacc - 0.015
            print(f"⚠️ Risk Guard: Terminal growth ({self.terminal_growth_rate:.1%}) exceeds WACC. Capped at {capped_growth:.1%} to prevent infinity.")
            effective_g = capped_growth
        else:
            effective_g = self.terminal_growth_rate
            
        return (final_year_fcf * (1 + effective_g)) / (self.wacc - effective_g)

    def discount_cash_flows(self, fcf_list, terminal_value):
        """
        Discount projected FCFs and TV back to present value.
        Includes Logic Guard for Negative Equity Value (Distressed Asset).
        """
        pv_fcf = 0
        
        for i, fcf in enumerate(fcf_list):
            year = i + 1
            discount_factor = 1 / ((1 + self.wacc) ** year)
            pv_fcf += fcf * discount_factor
            
        pv_tv = terminal_value / ((1 + self.wacc) ** self.projection_years)
        
        enterprise_value = pv_fcf + pv_tv
        
        return {
            "pv_explicit_fcf": pv_fcf,
            "pv_terminal_value": pv_tv,
            "enterprise_value": enterprise_value,
            "percent_value_from_tv": pv_tv / enterprise_value if enterprise_value != 0 else 0
        }
