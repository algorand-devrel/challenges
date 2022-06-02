import requests

validate_path = lambda challenge_id: f"https://staging.new-dev-site.algorand.org/api/challenges/{challenge_id}/verify/"


def validate(challenge_id, txids):
    result = requests.post(validate_path(challenge_id), {"transaction_ids": txids})
    if result.status_code != 200:
        print(result.json()["fallback_message"])
        return False

    return True