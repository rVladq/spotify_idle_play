import json
from utils import global_variables
from utils import player


def main():

    # save the current context if we can get it
    current_state = player.get_playback_state()
    if current_state is not None:
        current_state = player.extract_state_variables(current_state)
        is_idle = current_state["context_uri"] in global_variables.IDLE_ALBUMS and (current_state["volume"] == 0)
        if is_idle:
            with open("./data/PLAY_IDLE.json", 'w') as file:
                json.dump(current_state, file)
                return 0
        else:
            with open('./data/PLAY_RESUME.JSON', 'w') as file:
                json.dump(current_state, file)

    # execute the idling instructions
    with open('./data/PLAY_IDLE.json', 'r') as file:
        state_to_play = json.load(file)

    player.set_volume(0)
    player.toggle_shuffle("false")
    player.set_repeat("context")
    player.start_resume(state_to_play)


if __name__ == '__main__':
    main()
