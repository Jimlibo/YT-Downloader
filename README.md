# Youtube Downloader

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/pytube-v15.0.0-red.svg)


## General
A CLI (Command Line Interface) application, that allows the user to download and 
store videos from YouTube. The downloader offers two options:
1) Download and store a single video
2) Download and store multiple videos from different artists

The downloaded videos can be stored either as .mp3 or .mp4 files.

## Setup
In order to get the app running, first you need to clone this repository.
This can be done with the command:
```bash
git clone https://github.com/Jimlibo/YT-Downloader.git
```
Then to download the necessary python packages, run the command:
```bash
pip install -r requirements.txt
```
<b>Note:</b> You need to be in the home directory of this project in order to run 
the above command.

## Usage
The downloader has two basic modes: <b>single</b> and <b>mass</b>. The first 
one downloads a single video and stores it either as a .mp3 or as a .mp4 file.

### Single Mode
To run the downloader in single mode, run the commands:
```bash
cd source_code
python downloader.py single --video-url example_url --dest-file example_file --audio-only
```
<b>Notes</b>:
* Parameter <i>dest-file</i> is optional. If not specified, the video will be downloaded
with the default name inside the directory from which the script was executed.
* If you want the video to be downloaded as .mp4 file, ignore the parameter
<i>audio-only</i>.

### Mass Mode
In mass mode, the downloader takes as input a text file containing different artists' names, 
one name at each line. It also takes as input an integer N, that defines how many song from
each artist shall be downloaded.

To run the downloader in mass mode, run the commands:
```bash
cd source_code
python downloader.py mass --search-file sample.txt --dest-dir sample_dir --amount N --audio-only
```
<b>Notes</b>:
* Parameter <i>amount</i> expects an integer value that represents the number of songs of each artist
that will be downloaded
* If you want the videos to be downloaded as .mp4 file, ignore the parameter
<i>audio-only</i>.

### Search-file format example
An example of what a valid search file would look like, is this:
```text
Imagine Dragons
The Weekend
OneRepublic
David Guetta
```

\
\
You can read more about the downloader usage in its [documentation]

[documentation]: https://github.com/Jimlibo/YT-Downloader/blob/main/source_code/downloader.py



