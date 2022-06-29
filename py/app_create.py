from os import access
from algosdk import *
import base64
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from validate import validate
from error_printer import print_error


# Don't change
challenge_id = "tbd"

dir = "/home/ben/challenges"
with open(dir + "/approval.teal", "r") as f:
    approval = f.read()

with open(dir + "/clear.teal", "r") as f:
    clear = f.read()

access_code = "not-a-secret"


token = ""
server = "https://testnet-api.algonode.cloud"

client = AlgodClient(token, server)
txids = []

# Challenge starts here


# TODO: Paste your secret key here
secretKey = "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA=="

# Get the address from the secret key
addr = account.address_from_private_key(secretKey)

try:
    approval_result = None # TODO: use the client to compile `approval`, the teal source file contents
    # Convert the result of compilation from base64 to bytes
    approval_program = base64.b64decode(approval_result["result"])


    clear_result = None # TODO: use the client to compile `clear`, the teal source file contents
    # Convert the result of compilation from base64 to bytes
    clear_program = None # TODO: similar to the above approval program, convert the clear result base64 to bytes 


    # TODO: Set the global schema to 1 uint and 1 byteslice
    global_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    sp = client.suggested_params()
    app_create_txn = transaction.ApplicationCreateTxn(
        None, # TODO: should be your address
        sp,
        on_complete=transaction.OnComplete.NoOpOC,
        approval_program=None, # TODO: set to the compiled result of the approval program as bytes
        clear_program=None, # TODO: set to the compiled result of the clear program as bytes
        global_schema=None, # TODO: set to the global schema we prepared above
        local_schema=None, # TODO: set to the local schema we prepared above
        app_args=None, # TODO: this should be set to a list containing app args (the access key)
    )
    signed_app_create = app_create_txn.sign(secretKey)
    txid = client.send_transaction(signed_app_create)
    txids.append(txid)

    result = transaction.wait_for_confirmation(client, txid, 2)
    print(result)

    app_id = None # TODO: Get the newly created `application-index` from the transaction result  
    # An application gets an account we can send assets to or issue transactions from, the address
    # can be derived from the app id
    app_address = logic.get_application_address(app_id)

    print("Confirmed round: {}".format(result["confirmed-round"]))
    print("Created app id: {}".format(app_id))
    print("Created app address: {}".format(app_address))

    sp = client.suggested_params()
    app_call_txn = transaction.ApplicationCallTxn(
        None, # TODO: set to your address
        sp, 
        None,  # TODO: Set to the app id we got from the transaction result
        transaction.OnComplete.NoOpOC,  
        app_args=None # TODO: set to the same app args array as above 
    )
    signed_app_call_txn = app_call_txn.sign(secretKey)
    txid = client.send_transaction(signed_app_call_txn)
    txids.append(txid)
    result = transaction.wait_for_confirmation(client, txid, 2)

    print("Call confirmed in round: {}".format(result["confirmed-round"]))

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
