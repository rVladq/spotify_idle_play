import player

# start listening to an album that you want to add to IDLE_STATES, then run this script and copy-paste the output
print(player.extract_state_variables(player.get_playback_state())["context_uri"])
