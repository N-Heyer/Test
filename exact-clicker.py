import pyautogui
from pynput import keyboard
import time

click_points = []  # Stores saved click positions
listening = True  # Control flag for listener

def on_press(key):
    """Handles key press events."""
    global listening
    try:
        if key.char == 'p':  # Save the cursor position
            x, y = pyautogui.position()
            click_points.append((x, y))
            print(f"\nAdded point: {x}, {y}")

        elif key.char == 's':  # Start auto-clicking
            if not click_points:
                print("\nNo points selected! Add at least one point.")
            else:
                print("\nStarting auto-clicker...")
                listening = False  # Stop listening and start clicking
                return False  # Stop the listener

        elif key.char == 'q':  # Quit the script
            print("\nExiting...")
            exit()

    except AttributeError:
        pass  # Ignore special keys

def show_cursor_position():
    """Continuously shows cursor position until user starts clicking."""
    global listening
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")

    with keyboard.Listener(on_press=on_press) as listener:
        while listening:
            x, y = pyautogui.position()
            print(f"\rCurrent Cursor Position: {x}, {y}", end="", flush=True)
            time.sleep(0.1)  # Prevent spamming the output

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("Press 'q' to stop the auto-clicker.")

    def stop_on_q(key):
        """Stops auto-clicker when 'q' is pressed."""
        if key.char == 'q':
            print("\nAuto-clicker stopped.")
            return False  # Stop listener

    # Start a separate listener for 'q'
    listener = keyboard.Listener(on_press=stop_on_q)
    listener.start()

    while listener.running:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)

if __name__ == "__main__":
    show_cursor_position()
    auto_clicker()
