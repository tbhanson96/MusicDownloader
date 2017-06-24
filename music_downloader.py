###################################################################################
###     Author:         Tim Hanson                                              ###
###     Date:           06/16/2017                                              ###
###     Title:          Music Downloader                                        ###
###     Description:    Uses selenium and mutagen to download and convert       ###
###                 soundcloud music to mp3 files and tags them accordingly.    ###
###                 Also adds cover art after downloading from cover art        ###
###                 download site for each song.                                ###
###################################################################################


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import json
import sys, os, shutil, glob
from json_maker import JsonMaker

CONVERTER_URL = 'http://clipconverter.cc'
COVER_DOWNLOAD_URL = 'http://soundcloudcoverdownloader.pe.hu'

def download_music(media_url, browser):
    browser.get(CONVERTER_URL)
    elem = browser.find_element_by_name('mediaurl')
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

    while glob.glob('*.crdownload'):
        pass

def download_cover_art(media_url, browser):
    browser.get(COVER_DOWNLOAD_URL)
    url_input = browser.find_element_by_id('query_input')
    url_input.send_keys(media_url)

    submit_button = browser.find_element_by_css_selector('button.sccdgreen')
    submit_button.click()

    wait = WebDriverWait(browser, 10)
    wait.until(EC.visibility_of_element_located((By.ID, 'psongname')))
    download = browser.find_element_by_css_selector('img.responsive-img')
    download.click()

    while glob.glob('*.crdownload'):
        pass

    
def setup_browser():
    options = webdriver.ChromeOptions()
    cur_path = os.getcwd();
    prefs = {'download.default_directory' : '{}/media'.format(cur_path)}
    options.add_experimental_option('prefs',prefs)
    chromedriver = 'chromedriver'
    return webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

def tag_media(media_file_name, cover_file_name, tag_dict):
    media_file = MP3(media_file_name, ID3=ID3)
    if not media_file.tags:
        media_file.add_tags()
    media_file.tags.add(TIT2(encoding=3, text=tag_dict['TITLE']))
    media_file.tags.add(TPE1(encoding=3, text=tag_dict['ARTIST']))
    media_file.tags.add(TALB(encoding=3, text=tag_dict['TITLE']))
    
    media_file.tags.add(APIC(
                    encoding=3,
                    mime='image/'+cover_file_name.split('.')[1],
                    desc='Cover',
                    data=open(cover_file_name).read()
                    )
    )

    media_file.save()
    print media_file.tags
    new_file_name = tag_dict['ARTIST'] + ' - ' + tag_dict['TITLE'] + '.mp3'
    shutil.move(media_file_name, new_file_name)


def main():
    tag_file = open('music.json')
    json_tags = json.load(tag_file)
    chrome = setup_browser()

    os.chdir('media')
    for entry in json_tags:
        media_url = entry
        media_tags = json_tags[entry]
        download_music(media_url, chrome)
        media_file_name = max([f for f in os.listdir('.')], key=os.path.getctime)
        download_cover_art(media_url, chrome)
        cover_file_name = max([f for f in glob.glob('*')], key=os.path.getctime)
        chrome.close()
        tag_media(media_file_name, cover_file_name, media_tags)
    

if __name__ == '__main__':
    main()


