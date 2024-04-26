# Automatically start music in the background to be displayed as activity on [Discord](https://discord.com/)

![image](https://github.com/rVladq/spotify_idle_play/assets/142915917/966499ef-886f-4fde-8aea-a5938daa9d6e)

## Requires **spotify premium**!

    

This app detects if the playback has been paused for more than 10 minutes and starts playing an album of your choice on **mute**. 

Spotify *may* or may *not* count muted streams toward spotify **wrapped**.

## Config

This app is built in [Python](https://www.python.org/) and uses  Spotify's **Web API**.  
This app is **not** hosted, so you will have to configure and run it locally.
- **First**, clone the repository. Then, copy-paste everything from `.env.example` into a new `.env` file.
- `python -m venv venv` create a virtual environment folder named venv.
- Activate the virtual environment:
  - Windows: `.\venv\Scripts\activate`
  - Linux: `source ./venv/bin/activate`
- Install dependencies `pip install -r requirements.txt`
- Go to [spotify for developers](https://developer.spotify.com/) and login with your spotify account **(premium is required for all functionalities to work)**.
- Create a new app, then go to settings and find `CLIENT_ID` and `CLIENT_SECRET`. **Set them in** `.env`.
- Next, you will need to give the app permissions to your account.
  - `python ./bin/__init__.py` this should return a link in the console to the spotify authorization page.  
  - Open it using a browser and press **accept**.
  - `TOKEN` and `REFRESH_TOKEN` should now have been automatically set inside `.env`.
  - `CTRL`+`C` in the console to stop the server.
- **Lastly**, before running `python ./bin/__main__.py` you need to have spotify running and **playing** music.
  - This is only required so that `DEVICE_ID` is set successfully in `.env`, and is only required on the **first** run.
- Now that spotify is running and playing music, run `python ./bin/__main__.py`.
- You should see `'Checking if it's time to idle...'` written in the console.

##

### Adding idle albums:
`./bin/data/PLAY_IDLE.json` is what the script uses to start the playback from the last position.  
`./bin/utils/IDLE_STATES.json` is an array where we store the **albums**.  
`./bin/utils/GET_URI.py` is a script that returns an **albums**'s URI.

- We need to manually configure `PLAY_IDLE.json` and `IDLE_STATES.json`.  
  - Start playing the **album**, then run `python ./utils/GET_URI.py`. The URI should be returned in console. **Copy** it.
  - **Paste** it in `./utils/IDLE_STATES`, as a member of the array. 

##

### Switching between the idle albums: 
- In order to default an album all you need to do is let it play on **mute** in the background for 1 minute. 
- Then a message in the console should say: `Updated the idle_state.` 

##

### Environment variables: (also check `.env.example`)

| Variable               | Description                        |
|------------------------|------------------------------------|
| `REDIRECT_URI`                | http://localhost:3000       |
| `CLIENT_ID`                | Bot ID                      |
| `CLIENT_SECRET`                | Bot ID                  |
| `ACCESS_TOKEN`                | Account access                   |
| `REFRESH_TOKEN`            | Account access                  |
| `DEVICE_ID`             | -                         |
