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
from config import loan_static
from data_dictionaries import *
from utils import create_static_table
from utils import load_file


def create_loan_table(df):
    tmp = df.copy()
    _lt = tmp[loan_static]
    columns = {'LOAN_ID': 'loan_identifier',
               'ACT_PERIOD': 'portfolio_snapshot_id',
               'SELLER': 'portfolio_id',
               'CHANNEL': 'channel',
               'ORIG_RATE': 'original_interest_rate',
               'ORIG_UPB': 'original_upb',
               'ORIG_TERM': 'original_loan_term',
               'ORIG_DATE': 'origination_date',
               'FIRST_PAY': 'first_payment_date',
               'OLTV': 'original_loan_to_value_ratio',
               'OCLTV': 'original_combined_loan_to_value_ratio',
               'PURPOSE': 'loan_purpose',
               'PRODUCT': 'amortization_type',
               'RELOCATION_MORTGAGE_INDICATOR': 'relocation_mortgage_indicator',
               'HIGH_BALANCE_LOAN_INDICATOR': 'high_balance_loan_indicator',
               'MI_PCT': 'mortgage_insurance_percentage',
               'MI_TYPE': 'mortgage_insurance_type',
               'PPMT_FLAG': 'prepayment_penalty_indicator',
               'IO': 'interest_only_loan_indicator'}

    _lt = _lt.rename(columns=columns)
    _lt['channel'] = _lt['channel'].apply(lambda x: CHANNEL_DICT[x])
    _lt['origination_date'] = _lt['origination_date'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['first_payment_date'] = _lt['first_payment_date'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['loan_purpose'] = _lt['loan_purpose'].apply(lambda x: LOAN_PURPOSE_DICT[x])
    _lt['mortgage_insurance_type'] = _lt['mortgage_insurance_type'].apply(
        lambda x: MORTGAGE_INSURANCE_DICT[x] if not pd.isna(x) else 0)
    _lt['amortization_type'] = _lt['amortization_type'].apply(lambda x: AMORTIZATION_DICT[x])

    return _lt


if __name__ == '__main__':

    input_directory = "./PERF/"

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    loans = []
    for in_file in input_files:
        input_table = load_file(in_file, column_names)
        static_table = create_static_table(input_table)
        del input_table
        loan_table = create_loan_table(static_table)
        del static_table
        print(len(loan_table.index))
        loans.append(loan_table)

    loans_all = pd.concat(loans)
    print(len(loans_all.index))
    loans_all.to_csv("DB_TABLES/loan.csv", sep='|', index=False)
