



# PersonalStorage Smart Contract(assignment 3)

## Overview

PersonalStorage is a Solidity smart contract that allows users to securely store and retrieve their personal notes on the blockchain.
Each user can add multiple notes, and only the owner of the notes can view them. This contract demonstrates basic Solidity concepts such as structs, mappings, and user-specific data storage.



## Contract Details

* Language: Solidity
* Compiler Version: ^0.8.19
* License: MIT
* Type: Decentralized personal note storage


## What This Contract Does

* Allows users to add personal notes
* Stores notes separately for each wallet address
* Ensures that users can only access their own notes
* Keeps a global count of all notes added to the contract



## Data Structures Used

### Note Struct

The `Note` struct is used to store individual notes.
Each note contains:

* A message (string)
* A timestamp representing when the note was created on the blockchain



### User Notes Mapping

A mapping is used to associate each user’s wallet address with an array of notes.

* Each address has its own list of notes
* The mapping is marked as private to prevent other users from accessing someone else’s data
* This ensures privacy and data isolation



## Global Variable

* `totalNotes` stores the total number of notes added by all users
* It is declared public so anyone can view the total count

---

## Functions Explanation

### addNote

This function allows a user to add a new note.

* Uses `msg.sender` to identify the user
* Stores the note message along with the current blockchain timestamp
* Adds the note to the user’s personal note list
* Increments the global note counter



### getNotes

This function allows users to retrieve their own notes.

* Marked as a view function, so it does not modify blockchain data
* Returns only the notes of the caller
* Ensures users cannot read notes created by others



## Privacy and Security

* Notes are stored per user address
* Other users cannot view or access your notes
* Blockchain-based storage ensures data integrity and transparency



## Solidity and Blockchain Concepts Used

* `msg.sender` for user identification
* `block.timestamp` for recording note creation time
* `struct` for structured data storage
* `mapping` for efficient user-based data management

---

## Conclusion

This smart contract implements a simple and secure decentralized personal note storage system.
It is a beginner-friendly example that demonstrates how Solidity can be used to manage user-specific data on the blockchain while maintaining privacy and security.

