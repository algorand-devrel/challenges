const algosdk = require("algosdk");


const verifyChecks = {
    "confirmed":(ptr)=>{
        return ptr["confirmed-round"]>0
    },
    "sender == receiver": (ptr)=>{
        ptr['txn']['sender'] === ptr['txn']['receiver']
    },
    "amount == 1A": (ptr)=>{
        ptr['txn']['amount'] === 1e6
    }
};


export default function verifyTransaction(client, txId) {
    const result = algosdk.waitForConfirmation(client, txId, 3);

    for(const check in verifyChecks){
        if(!verifyChecks[check]) throw `Failed to verify: ${check}`
    }

    return true
}