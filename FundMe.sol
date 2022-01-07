//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address exchangeEthToUsd = 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;

    function fund() public payable {
        // Set a minimum funding level to USD 50
        uint256 minUSDFundValue = 50*10**26;
        uint256 currentUSDFundvalue = msg.value * getPrice();

        require(currentUSDFundvalue>=minUSDFundValue, "You have not provided sufficient funds. Minimum required fund is $50. Please try again!");
        addressToAmountFunded[msg.sender] += msg.value;
        
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceVersion = AggregatorV3Interface(exchangeEthToUsd);
        return priceVersion.version();
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceVersion = AggregatorV3Interface(exchangeEthToUsd);
        (,int256 answer,,,) = priceVersion.latestRoundData();
        return uint256(answer);
    } 
}

