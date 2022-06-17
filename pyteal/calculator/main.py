from algosdk.atomic_transaction_composer import *
from algosdk import account
from calculator import router
from deploy import client, deploy

secret = "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA=="

addr = account.address_from_private_key(secret)

signer = AccountTransactionSigner(secret)

approval, clear, contract = router.compile_program(version=6)

# app_id, app_addr = deploy(approval, clear, addr, secret)

# print("Created: {} with address: {}".format(app_id, app_addr))

app_id = 95884341
sp = client.suggested_params()

atc = AtomicTransactionComposer()

atc.add_method_call(
    app_id=app_id,
    method=contract.get_method_by_name("add"),
    sender=addr,
    sp=sp,
    signer=signer,
    method_args=[1, 1],
)

results = atc.execute(client, 2)
for result in results.abi_results:
    print(f"result of '{result.method.name}' => {result.return_value}")
