from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction

from utils import validate, print_error, algod_token, algod_server


# DO NOT CHANGE
challenge_id = "3462886918586161821"
client = AlgodClient(algod_token, algod_server)
txids = []

# TODO: Paste your secret key here
secretKey = "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA=="

# Get the address from the secret key
addr = account.address_from_private_key(secretKey)

# Get the suggested parameters from the Algod server.
# These include current fee levels and suggested first/last rounds.
sp = client.suggested_params()


# Create a payment transaction from you to you using the `acct` variable defined above
ptxn = transaction.PaymentTxn(addr, sp, addr, int(1e6))

# Sign the transaction.
# returns a SignedTxn object containing the bytes to be sent to the network
signed = ptxn.sign(secretKey)

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