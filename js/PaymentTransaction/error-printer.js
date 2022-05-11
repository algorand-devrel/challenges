

const errorMapper = {
    // TODO: maybe with capture groups to slurp out which acct overspent?
    "overspend":{
        "re":/overspend/,
        "message":"It looks you've tried to submit a transaction where an account did not have enough algos to complete the transaction.",
        "docs":[
            "https://developer.algorand.org/docs/get-details/transactions/#fees",
            "https://developer.algorand.org/docs/get-details/accounts/#minimum-balance"
        ]
    }
}



export default function printError(error) {
    for(const [k,v] of Object.entries(errorMapper)){
        if(v['re'].exec(error)){
            console.error(v['message'])
            console.error(v['docs'])
        }
    }
}