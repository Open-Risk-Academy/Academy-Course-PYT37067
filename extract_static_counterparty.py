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
from config import counterparty_static
from data_dictionaries import *
from utils import create_static_table
from utils import load_file


def create_counterparty_table(df):
    tmp = df.copy()
    _ct = tmp[counterparty_static]
    _ct = _ct.rename(columns={'LOAN_ID': 'counterparty_id',
                              'NUM_BO': 'number_of_borrowers',
                              'CSCORE_B': 'borrower_credit_score_at_origination',
                              'CSCORE_C': 'coborrower_credit_score_at_origination',
                              'FIRST_FLAG': 'first_time_home_buyer_indicator'})
    _ct['first_time_home_buyer_indicator'] = _ct['first_time_home_buyer_indicator'].apply(lambda x: FIRST_TIME_DICT[x])
    return _ct


if __name__ == '__main__':

    input_directory = "./PERF/"

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    counterparties = []
    for in_file in input_files:
        input_table = load_file(in_file, column_names)
        static_table = create_static_table(input_table)
        del input_table
        counterparty_table = create_counterparty_table(static_table)
        del static_table
        print(len(counterparty_table.index))
        counterparties.append(counterparty_table)

    counterparty_all = pd.concat(counterparties)
    print(len(counterparty_all.index))
    counterparty_all.to_csv("DB_TABLES/counterparty.csv", sep='|', index=False)
