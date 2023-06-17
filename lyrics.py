from mutagen.id3 import ID3, USLT
from pydantic import BaseModel
import math
import librosa
import os
import numpy as np
import pydub


class Lyrics(BaseModel):
    id: str
    content: str


def generate_lrc_file1(mp3_file_path, lrc_file_path):

    # Load the audio file
    audio_path = "DNOU.mp3"
    audio = ID3(audio_path)

    # Load the lyrics file
    lyrics_path = "DNOU.txt"
    with open(lyrics_path, "r") as f:
        lyrics = f.read()

    # Add the lyrics to the audio file and save as .lrc
    output_path = os.path.splitext(audio_path)[0] + ".lrc"
    uslt = USLT(encoding=3, lang=u'eng', desc=u'', text=lyrics)
    audio["USLT::eng"] = uslt
    audio.save(output_path)


def generate_lrc_file(audio_path, lyrics_path):
   # Load the audio file
    y, sr = librosa.load(audio_path)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # Use LibROSA to get the timing information
    # timestamps = librosa.frames_to_time(range(len(y)), sr=sr)
    timestamps = librosa.frames_to_time(beat_frames, sr=sr)
    print(timestamps)

    # Load the lyrics file
    with open(lyrics_path, "r") as f:
        lyrics = f.readlines()

    # Generate the .lrc file
    output_path = os.path.splitext(audio_path)[0] + "1.lrc"
    with open(output_path, "w") as f:
        for i, line in enumerate(lyrics):
            timestamp = f"[{librosa.time_to_frames(timestamps[i], sr=sr)}]"
            f.write(f"{timestamp}{line}")


async def generate_lrc_file_with_librosa(audio_file, lyrics_file):

    dur = pydub.utils.mediainfo(audio_file)["duration"]

    # Load the audio file using librosa
    y, sr = librosa.load(audio_file, duration=math.floor(float(dur)))

    # Load the lyrics from a text file
    with open(lyrics_file, "r", encoding="utf-8") as f:
        lyrics = [line.strip() for line in f.readlines()]

    # Compute the beat timestamps using librosa

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Compute the lyric timestamps
    lyric_times = np.linspace(0, beat_times[-1], len(lyrics) + 1)

    # Convert the lyric timestamps to LRC format
    lrc_timestamps = []
    for timestamp in lyric_times:
        minutes = int(timestamp // 60)
        seconds = int(timestamp % 60)
        hundredths = int((timestamp % 1) * 100)
        lrc_timestamps.append(f"[{minutes:02}:{seconds:02}.{hundredths:02}]")

    # Create the LRC file
    lrc_file = "audio_file.lrc"
    lrc_content = ""
    for i in range(len(lyrics)):
        lrc_content += f"{lrc_timestamps[i]}{lyrics[i]}\n"

    return lrc_content
    with open(lrc_file, "w", encoding="utf-8") as f:
        for i in range(len(lyrics)):
            f.write(f"{lrc_timestamps[i]}{lyrics[i]}\n")


def copy_lrc_content():
    lrc_path = "DNOU.lrc"
    with open(lrc_path, "r", encoding="ISO-8859-1") as lrc_file:
        lrc_contents = lrc_file.read()

    # Create a new text file and write the LRC contents to it using a specific encoding
    txt_path = "DNOU1.txt"
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(lrc_contents)


# rawdata = open("DNOU.lrc", "rb").read()
# encoding = chardet.detect(rawdata)['encoding']
# print(encoding)
