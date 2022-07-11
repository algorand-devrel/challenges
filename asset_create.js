const algosdk = require("algosdk");
const { encodeAddress } = require("algosdk");
const {validate, printError, algod} = require("./utils");

// DO NOT CHANGE
const challenge_id = "3471206611775576466"
const client = new algosdk.Algodv2(algod.token, algod.server, algod.port);
let txids = [];

const secretKey = ""; // TODO: Add your secret key 

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
      // TODO: fill in the transaction parameters to create a new Asset 
      // with total units of 100 but max supply of 1 and with name `Task Asset`

      from:  undefined,     // TODO: The from address should be your address
      assetName: undefined, // TODO: The name should be the string "Task Asset"
      total: undefined,     // TODO: The total number of units (should be 100)
      decimals: undefined,  // TODO: The number of decimals to display (should be 2)

      manager: undefined,   // TODO: The manager address should be your address (should be your address)
      freeze: undefined,    // TODO: The address that may issue freeze/unfreeze transactions  (shouuld be your address)
      clawback: undefined,  // TODO: The address that may clawback an asset  (should be your address)
      reserve: undefined,   // TODO: The account that should be treated as `Reserve` for computing number of tokens in circulation (should be your address)

      unitName: undefined,  // The unit name of the asset (can stay empty) 
      assetURL: undefined,  // The url of asset (can leave blank for this task, for an NFT this might be an IPFS uri) 
      defaultFrozen: false, // Whether or not to have the asset frozen on xfer (can leave false)
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
    console.log("Created asset id: " + result["asset-index"])
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
