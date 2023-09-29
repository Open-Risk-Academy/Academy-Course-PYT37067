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

"""
['loan_identifier', 'portfolio_snapshot_id',
       'high_loan_to_value_refinance_option_indicator', 'zero_balance_code',
       'zero_balance_effective_date', 'upb_at_the_time_of_removal',
       'total_principal_current', 'last_paid_installment_date',
       'months_to_amortization', 'mortgage_insurance_cancellation_indicator',
       'scheduled_principal_current', 'unscheduled_principal_current',
       'zero_balance_code_change_date', 'loan_holdback_indicator',
       'loan_holdback_effective_date', 'next_interest_rate_adjustment_date',
       'next_payment_change_date', 'servicer_name', 'current_interest_rate',
       'current_actual_upb', 'loan_age', 'remaining_months_to_legal_maturity',
       'remaining_months_to_maturity', 'maturity_date',
       'servicing_activity_indicator'
"""

import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    # load the loan state (variable fields)
    input_file = "loan_state.csv"
    input_table = pd.read_csv(input_file, header=0, sep='|')

    rem_mat = input_table['remaining_months_to_maturity'].squeeze()
    rem_mat.plot()
    print(type(rem_mat))
    # plt.show()
    plt.savefig("loan_maturity_all.png")
