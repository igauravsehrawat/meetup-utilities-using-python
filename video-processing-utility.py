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

def main():
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
        "{3}/g' ./preface-template.svg > ./preface-generated.svg").format(talk_title, talk_speaker, talk_month, talk_year)
    args = shlex.split(command)
    print(command)
    # process = subprocess.Popen(command)
    # subprocess.check_call(command)
    # while_true(process)

if __name__ == "__main__":
    main()
