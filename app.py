# import libraries
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib

# stocks dataframe creation
def create_stocks_dataframe():

    columns = [
        "Symbol",
        "Shares",
        "Purchase Price",
        "Current Price",
        "Cost",
        "Market Value",
        "Dollar Gain",
        "Growth",
        "Dividend",
        "Dividend Yield",
        "Dividend Income",
        "Industry",
        "Total Return ($)",
        "Total Return (%)"
    ]

    stocks = pd.DataFrame(columns = columns)

    return stocks

# get user stock, number of shares, and share price data to fill stocks dataframe
def user_stock_data():

    col1, col2, col3 = st.columns(3, border = True)

    with col1:
        symbol = st.text_input("Enter Stock Symbol", placeholder="e.g. AAPL")

    with col2:
        shares = st.number_input("Enter the number of shares bought", placeholder="e.g. 3.56")

    with col3:
        purchase_price = st.number_input("Enter the price at which you bought the shares", placeholder="e.g. 220.52")

    return symbol.upper(), shares, purchase_price

# get stock info
def get_stock_metrics(symbol, shares, purchase_price):

    ticker = yf.Ticker(symbol)
    info = ticker.fast_info

    current_price = info.get("last_price", None)
    dividend_yield = info.get("dividend_yield", 0) or 0
    dividend_rate = info.get("annual_dividend", 0) or 0
    
    try:
        industry = ticker.info.get("industry", "Unknown")
    except Exception:
        industry = "Unknown"

    cost = shares * purchase_price
    market_value = shares * current_price if current_price else None
    dollar_gain = (market_value - cost) if market_value else None
    growth = (dollar_gain / cost) if dollar_gain is not None else None
    dividend_income = market_value * dividend_yield if market_value else 0
    total_return_dollar = (dollar_gain + dividend_income) if dollar_gain else None
    total_return_percent = (total_return_dollar / cost) if total_return_dollar else None

    return {
        "Current Price": current_price,
        "Cost": cost,
        "Market Value": market_value,
        "Dollar Gain": dollar_gain,
        "Growth": growth,
        "Dividend": dividend_rate,
        "Dividend Yield": dividend_yield,
        "Dividend Income": dividend_income,
        "Industry": industry,
        "Total Return ($)": total_return_dollar,
        "Total Return (%)": total_return_percent
    }

# insert data into dataframe
def insert_data(data, dataframe):

    symbol, shares, purchase_price = data
    metrics = get_stock_metrics(symbol, shares, purchase_price)

    new_row = {
        "Symbol": symbol.upper(),
        "Shares": shares,
        "Purchase Price": purchase_price,
        **metrics  # merges all the calculated Yahoo fields
    }

    dataframe = pd.concat([pd.DataFrame([new_row]), dataframe], ignore_index=True)

    return dataframe


# main entry point
def main():
    
    # streamlit page configuration
    st.set_page_config(
        page_title = "Investment Portfolio Tracker",
        layout = "wide",
        initial_sidebar_state = "collapsed"
    )

    # create stocks dataframe if it does not yet exist, else add it to the session state
    if "stocks_dataframe" not in st.session_state:
        st.session_state.stocks_dataframe = create_stocks_dataframe()

    # UI
    st.title("📈 Investment Portfolio Tracker")
    st.write("---")

    # get user stock inputs
    symbol, shares, purchase_price = user_stock_data()

    # create stocks dataframe 
    stocks_dataframe = create_stocks_dataframe()

    # button to add data to stocks dataframe
    if st.button("Add to Portfolio"):
        st.session_state.stocks_dataframe = insert_data(
            (symbol, shares, purchase_price),
            st.session_state.stocks_dataframe
        )

    st.write("---")

    # show stocks dataframe
    st.dataframe(st.session_state.stocks_dataframe)



if __name__ == "__main__":
    main()