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
minutes_until_refresh = 55  # Then every other X minutes
countdown_until_refresh = minutes_until_refresh

while True:

    if countdown_until_refresh <= 0:
        global_variables.refresh_tokens(True)
        countdown_until_refresh = minutes_until_refresh

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
    countdown_until_refresh = countdown_until_refresh - seconds_until_nextIteration/60
