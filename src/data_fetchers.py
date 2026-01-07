"""
Data Fetchers for Energy Valuation Analysis
Retrieve financial data from multiple APIs
"""

import os
import yfinance as yf
import pandas as pd
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class DataFetcher:
    """Fetch financial data from APIs"""
    
    def __init__(self):
        self.fmp_key = os.getenv("FMP_API_KEY")
        self.fmp_url = "https://financialmodelingprep.com/api/v3"
    
    def get_stock_price(self, ticker, start_date="2019-01-01"):
        """
        Download historical stock prices using yfinance
        
        Args:
            ticker: Stock ticker (e.g., "XOM")
            start_date: Start date for historical data
            
        Returns:
            pd.DataFrame: OHLCV data
        """
        try:
            print(f"Fetching stock price for {ticker}...")
            # Note: yfinance auto-adjusts logic often, ensure library is up to date
            data = yf.download(ticker, start=start_date, progress=False)
            print(f"✓ Downloaded {len(data)} trading days for {ticker}")
            return data
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    def get_current_price(self, ticker):
        """Get current stock price"""
        try:
            ticker_obj = yf.Ticker(ticker)
            # Try fast info first
            if hasattr(ticker_obj, "fast_info"):
                price = ticker_obj.fast_info.last_price
            else:
                price = ticker_obj.info.get("currentPrice")
                
            if not price:
                price = yf.download(ticker, period="1d", progress=False)["Adj Close"].iloc[-1]
            return price
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_company_info(self, ticker):
        """Get company basic info"""
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info
            return {
                "company_name": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "market_cap": info.get("marketCap", 0) / 1e9 if info.get("marketCap") else None,
                "current_price": self.get_current_price(ticker),
                "shares_outstanding": info.get("sharesOutstanding", 0) / 1e6 if info.get("sharesOutstanding") else None,
            }
        except Exception as e:
            print(f"Error fetching info for {ticker}: {e}")
            return None

    # Note: The get_income_statement and similar methods below require a valid FMP API key.
    # If using free tier/no key, these will fail or need to be mocked.
    
    def get_income_statement(self, ticker, period="annual"):
        """Download income statement from FMP"""
        try:
            if not self.fmp_key:
                print("Warning: No FMP API Key found. Skipping Financials.")
                return None

            print(f"Fetching income statement for {ticker}...")
            url = f"{self.fmp_url}/income-statement/{ticker}"
            params = {"period": period, "apikey": self.fmp_key}
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                df = pd.DataFrame(data)
                print(f"✓ Downloaded {len(df)} years of income statement")
                return df
            else:
                print(f"No data returned for {ticker}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    # Test the fetcher
    fetcher = DataFetcher()
    
    # Test with ExxonMobil
    print("\n=== Testing DataFetcher ===\n")
    
    # Test stock price
    price_data = fetcher.get_stock_price("XOM")
    if price_data is not None:
        print(f"Latest price data shape: {price_data.shape}\n")
    
    # Test company info
    info = fetcher.get_company_info("XOM")
    if info:
        print(f"Company: {info.get('company_name')}")
        print(f"Sector: {info.get('sector')}")
        print(f"Market Cap: ${info.get('market_cap', 0):.1f}B\n")
