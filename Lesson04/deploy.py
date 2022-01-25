from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv

import os
import json

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Our Solidity

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

# To deploy we need the abi and bytecode

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Connecting to ganache fake blockchain

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = w3.eth.chain_id  # Ganache chain ID
my_address = w3.eth.accounts[0]
private_key = os.getenv("PRIVATE_KEY")

# Create the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get nonce by number of transactions
nonce = w3.eth.getTransactionCount(my_address)

# We deploy with a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
