from web3 import Web3
from brownie import (
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    accounts,
    network,
    config,
    interface,
)

DECIMALS = 8
STARTING_PRICE = 2000 * 10 ** 8
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

contract_to_mock = {
    "eth_usd_pricefeed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_account(index=None, id=None):
    # If we are in a local blockchain or forked blockchain environment then we need to get the account from the list of generated accounts
    if index:
        return accounts[index]
    elif id:
        return accounts.load(id)
    elif (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    # else for test network like rinkeby we need to get address from the Metamask wallet that has some Test ETHs
    elif network.show_active() in ["rinkeby", "kovan"]:
        return accounts.add(config["wallets"]["from_key"])
    # currently the script is configured to ignore every other networkk so as to prevent issues
    else:
        raise ValueError(
            "The current network is neither Rinkeby/Kovan nor Development. Please re-confirm network!!"
        )


def deploy_mocks():
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying MockV3Aggregator...")
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("MockV3Aggregator is deployed...")
    print("Deploying Link Token Mock contract...")
    link_token = LinkToken.deploy({"from": account})
    print("Link Token Mock contract is deployed...")
    print("Deploying VRFCoordinatorMock contract...")
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("VRFCoordinatorMock is deployed...")


def get_contract(contract_name):
    """
    This function will grab the contract addresses from brownie config if defined
    Otherwise it will deploy a mock version of the contract and return that mock contract
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of the contract
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type.name, contract_address, contract_type.abi
        )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=0.1 * 10 ** 18
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    # link_token = interface.LinkTokenInterface(link_token.address)
    fund_txn = link_token.transfer(contract_address, amount, {"from": account})
    fund_txn.wait(1)
    print("Contract has been funded with some Link tokens")
    return fund_txn
