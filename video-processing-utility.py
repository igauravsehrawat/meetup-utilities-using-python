#!/usr/local/bin/python3

import shlex
import subprocess
from time import sleep

def while_true(what, process):
    while True:
        if process.returncode is None:
            print("..", end="")
        elif process.returncode == 0:
            print(what, "Ran successfully")
            return
        elif process.returncode < 0:
            outs, errs = process.communicate()
            print(what, outs, errs)
            return
        elif process.returncode > 0:
            outs, errs = process.communicate()
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
        "sed -e 's/%title%/{0}/g' -e 's/%speaker%/"
        "{1}/g' -e 's/%month%/{2}/g' -e 's/%year%/"
        "{3}/g' ./title-template.svg").format(
            talk_title, talk_speaker, talk_month, talk_year)
    args = shlex.split(command)
    print(args)
    with open("preface.svg", "w") as generated_content:
        process = subprocess.run(args, stdout=generated_content)
        while_true("SVG generation", process)

def generate_png():
    width = input("What's your recorded video frame width?")
    height = input("What's your recorded video frame height?")

    command = (
        "convert preface.svg -density 150 -resize {0}x{1}! preface.png").format(
            width, height)
    args = shlex.split(command)
    print(args)
    process = subprocess.run(args)
    while_true("PNG Generation", process)

def generate_preface_video():
    command = (
        "ffmpeg -loop 1 -i preface.png -f lavfi -i aevalsrc=0 -acodec "
        "libvo_aacenc -ab 128k -map 0:0 -map 1:0 -t 7 -preset ultrafast -qp "
        "0 preface-video.mp4"
    )
    args = shlex.split(command)
    process = subprocess.run(args)
    while_true("Preface video generation", process)

def main():
    generate_banner()
    generate_png()
    generate_preface_video()

if __name__ == "__main__":
    main()
