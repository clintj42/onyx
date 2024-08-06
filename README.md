# Set up:

## Download and install whisper.cpp 
- cd into the parent directory of this repo
- `git clone git@github.com:ggerganov/whisper.cpp.git`
- `cd whisper.cpp`
- `bash ./models/download-ggml-model.sh base.en`
- `make`

## Setup this repo
- `sudo apt-get install portaudio19-dev`
- `pip install -r requirements.txt`
- `touch .env`
	- Add the following lines to your .env file: (change the paths to match your env)
	```
	ACCESS_KEY=COYGmwV78a4xDXKJVA4hNoKslXbUXbjL9H3JTMhIW6VgbMd1nHGVrg==
	KEYWORD_FILE_PATH=/home/clintj42/Documents/onyx/onyx_wake_word_model_rasp_pi.ppn
	WHISPER_MODEL_PATH=/home/clintj42/Documents/onyx/whisper.cpp/models/ggml-base.en.bin
	```
- `python detect_wake_word.py`
