import time
from scripts.support_functions import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
    fund_with_link,
)
from brownie import (
    Lottery,
    MockV3Aggregator,
    VRFCoordinatorMock,
    accounts,
    config,
    network,
)


def deploy_contract():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_pricefeed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Lottery contract is deployed at {lottery.address}")


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_txn = lottery.startLottery({"from": account})
    starting_txn.wait(1)

    print("Lottery has been started...")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    min_value = lottery.getEntranceFee()
    print(f"To enter the lotter you need to submit a minimum of {min_value} Weis")
    user_value = input("How  many Weis do you wantto enter in the lottery? ")
    while int(user_value) < min_value:
        user_value = input(f"You have not submitted enough Weis. Try again: ")
    enter_txn = lottery.enter({"from": account, "value": user_value})
    enter_txn.wait(1)
    print(f"You have entered the lottery with {user_value} Weis")


def end_lottery():
    # We have to fund a contract with link token before we can end it
    account = get_account()
    lottery = Lottery[-1]
    fund_txn = fund_with_link(lottery.address)
    fund_txn.wait(1)
    end_txn = lottery.endLottery({"from": account})
    end_txn.wait(1)
    time.sleep(10)
    print(f"{lottery.winner()} is the winner of this lottery")


def main():
    deploy_contract()
    start_lottery()
    enter_lottery()
    end_lottery()
