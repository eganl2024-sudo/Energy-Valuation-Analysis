"""
Configuration for Energy Valuation Analysis
Central hub for all companies, assumptions, and parameters
"""

# ============================================================================
# COMPANY UNIVERSE (Your 7 companies)
# ============================================================================

COMPANIES = {
    "XOM": {
        "name": "ExxonMobil",
        "type": "integrated",
        "country": "US",
        "description": "Largest US integrated oil & gas company"
    },
    "CVX": {
        "name": "Chevron",
        "type": "integrated",
        "country": "US",
        "description": "Second-largest US integrated, strong upstream"
    },
    "SHEL": {
        "name": "Shell",
        "type": "integrated",
        "country": "Europe",
        "description": "European major, most aggressive renewable pivot"
    },
    "TTE": {
        "name": "TotalEnergies",
        "type": "integrated",
        "country": "Europe",
        "description": "French major, balanced transition approach"
    },
    "BP": {
        "name": "BP",
        "type": "integrated",
        "country": "Europe",
        "description": "UK major, most extreme energy transition pivot"
    },
    "COP": {
        "name": "ConocoPhillips",
        "type": "upstream",
        "country": "US",
        "description": "Pure upstream producer, high capex"
    },
    "NEE": {
        "name": "NextEra Energy",
        "type": "renewables",
        "country": "US",
        "description": "Renewables leader, growth story"
    },
}

PRIMARY_TICKERS = ["XOM", "CVX", "SHEL", "TTE", "BP", "COP", "NEE"]

# ============================================================================
# SECTOR-SPECIFIC ASSUMPTIONS
# ============================================================================

SECTOR_ASSUMPTIONS = {
    "integrated": {
        "revenue_growth": [0.02, 0.01, 0.00, -0.01, -0.015],  # Years 1-5
        "ebitda_margin_base": 0.30,  # At $85 oil
        "ebitda_margin_high": 0.40,  # At $110 oil
        "ebitda_margin_low": 0.20,   # At $60 oil
        "capex_percent_revenue": 0.11,
        "tax_rate": 0.24,
        "terminal_growth": 0.015,
    },
    "upstream": {
        "revenue_growth": [0.02, 0.01, 0.00, -0.02, -0.02],
        "ebitda_margin_base": 0.40,
        "ebitda_margin_high": 0.50,
        "ebitda_margin_low": 0.30,
        "capex_percent_revenue": 0.16,
        "tax_rate": 0.24,
        "terminal_growth": 0.010,
    },
    "renewables": {
        "revenue_growth": [0.05, 0.05, 0.05, 0.04, 0.04],
        "ebitda_margin_base": 0.28,
        "ebitda_margin_high": 0.32,
        "ebitda_margin_low": 0.25,
        "capex_percent_revenue": 0.19,
        "tax_rate": 0.24,
        "terminal_growth": 0.025,
    },
}

# ============================================================================
# WACC PARAMETERS
# ============================================================================

WACC_PARAMETERS = {
    "risk_free_rate": 0.045,  # 10Y Treasury
    "market_risk_premium": 0.065,
    
    "betas": {
        "XOM": 1.15,
        "CVX": 1.15,
        "SHEL": 1.10,
        "TTE": 1.12,
        "BP": 1.18,
        "COP": 1.25,
        "NEE": 0.95,
    },
    
    "cost_of_debt": {
        "XOM": 0.0425,
        "CVX": 0.0425,
        "SHEL": 0.0475,
        "TTE": 0.0475,
        "BP": 0.0475,
        "COP": 0.045,
        "NEE": 0.04,
    },
    
    "capital_structure": {  # D/(D+E) ratios
        "XOM": 0.22,
        "CVX": 0.22,
        "SHEL": 0.28,
        "TTE": 0.28,
        "BP": 0.32,
        "COP": 0.23,
        "NEE": 0.45,
    },
}

# ============================================================================
# OIL PRICE SCENARIOS
# ============================================================================

OIL_SCENARIOS = {
    "low": {
        "price": 60,
        "scenario": "Recession/Oversupply",
        "margin_adjustment": -0.10,  # Margins compress 10%
    },
    "base": {
        "price": 85,
        "scenario": "Balanced",
        "margin_adjustment": 0.00,
    },
    "high": {
        "price": 110,
        "scenario": "Supply Disruption",
        "margin_adjustment": 0.10,  # Margins expand 10%
    },
}

# ============================================================================
# DCF PARAMETERS
# ============================================================================

DCF_PARAMETERS = {
    "projection_years": 5,
    "nwc_percent_revenue": 0.05,  # 5% of revenue
}

# ============================================================================
# DATA SOURCES
# ============================================================================

DATA_SOURCES = {
    "yfinance": "https://finance.yahoo.com",
    "fmp": "https://financialmodelingprep.com/api/v3",
    "fred": "https://api.stlouisfed.org/fred",
}

DATA_START_DATE = "2019-01-01"  # Pre-COVID for context

# ============================================================================
# LATEST FINANCIALS (TTM Estimates for MVP)
# Acts as a fallback database to make the model dynamic without an API Key
# ============================================================================

COMPANY_FINANCIALS = {
    "XOM": {"revenue": 344.6e9, "net_debt": 8.0e9, "shares": 4.0e9},
    "CVX": {"revenue": 200.9e9, "net_debt": 12.0e9, "shares": 1.8e9},
    "SHEL": {"revenue": 316.0e9, "net_debt": 44.0e9, "shares": 6.5e9},
    "TTE": {"revenue": 237.0e9, "net_debt": 18.0e9, "shares": 2.4e9},
    "BP":  {"revenue": 210.0e9, "net_debt": 22.0e9, "shares": 16.0e9}, # BP has huge share count (ADR/Ordinary diff)
    "COP": {"revenue": 58.0e9, "net_debt": 10.0e9, "shares": 1.2e9},
    "NEE": {"revenue": 28.0e9, "net_debt": 68.0e9, "shares": 2.0e9}, # Utility = High Debt
}

# ============================================================================
# ROBUSTNESS DEFAULTS (Safety Net)
# Used if a ticker is not found in the specific dictionaries above
# ============================================================================

GLOBAL_DEFAULTS = {
    "beta": 1.10,               # Market average energy beta
    "cost_of_debt": 0.05,       # Conservative debt cost
    "capital_structure": 0.30,  # 30% Debt / 70% Equity
    "tax_rate": 0.24,           # Standard US rate
    "terminal_growth": 0.015,   # Conservative long-term growth
    "ebitda_margin": 0.25,      # Conservative margin
    "capex_percent": 0.15,      # Capital intensive default
}
