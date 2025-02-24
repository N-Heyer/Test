import pyautogui
import time
import sys
import Quartz
import threading

click_points = []  # Stores saved click positions
start_clicking = False  # Flag to start auto-clicking

def key_callback(proxy, event_type, event, refcon):
    """Handles keypress events using Quartz."""
    global start_clicking
    key_code = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)

    # macOS Key Codes: 35 = 'p', 1 = 's', 12 = 'q'
    if key_code == 35:  # 'p' Key
        x, y = pyautogui.position()
        click_points.append((x, y))
        print(f"\nAdded point: {x}, {y}")

    elif key_code == 1:  # 's' Key
        if not click_points:
            print("\nNo points selected! Add at least one point.")
        else:
            print("\nStarting auto-clicker...")
            start_clicking = True
            return None  # Stop key listener

    elif key_code == 12:  # 'q' Key
        print("\nExiting...")
        sys.exit()

    return event

def listen_for_keys():
    """Listens for keypress events on macOS using Quartz."""
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")

    event_mask = Quartz.kCGEventKeyDown
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        Quartz.kCGEventTapOptionDefault,
        event_mask,
        key_callback,
        None
    )

    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    Quartz.CFRunLoopAddSource(Quartz.CFRunLoopGetCurrent(), run_loop_source, Quartz.kCFRunLoopCommonModes)
    Quartz.CGEventTapEnable(tap, True)
    Quartz.CFRunLoopRun()

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("\nPress 'q' to stop the auto-clicker.")

    while True:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)
        
        # Stop if 'q' is pressed
        if start_clicking is False:
            break

if __name__ == "__main__":
    key_listener_thread = threading.Thread(target=listen_for_keys)
    key_listener_thread.start()

    while True:
        if start_clicking:
            auto_clicker()
            break
