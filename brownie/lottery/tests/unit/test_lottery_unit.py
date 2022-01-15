from scripts.deploy import deploy_contract
from scripts.support_functions import (
    get_account,
    get_contract,
    fund_with_link,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import network, exceptions
from web3 import Web3
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_contract()
    entrance_fee = lottery.getEntranceFee()
    expected_entrace_fee = Web3.toWei(0.025, "ether")

    assert entrance_fee == expected_entrace_fee


def test_enter_only_after_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_contract()
    account = get_account()
    with pytest.raises(exceptions.VirtualMachineError):
        enter_txn = lottery.enter(
            {
                "from": account,
                "value": lottery.getEntranceFee(),
                "gas_limit": 6721975,
                "allow_revert": True,
            }
        )


def test_start_enter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_contract()
    start_txn = lottery.startLottery({"from": account})
    start_txn.wait(1)
    enter_txn = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    enter_txn.wait(1)

    assert lottery.isPlayer(account)
    assert lottery.playerBalance(account) == lottery.getEntranceFee()


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_contract()
    start_txn = lottery.startLottery({"from": account})
    start_txn.wait(1)
    enter_txn = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    enter_txn.wait(1)
    fund_txn = fund_with_link(lottery.address)
    fund_txn.wait(1)
    end_txn = lottery.endLottery({"from": account})
    end_txn.wait(1)

    assert lottery.lottery_state() == 2


def test_can_pick_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    account = get_account()
    lottery = deploy_contract()
    start_txn = lottery.startLottery({"from": account})
    start_txn.wait(1)
    enter_txn = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    enter_txn.wait(1)

    # Lets enter with a few additional players
    enter_txn = lottery.enter(
        {"from": get_account(index=5), "value": lottery.getEntranceFee()}
    )
    enter_txn.wait(1)
    enter_txn = lottery.enter(
        {"from": get_account(index=2), "value": lottery.getEntranceFee()}
    )
    enter_txn.wait(1)
    enter_txn = lottery.enter(
        {"from": get_account(index=7), "value": lottery.getEntranceFee()}
    )
    enter_txn.wait(1)

    fund_txn = fund_with_link(lottery.address)
    fund_txn.wait(1)
    end_txn = lottery.endLottery({"from": account})
    end_txn.wait(1)
    requestId = end_txn.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, 776, lottery.address, {"from": account}
    )
    start_acc_balance = account.balance()
    lottery_balance = lottery.balance()

    assert lottery.winner() == account
    assert lottery.balance() == 0
    assert account.balance() == start_acc_balance + lottery_balance
