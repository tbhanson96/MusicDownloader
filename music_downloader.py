###################################################################################
###     Author:         Tim Hanson                                              ###
###     Date:           06/16/2017                                              ###
###     Title:          Music Downloader                                        ###
###     Description:    Uses web crawler and web tools to download and convert  ###
###                 soundcloud music to mp3 files and tags them accordingly.    ###
###                 Also adds cover art after downloading from cover art        ###
###                 download site for each song.                                ###
###################################################################################


import mechanize
import taglib
import json
import sys

#TARGET_SONGS = sys.argv[1]
CONVERTER_URL = 'http://www.youtubeinmp3.com'
FORM_NAME = 'form'
URL_ELEMENT = 'video'
SUBMIT_ELEMENT = 'submit'
songname = 'https://www.youtube.com/watch?v=kffacxfA7G4'

br = mechanize.Browser()

br.open(CONVERTER_URL)
br.select_form(id=FORM_NAME)
mediaurl = br.form.find_control(id=URL_ELEMENT)
mediaurl.value = songname
res = br.submit()

print res.read()




