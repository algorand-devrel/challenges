const algosdk = require("algosdk");
const fs = require("fs");
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

const dir = "/home/ben/challenges"
// Read in the programs
const approval = fs.readFileSync(dir+"/approval.teal");
const clear = fs.readFileSync(dir+"/clear.teal");

const accessCode = new Uint8Array(Buffer.from("not-a-secret"));

(async function () {
  try {
    // Compile the teal programs to bytecode
    const approvalRes = await client.compile(approval).do()
    const approvalProgram = new Uint8Array(Buffer.from(approvalRes["result"], 'base64'));

    const clearRes = await client.compile(clear).do()
    const clearProgram = new Uint8Array(Buffer.from(clearRes["result"], 'base64'));

    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const createsp = await client.getTransactionParams().do();

    // Construct an asset create transaction. 
    // An asset create transaction is the same as an asset config transaction
    // with its asset id set to 0
    const txn = algosdk.makeApplicationCreateTxnFromObject({
      from: acct.addr,
      approvalProgram: approvalProgram,
      clearProgram: clearProgram,
      numGlobalByteSlices: 1,
      numLocalByteSlices: 0,
      numGlobalInts: 1,
      numLocalInts: 0,
      appArgs: [accessCode],
      suggestedParams: createsp,
    });

    // Sign the transaction. This should return a 
    // Uint8Array representing the bytes to be sent to the network
    const signed = txn.signTxn(acct.sk);

    // Send the transaction, returns the transaction id for 
    // the first transaction in the group
    const createDetails = await client.sendRawTransaction(signed).do();
    txids.push(createDetails.txId);

    // Wait for the transaction to be confirmed.
    const result = await algosdk.waitForConfirmation(client, createDetails.txId, 2);

    const app_id = result["application-index"]
    // Log out the confirmed round
    console.log("Confirmed round: " + result["confirmed-round"]);
    console.log("app id: " + app_id);

    // Call the app
    const callsp = await client.getTransactionParams().do();
    const ac_txn = algosdk.makeApplicationCallTxnFromObject({
      from: acct.addr,
      appIndex: app_id,
      appArgs: [accessCode],
      suggestedParams: callsp,
    })

    const callDetails = await client.sendRawTransaction(ac_txn.signTxn(acct.sk)).do()
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
