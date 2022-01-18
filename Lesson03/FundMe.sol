// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.4.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable {
        addressToAmountFunded[msg.sender] += msg.value;
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            address(0x9326BFA02ADD2366b30bacB125260Af641031331)
        );
    }
}
