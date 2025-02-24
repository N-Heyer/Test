import pyautogui
import time
import sys

# Detect platform (macOS or Windows)
if sys.platform == "win32":
    import keyboard  # Import only on Windows
    print("Using keyboard library for Windows")
elif sys.platform == "darwin":
    from pynput import keyboard
    print("Using pynput library for macOS")
else:
    print("Unsupported platform.")
    sys.exit()

click_points = []  # Stores saved click positions
start_clicking = False  # Flag to start auto-clicking

def on_press(key):
    """Handles key press events for pynput on macOS."""
    global start_clicking
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
                start_clicking = True
                return False  # Stop listener

        elif key.char == 'q':  # Quit the script
            print("\nExiting...")
            sys.exit()

    except AttributeError:
        pass  # Ignore special keys

def show_cursor_position():
    """Continuously shows cursor position until user starts clicking."""
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")

    global start_clicking
    with keyboard.Listener(on_press=on_press) as listener:
        while listener.running and not start_clicking:
            x, y = pyautogui.position()
            print(f"\rCurrent Cursor Position: {x}, {y}", end="", flush=True)
            time.sleep(0.1)

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("\nPress 'q' to stop the auto-clicker.")

    while True:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)  # Adjust for click speed

        # Stop condition for Windows
        if sys.platform == "win32" and keyboard.is_pressed('q'):
            print("\nAuto-clicker stopped.")
            break
        # Stop condition for macOS (using pynput)
        elif sys.platform == "darwin":
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
            break

if __name__ == "__main__":
    show_cursor_position()  # Wait until user presses 's'
    if start_clicking:
        auto_clicker()
