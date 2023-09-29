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
    counterparty_all.to_csv("counterparty.csv", sep='|', index=False)
