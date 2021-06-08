import pandas as pd
import json
from web3 import Web3
import ntpath
import os
import sys

WEB3_API_ENDPOINT = "https://api.archivenode.io/y6udo9856kjlliyfy6udo938hrmja53n"

def get_transaction_input_for_contract(csv_file_transaction_history, output_file, hash):
    '''
    :param csv_file_transaction_history, output_file:
    :return: a json file contains raw transaction input from etherscan
    '''
    if csv_file_transaction_history.endswith("csv") is False:
        raise Exception("The input file is not csv format")

    csv_record = pd.read_csv(csv_file_transaction_history, index_col=False)
    web3 = Web3(Web3.HTTPProvider(WEB3_API_ENDPOINT, request_kwargs={'timeout': 60}))
    transaction_hashes = csv_record['Txhash']

    dict_res = dict()
    dict_res['transactions'] = dict()

    for txh in transaction_hashes:
        transaction_detail = web3.eth.get_transaction(txh)
        dict_res['transactions'][txh] = transaction_detail['input']

    name = hash + "-input-raw.json"
    res_path = os.path.join(output_file, name)
    print(res_path)
    with open(res_path, 'w+') as dst_file:
        json.dump(dict_res, dst_file)


#args: csv_file_path, output_file, hash
if __name__ == '__main__':
    argumentList = sys.argv[1:]
    csv = argumentList[0]
    output_file = argumentList[1]
    hash = argumentList[2]
    get_transaction_input_for_contract(csv, output_file, hash)
    
    
