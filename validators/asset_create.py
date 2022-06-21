from typing import List, Dict, cast
from algosdk.future import transaction
from algosdk.constants import ASSETCONFIG_TXN
import util

# Asset Create
def validate_challenge_asset_create(
    txns: List[Dict], challenge_account_id: str
) -> bool:
    assert len(txns) == 1, "Expected a single transaction"
    assert txns[0]["confirmed-round"] > 0, "Expected confirmed transaction"

    txn = util.parse_transaction(txns[0]["txn"]["txn"])
    assert txn.type == ASSETCONFIG_TXN, "Expected an asset config transaction"
    txn = cast(transaction.AssetConfigTxn, txn)

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
    txns = util.get_txns(["5GOGJRRZDRRHFJNTF2JIBOAZWGZCCTNQMQ75Z3URRX3LNNTPWZJA"])
    validate_challenge_asset_create(
        txns, "2ZRSH6HENIK2VA3GM6DPPVXAVIYL4BONBUXEQSBYHVY2CCGVXVGDYBOMEI"
    )
