#!/usr/local/bin/python3
import os
import shlex
import subprocess
import json
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from time import sleep

def while_true(what, process):
    while True:
        if process.returncode is None:
            print("..", end="")
        elif process.returncode == 0:
            print(what, "Ran successfully")
            return
        elif process.returncode < 0:
            outs, errs = process.stdout, process.stderr
            print(what, outs, errs)
            return
        elif process.returncode > 0:
            outs, errs = process.stdout, process.stderr
            print(outs, errs)
            print(what, "Have you installed all the tools?")
            return
        sleep(1)

def generate_banner():
    talk_title = input("Enter the talk title: ")
    talk_speaker = input("Enter speaker's full name: ")
    talk_month = input("Which month the talk was recorded?: ")
    talk_year = input("Which year the talk was presented?: ")

    command = (
        """sed -e 's/%title%/{0}/g' -e 's/%speaker%/"""
        """{1}/g' -e 's/%month%/{2}/g' -e 's/%year%/"""
        """{3}/g' ./title-template.svg""").format(
            talk_title, talk_speaker, talk_month, talk_year)
    args = shlex.split(command)
    with open("preface.svg", "w") as generated_content:
        process = subprocess.run(args, stdout=generated_content)
        while_true("SVG generation", process)

def generate_png(width, height):
    command = (
        "convert preface.svg -density 150 -resize {0}x{1}! preface.png").format(
            width, height)
    args = shlex.split(command)
    process = subprocess.run(args)
    while_true("PNG Generation", process)

def generate_preface_video():
    command = (
        "ffmpeg -loop 1 -i preface.png -f lavfi -i aevalsrc=0 -c:a aac "
        "-ab 128k -map 0:0 -map 1:0 -t 7 -preset ultrafast -qp "
        "0 preface-video.mp4"
    )
    args = shlex.split(command)
    process = subprocess.run(args)
    while_true("Preface video generation", process)

def trim_the_video():
    osWalk = os.walk(".")
    allFiles = []
    for curDir, childDirs, files in osWalk:
        if curDir == ".":
            for file in files:
                if ("mp4" in file) or ("mov" in file) or ("webm" in file):
                    allFiles.append(file)
            break
    autoCompleteFiles = WordCompleter(allFiles, ignore_case=True)
    video_file_name = prompt(
        "Which video file you like to trim: ",
        completer=autoCompleteFiles,
        complete_while_typing=True)
    startTime = prompt("Start time for the video: ")
    endTime = prompt("End time for the video: ")

    command = (
        "ffmpeg -i {0} -r 24 -ss {1} -to {2} trimmed-{0}.mp4"
    ).format(video_file_name, startTime, endTime, video_file_name)

    process = subprocess
    args = shlex.split(command)
    process = subprocess.run(args)
    while_true("Video trimming", process)
    return video_file_name

def video_info(video_file_name):
    command = (
        "ffprobe -v error -show_entries stream=width,height "
        " -of default=noprint_wrappers=1 -of json {0}"
    ).format(video_file_name)
    process = subprocess
    args = shlex.split(command)
    process = subprocess.run(args, stdout=subprocess.PIPE)
    output = process.stdout
    if (output is not None):
        video_info = json.loads(output)
        stream_info = video_info["streams"][0]
        wh = [stream_info["width"], stream_info["height"]]
        return wh
    return None

def make_uploadable_video(video_file_name):
    print("Generating uploadable video")

    command = (
        """ffmpeg -i preface-video.mp4 -i trimmed-{0}.mp4 -filter_complex """
        """ "[0:0] [0:1] [1:0] [1:1] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" """
        """-map "[a]"  uploadable{0}.mp4"""
    ).format(video_file_name)
    process = subprocess
    args = shlex.split(command)
    process = subprocess.run(args)
    while_true("Making uploadable", process)

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
