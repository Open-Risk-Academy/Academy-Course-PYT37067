# Copyright (c) 2023 Open Risk (https://www.openriskmanagement.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os

import pandas as pd

from config import column_names
from utils import create_static_table
from utils import load_file


def create_portfolio_table(df):
    _pt = pd.DataFrame(columns=['name'])
    for seller in df['SELLER'].unique():
        _pt.loc[len(_pt.index)] = [seller]
    return _pt


def create_portfolio_snapshot_table(df):
    _pst = pd.DataFrame(columns=['monthly_reporting_period'])
    for period in df['ACT_PERIOD'].unique():
        _pst.loc[len(_pst.index)] = [period]
    _pst['monthly_reporting_period'] = _pst['monthly_reporting_period'].apply(
        lambda x: pd.to_datetime(x, format="%m%Y"))
    return _pst


if __name__ == '__main__':
    input_directory = "./PARTS/"
    filename = input_directory + '2010Q2.100.part.csv'

    files = os.listdir(input_directory)

    input_table = load_file(filename, column_names)
    static_table = create_static_table(input_table)
    portfolio_snapshot_table = create_portfolio_snapshot_table(input_table)
    portfolio_snapshot_table.to_csv("portfolio_snapshot.csv", sep='|', index=False)
