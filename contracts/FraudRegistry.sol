// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract PersonalStorage {

    
    struct Note {
        string message;
        uint timestamp;
    }

    // Mapping for every user address it creates array of notes and private so no other can see your notes
    mapping(address => Note[]) private userNotes;

    // global counter for total notes
    uint public totalNotes;

    // Function to add a note and memory is used for temporary data and .sender is used for address of user
    function addNote(string memory _message) public {
        userNotes[msg.sender].push(
            Note({
                message: _message,
                timestamp: block.timestamp // blockchain time
            })
        );

        totalNotes += 1;
    }

    // Function to get all notes of the user that call it view is used because so tha data can only be read and  no changes are tolerated
    function getNotes() public view returns (Note[] memory) {
        return userNotes[msg.sender];
    }
}
