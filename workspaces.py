#!/usr/bin/env python
"""
This program opens specified user workspaces to safe time

Upon starting this program will show a list of set workspaces.
Using the commandline input the use can specify the workspaces by typing
in the corresponding index.
If the user wishes to open multiple different workspaces, just write the input
simultaneously.

For example if one wishes to open the workspace 1 and 3, just type in
13, the program will split the input char by char and evaluate it
individually.

If the amount of workspaces exceeds the 10 this program will automatically
create pages and the ability to flip between them.

Known limitation: one can only select workspaces from the same page
"""

import itertools
import math
import os
import webbrowser

__author__ = "Simon Josef Kreuzpointner"


class Workspace:
    """
    This class represents a workspace

    A workspace consists of a collection of files, websites
    and programs that are needed in a specific work setting.

    Calling open() on a workspace opens all the given files, websites
    and programs so the end user does not need to open these by
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

    def __init__(self, title, urls=None, files=None, programs=None):
        """
        Parameters
        ----------
        title : str
            the title of the workspace
        urls : str[] optional
            an array of URLs to be opened
        files : str[] optional
            an array of file or directory paths
        programs : str[] optional
            an array of program paths
        """

        self.title = title
        self.__urls = urls
        self.__files = files
        self.__programs = programs

    def open(self):
        """
        This function opens the workspace.

        This means all the given Urls are opened first.
        Every URL will be opened in a new tab on the system default web browser.
        This will not check if the site is already opened.

        Second, it will open all the given files using the system default
        file-open-action. If the given file is directory it will be opened
        on the Windows Explorer.

        At last all the given programs will be opened. This program
        simulates a double click on the specified programs.
        """
        self.__open_urls()
        self.__open_files()
        self.__start_programs()

    def __open_urls(self):
        if self.__urls is None:
            return

        print("Opening URLs...")
        for url in self.__urls:
            webbrowser.open(url, new=2)

    def __open_files(self):
        if self.__files is None:
            return

        print("Opening files...")
        for f in self.__files:
            if os.path.isfile(f):
                os.startfile(f)
            elif os.path.isdir(f):
                os.startfile(f, operation="explore")

    def __start_programs(self):
        if self.__programs is None:
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
    cur_page : int
        This is the index of the current page, starting at 0
    page_size : int
        This is the amount if items one-page displays
    page_count : int
        The number of pages

    Methods
    -------
    displaySelection()
        This method displays the selection and handles the input.
        It returns the indices of the selection made or None on error.
    """

    def __init__(self, array):
        self.__array = array
        self.cur_page = 0
        self.page_size = 10
        self.page_count = math.ceil((len(self.__array) - 1) / self.page_size) - 1

    def display_selection(self):
        """
        This function displays the selection on different pages

        Note that the displayed page is one higher than the underlying variable
        curPage holds.
        """

        os.system('cls')
        intro()

        page_start_index = self.cur_page * self.page_size
        page_end_index = min(page_start_index + self.page_size, len(self.__array))

        # added 1 for better readability
        print("Page", self.cur_page + 1, "/", self.page_count + 1)
        self.__print_hints()

        i = 0
        for w in itertools.islice(self.__array, page_start_index, page_end_index):
            print(i, ") ", w.title, sep="")
            i = i + 1

        selection = input()

        if selection == "+":
            self.cur_page = min(self.cur_page + 1, self.page_count)
            return self.display_selection()

        if selection == "-":
            self.cur_page = max(self.cur_page - 1, 0)
            return self.display_selection()

        indices = []
        for c in selection:
            try:
                index = int(c)
                index = index + self.page_size * self.cur_page
            except ValueError:
                return None

            indices.append(index)

        return indices

    def __print_hints(self):
        if self.cur_page > 0:
            left_hint = "<< -"
        else:
            left_hint = "    "

        if self.cur_page < self.page_count:
            right_hint = "+ >>"
        else:
            right_hint = "    "

        print(left_hint, "   ", right_hint)


def main():
    workspaces = []
    """
    This is the array of set workspaces

    If you want to add one, just add it to test list by calling
        Workspace("", urls=[], files=[], programs=[])
    Fill in the parameters as needed:
        Workspace("Title of the workspace",
            urls=[array of urls],
            files=[array of directories, or files],
            programs=[array of programs])

    Also note, that the paths should only contain forward slashes. If copying a windows file path
    the default are backslashes. Replace them with forward slashes.
    This can be done by using Ctrl-F to find and replace these characters.
    """

    ps = PageableSelection(workspaces)
    indices = ps.display_selection()

    if indices is None:
        clear_screen()
        print("An error occurred.")
        main()

    for index in indices:
        if index < 0 or index >= len(workspaces):
            clear_screen()
            print(
                "The given input was out of range.\n")
            main()

        workspaces[index].open()


def intro():
    print(
        " _       __           __                                  ",
        "| |     / /___  _____/ /___________  ____ _________  _____",
        "| | /| / / __ \/ ___/ //_/ ___/ __ \/ __ `/ ___/ _ \/ ___/",
        "| |/ |/ / /_/ / /  / ,< (__  ) /_/ / /_/ / /__/  __(__  ) ",
        "|__/|__/\____/_/  /_/|_/____/ .___/\__,_/\___/\___/____/  ",
        "                           /_/                            ", sep="\n")
    print(
        "Select on of these workspaces by typing in the corresponding number, " +
        "select more by concatenating your choices.\n")


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(3)
