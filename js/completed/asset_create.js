const algosdk = require("algosdk");
const validate = require("../validate");
const printError = require("../error-printer");
const { encodeAddress } = require("algosdk");

const challenge_id = "TBD"

const token = "";
const server = "https://testnet-api.algonode.cloud";
const port = 0;
const client = new algosdk.Algodv2(token, server, port);
const txids = [];

const secretKey =
  "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA==";

// Decode the secretKey into a Uint8Array from base 64
// This will produce an array of length 64
const secret = new Uint8Array(Buffer.from(secretKey, "base64"));
const acct = {
  // The public key is the secret[32:], or the last 32 bytes
  // We encode it to the address which is easier to read and includes a checksum
  addr: encodeAddress(secret.slice(32)),
  // We need not do anything with the secret
  sk: secret,
};

(async function () {
  try {
    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const sp = await client.getTransactionParams().do();

    // Construct an asset create transaction. 
    // An asset create transaction is the same as an asset config transaction
    // with its asset id set to 0
    const txn = algosdk.makeAssetCreateTxnWithSuggestedParamsFromObject({
      from: acct.addr,
      manager: acct.addr,
      freeze: acct.addr,
      clawback: acct.addr,
      reserve: acct.addr,
      assetMetadataHash: undefined,
      assetURL: "http://example.com",
      unitName: "tsk",
      assetName: "Task Asset",
      decimals: 2,
      total: 100,
      suggestedParams: sp,
    });

    // Sign the transaction. This should return a 
    // Uint8Array representing the bytes to be sent to the network
    const signed = txn.signTxn(acct.sk);

    // Send the transaction, returns the transaction id for 
    // the first transaction in the group
    const { txId } = await client.sendRawTransaction(signed).do();
    txids.push(txId);

    // Wait for the transaction to be confirmed.
    const result = await algosdk.waitForConfirmation(client, txId, 2);

    // Log out the confirmed round
    console.log("Confirmed round: " + result["confirmed-round"]);
  } catch (error) {
    printError(error);
    return;
  }

  console.log("Verifying challenge work...");
  if(await validate(challenge_id, txids)){
    console.log("Challenge completed sucessfully!");
  }else{
    console.log("Something went wrong :(. Please review the error message and modify the code to try again")
  }

})();
