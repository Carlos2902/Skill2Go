import os
import json
import traceback
from web3 import Web3
from django.conf import settings
from solcx import compile_standard, install_solc
from exchange.models import BlockchainContract

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
install_solc("0.7.6")

if not web3.is_connected():
    raise ConnectionError("Could not connect to Ganache. Please make sure that Ganache is running on port 8545.")
def compile_contract():
    contract_path = os.path.join(settings.BASE_DIR, 'skill2go', 'blockchain', 'contracts','SkillCertification.sol')
    with open(contract_path, 'r') as file:
        contract_file = file.read()
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SkillCertification.sol": {"content": contract_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            }
        },
        solc_version="0.7.6",
    )
    abi = compiled_sol["contracts"]["SkillCertification.sol"]["SkillCertification"]["abi"]
    bytecode = compiled_sol["contracts"]["SkillCertification.sol"]["SkillCertification"]["evm"]["bytecode"]["object"]
    abi_path = os.path.join(settings.BASE_DIR, 'skill2go', 'blockchain', 'SkillCertification_abi.json')
    bytecode_path = os.path.join(settings.BASE_DIR, 'skill2go', 'blockchain', 'SkillCertification_bytecode.json')
    with open(abi_path, 'w') as file:
        json.dump(abi, file)
    with open(bytecode_path, 'w') as file:
        json.dump(bytecode, file) 
    return abi, bytecode
    
def deploy_contract():
    try:
        print("Starting contract compilation...")
        abi, bytecode = compile_contract()
        accounts = web3.eth.accounts
        print(f"Available accounts: {accounts}")
        print(f"Account balances:")
        for account in accounts:
            balance = web3.eth.get_balance(account)
            print(f"{account}: {web3.from_wei(balance, 'ether')} ETH")
        deployer_account = accounts[0] 
        web3.eth.default_account = deployer_account 
        
        # Explicit gas estimation
        contract = web3.eth.contract(abi=abi, bytecode=bytecode)
        
        try:
            gas_estimate = contract.constructor().estimate_gas()
            print(f"Estimated deployment gas: {gas_estimate}")
        except Exception as gas_est_error:
            print(f"Gas estimation error: {gas_est_error}")
        
        # Detailed transaction submission
        tx_hash = contract.constructor().transact({
            'from': deployer_account,
            'gas': 5000000,  
        })
        
        print(f"Transaction hash: {tx_hash.hex()}")
        
        # Wait for transaction receipt with timeout
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        contract_address = tx_receipt.contractAddress
        # receipt checking
        print("Transaction Receipt Details:")
        print(f"Status: {tx_receipt.status}")
        print(f"Gas Used: {tx_receipt.gasUsed}")
        print(f"Contract Address: {tx_receipt.contractAddress}")
        if tx_receipt.status == 0:
            print("Transaction FAILED. Check contract logic.")
            return None
        return contract_address, deployer_account

    except Exception as e:
        print(f"Deployment Error: {type(e).__name__}")
        print(f"Error Details: {str(e)}")
        raise 
    
def get_contract():
    contract_stored = BlockchainContract.objects.first()
    if not contract_stored:
        raise ValueError("No contract address stored in the database.")
    # reading the abi from the json file
    abi_path = os.path.join(settings.BASE_DIR, 'skill2go', 'blockchain', 'SkillCertification_abi.json')
    with open(abi_path, 'r') as file:
        contract_abi = json.load(file)
    contract_address = Web3.to_checksum_address(contract_stored.contract_address)
    return web3.eth.contract(address=contract_address, abi=contract_abi)

def get_certification_index(user_address, skill_name):
    contract = get_contract()
    # fetching the certififcations recorded on the chain
    certifications = contract.functions.getCertifications(user_address).call()
    # getting the index of a given certification
    for index, cert in enumerate(certifications):
        if cert[1] == skill_name: #the index 1 on the chain is the skill name
            return index
    return None

# Function to record certification on blockchain
def record_certification_on_chain(user_address, skill_name, document_hash):
    print(f"received user_address: {user_address}")
    contract = get_contract()
    checksum_address = Web3.to_checksum_address(user_address)
    tx_hash = contract.functions.addCertification(skill_name, document_hash).transact({'from': checksum_address})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Certification recorded on-chain, tx hash: {tx_receipt.transactionHash.hex()}")
    
    
    # assigning the on_chain_id to the certID expected by the contract  
    events = contract.events.CertificationAdded().proccessReceipt(tx_receipt)
    if not events:
        raise RuntimeError("No events found in transaction receipt.")
    contract_list = contract.functions.getCertifications(checksum_address).call()
    cert_id = len(contract_list) - 1
    return tx_receipt.transactionHash.hex(), cert_id

# Function to verify certification on blockchain
def verify_certification_on_chain(user_address, index):
    contract = get_contract()
    blockchain_index = get_certification_index(user_address, index)
    tx_hash = contract.functions.verifyCertification(user_address, blockchain_index).transact({'from': user_address})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Certification verified on-chain, tx hash: {tx_receipt.transactionHash.hex()}")
    return tx_receipt.transactionHash.hex()

# Function to record a rejection of certification on blockchain
def reject_certification_on_chain(user_address, index):
    contract = get_contract()
    blokchain_index = get_certification_index(user_address, index)
    tx_hash = contract.functions.rejectCertification(user_address
    , blokchain_index).transact({'from': user_address})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Certification rejected on-chain, tx hash: {tx_receipt.transactionHash.hex()}")
    return tx_receipt.transactionHash.hex()
