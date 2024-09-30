import solcx
import solcx.install
from web3 import Web3
import json

class ContractHandler:
    def __init__(self, ganacheurl = "HTTP://127.0.0.1:7545", account_address=None, contract_path=None):
        self.web3 = Web3(Web3.HTTPProvider(ganacheurl))
        if self.web3.is_connected():
            print("Connected to ganache")
        """
        TODO: remove default account and accept account from user(completed)
        """
        self.account_address = account_address if account_address else self.web3.eth.accounts[0]
        self.contract_path = contract_path

    def compiler_contract(self, contract_path):
        with open(contract_path, 'r') as file:
            contract_source = file.read()
        solcx.install_solc('0.8.0')
        compiled_sol = solcx.compile_standard({
            "language":"Solidity",
            "sources":{
                "FileStorage.sol":{"content": contract_source}
            },
            "settings":{
                "outputSelection":{
                    "*":{"*":["abi","metadata","evm.bytecode"]}
                }
            }
        }) 

        abi = compiled_sol['contracts']['FileStorage.sol']['FileStorage']['abi']
        print("abi = ", abi)
        bytecode = compiled_sol['contracts']['FileStorage.sol']['FileStorage']['evm']['bytecode']['object']
        print("bytecode = ", bytecode)
        return abi, bytecode
    
    def deploy_contract(self, abi, bytecode):
        FileStorage = self.web3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = FileStorage.constructor().transact()
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        print(f"Contract deployed at address: {contract_address}")
        return contract_address
    
    def store_file_hash(self, file_name, cid, abi, contract_address):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)

        tx_hash = contract.functions.storeFile(file_name, cid).transact({'from':self.account_address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"File hash stored in contract. Transaction confirmed. Transaction Hash = {self.web3.to_hex(tx_hash)}")

    def retrieve_file_hash(self, file_name, abi, contract_address):
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        cid = contract.functions.getFileHash(file_name).call()
        return cid