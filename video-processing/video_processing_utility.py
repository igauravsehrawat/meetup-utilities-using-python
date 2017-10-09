#!/usr/local/bin/python3
import shlex
import subprocess
import json
from halo import Halo
from prompt_toolkit import prompt
from common import trim_the_video
from prompt_toolkit.contrib.completers import WordCompleter

def generate_banner():
    talk_title = prompt("Enter the talk title: ")
    talk_speaker = prompt("Enter speaker's full name: ")
    months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"]
    auto_complete_files = WordCompleter(months, ignore_case=True)
    talk_month = prompt(
        "Which month the talk was recorded ?: ",
        completer=auto_complete_files,
        complete_while_typing=True)
    years = ["2017", "2018", "2019", "2020"]
    auto_complete_files = WordCompleter(years, ignore_case=True)
    talk_year = prompt(
        "Which year the talk was presented ?: ",
        completer=auto_complete_files,
        complete_while_typing=True)

    command = (
        """sed -e 's/%title%/{0}/g' -e 's/%speaker%/"""
        """{1}/g' -e 's/%month%/{2}/g' -e 's/%year%/"""
        """{3}/g' ./title-template.svg""").format(
            talk_title, talk_speaker, talk_month, talk_year)
    args = shlex.split(command)
    with Halo(text="Generating banner...", spinner='dots'):
        with open("preface.svg", "w") as generated_content:
            subprocess.run(args, stdout=generated_content)

def generate_png(width, height):
    command = (
        "convert preface.svg -density 150 -resize {0}x{1}! preface.png").format(
            width, height)
    args = shlex.split(command)
    with Halo(text="Generating preface png...", spinner='hamburger'):
        subprocess.run(args)


def generate_preface_video():
    command = (
        "ffmpeg -loop 1 -i preface.png -f lavfi -i aevalsrc=0 -c:a aac "
        "-ab 128k -map 0:0 -map 1:0 -t 7 -preset ultrafast -qp "
        "0 preface-video.mp4"
    )
    args = shlex.split(command)
    with Halo(text="Generating preface video...", spinner='arrow2'):
        subprocess.run(args)


def video_info(video_file_name):
    command = (
        "ffprobe -v error -show_entries stream=width,height "
        " -of default=noprint_wrappers=1 -of json {0}"
    ).format(video_file_name)
    args = shlex.split(command)
    with Halo(text="Getting video info...", spinner='bouncingBall'):
        process = subprocess.run(args, stdout=subprocess.PIPE)
    output = process.stdout
    print(type(output), video_file_name)
    if (output is not None):
        video_info = json.loads(output)
        stream_info = video_info["streams"][0]
        wh = [stream_info["width"], stream_info["height"]]
        print("jkfdsaf")
        return wh
    return None

def make_uploadable_video(video_file_name):
    print("Generating uploadable video")

    command = (
        """ffmpeg -i preface-video.mp4 -i {0} -filter_complex """
        """ "[0:0] [0:1] [1:0] [1:1] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" """
        """-map "[a]"  uploadable-{0}.mp4"""
    ).format(video_file_name)
    args = shlex.split(command)
    with Halo(text="Generating video for uploading...", spinner='runner'):
        subprocess.run(args)


def main():
    # 1, 2, 3, 4, 5
    generate_banner()
    video_file_name = trim_the_video()
    width, height = video_info(video_file_name)
    generate_png(width, height)
    generate_preface_video()
    make_uploadable_video(video_file_name)

if __name__ == "__main__":
    main()
