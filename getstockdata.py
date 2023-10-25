#!/usr/bin/env python

import argparse
from datetime import datetime
import dateutil.relativedelta
import pandas as pd
import yfinance as yf
import sys

DEFAULT_FORMAT_DATE = "%Y-%m-%d"
DEFAULT_END_DATE = datetime.today()
DEFAULT_START_DATE = DEFAULT_END_DATE - dateutil.relativedelta.relativedelta(years=1)
DEFAULT_GROUP_BY = "ticker"
DEFAULT_PRICE_TO_GET = "Close"

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--tickers",
    default="AMZN",
    type=str,
    help='Stocks tickers to get separated by space. Example: "AMZN MSFT"',
)
parser.add_argument(
    "-s",
    "--start",
    type=str,
    default=DEFAULT_START_DATE.strftime(DEFAULT_FORMAT_DATE),
    help='Start date to get stock values in YYYY-MM-DD format. Example: "2023-01-01"',
)
parser.add_argument(
    "-e",
    "--end",
    type=str,
    default=DEFAULT_END_DATE.strftime(DEFAULT_FORMAT_DATE),
    help='End date to get stock values in YYYY-MM-DD format. Example: "2023-12-31"',
)

parser.add_argument(
    "-f",
    "--file",
    type=str,
    default="asset_prices.csv",
    help='End date to get stock values in YYYY-MM-DD format. Example: "2023-12-31"',
)

args = parser.parse_args()

tickers_str = args.tickers
start_str = args.start
end_str = args.end
file = args.file

start = datetime.strptime(start_str, DEFAULT_FORMAT_DATE)
end = datetime.strptime(end_str, DEFAULT_FORMAT_DATE)

if end<start:
    print("ERROR: end date must be great or equal start date")
    sys.exit(1)

data = yf.download(tickers_str, start=start_str, end=end_str, group_by=DEFAULT_GROUP_BY, auto_adjust=True)
if data.empty:
    print("ERROR: Not able to read stock data")
    sys.exit(1)

tickers = tickers_str.split()
asset = pd.DataFrame()
if len(tickers) <=1 :
    asset[tickers_str] = data[DEFAULT_PRICE_TO_GET]    
else:    
    for ticker in tickers:
        asset[ticker] = data[ticker][DEFAULT_PRICE_TO_GET]

del data

asset.to_csv(file)
print(file)

del asset

sys.exit(0)