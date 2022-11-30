# Python Plex Music Tools
Some hobbyist python tools to have fun with my Plex music library.

These are things I wrote for fun and they are definitely imperfect. Python is not my main language. Please feel free to modify this code to work for what you want to do.

This is my way of letting you know that these scripts are janky as hell. Be aware that there is pretty much no error handling here, so things might break.

Huge thanks to the folks maintaining [Python-PlexAPI](https://python-plexapi.readthedocs.io/en/latest/introduction.html) & to [JonnyWong16](https://gist.github.com/JonnyWong16) for [this script](https://gist.github.com/JonnyWong16/2607abf0e3431b6f133861bbe1bb694e) that is the basis for my tools!

## Finding your Plex token

All of these tools require you to know the URL of your Plex server as well as your Plex token.

[This guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) explains how to get your token.

# Most Played (most_played.py)

This script tries to emulate the Spotify Wrapped playlist. It takes a given start date and figures out which songs in your library got the most plays during that time.

It can create a playlist with the top 100 (or however many you'd like) songs. It can also print out your top 10 artists by duration.

I don't think it factors in which user played the song, so if you have multiple people streaming from your library you may need to fiddle with the file.

If you have it make a playlist, the new playlist will just appear in your playlist tab in Plex. If you already had the page open you will have to refresh.

It will take a while to count up all of your plays for the year (could easily be 10 minutes), so give it some time if you're doing a full year. At some point I should optimize this at all.

## Usage

`python3 most_played.py -url PLEX_URL -token YOUR_TOKEN -playlist 100 -date 22/01/01 -print`

This will get your top songs played since Jan 1 2022. A playlist will be made with the 100 most played songs. Since `-print` is included, all the songs and play counts will also be printed to the console along with the 10 most played artists.

## Arguments

There are a bunch of arguments. Only `-token` is strictly necessary, although it won't do much if you don't make a playlist or print the results.

| Argument | Alt | Description | Default |
|--|--|--|--|
| -url | -u | Plex URL | http://localhost:32400 |
| -token | -t | Your Plex token | none (you need this) |
| -playlist | -p | Makes a playlist of the given length | False |
| -playlist_name | -n | Name for the playlist | "Top Songs [YEAR]" |
| -date | -d | Start date. Must be in the format YEAR/MONTH/DAY (year should only have 2 digits)| one year prior to today's date|
| -print | n/a | Prints all the info to the console | False |


# Import Playlist (import_playlist.py)

Tool for reading a text file and attempting to create a playlist that matches by searching for the songs in your library.

I made this to grab my playlists from Spotify and recreate them in my Plex library.

This does not add music to your library. It only makes a playlist from the music you already have.

## Usage

`python3 import_playlist.py -url PLEX_URL -t YOUR_TOKEN -i sample_playlist.txt -n 'My Good Tunes'`

This will go through the songs in sample_playlist.txt and make a playlist called My Good Tunes that includes the best match for each song.

## Arguments

You must provide a Plex token and a txt file.

| Argument | Alt | Description | Default |
|--|--|--|--|
| -url | -u | Plex URL | http://localhost:32400 |
| -token | -t | Your Plex token | none (you need this) |
| -input | -i | Txt file to pull from | none (you need this) |
| -name | -n | Name for the playlist | "New Playlist" |
| -exact | -e | Turns on exact match if present | False|

Don't forget to put quotes around the playlist name if it includes spaces.

## Generating the Txt File

You can use [this tool](https://www.spotlistr.com/export/spotify-playlist) to get a text file for a Spotify playlist. Make sure to check the box for "album name" and set the separator to "|". Then you can just copy/paste the text into a txt file.

There should be one song per line and each line should follow this pattern: SONG | ARTIST | ALBUM

Take a look at sample_playlist.txt for reference.

If you want to use a different separator character, you can edit the script at the start of main(). I avoid using a comma because many song titles include this character.

## Exact Match

If exact match is off (default) the name of the song is used to search and if there are no exact matches with the artist and album name for that song, it finds the song in your library that has the most matches (for instance song and album name match but the artist doesn't). In my sample playlist txt file, Whip It has the album "Freedom Of Choice (Remaster)" but in my library that album is called "Freedom Of Choice". With exact match on, it will not find it. With exact match off it will.

Sometimes with exact match off several songs seem equally good. In this case, all of those songs are added to the playlist but a warning is given in the console so you can remove them. This is surprisingly rare even for a very large library.

Exact match is useful if you made the text file from files in your library. If you are importing from something like Spotify, you probably want to leave it off because there may be small differences in the way things are labeled.

I'm sure the matching could be improved if you want to get in the guts of this script.