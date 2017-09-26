#!/usr/local/bin/python3

import shlex
import subprocess
from time import sleep

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

def generate_banner():
    # talk_title = input("Enter the talk title: ")
    # talk_speaker = input("Enter speaker's full name: ")
    # talk_month = input("Which month the talk was recorded?: ")
    # talk_year = input("Which year the talk was presented?: ")

    talk_title = "asdfklj"
    talk_speaker = "dsflakj"
    talk_month = "sdlkfj"
    talk_year = "dklfjsa"

    command = (
        "sed -e 's/%title%/{0}/g' -e 's/%speaker%/"
        "{1}/g' -e 's/%month%/{2}/g' -e 's/%year%/"
        "{3}/g' ./title-template.svg").format(talk_title, talk_speaker, talk_month, talk_year)
    args = shlex.split(command)
    print(command)
    print(args)
    with open("preface.svg", "w") as generated_content:
        subprocess.run(args, stdout=generated_content)
    # while_true(process)

def main():
    generate_banner()

if __name__ == "__main__":
    main()
