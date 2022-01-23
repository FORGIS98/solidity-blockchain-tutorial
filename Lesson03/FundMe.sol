// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.4.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;

    AggregatorV3Interface internal priceFeed;
    address owner;

    constructor() {
        priceFeed = AggregatorV3Interface(
            0x9326BFA02ADD2366b30bacB125260Af641031331
        );

        owner = msg.sender;
    }

    function fund() public payable {
        // Only accept a minimum of 5 USD
        uint256 minUSD = 5 * 10**18;
        require(
            getConversionRate(msg.value) >= minUSD,
            "You need to spend more ETH!"
        );

        addressToAmountFunded[msg.sender] += msg.value;
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    // price of ether in USD
    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        // answer has 8 decimal, we add 10 more
        // so getPrice returns value in WEIs.
        return uint256(answer * 10**10);
    }

    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 10**18;

        return ethAmountInUSD;
    }

    function withdraw() public payable {
        require(msg.sender == owner);
        msg.sender.transfer(address(this).balance);
    }
}
