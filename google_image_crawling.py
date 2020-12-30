from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # calling selenium libraries
import time
from datetime import datetime
import urllib.request
import os

url = "https://www.google.ca/imghp?hl=en&tab=wi&ogbl"
search_input = input("Enter keyword to search: ")
driver = webdriver.Chrome()  # Call chromedriver and store it in variable 'driver'
now = datetime.now()
current_time = now.strftime("%Y_%D_%H_%M_%S")
cwd = os.getcwd()
path = os.path.join(cwd, current_time + "_" + search_input)

SCROLL_PAUSE_TIME = 1  # Time pause between scrolls
IMAGE_PAUSE_TIME = 1.5  # Time pause after clicking an image
SCROLL_IMAGE = 50  # Number of images Chrome loads at one scrolling
IMAGE_LIMIT = 100  # Maximum number of images to download


def scroll_down():
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    while True:
        if scroll_count >= IMAGE_LIMIT // SCROLL_IMAGE:
            break

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        scroll_count += 1

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # When scroll reached to the bottom
        if new_height == last_height:

            try:
                # Click "Show more results" button at the bottom
                driver.find_element_by_css_selector('.mye4qd').click()

            except:
                # Stop scrolling if there's no more image to load
                break
        last_height = new_height


def save_images(images: list):
    count = 1
    for image in images:
        print(f"Scrawling {count}th link... ")
        try:
            image.click()
            time.sleep(IMAGE_PAUSE_TIME)
            img_url = driver.find_element_by_css_selector('.n3VNCb').get_attribute("src")
            urllib.request.urlretrieve(img_url, f"{path}/{search_input}_{count}.jpg")
        except:
            print(f"error has occurred at {count}th link")
        finally:
            count += 1
            if count > IMAGE_LIMIT:
                break


def google_scrawl_main():
    driver.get(url)
    elem = driver.find_element_by_name("q")  # Find searching input area using html name tag
    elem.send_keys(search_input)  # Type search_input to element
    elem.send_keys(Keys.RETURN)  # Enter ' ' key
    scroll_down()
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    os.makedirs(path)
    save_images(images)
    driver.close()


def init():
    google_scrawl_main()


if __name__ == '__main__':
    init()
