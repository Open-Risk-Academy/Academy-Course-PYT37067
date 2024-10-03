# Copyright (c) 2023 - 2024 Open Risk (https://www.openriskmanagement.com)
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

# Script used in Step 3 of the Open Risk Academy Course
# https://www.openriskacademy.com/mod/page/view.php?id=754

import os

import pandas as pd

from config import column_names
from config import counterparty_dynamic
from utils import load_file


def create_counterparty_state_table(df):
    tmp = df.copy()
    _ct = tmp[counterparty_dynamic]
    _ct = _ct.rename(columns={'LOAN_ID': 'counterparty_id',
                              'ACT_PERIOD': 'portfolio_snapshot_id',
                              'CURR_SCOREB': 'borrower_credit_score_current',
                              'CURR_SCOREC': 'coborrower_credit_score_current'})
    _ct['portfolio_snapshot_id'] = _ct['portfolio_snapshot_id'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))
    return _ct


if __name__ == '__main__':

    input_directory = "./PERF/"
    acquisition_year = '2010'
    acquisition_qtr = 'Q2'

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    counterparty_states = []
    for in_file in input_files[:10]:
        input_table = load_file(in_file, column_names)
        counterparty_state_table = create_counterparty_state_table(input_table)
        print(len(counterparty_state_table.index))
        counterparty_states.append(counterparty_state_table)

    counterparty_state_all = pd.concat(counterparty_states)
    print(len(counterparty_state_all.index))
    counterparty_state_all.to_csv("DB_TABLES/counterparty_state.csv", sep='|', index=False)
