import bin.utils.player as player
import time


def main():

    count = 0
    player.resume()
    print("This is a test! The playback state is Not Null. Will check every minute...")
    player.pause()

    while True:

        time.sleep(60)
        count = count + 1

        current_state = player.get_playback_state()
        if current_state:
            print("Still Not Null after " + str(count) + " minutes...")
        else:
            print("Became null after " + str(count) + " minutes.")
            return 0


if __name__ == '__main__':
    main()
