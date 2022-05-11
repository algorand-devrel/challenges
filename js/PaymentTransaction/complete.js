const algosdk = require("algosdk");
const validate = require("./validate");
const printError = require("./error-printer");

const token  = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const server = "http://localhost";
const port   = 4001;
const client = new algosdk.Algodv2(token, server, port);

const mn = "diesel minimum hood expire parade other market hotel spawn category rescue keen false coin success draft siren person denial student example rural better absorb tunnel";

const txids = [];


(async function(){
    try {
        // Initialize the account with the provided mnemonic
        const acct = algosdk.mnemonicToSecretKey(mn)

        // Get the suggested parameters from the Algod server. These include current fee levels and suggested first/last rounds.
        const sp = await client.getTransactionParams().do();

        // Create a payment transaction from you to you using the `acct` variable defined above
        const ptxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
            from: acct.addr,
            to: acct.addr,
            amount: 1e6,
            suggestedParams: sp
        })

        // Sign the transaction. This should return a Uint8Array representing the bytes to be sent to the network
        const signed = ptxn.signTxn(acct.sk); 

        // Send the transaction, returns the transaction id for the first transaction in the group
        const {txId} = await client.sendRawTransaction(signed).do()
        txids.push(txId)

        // Wait for the transaction to be confirmed.
        const result = await algosdk.waitForConfirmation(client, txId, 2)

        // Log out the confirmed round
        console.log("Confirmed round: "+result['confirmed-round'])

    }catch(error){
        printError(error)
        return
    }

    try {
        validate(txids)
    }catch(error){
        console.error(error)
        return
    }

})()