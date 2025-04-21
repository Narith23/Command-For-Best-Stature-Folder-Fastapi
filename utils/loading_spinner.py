import sys
import threading
import time


def loading_spinner(message="Loading", duration=2):
    done = False

    def spinner():
        while not done:
            for symbol in "|/-\\":
                sys.stdout.write(f"\r{message}... {symbol}")
                sys.stdout.flush()
                time.sleep(0.1)

    thread = threading.Thread(target=spinner)
    thread.start()
    time.sleep(duration)
    done = True
    thread.join()
    sys.stdout.write(f"\r{message}... ✅ Done!\n")
    sys.stdout.flush()
