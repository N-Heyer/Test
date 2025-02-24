import time
import pyautogui
from pynput import mouse, keyboard

click_positions = []
click_delay = 1.0  # Set delay between clicks (in seconds)
initial_delay = 10.0  # Delay before clicks can be registered
stop_flag = False

def on_click(x, y, button, pressed):
    if pressed:
        click_positions.append((x, y))
        print(f"Point added: {x}, {y}")
        if len(click_positions) >= 2:  # Stop after 5 points (adjust as needed)
            return False  # Stop listener

def on_press(key):
    global stop_flag
    if key == keyboard.Key.esc:
        stop_flag = True
        return False

def get_click_positions():
    print(f"Waiting {initial_delay} seconds before registering clicks...")
    time.sleep(initial_delay)
    print("You can now click on the points you want to be clicked.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    print("Selected points:", click_positions)

def auto_clicker():
    global stop_flag
    print("Starting auto clicker... Press ESC to stop.")
    
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            while not stop_flag:
                for pos in click_positions:
                    if stop_flag:
                        break
                    pyautogui.click(pos[0], pos[1])
                    print(f"Clicked: {pos}")
                    time.sleep(click_delay)
        except KeyboardInterrupt:
            pass
        finally:
            print("Auto clicker stopped.")

if __name__ == "__main__":
    get_click_positions()
    auto_clicker()
