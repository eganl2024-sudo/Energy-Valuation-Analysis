# Energy Sector Valuation Analysis

A comprehensive valuation framework for global energy companies. DCF analysis, comparable companies, and investment thesis for integrated majors, transition leaders, and renewables.

## Overview

This project analyzes 7 major energy companies:
- **ExxonMobil, Chevron, Shell** (Integrated Majors)
- **TotalEnergies, BP** (European Transition Leaders)
- **ConocoPhillips** (Upstream Pure Play)
- **NextEra Energy** (Renewables)

## Structure

```
energy-valuation-analysis/
├── config/              # Configuration and assumptions
├── src/                 # Source code
│   └── models/         # Valuation models
├── docs/               # Documentation
├── data/               # Financial data (raw & processed)
├── notebooks/          # Analysis notebooks
└── figures/            # Output visualizations
```

## Quick Start

1. Clone repo
2. `pip install -r requirements.txt`
3. Set up `.env` with API key
4. Run `notebooks/analysis.ipynb`

## Phase Status

- **Phase 1:** In Progress (Vacation Dec 26 - Jan 3)
  - [ ] Core assumptions document
  - [ ] Configuration & company setup
  - [ ] Data fetchers
  
- **Phase 2:** Scheduled (Jan 3-12)
  - [ ] DCF valuations
  - [ ] Comparable analysis
  - [ ] Investment thesis
  - [ ] Final notebook

## Requirements

- Python 3.8+
- pandas, numpy, yfinance, requests
- See `requirements.txt` for full list

## API Keys

Get free API keys:
- Financial Modeling Prep: https://financialmodelingprep.com
- FRED: https://fredaccount.stlouisfed.org (optional)

See `.env.example` for setup.
