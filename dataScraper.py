# -*- coding: utf-8 -*-


# Import Modules
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
from time import sleep
from random import randint
import validators
from cssselect.parser import parse


# Defining Some functions
# ------------------------------------------------------------------------------
# CSS Validator
def validate_css_selector(input_text):
    while True:
        selector = input(input_text)
        try:
            parse(selector)
            print("Your CSS selector looks good.")
            return selector
        except Exception:
            print("This is not a valid CSS selector. Please try again.")

# Ask for URL
while True:
    url = input("Submit the URL: ")
    if validators.url(url):
        print("That sounds like a URL...")
        break
    
    else:
        print("\nThat doesn't seems like a URL, please try again.\n") 

# Ask for CSS Selector
selector = validate_css_selector("Enter the CSS selector of Parent Page: ")


print(f"URL is {url}")
print(f"CSS Selector is {selector}")

# Check and store all instances in a list

print ("Holay! Shit just started...")
web = webdriver.Chrome()
print("Launched chrome")

web.get(url)
print("Waiting..")
input("Press Enter to continue...")


try:
    # Get the scroll height of the div
    div_scroll_height = web.execute_script("return document.getElementsByClassName('_vertical-scroll-results_1igybl')[0].scrollHeight;")
    pixels = 400
    while True:
        # Scroll down the div by the set number of pixels
        web.execute_script("document.getElementsByClassName('_vertical-scroll-results_1igybl')[0].scrollBy(0,arguments[0]);", pixels)
        time.sleep(3)
        # Get the new scroll height of the div
        new_div_scroll_height = web.execute_script("return document.getElementsByClassName('_vertical-scroll-results_1igybl')[0].scrollHeight;")
        # Check if the scroll height of the div has changed
        if new_div_scroll_height == div_scroll_height:
            break
        div_scroll_height = new_div_scroll_height
    time.sleep(5)
except:
    choice = input("CSS selector not found. Would you like to provide a new selector or ignore and continue? (provide/ignore)")
    if choice == "provide":
        new_selector = input("Please provide the new CSS selector:")
        # replace the className with the new provided selector
        div_scroll_height = web.execute_script("return document.querySelectorAll('"+new_selector+"')[0].scrollHeight;")
        pixels = 400
        while True:
            # Scroll down the div by the set number of pixels
            web.execute_script("document.querySelectorAll('"+new_selector+"')[0].scrollBy(0,arguments[0]);", pixels)
            time.sleep(3)
            # Get the new scroll height of the div
            new_div_scroll_height = web.execute_script("return document.querySelectorAll('"+new_selector+"')[0].scrollHeight;")
            # Check if the scroll height of the div has changed
            if new_div_scroll_height == div_scroll_height:
                break
            div_scroll_height = new_div_scroll_height
        time.sleep(5)
    else:
        pass

print("Checking for elements..")



elements = web.find_elements(By.CSS_SELECTOR, selector)


# Print the number of elements found
print(f"Number of elements found: {len(elements)}")


try:
    # Find the element containing the desired information
    child_selector = validate_css_selector("Enter the CSS selector of Child Page: ")

    # Open the CSV file
    with open('output.csv', mode='a',encoding='utf-8') as csv_file:
        fieldnames = ['Company Name', 'Website URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through the list of elements
        for element in elements:
            print(element.text)

            # Get the link's URL from the element
            link = element.get_attribute("href")
            # sleep(randint(5,10))

            # Open the link in a new tab
            actions = ActionChains(web)
            actions.key_down(Keys.CONTROL).click(element).key_up(Keys.CONTROL)
            actions.perform()

            # Switch to the new tab
            web.switch_to.window(web.window_handles[-1])

            # Wait for page to load
            try:
                elementb = WebDriverWait(web, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, child_selector))
                )
                # Copy the text from the desired element
                copied_text = elementb.get_attribute("href")

                # Print the copied text
                print(copied_text)

                # # Write to the CSV file
                # writer.writerow({'Company Name': element.text, 'Website URL': copied_text})

            except Exception as e:
                print(f'Error: {e}')

            # Close the new tab
            web.close()

            # Switch back to the original tab
            web.switch_to.window(web.window_handles[0])

            
            # Write to the CSV file
            writer.writerow({'Company Name': element.text, 'Website URL': copied_text})

    # Close the webdriver
    web.quit()

    print("All Done! Exiting")
except KeyboardInterrupt:
    # web.quit()
    print("Exiting")
    # exit()