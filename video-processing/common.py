import os
import shlex
import subprocess
from halo import Halo
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit import prompt

__all__ = ["auto_complete_prompt", "trim_the_video"]

def auto_complete_prompt(allowed_extensions, file_type):
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
        "Which {0} file you like to trim: ".format(file_type),
        completer=auto_complete_files,
        complete_while_typing=True)
    return video_file_name

def trim_the_video():
    allowed_extensions = [".mp4", ".mov", ".webm"]
    video_file_name = auto_complete_prompt(allowed_extensions, "video")
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

    args = shlex.split(command)
    with Halo(text="Generating preface video...", spinner='earth'):
        subprocess.run(args)
    return "trimmed-{0}.mp4".format(video_file_name)
