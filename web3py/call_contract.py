'''Below code should be in another python file called contract interaction'''
# Working with the contract
# We need 1. Contract Address 2. Contract ABI

import os
import json
from web3 import Web3
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# Retrieve the below fields from the env file
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_SERVER")))
chain_id = int(os.getenv("NETWORK_ID"))
my_address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")
contract_path = os.getenv("CONTRACT_PATH")
contract_name = os.getenv("CONTRACT_NAME")

# Load the contract attributes
with open(f"{contract_path}/compiled_code.json","r") as jsonfile:
    compiled_contract = json.load(jsonfile)
with open(f"{contract_path}/contract_receipt.json", "r") as jsonfile:
    contract_receipt = json.load(jsonfile)

contractAddress = contract_receipt["contractAddress"]
contractABI = compiled_contract["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["abi"]
loaded_contract = w3.eth.contract(address=contractAddress, abi=contractABI)

'''Printing Contract Application Binary Interface'''
pretty_contractABI = json.dumps(contractABI, indent=4)
print(pretty_contractABI)

# There are 2 types of function calls in a contract
# Call -> simulate making a call and getting a return value
# Transact -> actually make a state change on the blockchain

# Get the initial value of the favorite number
print(loaded_contract.functions.retrieve().call())

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Store a new value to favorite number; build a transaction, sign it and then send it 
store_txn = loaded_contract.functions.store(15).buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key = private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)

# Get the new value of the favorite number
print(loaded_contract.functions.retrieve().call())

