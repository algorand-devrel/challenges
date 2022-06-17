from pyteal import *

router = Router(
    name="global-state-wiggler",
    bare_calls=BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    ),
)


@router.method
def init_field(field_name: abi.String):
    # We return an Expression from the method that performs the
    # action we want
    return Seq(
        # A Sequence is a set of steps to perform, each step is itself an expression.
        #   Note: only the last step _MAY_ return a value, if any besides the last
        #   step try to return a value, it will result in a compile time error
        # First lets make sure the sender of the transaction is the same account
        # that created this application
        Assert(Txn.sender() == Global.creator_address()),
        # Now lets put the value 0 in the field specified by field_name from the arguments.
        # Global k/v pairs may hold up to 128 bytes combined but the key is limited to 64 bytes
        # so choose the key to be under 64 bytes
        App.globalPut(field_name.get(), Int(0)),
    )


@router.method
def incr_counter(field_name: abi.String):
    # Again, we return a sequence of expressions
    return Seq(
        # First lets _try_ to get the value stored in global state.
        # Here we're using the `Ex` suffixed getter since the non-suffixed
        # version will return a 0 either way, if there is no value at this key
        # we want to know and bail out of the program
        # The first argument, `Int(0)` is a reference to "Me" or my app id. If the caller
        # wanted to inspect global state from another app, that app id would be passed instead
        (val := App.globalGetEx(Int(0), field_name.get())),
        # Lets make sure that we found a valid value in the field_name
        Assert(val.hasValue()),
        # Finally lets overwrite the value stored at the key with the value + 1
        App.globalPut(field_name.get(), val.value() + Int(1)),
    )


approval, clear, contract = router.compile_program(version=6)
