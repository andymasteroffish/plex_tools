# Python Plex Music Tools
Some hobbyist python tools to have fun with my Plex music library.

These are things I wrote for fun and they are definitely imperfect. Python is not my main language. Please feel free to modify this code to work for what you want to do.

This is my way of letting you know that these scripts are janky as hell. Be aware that there is pretty much no error handling here, so things might break.

Huge thanks to the folks maintaining [Python-PlexAPI](https://python-plexapi.readthedocs.io/en/latest/introduction.html)!

## Finding your Plex token

All of these tools require you to know the URL of your Plex server as well as your Plex token.

[This guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) explains how to get your token.

# Most Played (most_played.py)

This script tries to emulate the Spotify Wrapped playlist. It takes a given start date and figures out which songs in your library got the most plays during that time.

It can create a playlist with the top 100 (or however many you'd like) songs.

I don't think it factors in which user played the song, so if you have multiple people streaming from your library you may need to fiddle with the file.

If you have it make a playlist, the new playlist will just appear in your playlist tab in Plex. If you already had the page open you will have to refresh.

## Usage

`python3 most_played.py -url PLEX_URL -token YOUR_TOKEN -playlist 100 -date 22/01/01 -print`

This will get your top songs played since Jan 1 2022. A playlist will be made with the 100 most played songs. Since `-print` is included, all the songs will also be printed to the console.

## Arguments

There are a bunch of arguments. Only `-token` is strictly necessary, although it won't do much if you don't make a playlist or print the results.

| Argument | Alt | Description | Default |
|--|--|--|--|
| -url | -u | Plex URL | http://localhost:32400 |
| -token | -t | Your Plex token | none (you need this) |
| -playlist | -p | Makes a playlist of the given length | False |
| -playlist_name | -n | Name for the playlist | "Top Songs [YEAR]" |
| -date | -d | Start date. Must be in the format YEAR/MONTH/DAY | one year prior to today's date|
| -print | n/a | Prints all the info to the console | False |


# Import Playlist (import_playlist.py)

(coming soon)

Tool for reading a text file and attempting to create a playlist that matches by searching for the songs in your library.

I made this to grab my playlists from Spotify and recreate them in my Plex library
