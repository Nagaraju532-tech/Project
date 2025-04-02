pragma solidity >= 0.8.11 <= 0.8.11;

contract BlockAccessWLAN {
    string public mine_transaction;
    
       
   
    function setTransaction(string memory mt) public {
       mine_transaction =mt;	
    }

    function getTransaction() public view returns (string memory) {
        return mine_transaction;
    }

    constructor() public {
        mine_transaction="";
    }
}