from typing import List, Dict, Any, cast
from algosdk.future import transaction
from algosdk.constants import PAYMENT_TXN, ASSETTRANSFER_TXN
import util

# Group transaction
def validate_challenge_group_transaction(
    txns: List[Dict], challenge_account_id: str
) -> bool:
    assert len(txns) == 2, "Expected two transactions"
    assert txns[0]["confirmed-round"] > 0, "Expected confirmed transaction"

    txn1 = util.parse_transaction(txns[0]["txn"]["txn"])
    assert txn1.type == PAYMENT_TXN, "Expected a payment transaction"
    txn1 = cast(transaction.PaymentTxn, txn1)

    assert txn1.sender == challenge_account_id, "Expected sender to be you"
    assert txn1.receiver == util.faucet_addr, "Expected receiver to be faucet address"
    assert txn1.amt == int(1e6), "Expected amount to be 1 algo"

    txn2 = util.parse_transaction(txns[1]["txn"]["txn"])
    assert txn2.type == ASSETTRANSFER_TXN, "Expected an asset transfer transaction"
    txn2 = cast(transaction.AssetTransferTxn, txn2)

    assert txn2.sender == challenge_account_id, "Expected sender to be you"
    assert txn2.receiver == challenge_account_id, "Expected receiver to be you"
    assert txn2.index == util.usdc_asset_id, "Expected asset id to be " + str(
        util.usdc_asset_id
    )
    assert txn2.amount == 0, "Expected amount to be 0"

    return True


if __name__ == "__main__":
    txns = util.get_txns(
        [
            "SZPWVUU6NH6N2W3QUFK4UAM3ZYO33FFBMQIOEVMYIZLXHREPHRAQ",
            "N7KHOI2LQFMQJFILT3DHBWLPQG5ANCYW4S66RVNX32LM2SO4VVHA",
        ]
    )
    validate_challenge_group_transaction(
        txns, "WGOY3PC5OBW7TVIGZ2AKLDLMKROIVFVRCGVTMOBUPY2A376XG2FQTGW3XM"
    )
