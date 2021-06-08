1. Download the CSV file from Etherscan.io, remove 'export-' from the beginning of the file name.
2. Run `harvest_contract_data.py` with args hash, csv_file_path, sol_file_path, output_file
3. Change `hashcode` in `config.py` to match the hash of the contract you are working on
4. Change `_fixed` in `config.py` based on if you are doing the original contract or fixed version
5. Create a folder in your root directory with the same name as the hash, append '-fixed' if it is the fixed version
6. Put the transactions csv from Etherscan and the decoded input json from `harvest_contract_data.py` into the folder
7. Run `start-ganache.py`, check to make sure `addresses.pickle` is in the folder
8. Run `mappings.py`, check to make sure `mapping.pickle`, `mapping.csv` are in the folder
9. Check the decoded input json for the contract name, find the corresponding solidity file, and take note of any constructor arguments
10. If need be, use addresses from Ganache as input parameters in the migrations files
11. Migrate contracts to blockchain with `truffle migrate`
12. Find the 'contract' field in the decoded input json, and change the 'contract_address' field in `config.py` to match the address that Truffle assigned to this contract
13. Run `execute_transactions.py`
