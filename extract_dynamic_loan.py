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
from config import loan_dynamic
from data_dictionaries import *
from utils import load_file


def create_loan_state_table(df):
    tmp = df.copy()
    _lt = tmp[loan_dynamic]

    columns = {'LOAN_ID': 'loan_identifier',
               'ACT_PERIOD': 'portfolio_snapshot_id',
               'HIGH_LOAN_TO_VALUE_HLTV_REFINANCE_OPTION_INDICATOR': 'high_loan_to_value_refinance_option_indicator',
               'ZERO_BAL_CODE': 'zero_balance_code',
               'ZB_DATE': 'zero_balance_effective_date',
               'LAST_UPB': 'upb_at_the_time_of_removal',
               'TOT_SCHD_PRNCPL': 'total_principal_current',
               'LAST_PAID_INSTALLMENT_DATE': 'last_paid_installment_date',
               'MNTHS_TO_AMTZ_IO': 'months_to_amortization',
               'MI_CANCEL_FLAG': 'mortgage_insurance_cancellation_indicator',
               'CURR_SCHD_PRNCPL': 'scheduled_principal_current',
               'UNSCHD_PRNCPL_CURR': 'unscheduled_principal_current',
               'ZERO_BALANCE_CODE_CHANGE_DATE': 'zero_balance_code_change_date',
               'LOAN_HOLDBACK_INDICATOR': 'loan_holdback_indicator',
               'LOAN_HOLDBACK_EFFECTIVE_DATE': 'loan_holdback_effective_date',
               'INTEREST_RATE_CHANGE_DATE': 'next_interest_rate_adjustment_date',
               'PAYMENT_CHANGE_DATE': 'next_payment_change_date',
               'SERVICER': 'servicer_name',
               'CURR_RATE': 'current_interest_rate',
               'CURRENT_UPB': 'current_actual_upb',
               'LOAN_AGE': 'loan_age',
               'REM_MONTHS': 'remaining_months_to_legal_maturity',
               'ADJ_REM_MONTHS': 'remaining_months_to_maturity',
               'MATURITY_DATE': 'maturity_date',
               'SERV_IND': 'servicing_activity_indicator'}

    _lt = _lt.rename(columns=columns)
    _lt['zero_balance_code'] = _lt['zero_balance_code'].apply(lambda x: ZERO_BALANCE_DICT[x] if not pd.isna(x) else 999)
    _lt['loan_holdback_indicator'] = _lt['loan_holdback_indicator'].apply(
        lambda x: LOAN_HOLDBACK_DICT[x] if not pd.isna(x) else None)
    _lt['portfolio_snapshot_id'] = _lt['portfolio_snapshot_id'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['last_paid_installment_date'] = _lt['last_paid_installment_date'].apply(
        lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['zero_balance_code_change_date'] = _lt['zero_balance_code_change_date'].apply(
        lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['loan_holdback_effective_date'] = _lt['loan_holdback_effective_date'].apply(
        lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['next_interest_rate_adjustment_date'] = _lt['next_interest_rate_adjustment_date'].apply(
        lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['next_payment_change_date'] = _lt['next_payment_change_date'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))
    _lt['maturity_date'] = _lt['maturity_date'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))

    return _lt


if __name__ == '__main__':

    input_directory = "./PERF/"
    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    loan_states = []
    for in_file in input_files[:1]:
        input_table = load_file(in_file, column_names)
        loan_state_table = create_loan_state_table(input_table)
        print(len(loan_state_table.index))
        loan_states.append(loan_state_table)

    loans_states_all = pd.concat(loan_states)
    print(len(loans_states_all.index))
    loans_states_all.to_csv("loan_state.csv", sep='|', index=False)
