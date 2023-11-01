# -*- coding: utf-8 -*-
"""
pytest test file for getstockdata.py.
Example:
    $ pytest getstockdata_test.py
    Rull all tests.
"""

import os
import os.path
import pytest
import getstockdata


class TestGetStockData:
    '''
    Class to contain all getstockdata.py pytest tests.
    '''

    def __print_file_info(self, file):
        '''
        Print file information
        '''
        print(f"File: {file}")
        print(f"os.path.exists: {os.path.exists(file)}")
        print(f"os.path.isfile: {os.path.isfile(file)}")
        print(f"os.path.getsize: {os.path.getsize(file)}")

    def test_processarguments_show_help(self, capsys):
        '''
        Testing process_arguments showing help.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        with pytest.raises(SystemExit):
            getstockdata.process_arguments(["-h"])

        captured = capsys.readouterr()
        assert captured.out.startswith("usage:")

        with pytest.raises(SystemExit):
            getstockdata.process_arguments(["--help"])

        captured = capsys.readouterr()
        assert captured.out.startswith("usage:")

    def test_processarguments_default_data(self):
        '''
        Testing process_arguments using default arguments.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        # Sending empty array to take dafault values
        tmp_args = getstockdata.process_arguments([])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            getstockdata.DEFAULT_TICKER_STRING,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            getstockdata.DEFAULT_END_DATE_STRING)

    def test_processarguments_passing_file_arg(self):
        '''
        Testing process_arguments passing just the file argument.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        tmp_file = "myfile.csv"
        tmp_args = getstockdata.process_arguments(["-f", tmp_file])
        assert tmp_args == (tmp_file,
                            getstockdata.DEFAULT_TICKER_STRING,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            getstockdata.DEFAULT_END_DATE_STRING)
        tmp_args = getstockdata.process_arguments(["--file", tmp_file])
        assert tmp_args == (tmp_file,
                            getstockdata.DEFAULT_TICKER_STRING,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            getstockdata.DEFAULT_END_DATE_STRING)

    def test_processarguments_passing_tickers_arg(self):
        '''
        Testing process_arguments passing just the tickers argument.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        tmp_tickers = "X Y Z"
        tmp_args = getstockdata.process_arguments(["-t", tmp_tickers])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            tmp_tickers,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            getstockdata.DEFAULT_END_DATE_STRING)
        tmp_args = getstockdata.process_arguments(["--tickers", tmp_tickers])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            tmp_tickers,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            getstockdata.DEFAULT_END_DATE_STRING)

    def test_processarguments_passing_start_arg(self):
        '''
        Testing process_arguments passing just the start argument.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        tmp_start = "2010-01-01"
        tmp_args = getstockdata.process_arguments(["-s", tmp_start])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            getstockdata.DEFAULT_TICKER_STRING,
                            tmp_start,
                            getstockdata.DEFAULT_END_DATE_STRING)
        tmp_args = getstockdata.process_arguments(["--start", tmp_start])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            getstockdata.DEFAULT_TICKER_STRING,
                            tmp_start,
                            getstockdata.DEFAULT_END_DATE_STRING)

    def test_processarguments_passing_end_arg(self):
        '''
        Testing process_arguments passing just the end argument.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        tmp_end = "3999-12-31"
        tmp_args = getstockdata.process_arguments(["-e", tmp_end])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            getstockdata.DEFAULT_TICKER_STRING,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            tmp_end)
        tmp_args = getstockdata.process_arguments(["--end", tmp_end])
        assert tmp_args == (getstockdata.DEFAULT_FILE_NAME,
                            getstockdata.DEFAULT_TICKER_STRING,
                            getstockdata.DEFAULT_START_DATE_STRING,
                            tmp_end)

    def test_processarguments_passing_all_args(self):
        '''
        Testing process_arguments passing just the end argument.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        '''
        tmp_filename = "myfile.csv"
        tmp_ticker = "YUP"
        tmp_start = "2023-01-01"
        tmp_end = "2023-12-31"

        tmp_args = getstockdata.process_arguments(
            ["-f", tmp_filename, "-t", tmp_ticker, "-s", tmp_start, "-e", tmp_end])
        assert tmp_args == (tmp_filename,
                            tmp_ticker,
                            tmp_start,
                            tmp_end)
        tmp_args = getstockdata.process_arguments(
            ["--file", tmp_filename, "--tickers",
             tmp_ticker, "--start",
             tmp_start, "--end", tmp_end])
        assert tmp_args == (tmp_filename,
                            tmp_ticker,
                            tmp_start,
                            tmp_end)

    def test_getstockdata_default_data(self, tmp_path):
        '''
        Testing file generation with default data.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        tmp_file = tmp_path / getstockdata.DEFAULT_FILE_NAME
        getstockdata.get_stock_data(file=tmp_file,
                                    tickers_str=getstockdata.DEFAULT_TICKER_STRING,
                                    start_str=getstockdata.DEFAULT_START_DATE_STRING,
                                    end_str=getstockdata.DEFAULT_END_DATE_STRING)
        self.__print_file_info(tmp_file)
        assert os.path.exists(tmp_file) and os.path.isfile(
            tmp_file) is True, "ERROR: File was not generated"
        assert os.path.getsize(tmp_file) > 0, "ERROR: File is empty"
        os.remove(tmp_file)

    def test_getstockdata_concrete_data(self, tmp_path):
        '''
        Testing file generation with concrete data.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        tmp_file = tmp_path / getstockdata.DEFAULT_FILE_NAME
        getstockdata.get_stock_data(file=tmp_file,
                                    tickers_str="AMZN",
                                    start_str="2010-01-01",
                                    end_str="2010-12-31")
        self.__print_file_info(tmp_file)
        assert os.path.exists(tmp_file) and os.path.isfile(
            tmp_file) is True, "ERROR: File was not generated"
        assert os.path.getsize(tmp_file) > 0, "ERROR: File is empty"
        os.remove(tmp_file)

    def test_getstockdata_all_invalid_arguments(self):
        '''
        Testing file generation with all arguments invalid.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        with pytest.raises(ValueError):
            getstockdata.get_stock_data("", "", "", "")

    def test_getstockdata_invalid_filename(self):
        '''
        Testing file generation with invalid filename.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        with pytest.raises(FileNotFoundError):
            getstockdata.get_stock_data(file="",
                                        tickers_str="AMZN",
                                        start_str="2010-01-01",
                                        end_str="2010-12-31")

    def test_getstockdata_invalid_ticker(self, tmp_path):
        '''
        Testing file generation with invalid stock symbol.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        with pytest.raises(SystemExit):
            tmp_file = tmp_path / getstockdata.DEFAULT_FILE_NAME
            getstockdata.get_stock_data(file=tmp_file,
                                        tickers_str="XXXX",
                                        start_str="2010-01-01",
                                        end_str="2010-12-31")

    def test_getstockdata_invalid_start(self, tmp_path):
        '''
        Testing file generation with invalid start date.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        with pytest.raises(SystemExit):
            tmp_file = tmp_path / getstockdata.DEFAULT_FILE_NAME
            getstockdata.get_stock_data(file=tmp_file,
                                        tickers_str="AMZN",
                                        start_str="",
                                        end_str="2010-12-31")

    def test_getstockdata_invalid_end(self, tmp_path):
        '''
        Testing file generation with invalid start date.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        with pytest.raises(SystemExit):
            tmp_file = tmp_path / getstockdata.DEFAULT_FILE_NAME
            getstockdata.get_stock_data(file=tmp_file,
                                        tickers_str="AMZN",
                                        start_str="2010-01-01",
                                        end_str="")

    def test_getstockdata_invalid_dates(self, tmp_path):
        '''
        Testing file generation with start date greater than end date.

        Parameters:
        __________

        self        :   object
                        it allows accessing class properties
        tmp_path    :   string
                        it allows to access temporary path to execute tests.
                        See: https://docs.pytest.org/en/6.2.x/tmpdir.html?highlight=tmp_path
        '''
        with pytest.raises(SystemExit):
            tmp_file = tmp_path / getstockdata.DEFAULT_FILE_NAME
            getstockdata.get_stock_data(file=tmp_file,
                                        tickers_str="AMZN",
                                        start_str="2010-12-31",
                                        end_str="2010-01-01")
