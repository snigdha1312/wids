// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract FraudRegistry {

    struct FraudRecord {
        bool isFraud;
        uint256 timestamp;
        bool exists;
    }

    mapping(bytes32 => FraudRecord) private records;

    event RecordAdded(
        bytes32 indexed txHash,
        bool isFraud,
        uint256 timestamp
    );

    function addRecord(bytes32 _txHash, bool _isFraud) external {
        require(!records[_txHash].exists, "Record already exists");

        records[_txHash] = FraudRecord({
            isFraud: _isFraud,
            timestamp: block.timestamp,
            exists: true
        });

        emit RecordAdded(_txHash, _isFraud, block.timestamp);
    }

    function getRecord(bytes32 _txHash)
        external
        view
        returns (bool isFraud, uint256 timestamp)
    {
        require(records[_txHash].exists, "Record not found");

        FraudRecord memory record = records[_txHash];
        return (record.isFraud, record.timestamp);
    }
}
