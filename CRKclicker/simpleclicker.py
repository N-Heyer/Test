import time
import pyautogui
import tkinter as tk
from pynput import mouse, keyboard
from threading import Thread, Event
import sys

click_positions = []
click_delay = 10.0  # Set delay between clicks (in seconds)
initial_delay = 5.0  # Delay before clicks can be registered
recording = False
clicking = Event()  # Use Event for better thread handling

def is_inside_gui(x, y):
    """Check if the click is inside the GUI window."""
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    return root_x <= x <= root_x + root_width and root_y <= y <= root_y + root_height

def on_click(x, y, button, pressed):
    if pressed and recording:
        if not is_inside_gui(x, y):  # Ignore GUI clicks
            click_positions.append((x, y))
            update_status(f"Point added: {x}, {y}")
            listbox.insert(tk.END, f"{x}, {y}")

def on_press(key):
    if key == keyboard.Key.esc:
        clicking.clear()  # Stop auto-clicking
        update_status("Stopped by ESC key.")

def listen_for_esc():
    """Runs the keyboard listener in a separate thread."""
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def get_click_positions():
    global recording
    update_status(f"Waiting {initial_delay} seconds before recording clicks...")
    time.sleep(initial_delay)
    update_status("Recording clicks now!")
    recording = True
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    update_status("Click recording finished.")

def auto_clicker():
    clicking.set()
    update_status("Starting auto clicker... Press ESC to stop.")
    try:
        while clicking.is_set():
            for pos in click_positions:
                if not clicking.is_set():
                    break
                try:
                    pyautogui.click(pos[0], pos[1])
                    update_status(f"Clicked: {pos}")
                    time.sleep(click_delay)
                except Exception as e:
                    update_status(f"Click error: {e}")
                    print(f"Click error at {pos}: {e}", file=sys.stderr)
    finally:
        update_status("Auto clicker stopped.")

def start_recording():
    Thread(target=get_click_positions, daemon=True).start()

def start_clicking():
    if not clicking.is_set():
        Thread(target=auto_clicker, daemon=True).start()

def update_status(msg):
    status_label.config(text=msg)
    print(msg)

def stop_program():
    clicking.clear()
    update_status("Stopped auto clicker.")

# Start ESC listener in a background thread
Thread(target=listen_for_esc, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Auto Clicker")
root.geometry("500x400")

tk.Label(root, text="Auto Clicker GUI", font=("Arial", 16)).pack()
status_label = tk.Label(root, text="Waiting to start...", font=("Arialß", 10))
status_label.pack()

listbox = tk.Listbox(root, height=8)
listbox.pack()

tk.Button(root, text="Start Recording", command=start_recording).pack()
tk.Button(root, text="Start Clicking", command=start_clicking).pack()
tk.Button(root, text="Stop Clicking", command=stop_program).pack()

root.mainloop()