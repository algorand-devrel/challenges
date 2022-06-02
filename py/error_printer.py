import re

error_map = {
    # TODO: maybe with capture groups to slurp out which acct overspent?
    "overspend":{
        "re":re.compile("overspend"),
        "message":"It looks you've tried to submit a transaction where an account did not have enough algos to complete the transaction.",
        "docs":[
            "https://developer.algorand.org/docs/get-details/transactions/#fees",
            "https://developer.algorand.org/docs/get-details/accounts/#minimum-balance"
        ]
    },
    "asset overspend":{
        "re":re.compile("underflow on subtracting"),
        "message":"It looks like you've tried to submit a transaction where an account did not have enough of an asset to transfer.",
        "docs":[
            # asset transfer
        ]
    },
    "opt in":{
        "re":re.compile("receiver error: must optin,"),
        "message":"It looks like you've tried to submit a transaction where the receiver has not yet opted in to the asset",
        "docs":[
            # asset opt in
        ]
    },
    "wrong signer":{
        "re": re.compile("should have been authorized by"),
        "message":"It looks like you've tried to submit a transaction where the actual signer is different from the expected signer",
        "docs":[
            # signing, auth addr, rekey
        ]
    }
}


def print_error(err):
    for v in error_map.values():
        if v["re"].search(err):
            print(v["message"])
            print("\n".join(v["docs"]))