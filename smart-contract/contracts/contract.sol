pragma solidity ^0.8.0;

contract FileStorage {
    mapping(string => string) public fileHashes;

    function storeFile(string memory fileName, string memory fileHash) public {
        fileHashes[fileName] = fileHash;
    }

    function getFileHash(string memory fileName) public view returns (string memory) {
        return fileHashes[fileName];
    }
}
