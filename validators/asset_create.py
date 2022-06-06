from typing import List, Dict
from algosdk.v2client.algod import AlgodClient
from algosdk import encoding
from algosdk.constants import ASSETCONFIG_TXN 
import base64


#token = "a" * 64
#host = "http://localhost:4001"

token = ""
host = "https://testnet-api.algonode.cloud"



def get_client():
    return AlgodClient(token, host)


def get_txns(txns: List[str])->List[Dict]:
    client = get_client()
    txn_info = [client.pending_transaction_info(txid) for txid in txns]
    return txn_info


# Asset Create 
def validate_challenge_asset_create(txns: List[Dict], challenge_account_id: str) -> bool:
    assert len(txns) == 1, "Expected a single transaction"
    assert txns[0]["confirmed-round"] > 0, "Expected confirmed transaction"

    base_txn = txns[0]["txn"]["txn"]

    # TODO: this should be included in the SDK itself
    base_txn["snd"] = encoding.decode_address(base_txn["snd"])
    base_txn["apar"]["f"] = encoding.decode_address(base_txn["apar"]["f"])
    base_txn["apar"]["r"] = encoding.decode_address(base_txn["apar"]["r"])
    base_txn["apar"]["m"] = encoding.decode_address(base_txn["apar"]["m"])
    base_txn["apar"]["c"] = encoding.decode_address(base_txn["apar"]["c"])
    base_txn["gh"] = base64.b64decode(base_txn["gh"])

    txn = encoding.future_msgpack_decode(base_txn)

    assert txn.type == ASSETCONFIG_TXN, "Expected an asset config transaction"

    assert txn.sender == challenge_account_id, "Expected sender to be you"
    assert txn.clawback == challenge_account_id, "Expected clawback to be you"
    assert txn.freeze == challenge_account_id, "Expected freeze to be you"
    assert txn.manager == challenge_account_id, "Expected manager to be you"
    assert txn.reserve == challenge_account_id, "Expected reserve to be you"

    assert txn.asset_name == "Task Asset", "Expected the name to be Task Asset"
    assert txn.total == 100, "Expected total to be 100"
    assert txn.decimals == 2, "Expected decimals to be 2"

    return True


if __name__ == "__main__":
    txns = get_txns(["5GOGJRRZDRRHFJNTF2JIBOAZWGZCCTNQMQ75Z3URRX3LNNTPWZJA"])
    validate_challenge_asset_create(txns, "2ZRSH6HENIK2VA3GM6DPPVXAVIYL4BONBUXEQSBYHVY2CCGVXVGDYBOMEI")