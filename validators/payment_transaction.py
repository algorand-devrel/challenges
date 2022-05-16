from typing import List, Dict
from algosdk.v2client.algod import AlgodClient
from algosdk import encoding
from algosdk.constants import PAYMENT_TXN
import base64


token = "a" * 64
host = "http://localhost:4001"


def get_client():
    return AlgodClient(token, host)


def get_txns(txns: List[str])->List[Dict]:
    client = get_client()
    txn_info = [client.pending_transaction_info(txid) for txid in txns]
    return txn_info


# Transaction Specialist
def validate_challenge_transaction_specialist(txns: List[Dict], challenge_account_id: str) -> bool:
    assert len(txns) == 1, "Expected a single transaction"
    assert txns[0]["confirmed-round"] > 0, "Expected confirmed transaction"

    base_txn = txns[0]["txn"]["txn"]

    # TODO: this should be included in the SDK itself
    base_txn["rcv"] = encoding.decode_address(base_txn["rcv"])
    base_txn["snd"] = encoding.decode_address(base_txn["snd"])
    base_txn["gh"] = base64.b64decode(base_txn["gh"])

    txn = encoding.future_msgpack_decode(base_txn)

    assert txn.type == PAYMENT_TXN, "Expected a payment transaction"
    assert txn.sender == challenge_account_id, "Expected sender to be you"
    assert txn.receiver == challenge_account_id, "Expected receiver to be you"
    assert txn.amt == 1e6, "Expected amount to be 1A"

    return True


if __name__ == "__main__":
    txns = get_txns(["3HI2XQVN4UQD5LZCPAJLY25T4YMGDZHW62MDFOXH7I5ZUPWGU2NQ"])
    validate_challenge_transaction_specialist(txns, "E4VCHISDQPLIZWMALIGNPK2B2TERPDMR64MZJXE3UL75MUDXZMADX5OWXM")