const algosdk = require("algosdk");
const verify = require("verify");

const token  = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const server = "http://localhost";
const port   = 4001;
const client = new algosdk.Algodv2(token, server, port);

const mn = "diesel minimum hood expire parade other market hotel spawn category rescue keen false coin success draft siren person denial student example rural better absorb tunnel";

(async function(){

    try {

        // Initialize the account with the provided mnemonic
        const acct = algosdk.mnemonicToSecretKey(mn)

        // Get the suggested parameters from the Algod server. These include current fee levels and suggested first/last rounds.
        // TODO: use the client initialized above to get the suggested parameters from the algod server


        // Create a payment transaction from you to you using the `acct` variable defined above
        const ptxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
            // TODO: Fill out the transaction parameters to construct a transaction
            // The sender and receiver should both be set to your address
            // The amount should be set to 1 algo (Hint: 1 algo is 1 million micro algos)
            // Use the suggested parameters you got from the client above
        })

        // Sign the transaction. This should return a Uint8Array representing the bytes to be sent to the network
        const signed = _ // TODO: Sign the transaction object using the accounts secret key

        // Send the transaction, returns the transaction id for the first transaction in the group
        const {txId} = await client.sendRawTransaction(signed).do()

        verify(client, txId)

    }catch(error){
        console.error("Failed to verify transaction: " + error)
    }

    // Wait for the transaction to be confirmed.
    const result = await algosdk.waitForConfirmation(client, txId, 2)

    // Log out the confirmed round
    console.log("Confirmed round: "+result['confirmed-round'])
})()