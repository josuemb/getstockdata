#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
This module allow downloading Yahoo Finance Stock Data and saving it into
a csv file.
Example:
    $ python getstockdata.py
    Get stock information from AMZN ticker in the last year.
Help:
    $ python getstockdata.py -h
    $ python getstockdata.py --help
"""

import argparse
import sys
from datetime import datetime
import dateutil.relativedelta
import pandas as pd
import yfinance as yf

DEFAULT_FILE_NAME = "asset_prices.csv"
DEFAULT_TICKER_STRING = "AMZN"
DEFAULT_FORMAT_DATE = "%Y-%m-%d"
DEFAULT_END_DATE = datetime.today()
DEFAULT_END_DATE_STRING = DEFAULT_END_DATE.strftime(DEFAULT_FORMAT_DATE)
DEFAULT_START_DATE = DEFAULT_END_DATE - \
    dateutil.relativedelta.relativedelta(years=1)
DEFAULT_START_DATE_STRING = DEFAULT_START_DATE.strftime(DEFAULT_FORMAT_DATE)
DEFAULT_GROUP_BY = "ticker"
DEFAULT_PRICE_TO_GET = "Close"
DEFAULT_AUTO_ADJUST = True


def process_arguments(arguments=None):
    '''
    Process provided arguments.

    Parameters:
    __________
    args - Arguments value (normally coming from sys.argv)

    Returns
    __________
    Multiple values:
        file,
        tickers_str,
        start_str,
        end_str
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--tickers",
        default=DEFAULT_TICKER_STRING,
        type=str,
        help='List of stock symbols separated by space. Example: "AMZN MSFT"',
    )
    parser.add_argument(
        "-s",
        "--start",
        type=str,
        default=DEFAULT_START_DATE_STRING,
        help='Start date to get stock values in YYYY-MM-DD format. Example: "2023-01-01"',
    )
    parser.add_argument(
        "-e",
        "--end",
        type=str,
        default=DEFAULT_END_DATE_STRING,
        help='End date to get stock values in YYYY-MM-DD format. Example: "2023-12-31"',
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=DEFAULT_FILE_NAME,
        help='Output file path wo write stock values. Example: asset_prices.csv',
    )

    args = parser.parse_args(arguments)
    tickers_str = args.tickers
    start_str = args.start
    end_str = args.end
    file = args.file
    start = datetime.strptime(start_str, DEFAULT_FORMAT_DATE)
    end = datetime.strptime(end_str, DEFAULT_FORMAT_DATE)

    if end < start:
        print("ERROR: end date must be great or equal start date")
        sys.exit(1)
    del start
    del end
    return file, tickers_str, start_str, end_str


def get_stock_data(file, tickers_str, start_str, end_str):
    '''
    Get closing value of the provided stock tickers from Yahoo Finance.
    Results will be written to a CSV file.

    Parameters:
    __________
    file        :   string
                    Output file path wo write stock values.
                    Example: asset_prices.csv
    tickers_str :   string
                    List of stock symbols separated by space.
                    Example: "AMZN MSFT"
    start_str   :   string
                    Start date to get stock values in YYYY-MM-DD format.
                    Example: "2023-01-01
    end_str     :   End date to get stock values in YYYY-MM-DD format.
                    Example: "2023-12-31"


    Returns
    __________
    None.
    '''
    data = yf.download(tickers_str, start=start_str, end=end_str,
                       group_by=DEFAULT_GROUP_BY, auto_adjust=DEFAULT_AUTO_ADJUST)
    if data.empty:
        print("ERROR: Not able to read stock data")
        sys.exit(1)

    asset = pd.DataFrame()
    tickers = tickers_str.split()
    if len(tickers) <= 1:
        asset[tickers_str] = data[DEFAULT_PRICE_TO_GET]
    else:
        for ticker in tickers:
            asset[ticker] = data[ticker][DEFAULT_PRICE_TO_GET]
    del data
    asset.to_csv(file)
    print(file)
    del asset


def main(file, tickers_str, start_str, end_str):
    '''
    Main function. It processes araguments and call the utility function
    with all argumts provided.

    Parameters:
    __________
    None

    Returns
    __________
    sys.exit(0) - If everythings goes well.
    sys.exit(1) - In case of any error. It also will print error.
    '''
    get_stock_data(file, tickers_str, start_str, end_str)
    sys.exit(0)


if __name__ == "__main__":
    arg_file, arg_tickers_str, arg_start_str, arg_end_str = process_arguments()
    main(arg_file, arg_tickers_str, arg_start_str, arg_end_str)
