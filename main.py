import os
from tempfile import SpooledTemporaryFile, NamedTemporaryFile
from typing import List
from fastapi import FastAPI, UploadFile, HTTPException
from mutagen.easyid3 import EasyID3
from exception import LyricsNotFoundException

from lyrics import generate_lrc_file_with_librosa
from lyrics_parser import get_lyrics


app = FastAPI()


@app.get("/")
async def root():
    return {
        "id": "1323"
    }


@app.post("/api/v1/lyrics")
async def create_lrc_content(file: UploadFile):

    audio_file = file.file
    audio_file_id3 = EasyID3(audio_file)
    audio_title = audio_file_id3["title"][0]
    audio_artist = audio_file_id3["artist"][0]

    local_file = "audio_file.mp3"
    local_lyrics = "audio_lyrics.txt"

    try:
        lyrics = await get_lyrics(audio_title, audio_artist)
        contents = audio_file.read()

        open(local_file, "wb").write(contents)
        open(local_lyrics, "w").write(lyrics)

        lrc_content = await generate_lrc_file_with_librosa(local_file, local_lyrics)
        return {
            "lrc_content": lrc_content,
            "message": "Succesfully retrieved synced lyrics"
        }
    except LyricsNotFoundException:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": 404,
                "error_message": f'Could not find lyrics for {audio_title}'
            })

    finally:
        silentremove(local_file)
        silentremove(local_lyrics)


def silentremove(filename):
    if os.path.exists(filename):
        os.remove(filename)
