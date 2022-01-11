from brownie import SimpleStorage, accounts, config

def read_contract():
    print(SimpleStorage)
    print(f"Contract deployed at : {SimpleStorage[0]}")

    simple_storage = SimpleStorage[-1] # -1 for the most recent deployment
    # Get Application Binary Interface
    stored_value = simple_storage.retrieve()
    print(stored_value)
    pass

def main():
    read_contract()
