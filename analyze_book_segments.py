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

# Script used in Step 2 of the Open Risk Academy Course
# https://www.openriskacademy.com/mod/page/view.php?id=754

import os

from config import column_names
from utils import load_file

input_directory = "./PARTS/"

if __name__ == '__main__':

    # create file list
    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    # operate on file list
    for in_file in input_files:
        input_table = load_file(in_file, column_names)
        tmp1 = input_table.groupby('LOAN_ID')
        performing_groups = []
        prepaid_groups = []
        npl_groups = []
        for name, group in tmp1:
            delinquencies = set(group['DLQ_STATUS'].values)
            modifications = set(group['MOD_FLAG'].values)
            zero_balance_codes = set(group['ZERO_BAL_CODE'].values)
            if '01' not in zero_balance_codes and 'Y' not in modifications and len(delinquencies) == 1:
                performing_groups.append(group)
            elif '01' in zero_balance_codes:
                prepaid_groups.append(group)
            elif '01' not in zero_balance_codes and ('Y' in modifications or len(delinquencies) > 1):
                npl_groups.append(group)

        print('Perf: ', len(performing_groups), 'Prep: ', len(prepaid_groups), 'NPL: ', len(npl_groups), 'Tot: ',
              tmp1.ngroups, 'Check:', len(performing_groups) + len(prepaid_groups) + len(npl_groups))
