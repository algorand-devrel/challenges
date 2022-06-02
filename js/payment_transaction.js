const algosdk = require("algosdk");
const validate = require("./validate");
const printError = require("./error-printer");

const challenge_id = "3462886918586161821"

const token =
  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const server = "http://localhost";
const port = 4001;
const client = new algosdk.Algodv2(token, server, port);

const sk = ""; // Add your secret key
const txids = [](async function () {
  try {
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


    // Get the suggested parameters from the Algod server. These include current fee levels and suggested first/last rounds.
    // TODO: use the client initialized above to get the suggested parameters from the algod server

    // Create a payment transaction from you to you using the `acct` variable defined above
    const ptxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      // TODO: Fill out the transaction parameters to construct a transaction
      // The sender and receiver should both be set to your address
      // The amount should be set to 1 algo (Hint: 1 algo is 1 million micro algos)
      // Use the suggested parameters you got from the client above
    });

    // Sign the transaction. This should return a Uint8Array representing the bytes to be sent to the network
    const signed = _; // TODO: Sign the transaction object using the accounts secret key

    // Send the transaction, returns the transaction id for the first transaction in the group
    const { txId } = await client.sendRawTransaction(signed).do();
    txids.push(txId);

    // Wait for the transaction to be confirmed.
    const result = await algosdk.waitForConfirmation(client, txId, 2);

    // Log out the confirmed round
    console.log("Confirmed round: " + result["confirmed-round"]);
  } catch (error) {
    printError(error);
  }

  if (await validate(challenge_id, txids)) {
    console.log("Success!");
  } else {
    console.error(
      "Something went wrong, please review the error and try again"
    );
  }
})();
