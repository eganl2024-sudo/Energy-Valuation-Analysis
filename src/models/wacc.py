"""
WACC (Weighted Average Cost of Capital) Calculator
Uses CAPM (Capital Asset Pricing Model) to determine discount rates.
"""

from config.settings import WACC_PARAMETERS, GLOBAL_DEFAULTS

class WACCCalculator:
    def __init__(self, ticker):
        self.ticker = ticker
        self.risk_free = WACC_PARAMETERS["risk_free_rate"]
        self.market_premium = WACC_PARAMETERS["market_risk_premium"]
        
        # --- DEFENSIVE CODING START ---
        # Try to get specific params, otherwise fall back to GLOBAL_DEFAULTS
        
        # 1. Beta
        self.beta = WACC_PARAMETERS["betas"].get(ticker, GLOBAL_DEFAULTS["beta"])
        
        # 2. Cost of Debt
        self.cost_of_debt = WACC_PARAMETERS["cost_of_debt"].get(ticker, GLOBAL_DEFAULTS["cost_of_debt"])
        
        # 3. Capital Structure
        self.debt_weight = WACC_PARAMETERS["capital_structure"].get(ticker, GLOBAL_DEFAULTS["capital_structure"])
        
        # Log warning if using defaults
        if ticker not in WACC_PARAMETERS["betas"]:
            print(f"⚠️ Warning: Ticker '{ticker}' not found in WACC config. Using sector defaults.")
            
        # --- DEFENSIVE CODING END ---
        
        self.tax_rate = 0.21 
        self.equity_weight = 1.0 - self.debt_weight

    def calculate_cost_of_equity(self):
        """
        CAPM Formula: Re = Rf + Beta * (Rm - Rf)
        """
        return self.risk_free + (self.beta * self.market_premium)

    def calculate_after_tax_cost_of_debt(self):
        """
        Rd * (1 - t)
        """
        return self.cost_of_debt * (1 - self.tax_rate)

    def calculate_wacc(self):
        """
        WACC = (E/V * Re) + (D/V * Rd * (1-t))
        """
        re = self.calculate_cost_of_equity()
        rd_after_tax = self.calculate_after_tax_cost_of_debt()
        
        wacc = (self.equity_weight * re) + (self.debt_weight * rd_after_tax)
        
        return {
            "ticker": self.ticker,
            "beta": self.beta,
            "cost_of_equity": re,
            "cost_of_debt_after_tax": rd_after_tax,
            "wacc": wacc
        }

if __name__ == "__main__":
    # Unit Test: Compare Exxon (Integrated) vs NextEra (Renewable) vs Conoco (Upstream)
    print("--- WACC ENGINE DIAGNOSTICS ---")
    
    for ticker in ["XOM", "NEE", "COP", "UNKNOWN"]:
        calc = WACCCalculator(ticker)
        result = calc.calculate_wacc()
        print(f"{ticker} | Beta: {result['beta']:.2f} | WACC: {result['wacc']:.2%}")
