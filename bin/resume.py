import json
from utils import player


def main():

# save the current context if we can get it
    player.refresh_state()
    current_state = player.get_playback_state()
    if current_state is not None:
        current_state = player.extract_state_variables(current_state)
        is_idle = current_state["context_uri"] == "spotify:album:2WT1pbYjLJciAR26yMebkH" and current_state["volume"] == 0
        if is_idle:
            with open("./data/PLAY_IDLE.json", 'w') as file:
                json.dump(current_state, file)
        else:
            with open('./data/PLAY_RESUME.JSON', 'w') as file:
                json.dump(current_state, file)
                return 0

# execute the resume instructions
    with open("./data/PLAY_RESUME.JSON", 'r') as file:
        state_to_play = json.load(file)

    player.start_resume(state_to_play)
    player.set_volume(state_to_play["volume"])
    player.toggle_shuffle(state_to_play["shuffle_state"])
    player.set_repeat(state_to_play["repeat_state"])


if __name__ == '__main__':
    main()
