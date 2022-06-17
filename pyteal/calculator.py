from typing import Tuple
import algosdk.abi  as sdk_abi
from pyteal import *
from deploy import *

router = Router(
    name="calculator",
    bare_calls=BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    ),
)


@router.method
def add(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
    return output.set(a.get() + b.get())


@router.method
def sub(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
    # implement a method to subtract b from a
    pass


@router.method
def mul(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
    # implement a method to multiply a and b
    pass


@router.method
def div(a: abi.Uint64, b: abi.Uint64, *, output: abi.Uint64):
    # implement a method to divide b by a
    pass


approval, clear, contract = router.compile_program(version=6)

addr = ""
secret = ""
gschema = None
lschema = None

app_id, app_addr = deploy(approval, clear, addr, secret, gschema, lschema)

print("Created: {} with address: {}".format(app_id, app_addr))