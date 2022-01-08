import os
from solcx import compile_standard

with open ("Documents/learn_solidity/web3py/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)

#Compile our solidity

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SimpleStorage.sol":
        {"content": simple_storage_file}
        },
    "settings": {"outputSelection":
        {"*": {"*": ["abi", "metadata", "evm.bytecode", "evmsourceMap"]}}
        },
    })
    
