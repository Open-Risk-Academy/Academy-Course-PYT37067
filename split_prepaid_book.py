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
from utils import load_file

input_directory = "./PARTS/"
output_directory = "./PREPAY/"

if __name__ == '__main__':

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]
    output_files = [output_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    i = 0
    for in_file, out_file in zip(input_files, output_files):
        if i < 10:
            input_table = load_file(in_file, column_names)
            tmp1 = input_table.groupby('LOAN_ID')
            output_groups = []
            for name, group in tmp1:
                delinquencies = set(group['DLQ_STATUS'].values)
                modifications = set(group['MOD_FLAG'].values)
                zero_balance_codes = set(group['ZERO_BAL_CODE'].values)
                if '01' in zero_balance_codes:
                    output_groups.append(group)
            print(in_file, len(output_groups))
            if len(output_groups) > 0:
                output_table = pd.concat(output_groups)
                output_table.to_csv(out_file, sep='|', index=False, header=False)
            i += 1
