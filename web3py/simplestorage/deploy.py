import os
import json
from web3 import Web3
from dotenv import load_dotenv
from solcx import compile_standard, install_solc

# Load the environment variables from .env file
load_dotenv()

# Retrieve the below fields from the env file
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_SERVER")))
chain_id = int(os.getenv("NETWORK_ID"))
my_address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")
contract_path = os.getenv("CONTRACT_PATH")
contract_name = os.getenv("CONTRACT_NAME")

# Pick the contract name from the .env file from variable CONTRACT PATH
with open (f"{contract_path}/{contract_name}.sol", "r") as file:
    contract_file = file.read()    

#Compile our solidity
# TODO - Read about py-solc-x documentation
install_solc("0.8.7")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": contract_file}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evmsourceMap"]}}},
    },
    solc_version="0.8.7",
)

# Writing the entire compiled code into a json output
with open(f"{contract_path}/compiled_code.json","w") as file:
    json.dump(compiled_sol, file)

# Get contract ByteCode from the compiled solidity contract
bytecode = compiled_sol["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["evm"]["bytecode"]["object"]

# Get the contract Application Binary Interace (ABI) from the compiled solidity contract
abi = compiled_sol["contracts"][f"{contract_name}.sol"][f"{contract_name}"]["abi"]

#Create the contract in python
loaded_contract = w3.eth.contract(abi=abi, bytecode=bytecode)

'''Now we have to deploy the contract into our selected RPC Address blockchain & Chain ID. We use the steps below to do so'''
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Creating a transaction object
transaction = loaded_contract.constructor().buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce})

# Signing the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key = private_key)

# Sending signed transaction 
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Wait for block confirmations
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
contract_receipt = {
        "blockHash": transaction_receipt.blockHash.hex(), "blockNumber":transaction_receipt.blockNumber, "gasUsed":transaction_receipt.gasUsed,
        "contractAddress": transaction_receipt.contractAddress, "cumulGasUsed":transaction_receipt.cumulativeGasUsed, "from":transaction_receipt["from"],
        "to": transaction_receipt.to, "txnHash": transaction_receipt.transactionHash.hex(), "logs": transaction_receipt.logs
        }

# Write the entire transaction receipt to a file so that it can be read from a different python code
with open(f"{contract_path}/contract_receipt.json", "w") as file:
    json.dump(contract_receipt, file)
