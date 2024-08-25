# Onyx

# Introduction

Onyx is a Raspberry Pi voice home assistant similar to Amazon Echo or Google Home device. The difference is that this project keeps your voice on the Raspberry Pi at all times. Your voice never leaves the device. A lot of people have complained about Amazon Echo or Google Home showing personalized ads for things you talk about in your home. This project aims to solve that problem. All models and text analyzing are loaded on the Raspberry Pi. The project can actually run just fine without even being connected to the internet. The only times it hits the internet, is if you ask it to. For example, if you say "Play a song on Spotify".

# Demo

[Link to the demo](https://youtu.be/YCklC0LMPE4)

# Set up:

## Download and install whisper.cpp

- cd into the parent directory of this repo
- `git clone git@github.com:ggerganov/whisper.cpp.git`
- `cd whisper.cpp`
- `bash ./models/download-ggml-model.sh base.en`
- `make`

## Setup this repo

- `sudo apt-get install portaudio19-dev`
- `sudo apt install sox`
- `sudo apt-get install espeak`
- `sudo apt install curl`
- `curl -fsSL https://ollama.com/install.sh | sh`
- `ollama run gemma2:2b`
- Install rust `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- `source $HOME/.cargo/env`
- `pip install -r requirements.txt`
- `touch .env`

  - Add the following lines to your .env file:

  ```
  KEYWORD_FILE_PATH=/home/username_here/onyx/onyx_wake_word_model_rasp_pi.ppn
  WHISPER_MODEL_PATH=/home/username_here/onyx/whisper.cpp/models/ggml-base.en.bin
  PORCUPINE_ACCESS_KEY=access_key_here
  SPOTIFY_CLIENT_ID=spotify_client_id_here
  SPOTIFY_CLIENT_SECRET=spotify_client_secret_here
  SPOTIFY_DEVICE_ID=spotify_device_id_here
  TODOIST_API_KEY=todoist_api_key_here
  TODOIST_PROJECT_ID=todoist_project_id_here
  KASA_USERNAME=kasa_username_here
  KASA_PASSWORD=kasa_password_here
  SPEAK_COMMAND=espeak
  ```

  - Change the file paths to match your device
  - This project uses porcupine to handle the wake word detection. You can get an api key by following this guide: https://picovoice.ai/docs/porcupine/
  - Get a spotify client id and secret by following this guide: https://developer.spotify.com/documentation/web-api/concepts/apps
  - For the spotify device id you can list available devices by running:

  ```
  curl --request GET \
  --url https://api.spotify.com/v1/me/player/devices \
  --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'
  ```

  - Get a todoist api key by following this guide: https://todoist.com/help/articles/find-your-api-token-Jpzx9IIlB.
  - The todoist project id can be found by hitting this API:

  ```curl -X GET \
  https://api.todoist.com/rest/v2/projects \
  -H "Authorization: Bearer 0123456789abcdef0123456789"
  ```

  - If you use kasa (tp-link) for your smart home devices you can put your username and password to the kasa website in as well.

## To run the project

- `python detect_wake_word.py`

## Credit

- This project was forked from the amazing pi-card project which can be found here: https://github.com/nkasmanoff/pi-card. I trained a few more bert models to handle the tools and current date and time. I used spaCy for checking for patterns and extracting songs, timer amounts, etc. Using this sped things up on my raspberry pi.
