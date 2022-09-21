# rekordbox-plex-sync

Synchronizes your Plex Media server to Rekordbox. 

Synchronziation is unidirectional (from Rekordbox to Plex). The script copies all of your music files to a new directory to avoid Plex modifiying any of your music and so that the file names are in a structure Plex can understand.  

--HOW TO--
* In Rekordbox preferences, turn Advanced->Browse->My Tag->Add "My Tag" to the "Comments" ON
* Use pip to install all the modules in requirements.txt
* Download rekordbox-plex-sync.py and set the constants at the top of the script (see CONSTANTS below)
* Run python rekordbox-plex-sync.py


--CONSTANTS--
* EMPTY_TARGET_FOLDER: If true, will delete all the files in the target folder before copying over files. Use if you want to hard reset (for example, you have deleted a bunch of music from your Rekordbox collection). 

* SOURCE_FOLDER: The location of your Rekordbox collection (assumes this is a flat directory).

* TARGET_FOLDER: The location of your Plex Library. A good practice is to keep a separate DJ library to avoid any collisions with other music libraries. 

* PLEX_USER: Username of your Plex account for synchronization.

* PLEX_PASSWORD: Password of your Plex account for sychronization.

* PLEX_SERVER: The name of your Plex Server. You can find this under the Library name on the Plex web app. 

* PLEX_LIBRARY: The name of the library you want to sychronize to. E.g. 'DJ Music'.

* TRACK_LIMIT: Used for testing. Use to limit the number of tracks the script will process. 

RECOMMENDED PLEX SETTINGS
To speed up library updates and avoid bad artist info/album art matches, the following Library settings are recommended:

* Scanner: Plex Music
* Agent: Personal Media Artists/Albums. Leave this on Plex Music if you want to have Plex try to find artist photos. Just know it doesn't always get it right and it substantially increases the time it take to update the library. 
* Sonic Analysis: Off
* Prefer Local Metdata: On
* Artist Bios: Off
* Album Reviews & Critic Ratings: Off
* Popular Tracks: Off
* Find Lyrics: Off
* Genres: Embedded Tags
* Album Art: Local Files Only
