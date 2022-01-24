// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.4.0 <0.9.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol"; // Solidity v6

contract FundMe {
    // using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    AggregatorV3Interface internal priceFeed;
    address public owner;

    constructor() {
        priceFeed = AggregatorV3Interface(
            0x9326BFA02ADD2366b30bacB125260Af641031331
        );

        owner = msg.sender;
    }

    modifier onlyOnwer() {
        require(msg.sender == owner, "Only owner can call this method!");
        _;
    }

    function fund() public payable {
        // Only accept a minimum of 5 USD
        uint256 minUSD = 5 * 10**18;
        require(
            getConversionRate(msg.value) >= minUSD,
            "You need to spend more ETH!"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
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

    function withdraw() public payable onlyOnwer {
        payable(msg.sender).transfer(address(this).balance);

        for (uint256 i = 0; i < funders.length; i++) {
            addressToAmountFunded[funders[i]] = 0;
        }

        funders = new address[](0);
    }
}
