//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    // Create a function to transfer funds into the contract
    // The fund should not be less than USD50
    // Create a mapping to hold the amount of fund recieved from each account
    // A constructor to set Owner account
    // A function to withdraw selected amount of the funds into the contract owner account
 
    mapping (address => uint256) public addressToAmountFunded;
    address rinkebyETHtoUSD = 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;
    address public owner;
    address[] public fundProviders;

    constructor () {
        owner = msg.sender;
    }

    function max(uint256 a, uint256 b) public pure returns(uint256) {
        uint256 maxval;
        if (a>b) {maxval = a;}
        else {maxval = b;}
        return maxval;
    }

    function fund() public payable {
        // This function should be enough to recieve funds
        uint256 minFund = 50 * 10**26;
        require(msg.value * getPriceData() >= minFund, "Below minimum fund! Try with more weis...");
        addressToAmountFunded[msg.sender] += msg.value;
        fundProviders.push(msg.sender);
    }

    function getPriceData() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(rinkebyETHtoUSD);
        (, int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer);
    }

    function getContractBalance() public view returns(uint256) {
        return address(this).balance;
    }

    modifier onlyOwner {
        require(msg.sender == owner,
        "Only owner is allowed to execute this function! If you are the owner, please use the owner address");
        _;
    }

    function withdrawFundToOwner(uint256 _withdrawbal) payable onlyOwner public {
        require(_withdrawbal <= getContractBalance(),
        "The contract doesn't have this much balance, try a lower amount");
        payable(msg.sender).transfer(_withdrawbal);
        uint256 deduction = _withdrawbal/fundProviders.length;
        for(uint256 i=0; i<fundProviders.length; i++) {
            address funder = fundProviders[i];
            uint256 currFunderBalance = addressToAmountFunded[funder];
            addressToAmountFunded[funder] = max(0, currFunderBalance-deduction);
        }
        if (getContractBalance()==0) {
            fundProviders = new address[](0);
        }
    }
}
