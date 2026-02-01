import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))

with open("abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=os.getenv("CONTRACT_ADDRESS"),
    abi=abi
)

account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

def store_on_chain(tx_hash: str, prediction: int):
    tx = contract.functions.addRecord(
        Web3.to_bytes(hexstr=tx_hash),
        bool(prediction)
    ).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 200000,
        "gasPrice": w3.to_wei("20", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, os.getenv("PRIVATE_KEY"))
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()
