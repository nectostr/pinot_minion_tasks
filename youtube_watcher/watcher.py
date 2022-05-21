"""
Module responsible for starting and ending selenium based chrome and viewing the video
"""


from returns.result import Result, Success, Failure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import re
import time
from typing import List


CHROME_DRIVER_PATH = r"L:\Users\nectostr\PycharmProjects\pinot_minion_tasks\extensions\chromedriver.exe"

ADDBLOCK_PATH = r"L:\Users\nectostr\PycharmProjects\pinot_minion_tasks\extensions\5.1.9.1_0"
    #r"L:\Users\nectostr\PycharmProjects\pinot_minion_tasks\extensions\5.1.9.1_0.crx"

STARTFORNERDS_PATH = r"L:\Users\nectostr\PycharmProjects\pinot_minion_tasks\extensions\chrome_extension"
#r"../extensions/chrome_extension"

def extract_qualities(text: str) -> List[int]:
    """
    Extracts numbers from specific youtube window menu text
    :param text: string with options from youtube menu
    :return: parsed numeric list
    """
    # Because of how youtube quality menu created
    lines = text.split("\n")[1:-1]

    nums = [int(s[:s.find("p")]) for s in lines]
    return nums

def find_closes(options: List[int], goal: int) -> int:
    """
    Accepts unsorted list of options and fins the index of closest to the goal option
    :param options:
    :param goal:
    :return: index of closest option
    """
    sorted_options = sorted(options)
    for ind, opt in enumerate(sorted_options):
        if opt >= goal:
            if ind > 0 and (goal - sorted_options[ind - 1] < opt - goal):
                return options.index(sorted_options[ind - 1])
            else:
                return options.index(opt)
    return options.index(opt)

def watch(url: str, how_long: int = 100, quality: int = None) -> Result[str, str]:
    """
    Function that completes the task of:
    1. Starting the chrome from selenium
    2. Adding the extensions to chrome (on start)
      2.1. AddBlock extension to avoid advertisement
      2.2. JS extension to collect StatsForNerds
    3. Stops Chrome by timeout
    :param url: valid http/s youtube url to video
    :param how_long: seconds, for timeout of video viewing. None for "till the end of video"
    :param quality: None for auto, int ~240-1024 for specific quality selection
    :return: 1 for success
    """
    # if not (quality is None):
    #     raise NotImplementedError(f"Quality selection not implemented yet,"
    #                               f" use None for automatic quality selection")

    if how_long is None:
        raise NotImplementedError(f'"Till the end" viewing option is not implemented yet,'
                                  f'use seconds in int')

    url_pattern = r"^https?://www.youtube.com/watch?.*"
    if not re.fullmatch(url_pattern, url):
        return Failure("Url does not much youtube video url")

    options = Options()
    options.headless = True

    # For unpacked extension
    options.add_argument("--load-extension=" + STARTFORNERDS_PATH)
    options.add_argument("--load-extension=" + ADDBLOCK_PATH) # path to folder

    # For packed extensions
    #options.add_extension(ADDBLOCK_PATH) # path to srx
    # try:

    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

    driver.get(url)


    video = driver.find_element(By.ID, 'movie_player')

    if not (quality is None):
        settings = driver.find_element(By.CLASS_NAME, "ytp-settings-button")    #.find_elements_by_class_name("ytp-settings-button")
        settings.click()
        menu = driver.find_elements(By.CLASS_NAME, 'ytp-menuitem')
        menu[3].click()
        quality_menu = driver.find_element(By.CLASS_NAME, 'ytp-quality-menu')
        options = extract_qualities(quality_menu.text)
        index_to_select = find_closes(options, quality) + 1 # Because we cutted first "go back to menu" option
        menu = driver.find_elements(By.CLASS_NAME, 'ytp-menuitem')
        menu[index_to_select].click()

    video.send_keys(Keys.SPACE)  # hits space
    time.sleep(how_long)


    video.send_keys(Keys.SPACE)
    driver.close()

    # except BaseException as e:
    #     return Failure(str(e))


    return Success("End of video")


if __name__ == '__main__':
    print(watch("https://www.youtube.com/watch?v=ZzwWWut_ibU", 5, 480))
