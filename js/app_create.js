const algosdk = require("algosdk");
const fs = require("fs");
const validate = require("../validate");
const printError = require("../error-printer");
const { encodeAddress, getApplicationAddress } = require("algosdk");

const challenge_id = "TBD"

const dir = "/home/ben/challenges"
// Read in the programs
const approval = fs.readFileSync(dir+"/approval.teal");
const clear = fs.readFileSync(dir+"/clear.teal");

const accessCode = new Uint8Array(Buffer.from("not-a-secret"));

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
    const approvalRes = undefined // TODO: use the client to compile `approval`, the teal source file contents 
    // Convert the result of compilation from base64 to bytes
    const approvalProgram = new Uint8Array(Buffer.from(approvalRes["result"], 'base64'));

    const clearRes = undefined  // TODO: use the client to compile `clear`, the teal source file contents 
    const clearProgram =  undefined // TODO: similar to the above for approval program, convert the clear result base64 to bytes 

    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const createsp = await client.getTransactionParams().do();

    // TODO: Construct an application create transaction. 
    const txn = algosdk.makeApplicationCreateTxnFromObject({
      from: undefined, // TODO: set to your address
      approvalProgram: undefined, // TODO: set to the approval program bytes decoded above
      clearProgram: undefined, // TODO: set to the clear program bytes decoded above
      numGlobalByteSlices: 0, // TODO: we need 1 global byte slice and 1 global int in our schema
      numGlobalInts: 0,
      numLocalByteSlices: 0,
      numLocalInts: 0,
      appArgs: undefined, // TODO: set to an array of 1 element containing `accessCode` above
      suggestedParams: createsp,
    });
    const signed = txn.signTxn(acct.sk);
    const createDetails = await client.sendRawTransaction(signed).do();
    txids.push(createDetails.txId);

    // Wait for the transaction to be confirmed.
    const result = await algosdk.waitForConfirmation(client, createDetails.txId, 2);

    const appId = undefined // TODO: Get the newly created `application-index` from the transaction result
    // Log out the confirmed round
    console.log("Confirmed round: " + result["confirmed-round"]);
    console.log("app id: " + appId);
    console.log("app address: " + getApplicationAddress(appId));
    

    // Call the app
    const callsp = await client.getTransactionParams().do();
    const ac_txn = algosdk.makeApplicationCallTxnFromObject({
      from: undefined, // TODO: set to your address
      appIndex: undefined, // TODO: set to the app id we got above
      appArgs: undefined, // TODO: set to an array containing the `accessCode` 
      suggestedParams: callsp,
    })
    const signedAc = ac_txn.signTxn(acct.sk)
    const callDetails = await client.sendRawTransaction().do(signedAc)
    txids.push(callDetails.txId)
    const callResult = await algosdk.waitForConfirmation(client, callDetails.txId, 2);
    console.log("Call confirmed in round: "+callResult["confirmed-round"])

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
