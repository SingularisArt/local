import os
import subprocess
from rofi import Rofi
from pathlib import Path

r = Rofi()

tex_types = ['.tex', '.latex']
new_chap = False
discourage_folders = ['images', 'assignments', 'figures', 'projects',
                      '.git', 'media', 'current-course']

EDITOR = 'nvim'
VIEWER = 'zathura'
TERMINAL = 'xfce4-terminal'
NOTES_DIR = Path('~/Documents/notes').expanduser()
ROOT = '{}/Grade-10/semester-2'.format(NOTES_DIR)
CURRENT_COURSE = '{}/current-course'.format(NOTES_DIR)
SOURCE_LESSONS_LOCATION = '{}/source-lessons.tex'.format(CURRENT_COURSE)

# if not os.path.isdir(CURRENT_COURSE):
#     r.error('''
#               You don\'t have a CURRENT_COURSE in your notes dir.
#                               Please set that up!
#               To do this, you can run `py rofi-current-course.py`
#                             or run `WINDOWS+ALT+c`.
#      Then, you choose the class that you want to set as your current class.
#                    After all of that, you can run this file.
# ''')
#     exit(1)


def rofi(prompt, options, rofi_args=[], fuzzy=True):
    optionstr = '\n'.join(option.replace('\n', ' ') for option in options)
    args = ['rofi', '-sort', '-no-levenshtein-sort']
    if fuzzy:
        args += ['-matching', 'fuzzy']
    args += ['-dmenu', '-p', prompt, '-format', 's', '-i']
    args += rofi_args
    args = [str(arg) for arg in args]

    result = subprocess.run(args, input=optionstr,
                            stdout=subprocess.PIPE, universal_newlines=True)
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
