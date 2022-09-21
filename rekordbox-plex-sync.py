# file manipulation
from distutils.log import debug
from operator import getitem
import os
import glob
import shutil
from os import listdir
from os.path import isfile, join

# metadata reader
from tinytag import TinyTag

# plex API
from plexapi.myplex import MyPlexAccount
from plexapi.playlist import Playlist

# collections
from collections import defaultdict

EMPTY_TARGET_FOLDER = True
SOURCE_FOLDER = '/Volumes/Samsung T5/DJ/Processed/'
TARGET_FOLDER = '/Users/josh/Music/Plex DJ Library/'
PLEX_USER = 'user@domain.com'
PLEX_PASSWORD = 'fido1234'
PLEX_SERVER = 'Josh\'s MacBook Pro'
PLEX_LIBRARY = 'DJ Music'
# use for testing. limits how many files the script processes
TRACK_LIMIT = 1000

# delete everything in the target folder
if (EMPTY_TARGET_FOLDER):
    print('Deleting all files in the target folder...')
    old_files = glob.glob(TARGET_FOLDER + '**/*.mp3', recursive=True)
    for f in old_files:
        try:   
            os.remove(f)
        except OSError as e:
            print('Error: %s : %s' %(f, e.strerror))

# copy all the files in the source folder but use the structure Plex understands e.g. Music/ArtistName/AlbumName/TrackNumber - TrackName.ext
print('Copying renamed files from source folder to target folder...')
source_tracks = [f for f in listdir(SOURCE_FOLDER) if isfile(join(SOURCE_FOLDER, f))]

# process all the files in the source folder
track_count = 0
for track_path in source_tracks:
    filename, file_extension = os.path.splitext(track_path)
    
    try:
        track_metadata = TinyTag.get(SOURCE_FOLDER + track_path)
    except:
        debug
        print('Error: cannot read metadata of ' + track_path)

    track_artist = track_metadata.artist
    track_title = track_metadata.title
    track_album = 'Unknown' if track_metadata.album is None else track_metadata.album
    track_num = '0' if track_metadata.track is None else track_metadata.track

    # if album or title is missing, log it as an error and skip the track 
    if track_artist is None or track_title is None:
        print('Warning: Skipped ' + track_path + ' because Artist or Title is missing' )
    
    # else, copy the track to a the target folder with a Plex-friendly path 
    else:
        target_subfolder = TARGET_FOLDER + track_artist + '/' + track_album + '/'
        target_filename = track_num + ' - '  + track_title + file_extension 
        target_path = target_subfolder + target_filename
        os.makedirs(os.path.dirname(target_subfolder), exist_ok=True)
        try:
            shutil.copyfile(src=SOURCE_FOLDER + track_path, dst=target_path)
        except FileNotFoundError as e:
            print('Error: Could not copy file ' + track_path + ' to ' + target_path) 
    
    # stop processing if we've reached the track limit
    track_count += 1
    if track_count >= TRACK_LIMIT: break


# sync the plex library    
account = MyPlexAccount(PLEX_USER, PLEX_PASSWORD)
plex = account.resource(PLEX_SERVER).connect()
music = plex.library.section(PLEX_LIBRARY)
print('Updating your Plex Library...')
music.update()
input('Press ENTER after the update is complete to continue.')

# delete all the playlists we've previously created 
playlists = music.playlists()
for playlist in playlists:
        if playlist.title[0:4] == '[RB]':
            playlist.delete()        

# create a dictionary of each rekordbox playlist
playlist_dict = defaultdict(list)

print ('Creating playlists from Rekordbox tags...')
tracks = music.searchTracks()
for track in tracks:
    track_path = track.locations[0]
    tag = TinyTag.get(track_path)
    main_comment = tag.comment
    rekordbox_tags_start = main_comment.find('/*')
    rekordbox_tags_end = main_comment.find('*/')
    rekordbox_tags = None
    rekordbox_tags_list = []
    if (rekordbox_tags_start > -1):
        rekordbox_tags = main_comment[rekordbox_tags_start + 3 : rekordbox_tags_end - 1] #trim the white space that rekordbox adds
        rekordbox_tags_list = rekordbox_tags.split(' / ')
    for tag in rekordbox_tags_list:
        playlist_dict[tag].append(track)

for playlist_title, track_list in playlist_dict.items():
    Playlist.create(server=plex, section=music, title='[RB] '+ playlist_title, items=track_list)
