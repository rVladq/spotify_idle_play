import time
import psutil
from utils import player
from utils import global_variables
import go_idle


seconds_until_nextIteration = 60  # seconds

is_spotify_open = None

# Checking to see if spotify is open
for proc in psutil.process_iter(['pid', 'name']):
    if 'Spotify' in proc.info['name']:
        is_spotify_open = True

if is_spotify_open is not True:
    psutil.Popen(["spotify"])
    print('Waiting for spotify to open')
    time.sleep(10)
else:
    print("Spotify is already open.")

# Tokens expire every hour, so we'll have to refresh them
global_variables.refresh_tokens(force=True)  # Initial reset when the script starts
started_at = time.monotonic() # seconds
minutes_until_refresh = 55  # Then every other X minutes

while True:

    # Checking to see if the set amount of minutes passed
    current_time = time.monotonic()
    if (current_time - started_at)/60 >= minutes_until_refresh:
        global_variables.refresh_tokens(True)
        started_at = current_time # setting this to check for the next refresh

    print('Checking if it\'s time to idle...')
    
    current_state = player.get_playback_state()
    
    # the playback_state becomes Null after 10 minutes of being paused
    if current_state is None:
        print('TIME TO IDLE!')
        go_idle.main()

    # if the playback_state is not Null, but we are idling -> update the idle state
    if current_state is not None:
        current_state = player.extract_state_variables(current_state)
        is_idle = (current_state["context_uri"] in global_variables.IDLE_ALBUMS) and (current_state["volume"] == 0)
        if is_idle:
            go_idle.main() # this will just save the current state to PLAY_IDLE.json because we already are idling
            print('Updated the idle_state.')
    
    # pausing
    time.sleep(seconds_until_nextIteration)
