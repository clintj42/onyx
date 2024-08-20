import spacy
from spacy.matcher import Matcher
import re


def spotify_extractor(command_text):
    artist_and_track_match = re.search(
        r"(Listen to|Play) (.*?) by (.*?) on spotify",
        command_text,
        re.IGNORECASE,
    )
    album_and_artist_match = re.search(
        r"(Listen to|Play) (the album) (.*?) by (.*?) on spotify",
        command_text,
        re.IGNORECASE,
    )
    album_only_match = re.search(
        r"(Listen to|Play) (the album) (.*?) on spotify",
        command_text,
        re.IGNORECASE,
    )
    artist_only_match = re.search(
        r"(Listen to|Play) (the artist |the band )?(.*?) on spotify",
        command_text,
        re.IGNORECASE,
    )
    track_only_match = re.search(
        r"(Listen to|Play) (the song|the track) (.*?) on spotify",
        command_text,
        re.IGNORECASE,
    )

    spotify_query = None
    query_type = None

    if artist_and_track_match:
        track_name = artist_and_track_match.group(2)
        artist_name = artist_and_track_match.group(3)
        spotify_query = f"artist:{artist_name} track:{track_name}"
        query_type = "artist,track"
    elif album_and_artist_match:
        album_name = album_and_artist_match.group(3)
        artist_name = album_and_artist_match.group(4)
        spotify_query = f"album:{album_name} artist:{artist_name}"
        query_type = "album,artist"
    elif album_only_match:
        album_name = album_only_match.group(3)
        spotify_query = f"album:{album_name}"
        query_type = "album"
    elif track_only_match:
        track_name = track_only_match.group(3)
        spotify_query = f"track:{track_name}"
        query_type = "track"
    elif artist_only_match:
        artist_name = artist_only_match.group(3)
        spotify_query = f"artist:{artist_name}"
        query_type = "artist"

    return spotify_query, query_type


if __name__ == "__main__":
    import time

    commands = [
        "Listen to the artist Jack Johnson on Spotify",
        "Listen to River of Dreams by Billy Joel on Spotify.",
        "Play Halo by Beyonce on Spotify",
        "Play the song Buddy Holly on Spotify",
        "Play Goodbye stranger by Supertramp on spotify",
        "Listen to Jupiter Nights on Spotify.",
        "Play the Blue album by Weezer on Spotify.",
        "Listen to the album Abbey Road on Spotify",
        "Play The Beatles on Spotify.",
    ]

    for command in commands:
        start = time.time()
        print(f"Command: {command}")
        spotify_query, query_type = spotify_extractor(command)
        print(f"Spotify Query: {spotify_query}")
        print(f"Query Type: {query_type}")
        stop = time.time()

        print(f"Time taken: {stop-start}")
        print("-----")
