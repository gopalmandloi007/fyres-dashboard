import streamlit as st
import pandas as pd
import datetime
import time
from utils import get_fyers_client

def get_prev_trading_close_fyers(fyers, symbol, upto_date=None):
    if upto_date is None:
        upto_date = datetime.datetime.now().date()
    else:
        upto_date = pd.to_datetime(upto_date).date()
    for days_ago in range(1, 10):
        dt = upto_date - datetime.timedelta(days=days_ago)
        dt_str = dt.strftime("%Y-%m-%d")
        data = {
            "symbol": symbol,
            "resolution": "1D",
            "date_format": "1",
            "range_from": dt_str,
            "range_to": dt_str,
            "cont_flag": "1"
        }
        try:
            candles = fyers.history(data)
            if candles.get('code') == 200 and candles.get('candles'):
                prev_close = candles['candles'][0][4]
                return prev_close, dt_str
        except Exception:
            time.sleep(0.5)
            continue
    return None, None

def show():
    st.header("FYERS Holdings / Positions / Funds")
    fyers = get_fyers_client()

    # --- Holdings ---
    holdings = fyers.holdings()
    if holdings.get('code') == 200:
        holdings_data = holdings.get('holdings', [])
        overall_data = holdings.get('overall', {})
        if holdings_data:
            holdings_table = []
            prev_close_cache = {}
            for idx, holding in enumerate(sorted(holdings_data, key=lambda x: x.get('symbol', '')), start=1):
                symbol = holding.get('symbol', '')
                ltp = holding.get('ltp', 0)
                investment = holding.get('costPrice', 0) * holding.get('quantity', 0)
                pl_percent = (holding.get('pl', 0) / investment) * 100 if investment != 0 else 0
                current_value = investment + holding.get('pl', 0)
                quantity = holding.get('quantity', 0)

                if symbol not in prev_close_cache:
                    prev_close, _ = get_prev_trading_close_fyers(fyers, symbol)
                    prev_close_cache[symbol] = prev_close
                else:
                    prev_close = prev_close_cache[symbol]

                today_pnl = 0
                today_perc = 0
                if prev_close is not None and quantity > 0:
                    today_pnl = (ltp - prev_close) * quantity
                    today_perc = ((ltp - prev_close) / prev_close) * 100 if prev_close != 0 else 0

                row = {
                    "Sr. No.": idx,
                    "Symbol": symbol,
                    "Current P&L": holding.get('pl', 0),
                    "P&L %": pl_percent,
                    "Quantity": quantity,
                    "Average Price": holding.get('costPrice', 0),
                    "LTP": ltp,
                    "Today %Change": today_perc if prev_close is not None else "N/A",
                    "Investment": investment,
                    "Current Value": current_value,
                    "Prev Close": prev_close if prev_close is not None else "N/A",
                    "Today P&L": today_pnl
                }
                holdings_table.append(row)
            df = pd.DataFrame(holdings_table)
            st.subheader("Holdings")
            st.dataframe(df)

            st.subheader("Overall Summary")
            st.write({
                "Total Investment": overall_data.get('total_investment', 0),
                "Total Current Value": overall_data.get('total_current_value', 0),
                "Overall P&L": overall_data.get('total_pl', 0),
            })
        else:
            st.info("No holdings data available.")
    else:
        st.error(f"Error fetching holdings: {holdings.get('message', 'No message available')}")

    # --- Positions ---
    positions = fyers.positions()
    if positions.get('code') == 200:
        positions_data = positions.get('netPositions', [])
        if positions_data:
            df = pd.DataFrame(positions_data)
            st.subheader("Positions")
            st.dataframe(df)
        else:
            st.info("No positions data available.")
    else:
        st.error(f"Error fetching positions: {positions.get('message', 'No message available')}")

    # --- Funds ---
    funds = fyers.funds()
    if funds.get('code') == 200:
        funds_data = funds.get('fund_limit', [])
        if funds_data:
            st.subheader("Available Funds")
            st.write({
                "Available Funds": funds_data[0].get('availableFunds', 0),
                "Used Margin": funds_data[0].get('usedMargin', 0),
                "Net Funds": funds_data[0].get('netFunds', 0),
                "Total Collateral": funds_data[0].get('totalCollateral', 0),
            })
        else:
            st.info("No funds data available.")
    else:
        st.error(f"Error fetching funds: {funds.get('message', 'No message available')}")
