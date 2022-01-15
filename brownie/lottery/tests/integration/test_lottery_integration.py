import time
import pytest
from brownie import network
from scripts.deploy import deploy_contract
from scripts.support_functions import (
    get_account,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def test_can_pick_winner_network():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()

    lottery = deploy_contract()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})

    # Wait from randomness to respond
    time.sleep(120)

    assert lottery.winner() == account
    assert lottery.balance() == 0
