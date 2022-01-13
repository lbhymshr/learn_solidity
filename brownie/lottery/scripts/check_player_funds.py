from brownie import Lottery, accounts
from scripts.support_functions import get_account


def enter_lottery():
    lottery = Lottery[-1]
    account = get_account()

    entrance_fee = lottery.getEntranceFee()

    print(f"You need to submit a minimum of {entrance_fee} Weis")
    fund_bal = input("How much do you want to fund (in ETH)?")
    print("Funding...")
    lottery.enter(
        {
            "from": account,
            "value": float(fund_bal) * 10 ** 18,
            "gas_limit": 6721975,
            "allow_revert": True,
        }
    )
    print(
        f"Total fund is now worth {lottery.balance()}. Thank you for your contribution!"
    )


def check_fund():
    lottery = Lottery[-1]
    account = get_account()
    print(f"Current address {account.address}")

    is_player = lottery.isPlayer(account.address)

    if is_player:
        player_bal = lottery.playerBalance(account.address)
        print(
            f"Player {account.address} is in the game and has submitted {player_bal} Weis"
        )
    else:
        print(f"Player {account.address} is not in the game currently!")


def main():
    enter_lottery()
    check_fund()
