"""
Created October 1, 2023
author: Dimitris Lymperopoulos
Description: A class that implements a single-file YouTube downloader

Usage:
1)
Download a single video file from YouTube and store it with a specific name
    python3 yt_single_downloader.py
    --video-url <url of the youtube video>
    [--dest-file < .mp4 file>]


2)
Download a single mp3 file from YouTube and store it with a specific name
    python3 yt_single_downloader.py
    --video-url <url of the youtube video>
    [--dest-file < .mp3 file>]
    --audio-only

Example:
    python3 yt_single_downloader.py
    --video-url http://youtube.com/my_video_url
    --dest-file /home/my_audio.mp3
    --audio-only

"""


import argparse
import os
from datetime import datetime
from pytube import YouTube
from source_code.utils import logger_info, logger_error


class YtSingleDownloader:
    def __init__(self, video_url, dest_file=None, audio_only=None):
        """

        :param video_url: string representing the url of the video to be downloaded
        :param dest_file: string, representing the destination file where the video will be stored
        :param audio_only: boolean value, representing whether to download audio only or not
        """

        if "www.youtube.com" not in video_url:
            logger_error("The video url should be from the YouTube website!")

        self.video_url = video_url
        self.dest_file = dest_file
        self.audio_only = False if audio_only is None else True

    def download_video(self):
        """
        A method that downloads the given video.

        :return: YtSingleDownloader object
        """
        logger_info("Downloading video...")

        # create destination path and destination filename
        dest_path = None if self.dest_file is None else os.path.dirname(os.path.abspath(self.dest_file))
        dest_filename = None if self.dest_file is None else os.path.basename(self.dest_file).split('/')[-1]

        if self.audio_only:
            # get only the audio (mp3)
            YouTube(self.video_url).streams.filter(only_audio=True)[0].download(output_path=dest_path,
                                                                                filename=dest_filename)
        else:
            # get the whole video (mp4)
            YouTube(self.video_url).streams.get_highest_resolution().download(output_path=dest_path,
                                                                              filename=dest_filename)

        return self


def parse_input(args=None):
    """
    param args: The command line arguments provided by the user
    :return:  The parsed input Namespace
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--video-url", type=str, action="store", metavar="video_url",
                        required=True, help="The video url")
    parser.add_argument("-d", "--dest-file", type=str, action="store", metavar="dest_file",
                        required=True, help="The destination file that the video will be downloaded")
    parser.add_argument('--audio-only', action='store_true', required=False,
                        help="Whether to download the video as mp4 (audio and video) or as mp3 (audio only)")

    return parser.parse_args(args)


def main(args):
    start_time = datetime.now()

    downloader = YtSingleDownloader(video_url=args.video_url, dest_file=args.dest_file, audio_only=args.audio_only)
    downloader.download_video()

    logger_info("Script execution time: " + str(datetime.now() - start_time))


if __name__ == '__main__':
    ARG = parse_input()
    main(ARG)
