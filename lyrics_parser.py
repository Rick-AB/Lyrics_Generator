
import re
from bs4 import BeautifulSoup
from urllib import parse
import asyncio
from requests_html import HTMLSession

from exception import LyricsNotFoundException

clearSpecialCharactersAndURL = re.compile(r'[|\[\]{}<>@].*')

clearTrackExtras = re.compile(
    r'(([\[(])(?!.*?(remix|edit|remake)).*?([])])|/|-| x |&|,|"|video official|official lyric video| feat.? |ft.?|\|+|yhlqmdlg|x100pre|[\U0001F400-\U0001F5FF]|\u274C)')
clearRegex = re.compile(r' {2,}')


async def get_lyrics(title: str, artist: str):
    formattedQuery = get_formatted_query(title, artist)
    encodedQuery = parse.quote(formattedQuery)
    url = f"https://www.google.com/search?q={encodedQuery}+lyrics&ie=UTF-8&tob=true"
    session = HTMLSession()
    loop = asyncio.get_event_loop()
    html = session.get(url).content  # await loop.run_in_executor(None, , url)
    doc = BeautifulSoup(html, 'lxml')

    lyrics = doc.find("div", {"data-lyricid": True})
    if lyrics is not None:
        lyrics = lyrics.find_next("div", recursive=False)
        if lyrics is not None:
            lyrics = lyrics.get_text("\n")

    if lyrics is None:
        raise LyricsNotFoundException

    return lyrics


def clean_info(info: str):
    info = info.lower()
    info = re.sub(clearSpecialCharactersAndURL, '', info)
    info = re.sub(r'https?://\S+', '', info)
    info = re.sub(clearTrackExtras, '', info)
    return info


def concat_info(info: str):
    info = re.sub(clearRegex, ' ', info).strip()
    info = info.replace(' ', '+')
    return info


def get_formatted_query(title: str, artist: str):
    return concat_info(clean_info(title) + " " + clean_info(artist))


# asyncio.run(get_lyrics("DNOU", "KB"))
