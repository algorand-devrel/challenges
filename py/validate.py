import requests

validate_path = (
    lambda challenge_id: f"https://staging.new-dev-site.algorand.org/api/challenges/{challenge_id}/verify/"
)


def validate(challenge_id, txids):
    result = requests.post(validate_path(challenge_id), {"transaction_ids": txids})
    if result.status_code == 200:
        return True
    elif result.status_code == 400:
        print(result.json()["fallback_message"])
        return False
    elif result.status_code > 400 and result.status_code < 500:
        print(result.json())
        return False
    print("Unexpected response from validator endpoint, please try again.)
    return False
