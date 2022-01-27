from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv

import os
import sys
import json
import pickle

load_dotenv()

# URL = "https://kovan.infura.io/v3/f0a85cb884f54c5882f912677b6b805d"
URL = "http://127.0.0.1:8545"

w3 = Web3(Web3.HTTPProvider(URL))

chain_id = w3.eth.chain_id  # chain ID
my_address = w3.eth.accounts[0]
# my_address = "0xBF436412b213d1Fcdd1bEEbcE13c91C3E2C66546"
private_key = os.getenv("PRIVATE_KEY")


def compile_smart_contract(simple_storage_file):
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.0",
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    return compiled_sol


def deploy_smart_contract(compiled_sol):
    # To deploy we need the abi and bytecode
    abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
    bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
        "bytecode"
    ]["object"]

    # Create the contract
    SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

    # Get nonce by number of transactions
    nonce = w3.eth.getTransactionCount(my_address)

    # We deploy with a transaction
    transaction = SimpleStorage.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
            "gasPrice": w3.eth.gas_price,
        }
    )

    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send the signed transaction

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt_contract = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Save tx_receipt_contract and abi in a file for future use
    with open("./tx_receipt_contract.db", "wb") as f:
        pickle.dump(dict(tx_receipt_contract), f)
        f.close()

    return tx_receipt_contract, abi


def retrieve():
    abi, tx_receipt_contract = get_abi_tx()

    # Call -> Simulate making the call and getting a return value
    simple_storage = w3.eth.contract(
        address=tx_receipt_contract["contractAddress"], abi=abi
    )

    return simple_storage.functions.retrieve().call()


def store_number(number):
    abi, tx_receipt_contract = get_abi_tx()

    # Transact -> When we actually make a state change
    simple_storage = w3.eth.contract(
        address=tx_receipt_contract["contractAddress"], abi=abi
    )
    nonce = w3.eth.getTransactionCount(my_address)
    store_trans = simple_storage.functions.store(number).buildTransaction(
        {
            "chainId": chain_id,
            "from": my_address,
            "nonce": nonce,
            "gasPrice": w3.eth.gas_price,
        }
    )

    signed_tx = w3.eth.account.sign_transaction(store_trans, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)


def get_abi_tx():
    with open("./compiled_code.json", "r") as file:
        json_file = json.load(file)

    abi = json_file["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

    with open("./tx_receipt_contract.db", "rb") as file:
        tx_receipt_contract = pickle.load(file)

    return abi, tx_receipt_contract


if __name__ == "__main__":
    with open("./SimpleStorage.sol", "r") as file:
        simple_storage_file = file.read()

    if sys.argv[1] == "compile":
        compile_smart_contract(simple_storage_file)
    elif sys.argv[1] == "deploy":
        deploy_smart_contract(compile_smart_contract(simple_storage_file))
    elif sys.argv[1] == "retrieve":
        print(retrieve())
    elif sys.argv[1] == "store":
        number = int(input("Number: "))
        store_number(number)
