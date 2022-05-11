const algosdk = require("algosdk");
const axios = require('axios')

const validate_path = challengeId => `/api/challenges/${challengeId}/verify/`

async function validate(challengeId, txIds) {
    const result = await axios.post(validate_path(challengeId), {
        "transaction_ids": txIds 
    })

    if(result.status !== 200) throw new Error("Validation failed: "+JSON.stringify(result.data))

    return true 
}

module.exports = validate