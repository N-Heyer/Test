import pygame
import sys
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Listener as KeyboardListener, Key
import time
import threading
import signal

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 700, 500
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Auto Clicker *use arrow keys')

# Colors and Font
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
BLACK = (0, 0, 0)
RED = (255,0,0)
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Menu options
options = ['Start Auto Clicker', 'Change Input Key', 'Change How Fast', 'Exit']
selected_option = 0

# Initialize mouse and keyboard controllers
mouse = MouseController()
keyboard_ctrl = KeyboardController()

# Auto-clicker settings
auto_click = False
click_interval = 0.1  # Default click speed
auto_key = 'left'  # Default to left mouse button

def toggle_auto_clicker():
    global auto_click
    auto_click = not auto_click

def change_key():
    global auto_key
    waiting_for_key = True
    while waiting_for_key:
        screen.fill(BLACK)
        prompt_text = small_font.render("Press a key to set for auto-click", True, RED)
        screen.blit(prompt_text, (100, 250))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                auto_key = event.unicode  # Set the key to whatever was pressed
                waiting_for_key = False

def change_interval():
    global click_interval
    waiting_for_input = True
    input_string = ""
    while waiting_for_input:
        screen.fill(WHITE)
        prompt_text = small_font.render("Enter interval (seconds):", True, BLACK)
        interval_text = font.render(input_string, True, BLACK)
        screen.blit(prompt_text, (100, 200))
        screen.blit(interval_text, (100, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        click_interval = float(input_string)
                        waiting_for_input = False
                    except ValueError:
                        input_string = ""  # Reset on invalid input
                elif event.key == pygame.K_BACKSPACE:
                    input_string = input_string[:-1]
                else:
                    input_string += event.unicode

# Signal handler to stop the program with Ctrl + C
def signal_handler(sig, frame):
    print("Program terminated.")
    pygame.quit()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)  # Attach signal handler

# Global keyboard listener to stop auto-clicker on 'Esc'
def on_press(key):
    global auto_click
    if key == Key.esc:
        auto_click = False
        print("Auto-clicker stopped by 'Esc' key")

listener = KeyboardListener(on_press=on_press)
listener.start()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size to the new window size
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

        # Handle key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and selected_option > 0:
                selected_option -= 1
            elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                selected_option += 1
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Auto Clicker
                    toggle_auto_clicker()
                elif selected_option == 1:  # Change Key
                    change_key()
                elif selected_option == 2:  # Change Interval
                    change_interval()
                elif selected_option == 3:  # Exit
                    running = False


    # Auto-clicker logic
    if auto_click:
        if auto_key == 'left':
            mouse.click(Button.left)
        elif auto_key == 'right':
            mouse.click(Button.right)
        else:
            keyboard_ctrl.press(auto_key)
            keyboard_ctrl.release(auto_key)
        time.sleep(click_interval)  # Wait for the specified interval

    # Draw the menu
    screen.fill(BLACK)
    for index, option in enumerate(options):
        if index == selected_option:
            text = font.render(option, True, RED)
        else:
            text = small_font.render(option, True, WHITE)
        screen.blit(text, (100, 100 + index * 100))

    pygame.display.flip()

# Quit Pygame and stop the listener
listener.stop()
pygame.quit()
sys.exit()
