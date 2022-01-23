// SPDX-License-Identifier: MIT
// contracts/OurToken.sol
pragma solidity >=0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OurToken is ERC20 {
    constructor(uint256 initialSupply) public ERC20("OurToken", "OTKN") {
        _mint(msg.sender, initialSupply);
    }
}

// Deploy this on a test net
