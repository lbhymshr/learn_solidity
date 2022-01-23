from brownie import OurToken
from scripts.support_functions import get_account

max_tokens = 21 * 10 ** 18


def deploy_token():
    account = get_account()
    print(account)
    our_token = OurToken.deploy(max_tokens, {"from": account})
    print(our_token.name())


def main():
    deploy_token()
