import time
import pyautogui
from pynput import mouse

click_positions = []
click_delay = 1.0  # Set delay between clicks (in seconds)


def on_click(x, y, button, pressed):
    if pressed:
        click_positions.append((x, y))
        print(f"Point added: {x}, {y}")
        if len(click_positions) >= 2:  # Stop after 5 points (adjust as needed)
            return False  # Stop listener


def get_click_positions():
    print("Click on the points you want to be clicked, then close the window.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    print("Selected points:", click_positions)


def auto_clicker():
    print("Starting auto clicker... Press Ctrl+C to stop.")
    try:
        while True:
            for pos in click_positions:
                pyautogui.click(pos[0], pos[1])
                print(f"Clicked: {pos}")
                time.sleep(click_delay)
    except KeyboardInterrupt:
        print("Auto clicker stopped.")


if __name__ == "__main__":
    get_click_positions()
    auto_clicker()