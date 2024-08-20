import spacy
from spacy.matcher import Matcher
import re


def spotify_extractor(command_text):
    artist_and_track_match = re.search(
        r"(Listen to|Play) (.*?) by (.*?) on spotify",
        command_text,
        re.IGNORECASE,
    )
    artist_only_match = re.search(
        r"(artist|band) (.*?) on spotify", command_text, re.IGNORECASE
    )
    track_only_match = re.search(
        r"(Listen to|Play) (.*?) on spotify", command_text, re.IGNORECASE
    )

    spotify_query = None
    query_type = None

    if artist_and_track_match:
        track_name = artist_and_track_match.group(2)
        artist_name = artist_and_track_match.group(3)
        spotify_query = f"artist:{artist_name} track:{track_name}"
        query_type = "artist,track"
    elif artist_only_match:
        artist_name = artist_only_match.group(2)
        spotify_query = f"artist:{artist_name}"
        query_type = "artist"
    elif track_only_match:
        track_name = track_only_match.group(2)
        spotify_query = f"track:{track_name}"
        query_type = "track"

    return spotify_query, query_type


if __name__ == "__main__":
    import time

    commands = [
        "Listen to the artist Jack Johnson on Spotify",
        "Listen to River of Dreams by Billy Joel on Spotify.",
        "Play Halo by Beyonce on Spotify",
        "Play Goodbye stranger by Supertramp on spotify",
        "Listen to Lemons by Jupiter Nights on Spotify.",
        "Listen to Blackbird on Spotify.",
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
