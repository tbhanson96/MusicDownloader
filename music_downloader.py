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
import sys, os, shutil, glob, time
from json_maker import JsonMaker

CONVERTER_URL = 'http://clipconverter.cc'
COVER_DOWNLOAD_URL = 'http://soundcloudcoverdownloader.pe.hu'
TAG_FILE = 'to_add.json'

def download_music(media_url, browser):
    browser.get(CONVERTER_URL)
    elem = browser.find_element_by_name('mediaurl')
    elem.send_keys(media_url)
    elem.send_keys(Keys.RETURN)


    wait = WebDriverWait(browser, 15)
    submit = wait.until(EC.visibility_of_element_located((By.ID, 'submitconvert')))

    button = submit.find_element_by_css_selector('input')
    button.click()

    wait = WebDriverWait(browser, 15)
    download = wait.until(EC.visibility_of_element_located((By.ID, 'downloadbutton')))

    download.click()

    #new = browser.find_element_by_link_text('Convert another video')
    #new.click()


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

 
def setup_browser():
    options = webdriver.ChromeOptions()
    cur_path = os.getcwd();
    prefs = {'download.default_directory' : cur_path + '/media/download'}
    options.add_experimental_option('prefs',prefs)
    chromedriver = 'chromedriver'
    return webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

def tag_media(media_file_name, cover_file_name, tag_dict):
    media_file = MP3(media_file_name, ID3=ID3)
    if not media_file.tags:
        media_file.add_tags()
    media_file.tags.add(TIT2(encoding=3, text=tag_dict['title']))
    media_file.tags.add(TPE1(encoding=3, text=tag_dict['artist']))
    album_tag = (tag_dict['album'] if tag_dict.has_key('album') else tag_dict['title']+' - single')
    media_file.tags.add(TALB(encoding=3, text=album_tag))
    
    media_file.tags.add(APIC(
                    encoding=3,
                    mime='image/'+cover_file_name.split('.')[-1],
                    desc='Cover',
                    data=open(cover_file_name).read()
                    )
    )

    media_file.save()

def loading_bar(current, total):
    new_bar = '\r['
    for i in xrange(current):
        new_bar += '=' 
    new_bar += '>'
    for i in xrange(total - current):
        new_bar += '_'  
    new_bar += ']'
    return new_bar


def find_and_move_file(path, extension, new_files_name):
    files_to_search = path + '/*.' + extension
    return_files = []
    while not return_files:
        return_files = glob.glob(files_to_search)

    return_file_name = return_files[0]
    os.rename(return_file_name, '{}.{}'.format(new_files_name, extension))
    return '{}.{}'.format(new_files_name, extension)
    

def main():
    print 'Initializing Selenium and starting download...'

    tag_file = open(TAG_FILE)
    json_tags = json.load(tag_file)
    chrome = setup_browser()
    log_file = open('log.txt', 'w')

    if not os.path.exists('media'):
        os.mkdir('media')
    os.chdir('media')

    num_finished = 0
    print loading_bar(num_finished, len(json_tags.keys())),
    for entry in json_tags:
        media_url = entry
        media_tags = json_tags[entry]
        new_files_name = '{} - {}'.format(media_tags['artist'], media_tags['title'])

        if os.path.exists(new_files_name+'.mp3'):
            log_file.write('skipped {}\n'.format(new_files_name))
            num_finished += 1
            print loading_bar(num_finished, len(json_tags.keys())),
            continue

        download_music(media_url, chrome)
        media_file_name = find_and_move_file('download', 'mp3', new_files_name)
        download_cover_art(media_url, chrome)
        cover_file_name = find_and_move_file('download', 'jpg', new_files_name)
        tag_media(media_file_name, cover_file_name, media_tags)

        log_file.write('completed: {}\n'.format(new_files_name))        
        num_finished += 1
        print loading_bar(num_finished, len(json_tags.keys())),

    chrome.close()
    

if __name__ == '__main__':
    main()


