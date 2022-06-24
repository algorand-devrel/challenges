from algosdk import *
from algosdk.v2client.algod import AlgodClient
from algosdk.atomic_transaction_composer import *
from algosdk.future import transaction

from utils import validate, print_error


challenge_id = "tbd"
token = ""
server = "https://testnet-api.algonode.cloud"

faucet_addr = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"
usdc_asa_id = 10458941


client = AlgodClient(token, server)
txids = []

# TODO: Paste your secret key here
secretKey = "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA=="

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
        txn=transaction.PaymentTxn(addr, sp, faucet_addr, int(1e6)), signer=signer
    )
)
atc.add_transaction(
    TransactionWithSigner(
        txn=transaction.AssetTransferTxn(addr, sp, addr, 0, usdc_asa_id), signer=signer
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
