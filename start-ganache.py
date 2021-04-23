from web3 import Web3, HTTPProvider
import subprocess
import os
import json
import pickle
import config

def get_web3(url_string):
    return Web3(HTTPProvider(url_string))


def get_accounts_appeared_in_transaction_history(input_json):
    with (open(input_json, 'r')) as src_file:
        json_obj = json.load(src_file)

    from_addresses = set(json_obj['from'])
    to_addresses = set(json_obj['to'])
    addresses = set(from_addresses)
    

    transactions = list(json_obj["transactions"])

    for transaction in transactions:
        for entry in transaction.values():
            if(entry != "None"):
                for subentry in entry["params"]:
                    if subentry['type'] == 'address' and subentry['value'] not in addresses:
                        addresses.add(subentry['value'])
                    elif subentry['type'] == 'address[]':
                        for address in subentry['value']:
                            if address not in addresses:
                                addresses.add(address)


    addresses = addresses.union(to_addresses)
    with open(config.root + "/addresses.pickle", 'wb') as handle:
            pickle.dump(addresses, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return (from_addresses, to_addresses, addresses)


def start_ganache_with_given_number_addresses(addresses_set):
    subprocess.run(['ganache-cli', '-a', str(len(addresses_set)), '-e', '15000'])

if __name__ == "__main__":
    res = get_accounts_appeared_in_transaction_history(config.input_file)
    start_ganache_with_given_number_addresses(res[2])


