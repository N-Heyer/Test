import pyautogui
import time
import keyboard  # Works on macOS with accessibility permissions

click_points = []  # Stores saved click positions

def listen_for_keys():
    """Listens for keypresses on macOS using keyboard module."""
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")

    while True:
        if keyboard.is_pressed("p"):
            x, y = pyautogui.position()
            click_points.append((x, y))
            print(f"\nAdded point: {x}, {y}")
            time.sleep(0.3)  # Prevent multiple detections

        elif keyboard.is_pressed("s"):
            if not click_points:
                print("\nNo points selected! Add at least one point.")
            else:
                print("\nStarting auto-clicker...")
                break  # Exit loop and start clicking

        elif keyboard.is_pressed("q"):
            print("\nExiting...")
            exit()

        time.sleep(0.1)

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("\nPress 'q' to stop the auto-clicker.")

    while True:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)

        if keyboard.is_pressed('q'):
            print("\nAuto-clicker stopped.")
            break

if __name__ == "__main__":
    listen_for_keys()
    auto_clicker()
