import shlex
import subprocess
from time import sleep
from code import InteractiveConsole

def while_true(process):
    while True:
        if process.returncode is None:
            print("..")
        elif process.returncode == 0:
            print("Ran successfully")
            return
        elif process.returncode < 0:
            outs, errs = process.communicate()
            print(outs, errs)
            return
        elif process.returncode > 0:
            outs, errs = process.communicate()
            print(outs, errs)
            print("Have you installed all the tools?")
            return
        sleep(1)

def main():
    talk_title = InteractiveConsole.raw_input(
        prompt="Enter the talk title")
    talk_speaker = InteractiveConsole.raw_input(
        prompt="Enter speaker's full name")
    talk_month = InteractiveConsole.raw_input(
        prompt="Which month the talk was recorded?")
    talk_year = InteractiveConsole.raw_input(
        prompt="Which year the talk was presented?")

    print("Generating the attribution..")
    command = (
        "sed -e 's/%title%/{talk_title}/g' -e 's/%speaker%/"
        "{talk_speaker}/g' -e 's/%month%/{talk_month}/g' -e 's/%year%/"
        "{talk_month}/g' preface-template.svg > preface-generated.svg")
    args = shlex.split(command)
    process = subprocess.Popen(args)
    while_true(process)

if __name__ == "__main__":
    main()
