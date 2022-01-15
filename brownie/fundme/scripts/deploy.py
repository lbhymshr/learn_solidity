from scripts.support_functions import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    deploy_mocks,
)
from brownie import FundMe, MockV3Aggregator, accounts, config, network


def deploy_contract():
    account = get_account()
    # If we are not on a local blockchain then we need to pass the actual ETH to USD price feed address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        eth_usd = config["networks"][network.show_active()]["eth_usd_pricefeed"]
    # else we deploy the Mock Aggregator for the local blockchains
    else:
        deploy_mocks()
        eth_usd = MockV3Aggregator[-1].address
    fundme = FundMe.deploy(
        eth_usd,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"The contract is deployed at {fundme.address}")

    print(f"The current price is {fundme.getPriceData()}")
    return fundme


def main():
    deploy_contract()
