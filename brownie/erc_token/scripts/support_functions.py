from brownie import accounts, network, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
TEST_BLOCKCHAIN_ENVIRONEMNTS = ["kovan", "rinkeby"]


def get_account(index=None, id=None):
    curr_network = network.show_active()
    if id:
        account = accounts.load(id)
    elif index:
        account = accounts[index]
    elif (
        curr_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or curr_network in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        account = accounts[0]
    elif curr_network in TEST_BLOCKCHAIN_ENVIRONEMNTS:
        account = accounts.add(config["wallets"]["from_key"])
    else:
        raise ValueError(
            "You have chosen an unconfigured network. please double check the config.yaml to configure properly!"
        )
    return account
