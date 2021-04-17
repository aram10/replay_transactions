1. Change `hashcode` in `config.py` to match the hash of the contract you are working on
2. Change `_fixed` in `config.py` based on if you are doing the original contract or fixed version
3. Create a folder in your root directory with the same name as the hash, append '-fixed' if it is the fixed version
4. Put the transactions csv and the decoded input json into the folder
5. Run `python3 start-ganache.py`, check to make sure `addresses.pickle` is in the folder
6. Run `python3 mappings.py`, check to make sure `mapping.pickle`, `mapping.csv` are in the folder
7. Migrate contracts to blockchain with `truffle migrate`
8. Find the 'contract' field in the decoded input json, and change the 'contract_address' field in `config.py` to match the address that Truffle assigned to this contract
9. Run `python3 execute_transactions.py`
