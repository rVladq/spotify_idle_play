import requests
from utils import global_variables


def extract_state_variables(state):
    return {
        "context_uri": state["context"]["uri"],
        "repeat_state": state["repeat_state"],
        "shuffle_state": state["shuffle_state"],
        "volume": state["device"]["volume_percent"],
        "track_number": state["item"]["track_number"],
        "time": state["progress_ms"],
    }


def set_access_token_using_client_credentials():

    response = requests.post(
                    url="https://accounts.spotify.com/api/token",
                    headers={
                         "Content-Type": "application/x-www-form-urlencoded"
                     },
                    data={
                         "grant_type": "client_credentials",
                         "client_id": global_variables.CLIENT_ID,
                         "client_secret": global_variables.CLIENT_SECRET,
                    },
                )

    if response.status_code == 200:
        global_variables.ACCESS_TOKEN = response.json()["access_token"]

    else:
        print(f"Error: {response.status_code}, {response.text}")


def get_artist_data(artist_id):

    response = requests.get(
        url=f"https://api.spotify.com/v1/artists/{artist_id}",
        headers={
            "Authorization": f"Bearer {global_variables.ACCESS_TOKEN}",
        },
    )

    if response.status_code == 200:
        return response.json()

    else:
        print(f"get_artist_data: Error: {response.status_code}, {response.text}")


def get_playback_state():

    response = requests.get(
        url="https://api.spotify.com/v1/me/player",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
        },
    )

    if response.status_code == 200:
        return response.json()

    else:
        print(f"get_playback_state: Error: {response.status_code}, {response.text}")


def start_resume(state):

    response = requests.put(
        url=f"https://api.spotify.com/v1/me/player/play?device_id={global_variables.DEVICE_ID}",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        },
        json={
            "context_uri": state["context_uri"],
            "offset": {
                "position": state.get("track_number", 0) - 1
            },
            "position_ms": state.get("time", 0)
        }
    )

    if response.status_code == 204:
        return 0

    else:
        print(f"start_resume: Error: {response.status_code}, {response.text}")
        return 1


def resume():
    
    response = requests.put(
        url=f"https://api.spotify.com/v1/me/player/play?device_id={global_variables.DEVICE_ID}",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
    )

    if response.status_code == 204:
        return 0

    else:
        print(f"resume: Error: {response.status_code}, {response.text}")
        return 1


def pause():

    response = requests.put(
        url=f"https://api.spotify.com/v1/me/player/pause",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
        }
    )

    if response.status_code == 204:
        return 0

    else:
        print(f"pause: Error: {response.status_code}, {response.text}")
        return 1


def set_volume(percentage):

    response = requests.put(
        url=f"https://api.spotify.com/v1/me/player/volume?volume_percent={percentage}&device_id={global_variables.DEVICE_ID}",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
        }
    )

    if response.status_code == 204:
        return 0

    else:
        print(f"mute: Error: {response.status_code}, {response.text}")
        return 1


def toggle_shuffle(state):
    response = requests.put(
        url=f"https://api.spotify.com/v1/me/player/shuffle?state={state}&device_id={global_variables.DEVICE_ID}",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
        }
    )

    if response.status_code == 204:
        return 0

    else:
        print(f"toggle_shuffle: Error: {response.status_code}, {response.text}")
        return 1


def set_repeat(state):
    response = requests.put(
        url=f"https://api.spotify.com/v1/me/player/repeat?state={state}&device_id={global_variables.DEVICE_ID}",
        headers={
            'Authorization': f'Bearer {global_variables.ACCESS_TOKEN}',
        }
    )

    if response.status_code == 204:
        return 0

    else:
        print(f"set_repeat: Error: {response.status_code}, {response.text}")
        return 1


def refresh_state():
    resume()
    pause()