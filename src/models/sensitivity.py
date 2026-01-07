"""
Sensitivity Analysis Module
Runs DCF valuations across multiple oil price scenarios.
"""
from src.models.dcf import DCFModel
from config.settings import OIL_SCENARIOS, SECTOR_ASSUMPTIONS, COMPANIES

class SensitivityAnalysis:
    def __init__(self, ticker, wacc, terminal_growth_rate):
        self.ticker = ticker
        self.wacc = wacc
        self.terminal_growth_rate = terminal_growth_rate
        
    def run_oil_price_sensitivity(self, base_revenue, tax_rate, capex_percent, net_debt, shares):
        """
        Iterates through Low/Base/High oil scenarios and returns implied share prices.
        Returns: Dictionary {scenario_name: share_price}
        """
        results = {}
        # Get sector-specific assumptions for this company
        company_data = COMPANIES.get(self.ticker, {'type': 'integrated'})
        sector = company_data['type']
        sector_assumptions = SECTOR_ASSUMPTIONS[sector] 
        
        print(f"--- Sensitivity Stress Test ({self.ticker}) ---")
        
        for scenario_name, params in OIL_SCENARIOS.items():
            # Adjust Margin based on scenario (The "What If")
            base_margin = sector_assumptions['ebitda_margin_base']
            margin_adjustment = params['margin_adjustment']
            adjusted_margin = base_margin + margin_adjustment
            
            # Initialize DCF
            dcf = DCFModel(self.ticker, self.wacc, self.terminal_growth_rate)
            
            # Project Cash Flows 
            # We assume Revenue stays same, but Margin takes the hit (Margin Compression)
            current_rev = base_revenue
            projected_fcf = []
            
            for i in range(5):
                growth_rate = sector_assumptions['revenue_growth'][i]
                current_rev = current_rev * (1 + growth_rate)
                fcf = dcf.calculate_fcf(current_rev, adjusted_margin, tax_rate, capex_percent)
                projected_fcf.append(fcf)
                
            # Valuation
            tv = dcf.calculate_terminal_value(projected_fcf[-1])
            val = dcf.discount_cash_flows(projected_fcf, tv)
            
            # Convert to Share Price
            equity_val = val['enterprise_value'] - net_debt
            share_price = equity_val / shares
            
            results[scenario_name] = share_price
            print(f"   Scenario {scenario_name.upper()} (${params['price']}/bbl): ${share_price:.2f}/share")
            
        return results
