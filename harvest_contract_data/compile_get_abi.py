'''
This file will compile origional source sol file to get ABI information, which is necessary for decode transaction
input data from etherscan
'''
import subprocess
import re
import os
import ntpath
import getopt, sys
import argparse


def get_compiler_version(sol_file_path):
    if sol_file_path.endswith("sol") is False:
        raise Exception("The input file is not a sol file")
    with open(sol_file_path, 'r') as src_file:
        lines = src_file.readlines()

    re_patten = "pragma solidity .*;"
    version = ""
    for l in lines:
        solc_version = re.findall(re_patten, l)
        if len(solc_version) > 0:
            version = solc_version[0].split(" ")[2]
            if version[0].isdigit() is False:
                version = version[1:len(version)-1]
            break

    if version == "":
        version = "0.4.26"       # Can not find version specified in sol file, use solc 0.4.26 as default version
    return version


def compile_sol_file_get_abi(sol_file_path, output_path, hash):
    head, tail = ntpath.split(sol_file_path)
    abi_tail = hash + "-abi.json"
    solc_version = get_compiler_version(sol_file_path)
    subprocess.run(['solc-select', 'use', solc_version])
    abi_file_path = os.path.join(output_path, abi_tail)
    abi_file_obj = open(abi_file_path, 'w+')
    subprocess.run(['solc', '--abi', sol_file_path], stdout=abi_file_obj)
    abi_file_obj.close()


def compile_sol_file_get_binary(sol_file_path, output_path, hash):
    head, tail = ntpath.split(sol_file_path)
    binary_tail = hash + "-binary.txt"
    solc_version = get_compiler_version(sol_file_path)
    subprocess.run(['solc-select', 'use', solc_version])
    binary_file_path = os.path.join(output_path, binary_tail)
    binary_file_obj = open(binary_file_path, 'w+')
    subprocess.run(['solc', '--bin', sol_file_path], stdout=binary_file_obj)
    binary_file_obj.close()


# args: sol_file_path, output_file, hash
if __name__ == "__main__":
    argumentList = sys.argv[1:]
    path = '/home/alex/Desktop/real_contracts_dataset_for_repair/DAO/0x2eae96e6bf99565c9d8ce978b24c3fc3b552dc7b.sol'
    compile_sol_file_get_binary(argumentList[0], argumentList[1], argumentList[2])
    compile_sol_file_get_abi(argumentList[0], argumentList[1], argumentList[2])
