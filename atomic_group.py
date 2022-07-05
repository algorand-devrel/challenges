from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.atomic_transaction_composer import *
from algosdk.future import transaction

from utils import (
    validate,
    print_error,
    faucet_addr,
    usdc_asa_id,
    algod_token,
    algod_server,
)


# DO NOT CHANGE
challenge_id = "3472343575287161170"
client = AlgodClient(algod_token, algod_server)
txids = []

# TODO: Paste your secret key here
secretKey = ""

# Get the address from the secret key
addr = account.address_from_private_key(secretKey)

# Create a TransactionSigner object we'll use later
signer = AccountTransactionSigner(secretKey)

# Get the suggested parameters from the Algod server.
# These include current fee levels and suggested first/last rounds.
sp = client.suggested_params()

atc = AtomicTransactionComposer()
atc.add_transaction(
    TransactionWithSigner(
        txn=transaction.PaymentTxn(
            sender=addr, sp=sp, receiver=faucet_addr, amt=int(1e6)
        ),
        signer=signer,
    )
)
atc.add_transaction(
    TransactionWithSigner(
        txn=transaction.AssetTransferTxn(
            sender=addr, sp=sp, receiver=addr, amt=0, index=usdc_asa_id
        ),
        signer=signer,
    )
)

try:
    result = atc.execute(client, 2)
    txids = result.tx_ids
    print(f"Confirmed in round {result.confirmed_round}")
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
