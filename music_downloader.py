###################################################################################
###     Author:         Tim Hanson                                              ###
###     Date:           06/16/2017                                              ###
###     Title:          Music Downloader                                        ###
###     Description:    Uses selenium and pytaglib  to download and convert     ###
###                 soundcloud music to mp3 files and tags them accordingly.    ###
###                 Also adds cover art after downloading from cover art        ###
###                 download site for each song.                                ###
###################################################################################


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import taglib
import json
import sys, os
from json_maker import JsonMaker

CONVERTER_URL = 'http://clipconverter.cc'
FORM_NAME = 'converter'
URL_ELEMENT = 'mediaurl'
SUBMIT_ELEMENT = 'submit'

def download_music(media_url, browser):
    browser.get(CONVERTER_URL)
    elem = browser.find_element_by_name(URL_ELEMENT)
    elem.send_keys(media_url)
    elem.send_keys(Keys.RETURN)


    wait = WebDriverWait(browser, 10)
    submit = wait.until(EC.visibility_of_element_located((By.ID, 'submitconvert')))

    button = submit.find_element_by_css_selector('input')
    button.click()

    wait = WebDriverWait(browser, 10)
    download = wait.until(EC.visibility_of_element_located((By.ID, 'downloadbutton')))
    download.click()

    new = browser.find_element_by_link_text('Convert another video')
    new.click()

def setup_browser():
    options = webdriver.ChromeOptions()
    cur_path = os.getcwd();
    prefs = {'download.default_directory' : '{}/media'.format(cur_path)}
    options.add_experimental_option('prefs',prefs)
    chromedriver = 'chromedriver'
    return webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

def parse_json_and_tag_files(json_file):
    json_string = open(json_file).read()
    json_object = json.loads(json_string)
    for song in json_object:
        song_data = json_object[song]
        



def main():
    download_music('https://soundcloud.com/lucianofficial/lucian-do-my-thing-ft-philosofie', setup_browser())

if __name__ == '__main__':
    main()

        
   

