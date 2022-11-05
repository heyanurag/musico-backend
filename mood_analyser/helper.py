
import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config
import random

availableGenres = [
    'acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues',
    'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical',
    'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco',
    'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french',
    'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock',
    'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie',
    'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin',
    'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age',
    'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep',
    'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton',
    'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes',
    'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish',
    'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']

moodToGenre = {
    'angry':  ["chill", "soul", "work-out", ],
    'happy': ["disco", "dance", "happy", "groove", ],
    'neutral': ["ambient", "holidays",  "party", "pop", ],
    'sad': ["acoustic", "piano",  "happy", "comedy"],
    'surprise': ["rock-n-roll", "road-trip", "trance", "romance", ]
}

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=config("SPOTIPY_CLIENT_ID"),
        client_secret=config("SPOTIPY_CLIENT_SECRET")))


def getTracksByMood(mood, limit=50):
    genres = moodToGenre[mood.lower()]
    res = sp.recommendations(seed_genres=genres, limit=limit)

    tracks = res["tracks"]
    # result = []
    # for track in tracks:
    #     temp = {
    #         "id": track["id"],
    #         "name": track["name"],
    #         "imgUrl": track["album"]["images"][0]["url"],
    #         "musicUrl": track["preview_url"],
    #         "durationMs": track["duration_ms"],
    #         "spotifyUrl": track["external_urls"]["spotify"],
    #         # "genre": track[""],
    #     }
    #     result.append(temp)

    random.shuffle(tracks)

    return tracks


def getSearchTracks(name, mood="all"):

    if mood == "all":
        query = name
    else:
        genres = moodToGenre[mood.lower()]
        query = urllib.parse.quote(f'''{name} genre:{",".join(genres)}''')

    result = sp.search(query, limit=50)
    # result = sp.search(name, limit=50)

    tracks = result["tracks"]["items"]
    random.shuffle(tracks)

    return tracks
