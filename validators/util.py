from typing import List, Dict, Any
from algosdk.v2client.algod import AlgodClient
from algosdk import encoding
from algosdk.future import transaction
import base64

token = ""
host = "https://testnet-api.algonode.cloud"

usdc_asset_id = 10458941
faucet_addr = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"


def get_client():
    return AlgodClient(token, host)


def get_txns(txns: List[str]) -> List[Dict]:
    client = get_client()
    txn_info = [client.pending_transaction_info(txid) for txid in txns]
    return txn_info


# TODO: this should be included in the SDK itself
def parse_transaction(base_txn: Dict[str, Any]) -> transaction.Transaction:
    if "snd" in base_txn:
        base_txn["snd"] = encoding.decode_address(base_txn["snd"])

    if "rcv" in base_txn:
        base_txn["rcv"] = encoding.decode_address(base_txn["rcv"])

    if "asnd" in base_txn:
        base_txn["asnd"] = encoding.decode_address(base_txn["asnd"])

    if "arcv" in base_txn:
        base_txn["arcv"] = encoding.decode_address(base_txn["arcv"])

    if "apar" in base_txn:
        if "f" in base_txn["apar"]:
            base_txn["apar"]["f"] = encoding.decode_address(base_txn["apar"]["f"])
        if "r" in base_txn["apar"]:
            base_txn["apar"]["r"] = encoding.decode_address(base_txn["apar"]["r"])
        if "m" in base_txn["apar"]:
            base_txn["apar"]["m"] = encoding.decode_address(base_txn["apar"]["m"])
        if "c" in base_txn["apar"]:
            base_txn["apar"]["c"] = encoding.decode_address(base_txn["apar"]["c"])

    if "gh" in base_txn:
        base_txn["gh"] = base64.b64decode(base_txn["gh"])

    if "grp" in base_txn:
        base_txn["grp"] = base64.b64decode(base_txn["grp"])

    if "apap" in base_txn:
        base_txn["apap"] = base64.b64decode(base_txn["apap"])

    if "apsu" in base_txn:
        base_txn["apsu"] = base64.b64decode(base_txn["apsu"])

    return encoding.future_msgpack_decode(base_txn)
