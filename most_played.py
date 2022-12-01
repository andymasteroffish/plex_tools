# Most Played tool by Andy Wallace (andymakes.com)
# Goes through play hostory and makes a list of topmplayed songs in a given period

# Drawing heavily from this exmaple
# https://gist.github.com/JonnyWong16/2607abf0e3431b6f133861bbe1bb694e

# API Docs
# https://python-plexapi.readthedocs.io/en/latest/index.html
# https://python-plexapi.readthedocs.io/en/latest/modules/library.html?highlight=history#plexapi.library.Library.history

# how to get your Plex token
# https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

import requests
import xmltodict
from plexapi.server import PlexServer
import urllib3  #for turning off warnings
from datetime import datetime, timedelta, date
import sys



class SongInfo:
    def __init__(self, id, title, album, artist, duration, raw_info):
        self.id = id
        self.title = title
        self.album = album
        self.artist = artist
        self.duration = duration
        self.raw_info = raw_info
        self.play_count = 1

class ArtistInfo:
    def __init__(self, name):
        self.name = name
        self.play_count = 0
        self.total_duration = 0


def main():

    PLEX_URL = 'http://localhost:32400'
    PLEX_TOKEN = 'UNKOWN'

    MAKE_PLAYLIST = False
    PLAYLIST_NAME = ""
    PLAYLIST_SIZE = 100

    PRINT_INFO = False

    #default is 365 days in the past
    start_datetime = datetime.now() - timedelta(days = 365)

    #look at arguments
    if (len(sys.argv) >= 1):
        i=1
        while i < len(sys.argv):
            arg = sys.argv[i]

            #URL
            if arg == '-url' or arg == '-u':
                PLEX_URL = sys.argv[i+1]
                i += 1

            #Token
            if arg == '-token' or arg == '-t':
                PLEX_TOKEN = sys.argv[i+1]
                i += 1

            #playlist
            if arg == '-playlist' or arg == '-p':
                MAKE_PLAYLIST = True
                PLAYLIST_SIZE = int(sys.argv[i+1])
                i += 1

            #playlist name
            if arg == '-playlist_name' or arg == '-n':
                PLAYLIST_NAME = sys.argv[i+1]
                i += 1

            #date
            if arg == '-date' or arg == '-d':
                start_datetime = datetime.strptime(sys.argv[i+1], '%y/%m/%d')
                i += 1

            #printing info
            if arg == '-print':
                PRINT_INFO = True

            #advance arguments
            i += 1
        
    print('url: '+PLEX_URL)
    print('token: ' + PLEX_TOKEN)

    print("make playlist: ",MAKE_PLAYLIST)
    if MAKE_PLAYLIST:
        print("playlist length: ",PLAYLIST_SIZE)

    print("start date: ",start_datetime.strftime('%Y-%m-%d %H:%M:%S'))


    all_songs = []
    all_artists = []
    playlist_test = []

    #default name if the playlist name is still blank
    if len(PLAYLIST_NAME) == 0:
        PLAYLIST_NAME = "Top Songs " + str(start_datetime.year)

    print("searching...")

    #contact plex
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    music = plex.library.section('Music')
    history = music.history(9999999, start_datetime)

    print("tallying... (this might take a while)")
    #check each item in the history
    for item in history:
        # check if there is a match in our list
        match_found = False
        for song in all_songs:
            if song.id == item.ratingKey:
                song.play_count += 1
                match_found = True

        #make a new entry if there were no matches
        if match_found == False:
            all_songs.append( SongInfo(item.ratingKey, item.title, item.parentTitle, item.grandparentTitle, item.duration, item))
            playlist_test.append(item)

        #check for the artist
        artist_found = False
        for artist in all_artists:
            if artist.name == item.grandparentTitle:
                #sometimes duration is a bad value. we want to skip anything that is not an int
                if type(item.duration) == type(1):
                    #print("   add to artist ",item.grandparentTitle)
                    artist.play_count += 1
                    artist.total_duration += item.duration
                    artist_found = True
                # else:
                #     print("  no duraiton value for ",item.title)
                

        #make a new entry if we did not find the artist
        if artist_found == False:
            #print("create artist ",item.grandparentTitle)
            all_artists.append( ArtistInfo(item.grandparentTitle))

    print("sorting...")



    #sort
    all_songs.sort(key=lambda x: x.play_count, reverse=True)
    all_artists.sort(key=lambda x: x.total_duration, reverse=True)

    #spit it to the console if we want to
    if PRINT_INFO:
        print('Top 100 Songs:')
        count = len(all_songs[:100])
        for song in reversed(all_songs[:100]):
            print("#",str(count),": ",song.artist," - ", song.title," (",str(song.play_count)," plays)", sep='')
            count -= 1


        print(" ")
        print("Top 10 Artists:")
        count = len(all_artists[:10])
        for artist in reversed(all_artists[:10]):
            seconds = artist.total_duration / 1000
            hours = 0
            minutes = 0
            while seconds >= 3600:
                hours += 1
                seconds -= 3600
            
            while seconds >= 60:
                minutes += 1
                seconds -= 60
            print("#",str(count),": ",artist.name," - ", str(hours)," hours, ",str(minutes)," minutes", sep='')
            count -= 1
        
        print(" ")


    ## try making a playlist ##
    if MAKE_PLAYLIST:
        print("making playlist")

        #grab the first X items
        trim_list = all_songs[0:PLAYLIST_SIZE]

        playlist_songs = []
        for song in trim_list:
            # if PRINT_INFO:
            #     print(song.artist," - ", song.title,": ",song.play_count)
            playlist_songs.append(song.raw_info)

        #create the playlist
        music.createPlaylist(PLAYLIST_NAME,playlist_songs,False)
        print("made playlist: ",PLAYLIST_NAME)
        print(" ")

    print("done")
    print("found ",len(history)," songs played in the given period",  sep='')
    return

if __name__ == "__main__":
    main()
