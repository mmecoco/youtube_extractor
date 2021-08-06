import pandas as pd
import urllib.request
import re
import unidecode
from pytube import YouTube

class TopXLoudnessDetector():
    def __init__(self, file_path, top=5, mp3_path="."):
        self._top = top
        self._file_path = file_path
        self._extracted_csv = None
        self._youtube_vid_format = "https://www.youtube.com/watch?v="
        self._youtube_search_format = "https://www.youtube.com/results?search_query="
        self._music_lists = []
        self._music_links = []
        self._etl()
    
    def _etl(self):
        data = pd.read_csv(self._file_path, encoding="latin")
        data.sort_values(by=["Loudness..dB.."])
        self._extracted_csv = data
        self._get_top_x_musics()

    def _get_top_x_musics(self):
        for i in range(self._top):
            self._music_lists.append((self._extracted_csv["Track.Name"][i], self._extracted_csv["Artist.Name"][i]))
        print(self._music_lists)
        self._get_link_from_lists()

    def _get_link_from_lists(self):
        for element in self._music_lists:
            try:
                title, artist = element
                title = unidecode.unidecode(title)
                artist = unidecode.unidecode(artist)
                html = urllib.request.urlopen(self._youtube_search_format + title.replace(" ", "") + artist.replace(" ", ""))
                video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
                self._music_links.append(self._youtube_vid_format + video_id)
            except:
                continue

    def extract_mp3_from_top_x(self):
        for link in self._music_links:
            video = YouTube(link)
            video.streams.get_by_itag(18).download()
