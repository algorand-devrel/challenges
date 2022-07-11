from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction

from utils import validate, print_error, algod_server, algod_token


# DO NOT CHANGE
challenge_id = "3471206611775576466"
client = AlgodClient(algod_token, algod_server)

txids = []

# TODO: Paste your secret key here
secretKey = ""

# Get the address from the secret key
addr = account.address_from_private_key(secretKey)

# Get the suggested parameters from the Algod server.
# These include current fee levels and suggested first/last rounds.
sp = client.suggested_params()


# TODO: Create a payment transaction from you to you using the `acct` variable defined above
# The asset should have a total supply of 1 but have 100 total units
# The asset should have the name `Task Asset`
txn = transaction.AssetCreateTxn(
    sender=None,  # TODO: Sender, should be your addr
    sp=sp,  # Suggested params we got above

    total=0,  # TODO: Total number of units (100)
    decimals=0,  # TODO: Total number of decimals (2)
    asset_name=None,  # TODO: The name of the asset (the string 'Task Asset' )

    reserve=None,  # TODO: Should be your address
    clawback=None,  # TODO: Should be your address
    freeze=None,  # TODO: Should be your address
    manager=None,  # TODO: Should be your address

    unit_name=None,  # The unit name of the asset (can leave blank for this task)
    url=None,  # The url of the asset (can leave blank for this task, for an NFT this might be an IPFS uri)

    default_frozen=False,  # Default frozen, leave false
)

# Sign the transaction.
# returns a SignedTxn object containing the bytes to be sent to the network
signed = txn.sign(secretKey)

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
    print(f"Created Asset: {result['asset-index']}")

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
