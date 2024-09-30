from ipfs_module.ipfs_handler import IPFSHandler
from eth_module.contract_handler import ContractHandler
from db_module.db_handler import DBHandler
import json

#create config.json file in config folder before running this file
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

ipfs_handler = IPFSHandler()
db_handler = DBHandler(**config['mysql'])
contract_handler = ContractHandler() #leave it blank for default account on ganache


#(compile, deploy, migrate your contract using truffle, copy it's abi and contract_address from build file)
#WARNING: DON'T USE THIS ABI AND CONTRACT ADDRESS OR BYTECODE, DEPLOY YOUR OWN CONTRACT ON GANACHE USING TURUFFLE)
abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "fileName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "fileHash",
                "type": "string"
            }
        ],
        "name": "storeFile",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "fileName",
                "type": "string"
            }
        ],
        "name": "getFileHash",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "name": "fileHashes",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
bytecode = '0x608060405234801561001057600080fd5b5061065b806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c806320de1070146100465780634527525214610062578063f880680b14610092575b600080fd5b610060600480360381019061005b91906103ab565b6100c2565b005b61007c6004803603810190610077919061036a565b6100f9565b6040516100899190610498565b60405180910390f35b6100ac60048036038101906100a7919061036a565b6101af565b6040516100b99190610498565b60405180910390f35b806000836040516100d39190610481565b908152602001604051809103902090805190602001906100f492919061025f565b505050565b600081805160208101820180518482526020830160208501208183528095505050505050600091509050805461012e90610584565b80601f016020809104026020016040519081016040528092919081815260200182805461015a90610584565b80156101a75780601f1061017c576101008083540402835291602001916101a7565b820191906000526020600020905b81548152906001019060200180831161018a57829003601f168201915b505050505081565b60606000826040516101c19190610481565b908152602001604051809103902080546101da90610584565b80601f016020809104026020016040519081016040528092919081815260200182805461020690610584565b80156102535780601f1061022857610100808354040283529160200191610253565b820191906000526020600020905b81548152906001019060200180831161023657829003601f168201915b50505050509050919050565b82805461026b90610584565b90600052602060002090601f01602090048101928261028d57600085556102d4565b82601f106102a657805160ff19168380011785556102d4565b828001600101855582156102d4579182015b828111156102d35782518255916020019190600101906102b8565b5b5090506102e191906102e5565b5090565b5b808211156102fe5760008160009055506001016102e6565b5090565b6000610315610310846104eb565b6104ba565b90508281526020810184848401111561032d57600080fd5b610338848285610542565b509392505050565b600082601f83011261035157600080fd5b8135610361848260208601610302565b91505092915050565b60006020828403121561037c57600080fd5b600082013567ffffffffffffffff81111561039657600080fd5b6103a284828501610340565b91505092915050565b600080604083850312156103be57600080fd5b600083013567ffffffffffffffff8111156103d857600080fd5b6103e485828601610340565b925050602083013567ffffffffffffffff81111561040157600080fd5b61040d85828601610340565b9150509250929050565b60006104228261051b565b61042c8185610526565b935061043c818560208601610551565b61044581610614565b840191505092915050565b600061045b8261051b565b6104658185610537565b9350610475818560208601610551565b80840191505092915050565b600061048d8284610450565b915081905092915050565b600060208201905081810360008301526104b28184610417565b905092915050565b6000604051905081810181811067ffffffffffffffff821117156104e1576104e06105e5565b5b8060405250919050565b600067ffffffffffffffff821115610506576105056105e5565b5b601f19601f8301169050602081019050919050565b600081519050919050565b600082825260208201905092915050565b600081905092915050565b82818337600083830152505050565b60005b8381101561056f578082015181840152602081019050610554565b8381111561057e576000848401525b50505050565b6000600282049050600182168061059c57607f821691505b602082108114156105b0576105af6105b6565b5b50919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052602260045260246000fd5b7f4e487b7100000000000000000000000000000000000000000000000000000000600052604160045260246000fd5b6000601f19601f830116905091905056fea2646970667358221220af3788d5906206751a73fc32826eb91a7531f2cb4a7eb47fee541f22b8459ab764736f6c63430008000033'
# abi, bytecode = contract_handler.compiler_contract('eth_module/contract.sol')
contract_address = "0x6d198Ad47FcbA2b7344eAC2bf4d13125Ac38eb34"

def upload_file(file_path):
    file_name = file_path.split('/')[-1]
    db_cid = db_handler.retrieve_file(file_name)
    if db_cid is not None:
        print(f"File name with {file_name} already exists. Do you wish to replace file?")
        option = input("Press Y to continue, press any key to abort..")
        if option == "Y" or option == "y":
            cid = ipfs_handler.upload_file(file_path)
            print(f"File uploaded to IPFS, CID: {cid}")

            #storing details in database
            db_handler.store_dublicate(file_name,cid)
            print(f"File stored in MySQL: {file_name} -> {cid}")

            #storing detalis on ethreum
            contract_handler.store_file_hash(file_name, cid, abi, contract_address)
            print("file hash stored on ethreum")
        else:
            print("Operation aborted...")
    else:
        cid = ipfs_handler.upload_file(file_path)
        print(f"File uploaded to IPFS, CID: {cid}")

        #storing details in database
        db_handler.store_file(file_name,cid)
        print(f"File stored in MySQL: {file_name} -> {cid}")

        #storing detalis on ethreum
        contract_handler.store_file_hash(file_name, cid, abi, contract_address)
        print("file hash stored on ethreum")
    

def retrieve_file(file_name, output_path):
    cid = db_handler.retrieve_file(file_name)
    print(f"CID retrieved from mySql: {cid}")

    cid2 = contract_handler.retrieve_file_hash(file_name=file_name, abi=abi, contract_address= contract_address)
    print(f"cid1 = {cid}\ncid2 = {cid2}")

    #match cid from smartcontract and database
    if (cid and cid2) and (cid == cid2):
        ipfs_handler.get_file(cid, output_path)
    else:
        print("file not found in mysql")

if __name__ == '__main__':
    
    #it is possible to upload a directory or a file but uploading a directory is preferred
    upload_file('hello2') 

    retrieve_file('hello2', 'download/')

"""
KNOWN ISSUES: 
1. Contract deployment using python is pending. Temporary fix: compiled and deployed on Ganache using Truffle.
2. IPFS version
3. Removing previous file details from database and pointing it to newer CID


"""