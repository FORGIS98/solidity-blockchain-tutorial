// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity >=0.4.0 <0.9.0;

contract SimpleStorage {
    uint256 favNumber;

    struct People {
        string name;
        uint256 favNumber;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavNumber;

    function store(uint256 _favNumber) public {
        favNumber = _favNumber;
    }

    function retrieve() public view returns (uint256) {
        return favNumber;
    }

    function add() public view returns (uint256) {
        return favNumber + 1;
    }

    function sum(uint256 _sum) public {
        favNumber = favNumber + _sum;
    }

    function addPeople(string memory _name, uint256 _favN) public {
        people.push(People(_name, _favN));
        nameToFavNumber[_name] = _favN;
    }
}
