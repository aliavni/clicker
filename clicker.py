import os
from time import sleep

import dearpygui.dearpygui as dpg
import pyautogui
from pynput import keyboard
from pynput.keyboard import Key

dpg.create_context()

VIEWPORT_HEIGHT = 100
VIEWPORT_WIDTH = 320

PRESSED_KEY = None
START_CLICK_DELAY_SECONDS = 3

CLICK_BUTTON_IDENTIFIER = "__click_button"
CLICK_BUTTON_LABEL = "Start clicking"

CLICKS_PER_SECOND_IDENTIFIER = "__clicks_per_second"

FONT_PATH = os.path.join(os.path.dirname(__file__), "assets/MonaspaceArgon-Regular.otf")

with dpg.font_registry():
    default_font = dpg.add_font(FONT_PATH, 20)
    small_font = dpg.add_font(FONT_PATH, 15)


def get_clicks_per_second():
    clicks_per_second_string = dpg.get_value(CLICKS_PER_SECOND_IDENTIFIER)
    clicks_per_second = float(clicks_per_second_string)

    return clicks_per_second


def start_clicking():
    global PRESSED_KEY
    global START_CLICK_DELAY_SECONDS

    delay = START_CLICK_DELAY_SECONDS
    while delay > 0:
        dpg.set_item_label(CLICK_BUTTON_IDENTIFIER, f"Starting in {delay}")
        sleep(1)
        delay -= 1

    dpg.set_item_label(CLICK_BUTTON_IDENTIFIER, "F1 to stop")

    while PRESSED_KEY != Key.f1:
        clicks_per_second = get_clicks_per_second()
        click_delay = 1 / clicks_per_second

        mouse_x, mouse_y = pyautogui.position()
        pyautogui.click(x=mouse_x, y=mouse_y)

        sleep(click_delay)

    dpg.set_item_label(CLICK_BUTTON_IDENTIFIER, CLICK_BUTTON_LABEL)
    PRESSED_KEY = None


def start_click_callback(sender, app_data):
    start_clicking()


def on_press(key) -> None:
    global PRESSED_KEY

    PRESSED_KEY = key


with dpg.window(
    label="Primary Window",
) as primary_window:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    dpg.bind_font(default_font)

    with dpg.group(horizontal=False):
        dpg.add_input_text(
            tag=CLICKS_PER_SECOND_IDENTIFIER,
            label="clicks per second",
            default_value="200",
            decimal=True,
            width=80,
            hint="Clicks per second",
        )
        dpg.add_button(
            tag=CLICK_BUTTON_IDENTIFIER,
            label=CLICK_BUTTON_LABEL,
            callback=start_click_callback,
        )

    with dpg.group(horizontal=False):
        info = dpg.add_text(
            default_value="(F1) Stop clicking",
        )
        dpg.bind_item_font(info, small_font)

dpg.create_viewport(
    title="Clicker",
    width=VIEWPORT_WIDTH,
    height=VIEWPORT_HEIGHT,
    resizable=False,
    small_icon="./assets/icon_64.ico",
    large_icon="./assets/icon_256.ico",
)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window(primary_window, True)
dpg.start_dearpygui()
dpg.destroy_context()
