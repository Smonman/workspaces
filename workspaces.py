#!/usr/bin/env python
"""
This program opens specified user workspaces to safe time

Upon starting this program will show a list of set workspaces.
Using the commandline input the use can specify the workspaces by typing
in the corresponding index.
If the user wishes to open multiple different workspaces, just write the input
simultaniously.

For example if one wishes to open the workspace 1 and 3, just type in
13, the program will split the input char by char and evaluate it
individually.

If the amount of worcspaces exceeds the 10 this program will automatically
create pages and the ability to flip between them.

Known issue: one can only select workspaces from the same page
"""

import webbrowser
import os
import math
import itertools

__author__ = "Simon Josef Kreuzpointner"
__version__ = "2.1"


class Workspace:
    """
    This class represents a workspace

    A workspace consists of a collection of files, websites
    and programs that are needed in a specific worksetting.

    Calling open() on a workspace opens all the given files, websites
    and programs so the enduser does not need to open these by
    themselves.

    Attributes
    ----------
    title : str
        the title of the workspace

    Methods
    -------
    open()
        opens the workspace
    """

    def __init__(self, title, URLs=None, files=None, programs=None):
        """
        Parameters
        ----------
        title : str
            the title of the workspace
        URLs : str[] optional
            an array of URLs to be opend
        files : str[] optional
            an array of file or directory paths
        programs : str[] optional
            an array of program paths
        """

        self.title = title
        self.__URLs = URLs
        self.__files = files
        self.__programs = programs

    def open(self):
        """
        This function opens the workspace.

        This means all the given Urls are opend first.
        Every URL will be opend in a new tab on the system default webbrowser.
        This will not check if the site is already opend.

        Second, it will open all the given files using the system default
        file-open-action. If the given file is directory it will be opend
        on the Windows Explorer.

        At last all the given programms will be opend. This program
        simulates a double click on the specified programs.
        """
        self.__openUrls()
        self.__openFiles()
        self.__startPrograms()

    def __openUrls(self):
        if self.__URLs == None:
            return

        print("Opening URLs...")
        for url in self.__URLs:
            webbrowser.open(url, new=2)

    def __openFiles(self):
        if self.__files == None:
            return

        print("Opening files...")
        for f in self.__files:
            if os.path.isfile(f):
                os.startfile(f)
            elif os.path.isdir(f):
                os.startfile(f, operation="explore")

    def __startPrograms(self):
        if self.__programs == None:
            return

        print("Starting programs...")
        for program in self.__programs:
            os.startfile(program)


class PageableSelection:
    """
    This class represents a pageable console selection

    This selection creates pages based on the length of the array of selectable items.
    each page has 10 entries and each item can be selected by typing in the corresponding
    number 0 - 9

    Attributes
    ----------
    curPage : int
        This is the index of the current page, starting at 0
    pageSize : int
        This is the amount if items one page displays
    pageCount : int
        The number of pages

    Methods
    -------
    displaySelection()
        This method displays the selection and handles the input.
        It returns the indecies of the selection made or None on error.
    """

    def __init__(self, array):
        self.__array = array
        self.curPage = 0
        self.pageSize = 10
        self.pageCount = math.ceil((len(self.__array) - 1) / self.pageSize) - 1

    def displaySelection(self):
        """
        This function displays the selection on different pages

        Note that the displayed page is one higher than the underlying variable
        curPage holds.
        """

        os.system('cls')
        intro()

        pageStartIndex = self.curPage * self.pageSize
        pageEndIndex = min(pageStartIndex + self.pageSize,
                           len(self.__array))

        # added 1 for better readability
        print("Page", self.curPage + 1, "/", self.pageCount + 1)
        self.__printHints()

        i = 0
        for w in itertools.islice(self.__array, pageStartIndex, pageEndIndex):
            print(i, ") ", w.title, sep="")
            i = i + 1

        selection = input()

        if selection == "+":
            self.curPage = min(self.curPage + 1, self.pageCount)
            return self.displaySelection()

        if selection == "-":
            self.curPage = max(self.curPage - 1, 0)
            return self.displaySelection()

        indecies = []
        for c in selection:
            try:
                index = int(c)
                index = index + self.pageSize * self.curPage
            except ValueError:
                return None

            indecies.append(index)

        return indecies

    def __printHints(self):
        if self.curPage > 0:
            leftHint = "<< -"
        else:
            leftHint = "    "

        if self.curPage < self.pageCount:
            rightHint = "+ >>"
        else:
            rightHint = "    "

        print(leftHint, "   ", rightHint)


workspaces = []
"""
This is the array of set workspaces

If you want to add one, just add it to test list by calling
    Workspace("", URLs=[], files=[], programs=[])
Fill in the parameters as needed:
    Workspace("Title of the workspace", URLs=[array of urls], files=[array of directories, or files], programs=[array of programs])

Also note, that the paths should only contain forward slashes. If copying a windows file path
the default are backslashed. Replace them with forward slashes.
This can be done by using Ctrl-F to find and replace these characters.
"""

ps = PageableSelection(workspaces)


def main():
    indecies = ps.displaySelection()

    if indecies == None:
        os.system('cls')
        print("An error ocurred.")
        main()

    for index in indecies:
        if index < 0 or index >= len(workspaces):
            os.system('cls')
            print(
                "The given input was out of range.\n")
            main()

        workspaces[index].open()


def intro():
    print(
        " _       __           __                                  \n",
        "| |     / /___  _____/ /___________  ____ _________  _____\n",
        "| | /| / / __ \/ ___/ //_/ ___/ __ \/ __ `/ ___/ _ \/ ___/\n",
        "| |/ |/ / /_/ / /  / ,< (__  ) /_/ / /_/ / /__/  __(__  ) \n",
        "|__/|__/\____/_/  /_/|_/____/ .___/\__,_/\___/\___/____/  \n",
        "                           /_/                            \n", sep="")
    print("Select on of these workspaces by typing in the corresponding number, select more by concatinating your choices.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(3)
