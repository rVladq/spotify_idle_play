import dotenv
import base64

import requests

from utils.IDLE_STATES import albums
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

IDLE_ALBUMS= albums

REDIRECT_URI = dotenv.get_key(dotenv_file, "REDIRECT_URI")
CLIENT_ID = dotenv.get_key(dotenv_file, "CLIENT_ID")
CLIENT_SECRET = dotenv.get_key(dotenv_file, "CLIENT_SECRET")
DEVICE_ID = dotenv.get_key(dotenv_file, "DEVICE_ID")

ACCESS_TOKEN = None
REFRESH_TOKEN = None


def load_tokens():
    global ACCESS_TOKEN, REFRESH_TOKEN

    ACCESS_TOKEN = dotenv.get_key(dotenv_file, "ACCESS_TOKEN")
    REFRESH_TOKEN = dotenv.get_key(dotenv_file, "REFRESH_TOKEN")


def check_token_validity():
    response = requests.get(
        url=f"https://api.spotify.com/v1/me",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        },
    )

    if response.status_code == 200:
        return response.json()

    else:
        print(f"check_token_validity: Error: {response.status_code}, {response.text}")
        return 1


def refresh_tokens(force: bool = False):
    if (check_token_validity() != 1) and not force:
        return
    else:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        headers = {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
        }

        re = requests.post(
            url="https://accounts.spotify.com/api/token",
            headers=headers,
            data=data,
        ).json()

        refresh = re.get('refresh_token')

        dotenv.set_key(dotenv_file, "ACCESS_TOKEN", re.get('access_token'))
        dotenv.set_key(dotenv_file, "REFRESH_TOKEN", REFRESH_TOKEN if refresh is None else refresh)

        load_tokens()


def get_current_device():

    re = requests.get(
        url="https://api.spotify.com/v1/me/player/devices",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
        }
    ).json()

    global DEVICE_ID
    if re['devices']:
        DEVICE_ID = re['devices'][0]["id"]
        dotenv.set_key(dotenv_file, "DEVICE_ID", DEVICE_ID)


load_tokens()
refresh_tokens()


get_current_device()
