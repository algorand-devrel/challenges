const algosdk = require("algosdk");
const axios = require('axios')

const validate_path = (challenge_id)=> `https://staging.new-dev-site.algorand.org/api/challenges/${challenge_id}/verify/`

async function validate(challenge_id, txIds) {
    const body = {"transaction_ids": txIds };
    try {
        await axios.post(validate_path(challenge_id), body)
        return true
    } catch (error) { console.log("Valdiation Error:" + error); }
    return false
}

module.exports = validate
