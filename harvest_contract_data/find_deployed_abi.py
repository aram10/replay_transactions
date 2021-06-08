#This file will find the abi according to the contract-creation transaction's input field
import json
import os
import pandas
from difflib import SequenceMatcher
import ntpath
import sys

def find_correct_abi_according_to_creation(hash, raw_transaction_input, abi_file, binary_file, csv_record, output_file):
    """
    :param raw_transaction_input:
    :param abi_file:
    :param binary_file:
    :param hash:
    :param output_file:
    :return: the abi corresponding to the deployment
    """
    creation_input = ""
    with open(raw_transaction_input, 'r') as src_file:
        input_obj = json.load(src_file)
        hashes = input_obj['transactions']
        for k in hashes:
            creation_input = hashes[k]
            break

    if creation_input == "":
        raise Exception("Input of creation transaction is missing!")

    abi_file_obj = open(abi_file, 'r')
    contract_to_abi = process_abi_file_obj(abi_file_obj)
    abi_file_obj.close()

    binary_file_obj = open(binary_file, 'r')
    contract_to_binary = process_binary_file_obj(binary_file_obj)
    binary_file_obj.close()

    max = 0.0
    corresponding_contract = ""
    for k in contract_to_binary:
        score = SequenceMatcher(None, contract_to_binary[k], creation_input).ratio()
        if score >= max:
            max = score
            corresponding_contract = k
    
    name = hash + "-raw-transaction-with-abi.json"
    file_name = os.path.join(output_file, name)

    interact_addresses = collect_address_from_transaction_csv(csv_record)

    with open(raw_transaction_input, 'r') as src_file:
        with (open(file_name, 'w')) as dst_file:
            json_obj = json.load(src_file)
            json_obj['contract'] = corresponding_contract
            json_obj['abi'] = contract_to_abi[corresponding_contract]
            json_obj['from'] = list(interact_addresses[0])
            json_obj['to'] = list(interact_addresses[1])
            json.dump(json_obj, dst_file)
    print("Output abi and transaction to " + file_name)




def process_abi_file_obj(abi_file_obj):
    '''
    :param abi_file_obj:
    :return: a dictonary: key is contract name, value is abi
    '''
    res = dict()
    lines = abi_file_obj.readlines()
    for i in range(len(lines)):
        cur_line = lines[i]
        if cur_line.startswith("==="):
            contract_name = cur_line.split(":")[1]
            contract_name = contract_name.split(" ")[0]
            res[contract_name] = lines[i+2]
    return res


def process_binary_file_obj(binary_file_obj):
    res = dict()
    lines = binary_file_obj.readlines()
    for i in range(len(lines)):
        cur_line = lines[i]
        if cur_line.startswith("==="):
            contract_name = cur_line.split(":")[1]
            contract_name = contract_name.split(" ")[0]
            res[contract_name] = lines[i+2]
    return res


def collect_address_from_transaction_csv(csv_file):
    if csv_file.endswith("csv") is False:
        raise Exception("The input is not a csv file")

    transaction_obj = pandas.read_csv(csv_file, index_col=False)
    from_set = set()
    to_set = set()
    from_addresses = transaction_obj['From']
    to_addresses = transaction_obj['To'].dropna()

    for a in from_addresses:
        from_set.add(a)

    for a in to_addresses:
        to_set.add(a)

    return (from_set, to_set)

#args: hash, input_raw_json, abi, binary, csv, output_file
if __name__ == "__main__":
    argumentList = sys.argv[1:]
    
    hash = argumentList[0]
    transaction_input = argumentList[1]
    abi_file = argumentList[2]
    binary_file = argumentList[3]
    csv_record = argumentList[4]
    output_file = argumentList[5]
    find_correct_abi_according_to_creation(hash,transaction_input,abi_file, binary_file, csv_record, output_file)

