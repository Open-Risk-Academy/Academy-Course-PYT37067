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
from config import property_collateral_static
from data_dictionaries import *
from utils import create_static_table
from utils import load_file


def create_property_collateral_table(df):
    _pct = df[property_collateral_static]
    columns = {
        'LOAN_ID': 'loan_id',
        'PROP': 'property_type',
        'NO_UNITS': 'number_of_units',
        'OCC_STAT': 'occupancy_status',
        'STATE': 'property_state',
        'MSA': 'metropolitan_statistical_area',
        'ZIP': 'zip_code_short'}
    _pct = _pct.rename(columns=columns)
    _pct['property_type'] = _pct['property_type'].apply(lambda x: PROPERTY_DICT[x])
    _pct['occupancy_status'] = _pct['occupancy_status'].apply(lambda x: OCCUPANCY_DICT[x])
    return _pct


if __name__ == '__main__':

    input_directory = "./PERF/"

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    properties = []
    for in_file in input_files:
        input_table = load_file(in_file, column_names)
        static_table = create_static_table(input_table)
        del input_table
        property_table = create_property_collateral_table(static_table)
        del static_table
        print(len(property_table.index))
        properties.append(property_table)

    properties_all = pd.concat(properties)
    print(len(properties_all.index))
    properties_all.to_csv("property_collateral.csv", sep='|', index=False)
