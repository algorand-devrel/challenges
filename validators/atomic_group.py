from typing import List, Dict, Any, cast
from algosdk.v2client.algod import AlgodClient
from algosdk import encoding
from algosdk.future import * 
from algosdk.constants import * 
import base64

#token = "a" * 64
#host = "http://localhost:4001"

token = ""
host = "https://testnet-api.algonode.cloud"

usdc_asset_id = 10458941
faucet_addr = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"



def get_client():
    return AlgodClient(token, host)


def get_txns(txns: List[str])->List[Dict]:
    client = get_client()
    txn_info = [client.pending_transaction_info(txid) for txid in txns]
    return txn_info

# TODO: this should be included in the SDK itself
def parse_transaction(base_txn: Dict[str,Any])->transaction.Transaction:
    if "snd" in base_txn:
        base_txn["snd"] = encoding.decode_address(base_txn["snd"])

    if "rcv" in base_txn:
        base_txn["rcv"] = encoding.decode_address(base_txn["rcv"])

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

    return encoding.future_msgpack_decode(base_txn)

# Group transaction 
def validate_challenge_group_transaction(txns: List[Dict], challenge_account_id: str) -> bool:
    assert len(txns) == 2, "Expected two transactions"
    assert txns[0]["confirmed-round"] > 0, "Expected confirmed transaction"

    txn1 = cast(transaction.PaymentTxn, parse_transaction(txns[0]["txn"]["txn"]))
    assert txn1.type == PAYMENT_TXN, "Expected a payment transaction"
    assert txn1.sender == challenge_account_id, "Expected sender to be you"
    assert txn1.receiver == faucet_addr, "Expected receiver to be faucet address"
    assert txn1.amt == int(1e6), "Expected amount to be 1 algo"

    txn2 = cast(transaction.AssetTransferTxn, parse_transaction(txns[1]["txn"]["txn"]))
    assert txn2.type == ASSETTRANSFER_TXN, "Expected an asset transfer transaction"
    assert txn2.sender == challenge_account_id, "Expected sender to be you"
    assert txn2.receiver == challenge_account_id, "Expected receiver to be you"
    assert txn2.index == usdc_asset_id, "Expected asset id to be " + str(usdc_asset_id)
    assert txn2.amount == 0, "Expected amount to be 0"

    return True


if __name__ == "__main__":
    txns = get_txns(["5GOGJRRZDRRHFJNTF2JIBOAZWGZCCTNQMQ75Z3URRX3LNNTPWZJA", "5GOGJRRZDRRHFJNTF2JIBOAZWGZCCTNQMQ75Z3URRX3LNNTPWZJA"])
    validate_challenge_group_transaction(txns, "2ZRSH6HENIK2VA3GM6DPPVXAVIYL4BONBUXEQSBYHVY2CCGVXVGDYBOMEI")