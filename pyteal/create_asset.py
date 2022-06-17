from pyteal import *

router = Router(
    name="asset-creator",
    bare_calls=BareCallActions(
        no_op=OnCompleteAction.create_only(Approve()),
    ),
)


@router.method
def create_asset(
    name: abi.String, unit: abi.String, supply: abi.Uint64, *, output: abi.Uint64
):
    return Seq(
        Assert(Txn.sender() == Global.creator_address()),
        Assert(unit.length() <= Int(8)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields(
            {
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset_name: name.get(),
                TxnField.config_asset_unit_name: unit.get(),
                TxnField.config_asset_total: supply.get(),
                TxnField.config_asset_clawback: Global.current_application_address,
                TxnField.config_asset_freeze: Global.current_application_address,
                TxnField.config_asset_reserve: Global.current_application_address,
                TxnField.config_asset_manager: Global.current_application_address,
            }
        ),
        InnerTxnBuilder.Submit(),
        output.set(InnerTxn.created_asset_id()),
    )


approval, clear, contract = router.compile_program(version=6)
