import getopt, sys
import subprocess as sb
import ntpath
import multiprocessing as mp



#args: hash, csv_file_path, sol_file_path, output_file
if __name__ == "__main__":
   argumentList = sys.argv[1:]
   
   hash = argumentList[0]
   csv_file_path = argumentList[1]
   sol_file_path = argumentList[2]
   output_file = argumentList[3]

   str1 = 'python3 compile_get_abi.py ' + sol_file_path + ' ' + output_file + ' ' + hash

   sb.run(str1, shell=True)

   abi_file = output_file + hash + '-abi.json'
   binary_file = output_file + hash + '-binary.txt'

   str2 = 'python3 collect-transact-input.py ' + csv_file_path + ' ' + output_file + ' ' + hash

   sb.run(str2, shell=True)

   input_raw_file = output_file + hash + '-input-raw.json'

   str3 = 'python3 find_deployed_abi.py ' + hash + ' ' + input_raw_file + ' ' + abi_file + ' ' + binary_file + ' ' + csv_file_path + ' ' + output_file
   
   sb.run(str3, shell=True)

   raw_transaction_input = output_file + hash + '-raw-transaction-with-abi.json'

   str4 = 'node javascripts/DecodeInput.js ' + hash + ' ' + raw_transaction_input + ' ' + output_file

   sb.run(str4, shell=True)
