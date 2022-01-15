// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery is VRFConsumerBase, Ownable {
    AggregatorV3Interface internal priceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    mapping(address => uint256) public playerToEntryAmount;
    mapping(address => bool) public players;

    address payable[] internal playerList;
    address payable public winner;

    bytes32 public keyhash;

    uint256 public randomness;
    uint256 public minUSD;
    uint256 public fee;

    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeed,
        address _vrfCoordinatior,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinatior, _link) {
        lottery_state = LOTTERY_STATE.CLOSED;
        minUSD = 50;
        priceFeed = AggregatorV3Interface(_priceFeed);
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        /*
        Starting with v0.8 of Solidity addresses are not payable by default
        so each msg.sender needs to be typecasted into payble before being pushed
        */
        bool player_exist = isPlayer(msg.sender);
        if (!player_exist) {
            require(
                lottery_state == LOTTERY_STATE.OPEN,
                "Lottery has not started yet!!"
            );
            require(
                msg.value >= getEntranceFee(),
                "You have not submitted minimum Weis required to participate!"
            );
            playerList.push(payable(msg.sender));
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

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // Getting a real random number in a deterministic blockchain is truly impossible
        // Lets use the nonce, msg.sender, block difficulty & block.timestamp as seeds for random number generator
        // This is not a safe method
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        uint256(
            keccak256(
                abi.encodePacked(
                    tx.gasprice, // is predictable
                    msg.sender, // is knows
                    block.difficulty, //difficulty can be manipulated by the miners
                    block.timestamp // this is predictable
                )
            )
        ) % playerList.length;

        // Chainlink VRF provides provable verified random number
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    // Internal function so that only VRFCoordinator is calling this function
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Not calculating winner yet!"
        );
        require(_randomness > 0, "Random not found");
        uint256 indexOfWinner = _randomness % playerList.length;
        winner = playerList[indexOfWinner];

        payable(winner).transfer(address(this).balance);

        // Reset the lottery state to closed
        lottery_state = LOTTERY_STATE.CLOSED;

        // Reset the playerList array
        playerList = new address payable[](0);

        // Reset the mappings
        for (uint256 i = 0; i < playerList.length; i++) {
            address playerAddress = playerList[i];
            playerToEntryAmount[playerAddress] = 0;
            players[playerAddress] = false;
        }

        randomness = _randomness;
    }
}
