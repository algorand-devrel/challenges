const algosdk = require("algosdk");
const {validate, printError, algod} = require("./utils");

const challenge_id = "3472343575287161170"
const faucet_addr = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"
const usdc_asa_id = 10458941

const client = new algosdk.Algodv2(algod.token, algod.server, algod.port);
txids = [];

const secretKey =
  "sYgLa2BSnHCYG1tlugubFuoLYjGoPoHiM71JkONCn3zWYyP45GoVqoNmZ4b31uCqML4FzQ0uSEg4PXGhCNW9TA==";

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

(async function () {
  try {

    // Construct a `signer` object that will be used to sign transactions
    // later the during AtomicTransactionComposer group transaction construction
    // process
    const signer = algosdk.makeBasicAccountTransactionSigner(acct) 

    // AtomicTransactionComposer allows us to easily add transactions
    // and ABI method calls to construct an atomic group
    const atc = new algosdk.AtomicTransactionComposer()

    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const sp = await client.getTransactionParams().do();

    // Send 1Algo to the faucet address
    const txn1 = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: undefined, // TODO: replace with your address
      to: faucet_addr,
      amount: 1e6,
      suggestedParams: sp,
    });
    atc.addTransaction({ txn: txn1, signer: signer })

    // Opt into `usdc_asa_id`
    const txn2 = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
      from: undefined, // TODO: replace with your address
      to: undefined, // TODO: replace with your address
      assetIndex: undefined, // TODO: replace with the asset id of usdc on testnet
      amount: 0,
      suggestedParams: sp,
    });
    atc.addTransaction({ txn: txn2, signer: signer })

    // Send the transaction, returns the transaction id for 
    // the first transaction in the group
    const results = await atc.execute(client, 2);
    txids = results.txIDs

    console.log("Confirmed in round: ", results.confirmedRound)
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