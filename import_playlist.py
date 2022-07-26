# Creates a plex playlist by searching for songs in a text file
# Tool by Andy Wallace

# Drawing heavily from this exmaple
# https://gist.github.com/JonnyWong16/2607abf0e3431b6f133861bbe1bb694e

# API Docs
# https://python-plexapi.readthedocs.io/en/latest/index.html


import requests
import xmltodict
from plexapi.server import PlexServer
import urllib3  #for turning off warnings

import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #turn off warnings
    
def main():

    SEPARATOR = ' | '

    PLEX_URL = 'http://localhost:32400'
    PLEX_TOKEN = 'UNKOWN'

    INPUT_SOURCE = 'playlist.txt'
    PLAYLIST_NAME = 'New Playlist'

    USE_EXACT = False #if true, all fields must exactly match. Typically should only be used if you got the list from your own library

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

            #input
            if arg == '-input' or arg == '-i':
                INPUT_SOURCE = sys.argv[i+1]
                i += 1

            #playlist name
            if arg == '-name' or arg == '-n':
                PLAYLIST_NAME = sys.argv[i+1]
                i += 1

            #exact match
            if arg == '-exact' or arg == '-e':
                USE_EXACT = True

            #advance arguments
            i += 1


    print("playlist name: ",PLAYLIST_NAME)
    print("pulling from:",INPUT_SOURCE)
    print("exact match only: ",USE_EXACT)

    search_targets = []

    #process the txt file
    input_file = open(INPUT_SOURCE, 'r')
    lines = input_file.readlines()
    for line in lines:
        parts = line.strip().split(SEPARATOR)
        search_targets.append(parts)


    print("looking for ",len(search_targets)," songs")
    print("  ... give me a second")

    #setup Plex
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    plex_playlists = {playlist.title: playlist.items() for playlist in plex.playlists()}
    music = plex.library.section('Music')

    #keep track of what we find and what we miss
    items_to_add = []
    missing_items = []

   
    for target in search_targets:
        found_track = False

        track_title = target[1]
        artist = target[0]
        album = target[2]

        songs = music.searchTracks(title=track_title)
        
        #exact search - all fields must match
        if USE_EXACT == True:
            for obj in songs:
                if obj.title == track_title and obj.parentTitle == album and obj.grandparentTitle == artist:
                    items_to_add.append(obj)
                    found_track = True
                    print("add:",obj.title,SEPARATOR,obj.grandparentTitle,SEPARATOR,obj.parentTitle)

        #loose search
        else:
            #if there's nothing we can't do anything
            if len(songs) == 0:
                found_track = False
            #if there is only one, add it
            elif len(songs) == 1 :
                this_song = songs[0]
                items_to_add.append(this_song)
                found_track = True
                print(len(items_to_add),":",this_song.title,SEPARATOR,this_song.grandparentTitle,SEPARATOR,this_song.parentTitle)

            #if there are multiple, narrow it down
            else:
                # print("🔎 search:",track_title.lower(),SEPARATOR,artist.lower(),SEPARATOR,album.lower())
                # print("  initial results: ",len(songs))
                match_levels = []
                for x in range(4):
                    match_levels.append([])

                for obj in songs:
                    #print("   compare:",obj.title.lower(),SEPARATOR,obj.grandparentTitle.lower(),SEPARATOR,obj.parentTitle.lower())
                    matches = 0
                    if obj.grandparentTitle.lower() == artist.lower():
                        matches = matches + 1 
                    if obj.title.lower() == track_title.lower():
                        matches = matches + 1 
                    if obj.parentTitle.lower() == album.lower():
                        matches = matches + 1

                    #print("    match level:",matches)
                    if matches > 0 :
                        match_levels[matches].append(obj)

                #starting with the highest match value, go backwards and add the first tier we find
                for level in reversed(match_levels):
                    if len(level) > 0:
                        if len(level) > 1:
                            print("⚠️ ",len(level)," possible tracks found for ",track_title,SEPARATOR,artist," adding all")
                        for song in level:
                            items_to_add.append(song)
                            found_track = True
                            print(len(items_to_add),":",song.title,SEPARATOR,song.grandparentTitle,SEPARATOR,song.parentTitle)
                        break

        if found_track == False:
            print("❗️could not find:",target[1],SEPARATOR,target[0],SEPARATOR,target[2])
            missing_items.append(target)


    print(" ")
    print("Found ",len(items_to_add)," out of ",len(search_targets)," target items")

    print(" ")
    print("Could not find ",len(missing_items)," items")
    for missing in missing_items:
        print("❗️could not find:",missing[1],SEPARATOR,missing[0],SEPARATOR,missing[2])

    print(" ")
    print("making playlist ",PLAYLIST_NAME," with ",len(items_to_add)," songs")
    
    # create a new playlist
    music.createPlaylist(PLAYLIST_NAME,items_to_add,False)

    return

if __name__ == "__main__":
    main()
