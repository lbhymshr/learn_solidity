from brownie import FundMe, accounts
from scripts.support_functions import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.viewMinimumWei()
    current_price = fund_me.getPriceData()
    print(f"Current price is {current_price/10**18} ETH per USD")
    print(f"You need to submit a minimum of {entrance_fee} Weis")
    fund_bal = input("How much do you want to fund (in ETH)?")
    print("Funding...")
    fund_me.fund(
        {
            "from": account,
            "value": float(fund_bal) * 10 ** 18,
            "gas_limit": 6721975,
            "allow_revert": True,
        }
    )
    print(
        f"Total fund is now worth {fund_me.balance()}. Thank you for your contribution!"
    )


def withdraw():
    withdraw = FundMe[-1]
    account = get_account()
    print(f"Existing balance in the fund is {withdraw.balance()} Weis")
    withdraw_bal = input("How much do you want to withdraw? (in Weis)")
    withdraw.withdrawFundToOwner(
        withdraw_bal, {"from": account, "gas_limit": 6721975, "allow_revert": True}
    )
    print(f"We have now {withdraw.balance()} Weis in the fund")


def main():
    fund()
    withdraw()
