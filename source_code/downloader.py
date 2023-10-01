"""
Created October 1, 2023
author: Dimitris Lymperopoulos
Description: A class that implements a general yt downloader with options for both single and multiple files downloads

Usage:
1)
Download a fixed amount of  videos from each artist based on a text file and store them at a specified directory
    python3 downloader.py
    mass
    --search-file <.txt file>
    --dest-dir <directory>
    --amount N   [N is integer]

2)
Download a fixed amount of mp3 files from each artist based on a text file and store them at a specified directory
    python3 downloader.py
    mass
    --search-file <.txt file>
    --dest-dir <directory>
    --amount N   [N is integer]
    --audio-only

3)
Download a single video file from YouTube and store it with a specific name
    python3 downloader.py
    single
    --video-url <url of the youtube video>
    [--dest-file < .mp4 file>]


4)
Download a single mp3 file from YouTube and store it with a specific name
    python3 downloader.py
    single
    --video-url <url of the youtube video>
    [--dest-file < .mp3 file>]
    --audio-only

Example:
1)
    python3 downloader.py
    mass
    --search-file /home/artists.txt
    --dest-dir /home/my_videos
    --amount 10
    --audio-only

2)
    python3 downloader.py
    single
    --video-url http://youtube.com/my_video_url
    --dest-file /home/my_audio.mp3
    --audio-only
"""

import argparse
from datetime import datetime
from yt_single_downloader.yt_single_downloader import YtSingleDownloader
from yt_mass_downloader.yt_mass_downloader import YtMassDownloader
from utils import logger_info, logger_error


def parse_input(args=None):
    """
    param args: The command line arguments provided by the user
    :return:  The parsed input Namespace
    """

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # create parser and arguments for single-file download
    single_parser = subparsers.add_parser("single", help="parser for single-file download")
    single_parser.add_argument("-v", "--video-url", type=str, action="store", metavar="video_url",
                               required=True, help="The video url")
    single_parser.add_argument("-d", "--dest-file", type=str, action="store", metavar="dest_file",
                               required=True, help="The destination file that the video will be downloaded")
    single_parser.add_argument('--audio-only', action='store_true', required=False,
                               help="Whether to download the video as mp4 (audio and video) or as mp3 (audio only)")

    # create parser and arguments for multiple-files download
    mass_parser = subparsers.add_parser("mass", help="parser for multiple-files download")
    mass_parser.add_argument("-s", "--search-file", type=str, action="store", metavar="search_file",
                             required=True, help="The file containing artists' names")
    mass_parser.add_argument("-a", "--amount", type=int, action="store", metavar="amount",
                             required=True, help="The file containing artists' names")
    mass_parser.add_argument("-d", "--dest-dir", type=str, action="store", metavar="dest_dir",
                             required=True, help="The destination directory that the videos will be downloaded")
    mass_parser.add_argument('--audio-only', action='store_true', required=False,
                             help="Whether to download the video as mp4 (audio and video) or as mp3 (audio only)")

    return parser.parse_args(args)


def main(args):
    start_time = datetime.now()

    if args.command == 'single':
        downloader = YtSingleDownloader(video_url=args.video_url, dest_file=args.dest_file, audio_only=args.audio_only)
        downloader.download_video()

    elif args.command == "mass":
        downloader = YtMassDownloader(search_file=args.search_file, amount=args.amount, dest_dir=args.dest_dir,
                                      audio_only=args.audio_only)
        downloader.pipeline()

    else:
        logger_error("Option {} is not available!".format(args.command))

    logger_info("Script execution time: " + str(datetime.now() - start_time))


if __name__ == '__main__':
    ARG = parse_input()
    main(ARG)
