"""
Created October 1, 2022,
author: Dimitris Lymperopoulos
Description: A class that implements a multiple-files YouTube downloader

Usage:
1)
Download a fixed amount of  videos from each artist based on a text file and store them at a specified directory
    python3 yt_mass_downloader.py
    --search-file <.txt file>
    --dest-dir <directory>
    --amount N   [N is integer]

2)
Download a fixed amount of mp3 files from each artist based on a text file and store them at a specified directory
    python3 yt_mass_downloader.py
    --search-file <.txt file>
    --dest-dir <directory>
    --amount N   [N is integer]
    --audio-only

Example:
    python3 yt_mass_downloader.py
    --search-file /home/artists.txt
    --dest-dir /home/my_videos
    --amount 10
    --audio-only

"""


import argparse
import urllib
import os
import re
from datetime import datetime
from pytube import YouTube
from ..utils import logger_info, logger_error


class YtMassDownloader:
    def __init__(self, search_file, amount, dest_dir, audio_only=None):
        if not os.path.exists(search_file):   # check if search_file exists
            logger_error("Search file {} does not exist".format(search_file))
        self.search_file = search_file

        if amount is None:
            logger_error("Amount of songs cannot be None")
        self.amount = amount

        if dest_dir is None:   # check that destination folder has been specified
            logger_error("Destination folder is required")
        self.dest_dir = dest_dir

        self.audio_only = audio_only   # flag that decided the format of the downloaded videos
        self.links = []   # to keep the links of the desired videos
        self.artists = []  # to keep the names for the YouTube search

    def read_artists(self):   # store the artists from the file to a list
        logger_info("Parsing artists' list")
        with open(self.search_file) as f:
            for line in f:
                self.artists.append(line.replace(' ', '+'))

        return self

    def gather_videos(self):   # get all video links that wil be downloaded later
        logger_info("Gathering and filtering video links")

        for name in self.artists:  # for each artist
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + name)  # get yt url link
            vid_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # get all video links
            dirty_links = []

            for vid in vid_id[:100]:   # pick the first 100 videos
                video_link = "https://www.youtube.com/watch?v=" + vid   # create complete video link
                yt = YouTube(video_link)
                if yt.length <= 600:  # pick only videos less or equal to 10 minutes
                    dirty_links.append(video_link)

            for element in dirty_links[:self.amount]:  # keep only desired amount of videos for each artist
                self.links.append(element)

        return self

    def download_videos(self):
        logger_info("Downloading videos...")

        for video in self.links:
            if self.audio_only:
                YouTube(video).streams.filter(only_audio=True)[0].download(self.dest_dir)  # get only the audio (mp3)
            else:
                YouTube(video).streams.get_highest_resolution().download(self.dest_dir)  # get the whole video (mp4)

        return self

    def format_to_mp3(self):
        if self.audio_only:  # only if mp3 has been chosen as desired format
            logger_info("Converting files from mp4 to mp3")

            for file in os.listdir(self.dest_dir):
                new_name = file.replace(".mp4", ".mp3")  # change the type of the file
                if os.path.exists(os.path.join(self.dest_dir, new_name)) and new_name != file:
                    os.remove(os.path.join(self.dest_dir, new_name))
                os.rename(os.path.join(self.dest_dir, file), os.path.join(self.dest_dir, new_name))

        return self

    def pipeline(self):
        # we combine all the previous methods to create pipeline that downloads the necessary videos
        self.read_artists().gather_videos().download_videos().format_to_mp3()


def parse_input(args=None):
    """
    param args: The command line arguments provided by the user
    :return:  The parsed input Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--search-file", type=str, action="store", metavar="search_file",
                        required=True, help="The file containing artists' names")
    parser.add_argument("-a", "--amount", type=int, action="store", metavar="amount",
                        required=True, help="The file containing artists' names")
    parser.add_argument("-d", "--dest-dir", type=str, action="store", metavar="dest_dir",
                        required=True, help="The destination directory that the videos will be downloaded")
    parser.add_argument('--audio-only', action='store_true', required=False,
                        help="Whether to download the video as mp4 (audio and video) or as mp3 (audio only)")

    return parser.parse_args(args)


def main(args):
    start_time = datetime.now()

    downloader = YtMassDownloader(search_file=args.search_file, amount=args.amount, dest_dir=args.dest_dir,
                                  audio_only=args.audio_only)
    downloader.pipeline()

    logger_info("Script execution time: " + str(datetime.now() - start_time))


if __name__ == '__main__':
    ARG = parse_input()
    main(ARG)
