import os
import json
from web3 import Web3
from dotenv import load_dotenv
from solcx import compile_standard, install_solc

load_dotenv()

with open ("Documents/learn_solidity/web3py/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()    

#Compile our solidity

#Read about py-solc-x documentation
install_solc("0.8.7")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evmsourceMap"]}}},
    },
    solc_version="0.8.0",
)

# Writing the entire compiled code into a json output
with open("Documents/learn_solidity/web3py/compiled_code.json","w") as file:
    json.dump(compiled_sol, file)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337 
my_address = "0xDD091E1d4984Aa555B1621f2C3B20f06e3C47662"
private_key = os.getenv("PRIVATE_KEY")

#Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Creating a transaction object
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce})

# Signing the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key = private_key)

# Sending signed transaction 
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Wait for block confirmations
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Working with the contract
# We need 1. Contract Address 2. Contract ABI
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

# There are 2 types of function calls in a contract
# Call -> simulate making a call and getting a return value
# Transact -> actually make a state change on the blockchain

# Get the initial value of the favorite number
print(simple_storage.functions.retrieve().call())

# Store a new value to favorite number; build a transaction, sign it and then send it 
store_txn = simple_storage.functions.store(15).buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce+1})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key = private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)

# Get the new value of the favorite number
print(simple_storage.functions.retrieve().call())

