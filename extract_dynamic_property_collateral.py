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
from config import property_collateral_dynamic
from utils import load_file


def create_property_collateral_state_table(df):
    _pct = df[property_collateral_dynamic]
    columns = {
        'LOAN_ID': 'loan_id',
        'ACT_PERIOD': 'portfolio_snapshot_id',
        'PROPERTY_PRESERVATION_AND_REPAIR_COSTS': 'property_preservation_and_repair_costs',
        'MISCELLANEOUS_HOLDING_EXPENSES_AND_CREDITS': 'miscellaneous_holding_expenses_and_credits',
        'ASSOCIATED_TAXES_FOR_HOLDING_PROPERTY': 'associated_taxes_for_holding_property',
        'PROPERTY_INSPECTION_WAIVER_INDICATOR': 'property_valuation_method'}
    _pct = _pct.rename(columns=columns)
    _pct['portfolio_snapshot_id'] = _pct['portfolio_snapshot_id'].apply(lambda x: pd.to_datetime(x, format="%m%Y"))
    return _pct


if __name__ == '__main__':

    input_directory = "./PERF/"

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    property_states = []
    for in_file in input_files[:1]:
        input_table = load_file(in_file, column_names)
        property_state_table = create_property_collateral_state_table(input_table)
        print(len(property_state_table.index))
        property_states.append(property_state_table)

    property_states_all = pd.concat(property_states)
    print(len(property_states_all.index))
    property_states_all.to_csv("property_collateral_state.csv", sep='|', index=False)
