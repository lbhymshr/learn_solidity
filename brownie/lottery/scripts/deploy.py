from scripts.support_functions import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    deploy_mocks,
)
from brownie import Lottery, MockV3Aggregator, accounts, config, network


def deploy_contract():
    account = get_account()
    # If we are not on a local blockchain then we need to pass the actual ETH to USD price feed address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        eth_usd = config["networks"][network.show_active()]["eth_usd_pricefeed"]
    # else we deploy the Mock Aggregator for the local blockchains
    else:
        deploy_mocks()
        eth_usd = MockV3Aggregator[-1].address
    lottery = Lottery.deploy(
        eth_usd,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"The contract is deployed at {lottery.address}")
    return lottery


def main():
    deploy_contract()