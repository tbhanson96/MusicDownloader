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

TARGET_SONGS = sys.argv[1]

br = mechanize.Browser()

br.open('http://clipconverter.cc')
br.select_form(id='converter')
mediaurl = br.form.find_control(name='mediaurl')
mediaurl.value = 'https://www.youtube.com/watch?v=ZiXQG6A4itE'
res = br.submit()

print TARGET_SONGS
song = taglib.File('blank.mp3')
print song.tags


