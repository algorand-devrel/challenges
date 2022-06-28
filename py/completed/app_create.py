from os import access
from algosdk import *
import base64
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from validate import validate
from error_printer import print_error


challenge_id = "tbd"

token = ""
server = "https://testnet-api.algonode.cloud"

client = AlgodClient(token, server)
txids = []

# TODO: Paste your secret key here
secretKey = "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA=="

# Get the address from the secret key
addr = account.address_from_private_key(secretKey)

access_code = "not-a-secret"

dir = "/home/ben/challenges"
with open(dir + "/approval.teal", "r") as f:
    approval = f.read()

with open(dir + "/clear.teal", "r") as f:
    clear = f.read()


try:
    approval_result = client.compile(approval)
    approval_program = base64.b64decode(approval_result["result"])

    clear_result = client.compile(clear)
    clear_program = base64.b64decode(clear_result["result"])

    sp = client.suggested_params()

    global_schema = transaction.StateSchema(num_uints=0, num_byte_slices=1)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=1)

    app_create_txn = transaction.ApplicationCreateTxn(
        addr,
        sp,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema,
        app_args=[access_code],
    )

    signed_app_create = app_create_txn.sign(secretKey)

    txid = client.send_transaction(signed_app_create)
    txids.append(txid)

    result = transaction.wait_for_confirmation(client, txid, 2)

    app_id = result["application-index"]
    app_address = logic.get_application_address(app_id)

    print("Confirmed round: {}".format(result["confirmed-round"]))
    print("Created app id: {}".format(app_id))
    print("Created app address: {}".format(app_address))

    sp = client.suggested_params()
    app_call_txn = transaction.ApplicationCallTxn(
        addr, sp, app_id, transaction.OnComplete.NoOpOC, app_args=[access_code]
    )
    signed_app_call_txn = app_call_txn.sign(secretKey)

    txid = client.send_transaction(signed_app_call_txn)
    txids.append(txid)

    result = transaction.wait_for_confirmation(txid)
    print("Call confirmed in round: {}".format(result["confiremd-round"]))

except error.AlgodHTTPError as err:
    print_error(str(err))
else:
    print("Verifying challenge is complete...")
    if validate(challenge_id, txids):
        print("Transactions validated! Collect your badge :)")
    else:
        print(
            "Something went wrong :( Check the error message, update the code and try again!"
        )
