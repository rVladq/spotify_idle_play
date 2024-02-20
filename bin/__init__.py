import dotenv
import base64
from urllib.parse import urlencode
import flask
import requests

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

CLIENT_ID = dotenv.get_key(dotenv_file, "CLIENT_ID")
CLIENT_SECRET = dotenv.get_key(dotenv_file,"CLIENT_SECRET")
REDIRECT_URI = dotenv.get_key(dotenv_file,"REDIRECT_URI")


def get_auth_url():

    url = "https://accounts.spotify.com/authorize"
    data = {
        "client_id": CLIENT_ID,
        "response_type": 'code',
        "redirect_uri": REDIRECT_URI,
        "scope": "user-read-private user-read-playback-state user-modify-playback-state "
                 "user-read-currently-playing streaming",
    }
    data = urlencode(data)
    full_url = f"{url}?{data}"
    return full_url


app = flask.Flask(__name__)


@app.route("/")
def handle_request():
    code = flask.request.args.get('code')

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    re = requests.post(
        url="https://accounts.spotify.com/api/token",
        headers=headers,
        data=data,
        json=True,
    ).json()

    dotenv.set_key(dotenv_file, "ACCESS_TOKEN", re.get('access_token'))
    dotenv.set_key(dotenv_file, "REFRESH_TOKEN", re.get('refresh_token'))

    # tokens = json.dumps({
    #     "ACCESS_TOKEN": re.get('access_token'),
    #     "REFRESH_TOKEN": re.get('refresh_token'),
    # })

    # with open("./data/TOKENS.json", "w") as outfile:
    #     outfile.write(tokens)

    return '   -_-   "'


def main():
    print(get_auth_url())
    app.run('localhost', 3000)


if __name__ == '__main__':
    main()
