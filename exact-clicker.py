import pyautogui
import time
import sys

# Detect platform (macOS or Windows)
if sys.platform == "win32":
    import keyboard
    print("Using keyboard library for Windows")
elif sys.platform == "darwin":
    from pynput import keyboard
    print("Using pynput library for macOS")
else:
    print("Unsupported platform.")
    sys.exit()

click_points = []  # Stores saved click positions

def on_press(key):
    """Handles key press events for pynput on macOS."""
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
                return False  # Stop listener

        elif key.char == 'q':  # Quit the script
            print("\nExiting...")
            exit()

    except AttributeError:
        pass  # Ignore special keys

def show_cursor_position():
    """Continuously shows cursor position until user starts clicking."""
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")

    if sys.platform == "win32":  # For Windows, using keyboard library
        while True:
            x, y = pyautogui.position()
            print(f"\rCurrent Cursor Position: {x}, {y}", end="", flush=True)
            time.sleep(0.1)

            if keyboard.is_pressed('p'):
                click_points.append((x, y))
                print(f"\nAdded point: {x}, {y}")
            elif keyboard.is_pressed('s'):
                if not click_points:
                    print("\nNo points selected! Add at least one point.")
                else:
                    print("\nStarting auto-clicker...")
                    break  # Stop position tracking and start clicking
            elif keyboard.is_pressed('q'):  # Quit the script
                print("\nExiting...")
                exit()

    elif sys.platform == "darwin":  # For macOS, using pynput
        with keyboard.Listener(on_press=on_press) as listener:
            while True:
                x, y = pyautogui.position()
                print(f"\rCurrent Cursor Position: {x}, {y}", end="", flush=True)
                time.sleep(0.1)  # Prevent spamming the output

                if not listener.running:
                    break  # Stop if the listener stops

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("Press 'q' to stop the auto-clicker.")
    while True:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)

        if sys.platform == "win32" and keyboard.is_pressed('q'):
            print("\nAuto-clicker stopped.")
            break
        elif sys.platform == "darwin" and keyboard.is_pressed('q'):
            print("\nAuto-clicker stopped.")
            break

if __name__ == "__main__":
    show_cursor_position()
    auto_clicker()
