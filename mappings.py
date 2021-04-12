from web3 import Web3, HTTPProvider
import subprocess
import os
import json
import csv
import config
import pickle

def get_web3(url_string):
    return Web3(HTTPProvider(url_string))


def get_accounts_appeared_in_transaction_history(input_json):
    with (open(input_json, 'r')) as src_file:
        json_obj = json.load(src_file)

    from_addresses = set(json_obj['from'])
    to_addresses = set(json_obj['to'])
    addresses = set(from_addresses)
    addresses = addresses.union(to_addresses)
    return (from_addresses, to_addresses, addresses)

def create_account_mapping(address_from_transaction, address_from_ganache):
    res = dict()
    if len(address_from_transaction) != len(address_from_ganache):
        raise Exception("The account number is not same. Can not create mapping.")

    for i in range(len(address_from_transaction)):
        res[address_from_transaction[i]] = address_from_ganache[i]

    return res


if __name__ == "__main__":
    res = pickle.load(open("addresses.pickle", "rb"))
    web3 = get_web3(config.url)
    accounts = web3.eth.get_accounts()
    mapping = create_account_mapping(list(res), accounts)

    csv_file = 'mapping.csv'
    pickle_file = 'mapping.pickle'
    
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for key, value in mapping.items():
                writer.writerow([key, value])
        with open(pickle_file, 'wb') as handle:
            pickle.dump(mapping, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except IOError:
        print("I/O error")

