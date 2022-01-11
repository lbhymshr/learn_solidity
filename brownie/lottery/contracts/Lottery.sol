//SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

contract Lottery {
    address payable[] public players;
    uint256 public usdEntryFee;

    function enter() public payable {
        // $50 min entry fee
        players.push(msg.sender);
    }

    function getEntranceFee() public {
        // What do I need to do here?
    }

    function startLottery() public {}

    function endLottery() public {}
}
