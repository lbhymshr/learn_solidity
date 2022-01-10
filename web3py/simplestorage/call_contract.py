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

# Get the NONCE for the wallet address
nonce = w3.eth.getTransactionCount(my_address)

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

# TODO - Write a loop that asks user to select a function from the contract ABI and asks for the arguemnts required by the function and calls that function on the contract
# There are 2 types of function calls in a contract
# Call -> simulate making a call and getting a return value
# Transact -> actually make a state change on the blockchain

print("We are now going to call the contract functions....")
user_flag = True

print(f"There are {len(contractABI)} callable functions in the contract")
idx = 0
for fxn in contractABI:
    print(f"Serial Number: {idx}"," || ",f"Function Name: {fxn['name']}", " || ", f"Function Type: {fxn['stateMutability']}")
    idx +=1
called_fxn_idx = input("Which function would you like to call? Pick a serial number from above list: ")

contract_fxn = contractABI[int(called_fxn_idx)]
print(contract_fxn)

'''
# Get the initial value of the favorite number
print(loaded_contract.functions.retrieve().call())

# Store a new value to favorite number; build a transaction, sign it and then send it 
store_txn = loaded_contract.functions.store(15).buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce})
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key = private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)

# Get the new value of the favorite number
print(loaded_contract.functions.retrieve().call())
'''
