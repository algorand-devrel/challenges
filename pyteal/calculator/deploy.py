from typing import Tuple
from algosdk.v2client.algod import AlgodClient
from algosdk.atomic_transaction_composer import *
from algosdk.future import transaction
from algosdk.logic import get_application_address
import base64

token = ""
host = "https://testnet-api.algonode.cloud"
client = AlgodClient(token, host)


def deploy(
    approval: str,
    clear: str,
    addr: str,
    secret: str,
    gschema: transaction.StateSchema = transaction.StateSchema(),
    lschema: transaction.StateSchema = transaction.StateSchema(),
) -> Tuple[str, str]:
    approval_result = client.compile(approval)
    approval_bytes = base64.b64decode(approval_result["result"])

    clear_result = client.compile(clear)
    clear_bytes = base64.b64decode(clear_result["result"])

    sp = client.suggested_params()

    txn = transaction.ApplicationCreateTxn(
        addr,
        sp,
        transaction.OnComplete.NoOpOC,
        approval_bytes,
        clear_bytes,
        gschema,
        lschema,
    )
    signed = txn.sign(secret)
    txid = client.send_transaction(signed)
    result = transaction.wait_for_confirmation(client, txid, 2)

    app_id = result["application-index"]
    app_addr = get_application_address(app_id)

    return app_id, app_addr


def update(app_id: int, approval: str, clear: str, addr: str, secret: str):

    approval_result = client.compile(approval)
    approval_bytes = approval_result["result"]

    clear_result = client.compile(clear)
    clear_bytes = clear_result["result"]

    sp = client.suggested_params()

    txn = transaction.ApplicationUpdateTxn(
        addr,
        sp,
        app_id,
        approval_bytes,
        clear_bytes,
    )
    signed = txn.sign(secret)
    txid = client.send_transaction(signed)
    transaction.wait_for_confirmation(client, txid, 2)

    return
