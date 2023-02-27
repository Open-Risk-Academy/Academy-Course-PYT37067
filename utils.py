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

import pandas as pd
from config import column_datatypes
from config import static_fields


# Set up a function to read in the Loan Performance files

def load_file(filename, col_names):
    df = pd.read_csv(filename,
                     sep="|",
                     names=col_names,
                     dtype=column_datatypes
                     )
    return df


def create_static_table(df):
    df1 = df.copy()
    df1['ACT_PERIOD_NUM'] = df1['ACT_PERIOD'].apply(
        lambda x: 12 * int(str(x)[1:5]) + int(str(x)[0:1]) if len(str(x)) == 5 else 12 * int(str(x)[2:6]) + int(
            str(x)[0:2]) if len(str(x)) == 6 else 0)
    selected_fields = static_fields.copy()
    selected_fields.append('ACT_PERIOD_NUM')
    selected_fields.append('ACT_PERIOD')
    df1 = df1[selected_fields]
    _static_table = df1.loc[df1.groupby('LOAN_ID')['ACT_PERIOD_NUM'].idxmin()]
    del selected_fields
    return _static_table
