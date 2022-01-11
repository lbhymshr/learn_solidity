import os
import pytest
from scripts.deploy import deploy_contract
from scripts.support_functions import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network, accounts, exceptions


def test_onlyowner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("This test is only for local testing")
    # Arrange
    account = get_account()
    fund_me = deploy_contract()
    bad_actor = accounts[7]
    fund_bal = fund_me.viewMinimumWei()
    txn_fund = fund_me.fund({"from": bad_actor, "value": fund_bal})
    txn_fund.wait(1)

    # Act & Assert
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdrawFundToOwner(
            fund_bal, {"from": bad_actor, "gas_limit": 6721975, "allow_revert": True}
        )


def test_fund_withdraw():
    # Arrange
    account = get_account()
    fund_me = deploy_contract()
    fund_bal = 0.025 * 10 ** 18

    # Act on Fund
    print(f"Current account with address {account.address} balance {account.balance()}")
    print(f"Calling Fund with {fund_bal} Weis")
    txn_fund = fund_me.fund({"from": account, "value": fund_bal, "gas_limit": 6721975})
    txn_fund.wait(1)

    # Assert
    assert fund_me.addressToAmountFunded(account.address) == fund_bal

    # Act on Withdraw
    txn_withdraw = fund_me.withdrawFundToOwner(
        fund_bal, {"from": account, "gas_limit": 6721975, "allow_revert": True}
    )
    txn_withdraw.wait(1)

    assert fund_me.addressToAmountFunded(account.address) == 0
