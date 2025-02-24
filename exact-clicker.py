import pyautogui
import time
import sys
import threading
from AppKit import NSEvent
import Quartz

click_points = []  # Stores saved click positions
start_clicking = False  # Flag to start auto-clicking

def listen_for_keys():
    """Listens for keypress events using NSEvent (macOS-native)."""
    global start_clicking

    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")

    while True:
        event = NSEvent.keyEventWithType_location_modifierFlags_timestamp_windowNumber_context_characters_charactersIgnoringModifiers_isARepeat_keyCode_(
            Quartz.kCGEventKeyDown,
            (0, 0),
            0,
            0,
            0,
            None,
            None,
            None,
            False,
            0,
        )

        if not event:
            continue

        key_pressed = event.charactersIgnoringModifiers()

        if key_pressed == "p":  # Save cursor position
            x, y = pyautogui.position()
            click_points.append((x, y))
            print(f"\nAdded point: {x}, {y}")

        elif key_pressed == "s":  # Start auto-clicking
            if not click_points:
                print("\nNo points selected! Add at least one point.")
            else:
                print("\nStarting auto-clicker...")
                start_clicking = True
                break  # Exit key listener

        elif key_pressed == "q":  # Quit the script
            print("\nExiting...")
            sys.exit()

        time.sleep(0.1)

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("\nPress 'q' to stop the auto-clicker.")

    while True:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)

        if not start_clicking:
            break

if __name__ == "__main__":
    key_listener_thread = threading.Thread(target=listen_for_keys)
    key_listener_thread.start()

    while True:
        if start_clicking:
            auto_clicker()
            break
