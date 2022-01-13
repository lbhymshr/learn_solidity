//SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    mapping(address => uint256) public playerToEntryAmount;
    mapping(address => bool) public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface public priceFeed;
    uint256 public minUSD = 50;
    address public owner;

    constructor(address _priceFeed) {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function enter() public payable {
        /*
        Starting with v0.8 of Solidity addresses are not payable by default
        so each msg.sender needs to be typecasted into payble before being pushed
        */
        bool player_exist = isPlayer(msg.sender);
        if (!player_exist) {
            require(
                msg.value >= getEntranceFee(),
                "You have not submitted minimum Weis required to participate!"
            );
            players[msg.sender] = true;
        }
        playerToEntryAmount[msg.sender] += msg.value;
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        uint256 priceData = uint256(answer) * 10**10;
        return ((minUSD * 10**36) / priceData);
    }

    function isPlayer(address _playeraddress) public view returns (bool) {
        bool player_exist = false;
        if (players[_playeraddress]) {
            player_exist = true;
        }
        return player_exist;
    }

    function playerBalance(address _playeraddress)
        public
        view
        returns (uint256)
    {
        // First check if player exists
        bool player_exists = isPlayer(_playeraddress);
        if (player_exists) {
            return playerToEntryAmount[_playeraddress];
        } else {
            return 0;
        }
    }

    function getPriceData() public view returns (uint256) {}

    function startLottery() public {}

    function endLottery() public {}
}
