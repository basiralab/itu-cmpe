# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# @ Filename: methods
# @ Date: 12-Dec-2020
# @ AUTHOR: batuhanfaik
# @ Copyright (C) 2020 Batuhan Faik Derinbay
# @ Project: hw3
# @ Description: Useful static methods
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pyautogui
import time

from common.exceptions import GameNotInitiatedCorrectly, GameSizeNotCorrect


def get_resolution():
    w, h = pyautogui.size()
    # If the width is more than twice the height there probably are multiple monitors
    # For more than two monitors, the code is likely to fail
    if w / h > 2 / 1:
        w //= 2
    return w, h


def center_of_button_on_screen(button_img_path, button_name=""):
    button = pyautogui.locateOnScreen(button_img_path)
    if not button:
        raise GameNotInitiatedCorrectly("Couldn't locate the {} button!".format(button_name))
    else:
        return pyautogui.center(button)


def prepare_web_game(secs=5):
    mode = 0
    if not pyautogui.locateOnScreen("assets/fullscreen-button.png"):
        print("Waiting for the user to prepare the game and click 'OK'")
        pyautogui.alert(text="Please launch the game within the next {} seconds.".format(secs),
                        title="Game is not ready!", button='OK')
        time.sleep(secs)
        print("Resuming")
        if not pyautogui.locateOnScreen("assets/fullscreen-button.png"):
            fs_mode = pyautogui.confirm(
                text="There seems to be a problem when locating the fullscreen button. Would you "
                     "like to manually put the game in fullscreen mode or try locating the "
                     "fullscreen button?",
                title="Mode Selection",
                buttons=['Fullscreen Manually', 'Try Again'])
            if "Fullscreen Manually" == fs_mode:
                pyautogui.alert(
                    text="Game should be put into fullscreen mode manually. Failure to do so "
                         "within {} seconds will cause the program to malfunction, and likely "
                         "crash. Do you acknowledge?".format(secs),
                    title="Fullscreen Alert", button='Yes')
                print("OK! Waiting for the user to put the game in "
                      "fullscreen mode for {} seconds.".format(secs))
                time.sleep(secs)
                print("Resuming")
                mode = 1
            else:
                print("OK! Retrying within {} seconds.".format(secs))
                time.sleep(secs)
                print("Resuming")
                if not pyautogui.locateOnScreen("assets/fullscreen-button.png"):
                    raise GameNotInitiatedCorrectly()
    return mode


def go_to_page(page_name, mode=0):
    if not mode:
        fullscreen_button = center_of_button_on_screen("assets/fullscreen-button.png", "fullscreen")
        pyautogui.click(fullscreen_button)
    time.sleep(4)  # Wait until fullscreen notification is closed

    game_size = get_resolution()
    game_region = (0, 0, game_size[0], game_size[1])

    all_shapes_coords = (int(game_size[0] * 0.97), int(game_size[1] * 0.17))
    vabank_coords = (int(game_size[0] * 0.97), int(game_size[1] * 0.27))
    shame_coords = (int(game_size[0] * 0.97), int(game_size[1] * 0.38))

    if page_name == "All-Shapes":
        button = all_shapes_coords
    elif page_name == "Vabank":
        button = vabank_coords
    elif page_name == "Shame":
        button = shame_coords
    else:
        raise Exception("Button is not valid")

    pyautogui.click(button)
    time.sleep(0.25)  # Wait until shapes appear

    return game_region


def back_to_original_state():
    game_size = get_resolution()
    back_coords = (int(game_size[0] * 0.97), int(game_size[1] * 0.95))
    pyautogui.click(back_coords)
    pyautogui.press("esc")
    pyautogui.press("esc")
