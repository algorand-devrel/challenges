const algosdk = require("algosdk");
const {validate, printError, algod} = require("./utils");

const challenge_id = "3462886918586161821"
const client = new algosdk.Algodv2(algod.token, algod.server, algod.port);
const txids = [];

const secretKey =
  "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA==";


(async function () {
  try {
    // Decode the secretKey into a Uint8Array from base 64
    // This will produce an array of length 64
    const secret = new Uint8Array(Buffer.from(secretKey, "base64"));
    const acct = {
      // The public key is the secret[32:], or the last 32 bytes
      // We encode it to the address which is easier to read and includes a checksum
      addr: algosdk.encodeAddress(secret.slice(32)),
      // We need not do anything with the secret
      sk: secret,
    };

    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const sp = await client.getTransactionParams().do();

    // Create a payment transaction from you to you using the `acct` variable defined above
    const ptxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: acct.addr,
      to: acct.addr,
      amount: 1e6,
      suggestedParams: sp,
    });

    // Sign the transaction. This should return a 
    // Uint8Array representing the bytes to be sent to the network
    const signed = ptxn.signTxn(acct.sk);

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
  try {
    await validate(challenge_id, txids);
  } catch (error) {
    console.error(error);
    return;
  }
  console.log("Challenge completed sucessfully!");
})();
