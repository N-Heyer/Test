import pyautogui
import keyboard
import time

# List to store click points
click_points = []

def show_cursor_position():
    """Continuously shows cursor position until user adds points or quits."""
    print("\nMove your cursor to a position and press 'p' to save it.")
    print("Press 's' to start auto-clicking, or 'q' to quit.")
    
    while True:
        x, y = pyautogui.position()
        print(f"\rCurrent Cursor Position: {x}, {y}", end="", flush=True)
        
        if keyboard.is_pressed("p"):
            click_points.append((x, y))
            print(f"\nAdded point: {x}, {y}")
            time.sleep(0.3)  # Prevent accidental multiple entries
        
        if keyboard.is_pressed("s"):
            if not click_points:
                print("\nNo points selected! Add at least one point.")
            else:
                print("\nStarting auto-clicker...")
                return  # Exit the function to start clicking
        
        if keyboard.is_pressed("q"):
            print("\nExiting...")
            exit()

def auto_clicker():
    """Clicks at saved locations until 'q' is pressed."""
    print("Press 'q' to stop the auto-clicker.")
    time.sleep(2)

    while True:
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(0.1)  # Short delay to avoid issues
            
        if keyboard.is_pressed("q"):
            print("\nAuto-clicker stopped.")
            break

if __name__ == "__main__":
    show_cursor_position()  # Gather points first
    auto_clicker()
