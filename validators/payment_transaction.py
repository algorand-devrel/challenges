from typing import List
from algosdk.v2client.algod import AlgodClient 
from algosdk import encoding 
from algosdk.constants import PAYMENT_TXN


token = ""
host = ""

def get_client():
    return AlgodClient(token, host)

def get_txns(txns: List[str]):
    client = get_client()
    txn_info = [client.pending_transaction_info(txid) for txid in txns]
    return txn_info

# Transaction Specialist
def validate_challenge_transaction_specialist(transaction_ids: List[str], challenge_account_id: str) -> bool:
    txns = get_txns(transaction_ids)

    assert len(txns) == 1, "Expected a single transaction"
    assert txn[0]['confirmed-round'] > 0, "Expected confirmed transaction"

    txn = encoding.future_msgpack_decode(txns[0]["txn"])

    assert txn.type == PAYMENT_TXN, "Expected a payment transaction"
    assert txn.sender == challenge_account_id, "Expected sender to be you"
    assert txn.receiver == challenge_account_id, "Expected receiver to be you"
    assert txn.amount == 1e6, "Expected amount to be 1A"

    return True