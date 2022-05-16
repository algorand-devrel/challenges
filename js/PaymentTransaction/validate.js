const algosdk = require("algosdk");
const axios = require('axios')

const validate_path = `https://staging.new-dev-site.algorand.org/api/challenges/3462886918586161821/verify/`

async function validate(txIds) {
    const body = {
        "transaction_ids": txIds
    };

    try {
        const result = await axios.post(validate_path, body)
    } catch (error) {
        console.log("Error:" + error);
    }
    return true
}

module.exports = validate
