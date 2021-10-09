#! /usr/bin/env python3
"""A good 'ole templatin' script."""


import os
import argparse
from shutil import copy2
from dataclasses import dataclass
from glob import glob
from subprocess import run


# version of the program
VERSION = "v0.0.1"


@dataclass(frozen=True)
class Blueprint:
    """Class that stores the information about a blueprint."""

    name: str
    path: str
    initScript: str = None
    fileDir: list = None

    def __str__(self) -> str:
        """Display Blueprint information."""
        namestr = self.name + "\n"
        descstr = f" path: {self.path}\n" +\
                  f" init script: {self.initScript}\n" +\
                  f" accessory files: {self.fileDir}"
        return namestr + descstr

    @property
    def filePath(self):
        """Path of template file."""
        for f in glob(self.path + "/*"):
            if os.path.basename(f.split(".")[0]) == self.name:
                return f

    @property
    def initPath(self):
        """Path of init file."""
        return self.path + "/" + self.initScript

    @property
    def dirPath(self):
        """Path of accessory file directory."""
        return self.path + "/" + self.fileDir + "/"


def bpCopy(myBp: Blueprint, dirName: str):
    """Copy myBp in dirName."""
    copy2(myBp.filePath, dirName)


def bpAccessory(myBp: Blueprint, dirName: str):
    """Copy contents of myBp accessory folder into dirName."""
    if myBp.fileDir is None:
        return
    for file in glob(myBp.dirPath + "*"):
        copy2(file, dirName)


def bpInit(myBp: Blueprint, dirName: str):
    """Copy and execute init script of myBp."""
    if myBp.initScript is None:
        return
    copy2(myBp.initPath, dirName)
    st = os.stat(myBp.initPath)
    mode = st.st_mode | 0o111  # add execute permission bits
    os.chmod("./" + myBp.initScript, mode | 0o0111)
    run(["sh", "./" + myBp.initScript])


def bpCreate(myBp: Blueprint, dirName: str = ".",
             init: bool = True, accessory: bool = True):
    """Create the template."""
    print("Template goin' up!")
    bpCopy(myBp, dirName)
    if accessory:
        print("Now, let's copy those other files.")
        bpAccessory(myBp, dirName)
    if init:
        print("Executin' the script!")
        bpInit(myBp, dirName)
    print("We're all done here.")


# directories excluded by default from traversing
defaultExcludeDirs = [
    ".git",
    "__pycache__",
    "venv"
]


def bpDiscover(bpDir: str, excludeDirs: list = defaultExcludeDirs) -> dict:
    """Discover templates in the directory."""
    # directory generator
    myDir = os.walk(bpDir)
    # initialize bpDict
    bpDict = {}
    # split the directory tree in: templates, dotfiles, dotdirs
    for dirCurr, dirNames, fileNames in myDir:
        # all files not starting with a '.' are templates.
        templates = [f.split(".")[0] for f in fileNames
                     if not f.startswith(".")]
        # list of init scripts
        initScriptNames = ("." + f for f in templates)
        initScripts = [n if n in fileNames else None for n in initScriptNames]
        # list of file dirs
        fileDirNames = ("." + f + ".d" for f in templates)
        fileDirs = [n if n in dirNames else None for n in fileDirNames]
        # remove dirs that should not be recursed
        pruneDirs(dirNames, *fileDirs, *excludeDirs)
        # update bpDict
        bpDict.update({t: Blueprint(t, dirCurr, s, d)
                       for t, s, d in zip(templates, initScripts, fileDirs)})
    return bpDict


def pruneDirs(dirNames: list, *args):
    """Remove from dirNames all args in place."""
    for n in filter(lambda x: x is not None, args):
        if n in dirNames:
            dirNames.remove(n)


def bpDisplay(bpDict: dict):
    """Display the templates in the directory."""
    for x in bpDict.values():
        print(x)


def argParse():
    """Parse the command line arguments."""
    # top parsing
    topDescStr = "Blueprint {}.".format(VERSION) +\
        "A good 'ole python script for all your templatin' needs."

    topParser = argparse.ArgumentParser(description=topDescStr)

    # specify top directory
    topParser.add_argument(
        "--topdir", help="Where are those darn blueprints?", default=None)

    # sub command parsing
    subParsers = topParser.add_subparsers(dest="cmd")
    # list has no additional arguments
    subParsers.add_parser(
        "list", help="Let's see what those blueprints are.")
    # create does
    createParser = subParsers.add_parser(
        "create", help="Let's deploy that blueprint.")

    # create arguments
    createParser.add_argument(
        "name", help="Yup, that's the blueprint to be created.")
    createParser.add_argument(
        "--no-script", help="No script is gonna be executed.",
        action="store_true")
    createParser.add_argument(
        "--no-accessories", help="Don't bring any of those fancy accessory \
        files.", action="store_true")
    # do the arg parsing and return
    return topParser.parse_args()


def main():
    """Execute the program."""
    # template directory for the system
    bpDir = os.environ["HOME"] + "/Templates"

    args = argParse()

    # topdir settings
    if args.topdir is not None:
        # get abspath in order not to have any surprise
        bpDir = str(os.path.abspath(args.topdir))

    # discover templates
    bpDict = bpDiscover(bpDir)

    # list subcommand
    if args.cmd == "list":
        bpDisplay(bpDict)

    # create subcommand
    if args.cmd == "create":
        bpSelected = args.name
        bpCreate(bpDict[bpSelected],
                 init=not args.no_script,
                 accessory=not args.no_accessories)


# do the main things
if __name__ == '__main__':
    main()
