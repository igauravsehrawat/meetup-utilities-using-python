import shlex
import subprocess
from prompt_toolkit import prompt
from common import auto_complete_files, while_true, trim_the_video

def trim_audio():
    allowed_extensions = [".wav", ".aac", ".mp3", ".mp4"]
    audio_to_trim = auto_complete_files(allowed_extensions)
    start_time = prompt("Enter start time: ")
    end_time = prompt("Enter end time: ")
    command = ("ffmpeg -i {0} -ss {1} -to {2} trimmed-{0}.wav").format(
        audio_to_trim, start_time, end_time)
    args = shlex.split(command)
    process = subprocess.call(args)
    while_true("Trim the audio", process)
    return ("trimmed-{0}.wav").format(audio_to_trim)

def merge_audio_video(audio, video):
    command = ("ffmpeg -i {0} -i {1} -shortest overlayed-audio{1}.mp4").format(
        audio, video)
    args = shlex.split(command)
    process = subprocess.call(args)
    while_true("Merge audio and video", process)

if __name__ == "__main__":
    trimmed_audio = trim_audio()
    trimmed_video = trim_the_video()
    merge_audio_video(trimmed_audio, trimmed_video)
