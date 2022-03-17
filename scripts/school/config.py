import os
import subprocess
from rofi import Rofi
from pathlib import Path


class Configuration:
    """
    Methods:
    --------
    rofi: This is a wrapper function that helps you ask the user for input
    """

    def __init__(self):
        """
        Attributes:
        -----------
        editor: The editor to use (neovim)
        viewer: The pdf viewer to use (zathura)
        terminal: The terminal to use (xfce4-terminal)
        notes_dir: The base path to the notes directory (~/Documents/notes)
        root: The base directory for your classes
                                        (~/Documents/notes/Grade-10/semester-2)
        current_course: Path to current course (~/Documents/notes/current)
        source_lessons_location: The path to the source-lessons.tex file
                                         (~/Documents/notes/source-lessons.tex)
        r: An instance of the Rofi class
        text_types: A list of file types that are considered latex files
                                                           (['.tex', '.latex'])
        new_chap: A boolean indicating if we need to create a new chapter
                                                                        (False)
        discourage_folders: A list of folders that should not be considered
                                          (['images', 'assignments', 'figures',
                                            'projects', '.git', 'media',
                                            'current-course'])
        """

        self.editor = 'nvim'
        self.viewer = 'zathura'
        self.terminal = 'xfce4-terminal'
        self.notes_dir = Path('~/Documents/notes').expanduser()
        self.root = '{}/Grade-10/semester-2'.format(self.notes_dir)
        self.current_course = '{}/current-course'.format(self.notes_dir)
        self.source_lessons_location = '{}/source-lessons.tex'.format(
            self.current_course)

        self.r = Rofi()

        self.tex_types = ['.tex', '.latex']
        self.discourage_folders = ['images', 'assignments', 'figures',
                                   'projects', '.git', 'media',
                                   'current-course']
        self.new_chap = False

        self.unit_info_name = 'unit-info.tex'

        self.home = Path.home()
        self.user = os.getenv('USER')

    # These are the functions that only the

    def rofi(self, prompt, options, rofi_args=[], fuzzy=True):
        """
        Wrapper function for rofi.

        Parameters:
        -----------

        prompt: The prompt to display to the user
        options: A list of options to display to the user
        rofi_args: A list of arguments to pass to rofi ([])
        fuzzy: A boolean indicating if we should use fuzzy matching (True)
        """

        optionstr = '\n'.join(option.replace('\n', ' ') for option in options)

        args = ['rofi', '-sort', '-no-levenshtein-sort']

        if fuzzy:
            args += ['-matching', 'fuzzy']

        args += ['-dmenu', '-p', prompt, '-format', 's', '-i']
        args += rofi_args
        args = [str(arg) for arg in args]

        result = subprocess.run(args, input=optionstr,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)

        returncode = result.returncode
        stdout = result.stdout.strip()

        selected = stdout.strip()

        try:
            index = [opt.strip() for opt in options].index(selected)
        except ValueError:
            index = -1

        if returncode == 0:
            key = 0
        if returncode == 1:
            key = -1
        if returncode > 9:
            key = returncode - 9

        return key, index, selected
