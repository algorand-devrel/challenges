from typing import List, Dict, cast
from algosdk.future import transaction
from algosdk.constants import PAYMENT_TXN
import util


# Transaction Specialist
def validate_challenge_transaction_specialist(
    txns: List[Dict], challenge_account_id: str
) -> bool:
    assert len(txns) == 1, "Expected a single transaction"
    assert txns[0]["confirmed-round"] > 0, "Expected confirmed transaction"

    txn = util.parse_transaction(txns[0]["txn"]["txn"])
    assert txn.type == PAYMENT_TXN, "Expected a payment transaction"
    txn = cast(transaction.PaymentTxn, txn)

    assert txn.sender == challenge_account_id, "Expected sender to be you"
    assert txn.receiver == challenge_account_id, "Expected receiver to be you"
    assert txn.amt == 1e6, "Expected amount to be 1A"

    return True


if __name__ == "__main__":
    txns = util.get_txns(["3HI2XQVN4UQD5LZCPAJLY25T4YMGDZHW62MDFOXH7I5ZUPWGU2NQ"])
    validate_challenge_transaction_specialist(
        txns, "E4VCHISDQPLIZWMALIGNPK2B2TERPDMR64MZJXE3UL75MUDXZMADX5OWXM"
    )
