hashcode = '0x0e8d6b471e332f140e7d9dbb99e5e3822f728da6'
_fixed = True

root = './' + hashcode + '-fixed' if _fixed else './' + hashcode
url = 'http://127.0.0.1:8545'
input_file = root + '/' + hashcode + '-with-decoded-input.json'
transactions_csv = root + '/' + hashcode + '.csv'
contract_address = '0xa34195Fc14F177660C60ff23fC34347acB2f11Cf'
