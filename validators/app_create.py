from typing import List, Dict, cast
from algosdk.future import transaction
from algosdk.constants import APPCALL_TXN 
import util

# Transaction Specialist
def validate_challenge_transaction_specialist(
    txns: List[Dict], challenge_account_id: str
) -> bool:
    assert len(txns) == 2, "Expected a single transaction"
    assert txns[0].get("confirmed-round", 0) > 0, "Expected App Create to be confirmed"
    assert txns[1].get("confirmed-round", 0) > 0, "Expected App Call to be confirmed"


    app_create_txn = util.parse_transaction(txns[0]["txn"]["txn"])
    assert app_create_txn.type == APPCALL_TXN, "Expected an app call transaction"
    app_create_txn = cast(transaction.ApplicationCreateTxn, app_create_txn)

    assert app_create_txn.sender == challenge_account_id, "Expected sender to be you"
    assert app_create_txn.index ==  0, "Expected app index to be 0 for a create"
    assert len(app_create_txn.app_args) == 1, "Expected a single application argument"
    assert app_create_txn.global_schema.num_byte_slices == 1, "Expected 1 global byte slice"
    assert app_create_txn.global_schema.num_uints == 1, "Expected 1 global uint"
    assert app_create_txn.on_complete == None, "Expected On Complete to be set to NoOp"

    assert "application-index" in txns[0], "Expected a created application"

    created_app_id = txns[0]["application-index"]

    app_call_txn = util.parse_transaction(txns[1]["txn"]["txn"])
    assert app_call_txn.type == APPCALL_TXN, "Expected an app call transaction"
    app_call_txn = cast(transaction.ApplicationCallTxn, app_call_txn)

    assert app_call_txn.sender == challenge_account_id, "Expected sender to be you"
    assert app_call_txn.index ==  created_app_id, "Expected app index to be 0 for a create"
    assert len(app_call_txn.app_args) == 1, "Expected a single application argument"
    assert app_call_txn.app_args[0] == app_create_txn.app_args[0], "Expected the same app arg in create and call transactions"
    assert app_call_txn.on_complete == None, "Expected On Complete to be set to NoOp"

    return True


if __name__ == "__main__":
    txns = util.get_txns(["ISPBGYN4ZQPHGRPXAE4MAZJH7SQREJPNOFS4TVNCLMOG5BYWIQ6Q", "V4RX26V4NLL6JZ6S4JRSKUUN4LGJ3ZX4S7I33S5L5Z2JGGKRY76A"])
    validate_challenge_transaction_specialist(
        txns, "2ZRSH6HENIK2VA3GM6DPPVXAVIYL4BONBUXEQSBYHVY2CCGVXVGDYBOMEI"
    )
