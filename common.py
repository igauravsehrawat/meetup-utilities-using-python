import os
import shlex
import subprocess
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt
from time import sleep
import colorama
from common import auto_complete_files, while_true, trim_the_video

__all__ = [while_true, auto_complete_files, trim_the_video]

def while_true(what, process):
    while True:
        print("process returncode", process.returncode)
        if process.returncode == 0:
            print(colorama.Fore.GREEN, what, ", ran successfully")
            print(colorama.Style.RESET_ALL)
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

def auto_complete_prompt(allowed_extensions):
    os_walk = os.walk(".")
    all_files = []
    for cur_dir, child_dirs, files in os_walk:
        if cur_dir == ".":
            for file in files:
                file_name, extension = os.path.splitext(file)
                if (extension in allowed_extensions):
                    all_files.append(file)
            break
    auto_complete_files = WordCompleter(all_files, ignore_case=True)
    video_file_name = prompt(
        "Which video file you like to trim: ",
        completer=auto_complete_files,
        complete_while_typing=True)
    return video_file_name

def trim_the_video():
    allowed_extensions = [".mp4", ".mov", ".webm"]
    video_file_name = auto_complete_prompt(allowed_extensions)
    start_time = prompt("Start time for the video: ")
    end_time = prompt("End time for the video: ")
    file_name, extension = os.path.splitext(video_file_name)
    if extension not in allowed_extensions:
        print("The file you specified isn't supported at the moment.")
        print("Exiting now.")
        exit()
    command = (
        "ffmpeg -i {0} -r 24 -ss {1} -to {2} trimmed-{0}.mp4"
    ).format(video_file_name, start_time, end_time, video_file_name)

    process = subprocess
    args = shlex.split(command)
    process = subprocess.run(args)
    while_true("Video trimming", process)
    return video_file_name
