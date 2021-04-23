from web3 import Web3, HTTPProvider
import json
import config
import pandas as pd
import pickle
from web3 import exceptions




def get_web3(url_string):
    return Web3(HTTPProvider(url_string))

def isAddressList(add_list):
    if not isinstance(add_list, list):
        return False
    for add in add_list:
        if not web3.isAddress(add):
            return False
    return True

if __name__ == "__main__":

    with open(config.input_file) as f:
        data = json.load(f)

    #web3
    web3 = get_web3(config.url)
    web3.eth.defaultAccount = web3.eth.accounts[0]
    
    #contract
    address = web3.toChecksumAddress(config.contract_address)
    abi = data['abi']
    contract = web3.eth.contract(address, abi=abi)

    df = pd.read_csv(config.transactions_csv, index_col=False)

    with open(config.root + '/mapping.pickle', 'rb') as handle:
        mapping = pickle.load(handle)

    transactions = data['transactions']

    transaction_list = []
    transaction_list_error = []

    for transaction in transactions:
        key = list(transaction.keys())[0]
        if transaction.get(key) == "None":
            #skip contract creation
            if pd.isnull(df.loc[df['Txhash'] == key]['To'].values[0]):
                continue
            ether = df.loc[df['Txhash'] == key]['Value_IN(ETH)'].values[0]
            wei = web3.toWei(ether, "ether")
            from_add_original = df.loc[df['Txhash'] == key]['From'].values[0]
            to_add_original = df.loc[df['Txhash'] == key]['To'].values[0]
            from_add = web3.toChecksumAddress(mapping.get(from_add_original))
            to_add = web3.toChecksumAddress(mapping.get(to_add_original))
            try:
                tx_hash = web3.eth.sendTransaction({'from': from_add, 'to': to_add, 'value': wei})
                tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                trans = ['Send Ether', from_add_original, to_add_original, wei, tx_hash, tx_receipt]
                transaction_list.append(trans)
            except Exception as error:
                trans = ['Send Ether', from_add_original, to_add_original, wei, 'error', error]
                transaction_list_error.append(trans) 
        elif transaction.get(key).get('name') != 'init':
            func_name = transaction.get(key).get('name')
            func_params = transaction.get(key).get('params')
            params_list = []
            for val in func_params:
                param = val['value']
                if isAddressList(param):
                    adds = []
                    for add in param:
                        print(add)
                        print(mapping.get(add))
                        newadd = web3.toChecksumAddress(mapping.get(add))
                        print(newadd)
                        adds.append(newadd)
                    params_list.append(adds)
                    continue
                if web3.isAddress(param):
                    param = web3.toChecksumAddress(mapping.get(param))
                if val['type'].startswith('uint'):
                    param = int(param)
                params_list.append(param)
            encoded = contract.encodeABI(fn_name=func_name, args=params_list)
            try:
                tx_hash = web3.eth.sendTransaction({'to': address, 'data': encoded})
                tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
                trans = ['Contract Function', key, func_name, func_params, encoded, tx_hash, tx_receipt]
                transaction_list.append(trans)
            except Exception as error:
                trans = ['Contract Function', key, func_name, func_params, encoded, 'error', error]
                transaction_list_error.append(trans)
        else:
            continue

    with open(config.root + '/transactions.pickle', 'wb') as handle:
            pickle.dump(transaction_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(config.root + '/transactions_error.pickle', 'wb') as handle:
            pickle.dump(transaction_list_error, handle, protocol=pickle.HIGHEST_PROTOCOL)