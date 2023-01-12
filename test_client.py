"""
This module contains an example of a requests based test for the example app.
Feel free to modify this file in any way.
"""
import requests

# testing constants that match values in auth.py
BASE_URL = "http://127.0.0.1:5000"
ACCESS_TOKEN_1 = "31cd894de101a0e31ec4aa46503e59c8"
ACCESS_TOKEN_2 = "97778661dab9584190ecec11bf77593e"
USERNAME_1 = "challengeuser1"
USERNAME_2 = "challengeuser2"
USER_ID_1 = "8bde3e84-a964-479c-9c7b-4d7991717a1b"
USER_ID_2 = "45e3c49a-c699-405b-a8b2-f5407bb1a133"


def example_test():
    """
    Example of using requests to make a test call to the example Flask app
    """
    path = BASE_URL + "/"

    for access_token, username in [
        (ACCESS_TOKEN_1, USERNAME_1),
        (ACCESS_TOKEN_2, USERNAME_2),
    ]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }

        r = requests.get(path, headers=headers)
        message = r.json()["message"]
        assert "Hello {}".format(username) in message
        assert "0 projects" in message


if __name__ == "__main__":
    example_test()
