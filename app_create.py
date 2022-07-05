from algosdk import *
import base64
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction

from utils import validate, print_error, algod_token, algod_server


# Don't change
challenge_id = "3475012173671627630"
client = AlgodClient(algod_token, algod_server)
txids = []

# Challenge starts here
access_code = "not-a-secret"

# First, read in the source TEAL of the approval program and clear program
with open("approval.teal", "r") as f:
    approval = f.read()

with open("clear.teal", "r") as f:
    clear = f.read()

# TODO: Paste your secret key here
secretKey = ""

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
    # No local state is needed, leave this as 0s
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    sp = client.suggested_params()
    app_create_txn = transaction.ApplicationCreateTxn(
        sender=None, # TODO: should be your address
        sp=sp,
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

    # https://developer.algorand.org/docs/rest-apis/algod/v2/#pendingtransactionresponse
    app_id = None # TODO: Get the newly created `application-index` from the PendingTransactionResponse

    # An application gets an account we can send assets to or issue transactions from, the address
    # can be derived from the app id
    app_address = logic.get_application_address(app_id)

    print("Confirmed round: {}".format(result["confirmed-round"]))
    print("Created app id: {}".format(app_id))
    print("Created app address: {}".format(app_address))

    sp = client.suggested_params()
    app_call_txn = transaction.ApplicationCallTxn(
        sender=None, # TODO: set to your address
        sp=sp, 
        on_complete=transaction.OnComplete.NoOpOC,  
        index=None,  # TODO: Set to the app id we got from the transaction result
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
