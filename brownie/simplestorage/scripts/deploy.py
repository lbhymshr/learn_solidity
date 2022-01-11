import os
from brownie import accounts, network, config, SimpleStorage

def deploy_contract():
    account = get_account()

    simple_storage = SimpleStorage.deploy({"from": account})
    print(f"Contract deployment details:\n {simple_storage}")

    stored_value = simple_storage.retrieve()
    print(f"Favorite Number: {stored_value}")

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    print("Favorite Number is updated")

    stored_value = simple_storage.retrieve()
    print(f"Favorite Number: {stored_value}")

def get_account():
    if (network.show_active() == "development"):
        return accounts[0]
    elif (network.show_active() == "rinkeby"):
        return accounts.add(config["wallets"]["from_key"])
    else:
        raise ValueError("The current network is neither Rinkeby nor Development. Please re-confirm network!!")

def main():
    deploy_contract()
