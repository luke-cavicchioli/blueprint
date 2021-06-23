#! /usr/bin/env python3

import os
import json
import argparse

# version of the program
VERSION = "v0.0.1"


class Blueprint():
    pass


def bpCreate(myBp):
    pass


def bpDiscover(bpDir):
    pass


def bpDisplay(bpDict):
    pass


def main():
    # template directory for the system
    bpDir = os.environ["HOME"] + "/Templates"

    # argument parsing
    # top parsing
    topDescStr = "Blueprint {}.".format(VERSION) +\
        "A good 'ole python script for all your templatin' needs."

    topParser = argparse.ArgumentParser(description=topDescStr)

    # specify top directory
    topParser.add_argument(
        "--topdir", help="Where are those darn blueprints?", default=None)

    # sub command parsing
    subParsers = topParser.add_subparsers()
    listParser = subParsers.add_parser(
        "list", help="Let's see what those blueprints are.")
    createParser = subParsers.add_parser(
        "create", help="Let's deploy that blueprint.")

    # create arguments
    createParser.add_argument(
        "name", help="Yup, that's the blueprint to be created.")
    createParser.add_argument(
        "--no-script", help="No script is gonna be executed.", action="store_true")
    createParser.add_argument(
        "--no-accessories", help="Don't bring any of those fancy accessory \
        files.", action="store_true")
    createParser.add_argument("--no-git", help="No version control, just like \
        real men.", action="store_true")

    # do the arg parsing
    args = topParser.parse_args()

    # topdir settings
    if args.topdir is not None:
        bpDir = args.topdir

    # discover templates
    bpDict = bpDiscover(bpDir)

    # if list subcommand
    bpDisplay(bpDict)

    # if create subcommand
    bpCreate(bpDict[bpSelected])


# do the main things
if __name__ == '__main__':
    main()
