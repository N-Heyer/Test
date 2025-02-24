import pyautogui
import time
import sys
from pynput import keyboard

click_points = []  # Stores saved click positions
start_clicking = False  # Flag to start auto-clicking

def on_press(key):
    """Handles key press events using pynput."""
    global start_clicking
    try:
        if key == keyboard.Key.esc:
            print("\nExiting...")
            return False  # Stop listener

        elif hasattr(key, 'char'):
            if key.char == 'p':  # Save cursor position
                x, y = pyautogui.position()
                click_points.append((x, y))
                print(f"\nAdded point: {x}, {y}")

            elif key.char == 's':  # Start auto-clicking
                if not click_points:
                    print("\nNo points selected! Add at least one point.")
                else:
                    print("\nStarting auto-clicker...")
                    start_clicking = True
                    return False  # Stop listener

    except AttributeError:
        pass  # Ignore special keys

def listen_for_keys():
    """Listens for keypresses using pynput (macOS-compatible)."""
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or press 'Esc' to quit.")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Keep listening until stopped

def auto_clicker():
    """Clicks at saved locations until 'Esc' is pressed."""
    print("\nPress 'Esc' to stop the auto-clicker.")

    def stop_clicker(key):
        if key == keyboard.Key.esc:
            print("\nAuto-clicker stopped.")
            return False  # Stop listener

    stop_listener = keyboard.Listener(on_press=stop_clicker)
    stop_listener.start()

    while stop_listener.running:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)

if __name__ == "__main__":
    listen_for_keys()
    if start_clicking:
        auto_clicker()
