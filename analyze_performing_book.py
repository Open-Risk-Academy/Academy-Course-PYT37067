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
import re

from config import column_names, static_fields
from utils import load_file


def tokenize(input_name):
    tmp1 = re.sub(r"[^\w\s]|_", "", input_name)
    tmp2 = tmp1.lower()
    tmp3 = " ".join(tmp2.split())
    return tmp3


messy = ['ORIG_DATE', 'FIRST_PAY', 'OCLTV']

if __name__ == '__main__':

    input_directory = "./PERF/"

    files = os.listdir(input_directory)
    input_files = [input_directory + f for f in files if os.path.isfile(input_directory + '/' + f)]

    for in_file in input_files:
        changing_fields = []
        input_table = load_file(in_file, column_names)
        input_table['SELLER'] = input_table['SELLER'].apply(lambda x: tokenize(x))
        tmp1 = input_table.groupby('LOAN_ID')
        output_groups = []
        for name, group in tmp1:
            # fill in nan's with zero
            group.fillna(0, inplace=True)

            for field in static_fields:
                variability = len(set(group[field].values))
                if variability == 1:
                    pass
                else:
                    changing_fields.append(field)
                    if field in messy:
                        print(field, set(group[field].values))
