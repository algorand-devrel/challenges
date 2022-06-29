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
secretKey = ""

# Get the address from the secret key
addr = account.address_from_private_key(secretKey)

# TODO: Get the suggested parameters from the Algod server.
sp = None

# TODO: Create a payment transaction from you to you for 1 Algo
# hint: From and To should be your `addr` and 1 Algo is 1m microAlgos
ptxn = transaction.PaymentTxn(None, sp, None, None)


# TODO: Sign the transaction.
signed = None

# Send the transaction, returns the transaction id for
# the first transaction in the group

try:
    # Send the transaction to the network
    # this returns the first transaction id in the group
    txId = client.send_transaction(signed)

    # Add txid to list to be validated later
    txids.append(txId)

    # Wait for the transaction to be confirmed.
    result = transaction.wait_for_confirmation(client, txId, 2)

    # Log out the confirmed round
    print(f"Confirmed round: {result['confirmed-round']}")

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
