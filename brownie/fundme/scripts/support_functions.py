from web3 import Web3
from brownie import MockV3Aggregator, accounts, network, config

DECIMALS = 8
STARTING_PRICE = 2000 * 10 ** 8
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    # If we are in a local blockchain or forked blockchain environment then we need to get the account from the list of generated accounts
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    # else for test network like rinkeby we need to get address from the Metamask wallet that has some Test ETHs
    elif network.show_active() == "rinkeby":
        return accounts.add(config["wallets"]["from_key"])
    # currently the script is configured to ignore every other networkk so as to prevent issues
    else:
        raise ValueError(
            "The current network is neither Rinkeby nor Development. Please re-confirm network!!"
        )


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    if len(MockV3Aggregator) <= 0:
        print("Deploying mock aggregator...")
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mock is deployed...")
    else:
        print("Mock already exists!!")
