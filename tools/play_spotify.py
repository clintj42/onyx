from spotipy.oauth2 import SpotifyOAuth
import spotipy
import ollama
import traceback
from dotenv import load_dotenv
import os
import json

load_dotenv()

SPEAK_COMMAND = os.getenv("SPEAK_COMMAND")
spotify_control_commands = [
    "next",
    "skip",
    "stop",
    "pause",
    "play",
    "previous",
    "repeat",
    "repeat off",
    "restart",
    "start over",
]


def refine_search_query(search_query):
    refine_search_prompt = f"""Given the input of a Spotify search query, return a json object in the following schema:
    {{
        "refined_query": "artist:artist_name track:track_name album:album_name",
        "type: "artist,track,album"
    }}

    Example Input: Listen to Billy Joel on Spotify. 
    Output: {{ "refined_query": "artist: Billy Joel", "type": "artist" }}
    Example Input: Play the Track Halo by Beyonce on Spotify. 
    Output: {{ "refined_query": "track:Halo artist:Beyonce", "type": "track,artist" }}
    Example Input: Play Under the Bridge on Spotify
    Output: {{ "refined_query": "track:Under the Bridge", "type": "track" }}
    Example Input: Play the album Jupiter Nights by Jupiter Nights on Spotify
    Output: {{ "refined_query": "artist:Jupiter Nights album:Jupiter Nights", "type": "artist,album" }}
    Example Input: Listen to Come Together on the album Abbey Road by The Beatles on Spotify.
    Output: {{ "refined_query": "track:Come Together album:Abbey Road artist:The Beatles", "type": "track,album,artist" }}

    Respond only with the output. Do not add any additional Notes or Explanations. Correct any obvious spelling mistakes in the input.
    Like Super trap should be corrected to Supertramp for instance.


    Input: {search_query}"""
    refined_search = ollama.generate(model="gemma2:2b", prompt=refine_search_prompt)
    return refined_search["response"]


def play_spotify(search_query):
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri="http://google.com/callback/",
                scope="user-read-playback-state,user-modify-playback-state,streaming",
            )
        )

        refined_query_json = refine_search_query(search_query)
        refined_query_json = (
            refined_query_json.strip("```json").strip("`").replace('""', '"').strip()
        )

        # Extract the refined query and type from the json
        data = json.loads(refined_query_json)
        refined_query = data["refined_query"]
        type = data["type"]
        print("Sending the following search to Spotify\n", refined_query, "\n", type)

        # Search by artist, album or track
        result = sp.search(refined_query, limit=1, type=type)

        context_uri = None

        if (
            "albums" in result
            and "items" in result["albums"]
            and len(result["albums"]["items"]) > 0
        ):
            album = result["albums"]["items"][0]
            context_uri = album["uri"]
        elif (
            "tracks" in result
            and "items" in result["tracks"]
            and len(result["tracks"]["items"]) > 0
        ):
            track = result["tracks"]["items"][0]
            context_uri = track["uri"]
        elif (
            "artists" in result
            and "items" in result["artists"]
            and len(result["artists"]["items"]) > 0
        ):
            artist = result["artists"]["items"][0]
            context_uri = artist["uri"]

        # Get the current user's devices
        devices = sp.devices()
        device_id = None

        for device in devices["devices"]:
            device_id = device["id"]
            break

        if context_uri is None:
            os.system(
                f'{SPEAK_COMMAND} "Could not find any music for the following command: {search_query}"'
            )
        else:
            if device_id:
                # Start playback with the album URI, Spotify will continue with the album's songs
                if "track" in context_uri:
                    sp.start_playback(device_id=device_id, uris=[context_uri])
                elif "artist in context_uri":
                    sp.start_playback(device_id=device_id, context_uri=context_uri)
                elif "album" in context_uri:
                    sp.start_playback(device_id=device_id, context_uri=context_uri)
    except Exception as e:
        print(e)
        traceback.print_exc()
        os.system(
            f'{SPEAK_COMMAND} "An error occurred while trying to play the music."'
        )


def should_control_spotify(command):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri="http://google.com/callback/",
            scope="user-read-playback-state,user-modify-playback-state,streaming",
        )
    )

    devices = sp.devices()
    device_id = None

    for device in devices["devices"]:
        device_id = device["id"]
        break

    if not device_id:
        return False

    return command.lower() in spotify_control_commands


def control_spotify(command):
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri="http://google.com/callback/",
                scope="user-read-playback-state,user-modify-playback-state,streaming",
            )
        )

        # Get the current user's devices
        devices = sp.devices()
        device_id = None

        for device in devices["devices"]:
            device_id = device["id"]
            break

        if not device_id:
            # os.system(f'{SPEAK_COMMAND} "No active device found."')
            return

        if command.lower() == "next" or command.lower() == "skip":
            sp.next_track(device_id=device_id)
        elif command.lower() == "stop" or command.lower() == "pause":
            if sp.current_playback()["is_playing"]:
                sp.pause_playback(device_id=device_id)
        elif command.lower() == "play":
            sp.start_playback(device_id=device_id)
        elif command.lower() == "previous":
            sp.previous_track(device_id=device_id)
        elif command.lower() == "repeat":
            sp.repeat("track", device_id=device_id)
            os.system(f'{SPEAK_COMMAND} "Repeating the current track."')
        elif command.lower() == "repeat off":
            sp.repeat("off", device_id=device_id)
            os.system(f'{SPEAK_COMMAND} "Repeat mode turned off."')
        elif command.lower() == "restart" or command.lower() == "start over":
            sp.seek_track(position_ms=0, device_id=device_id)
        else:
            os.system(f'{SPEAK_COMMAND} "Command not recognized."')

    except Exception as e:
        print(e)
        traceback.print_exc()
        os.system(
            f'{SPEAK_COMMAND} "An error occurred while trying to control the music."'
        )


if __name__ == "__main__":
    play_spotify("Play Jupiter Nights album by Jupiter Nights on Spotify.")
    play_spotify("Listen to Jack Johnson on Spotify")
    play_spotify("Listen to the album Abbey Road by The Beatles on Spotify")
    play_spotify("Listen River of Dreams on Spotify.")
    play_spotify("Play Halo by Beyonce on Spotify")
    play_spotify("Play Goodbye stranger by Super trap on spotify")
    play_spotify('Listen to "Lemons" by Jupiter Knights on Spotify.')
    play_spotify("Listen to blackbird by the Beatles on Spotify.")
    while True:
        control = input("Enter a command: ")
        control_spotify(control)
