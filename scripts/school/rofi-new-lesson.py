#!/usr/bin/env python3

import re
import os
import sys
from datetime import date, datetime

HOME = os.path.expanduser('~')

sys.path.insert(0, '{}/ ~/Singularis/local/scripts/school/')

from config import CURRENT_COURSE, tex_types, r

file_name = r.text_entry('File name EX: (unit-1/lesson-19.tex)')

# Check if the file isn't a LaTeX file
if file_name[-4:] not in tex_types:
    tex_types = ', '.join(tex_types)
    r.error('Sorry! The file must a LaTeX file ({})'.format(tex_types))

# Perform the regex to get the unit number and lesson number
lesson_match = re.search(r'unit-(\d+)/(lesson-\d+)\.tex', file_name)

# If the lesson is the first lesson, then we ask for the module name
try:
    if lesson_match.group(2) == 'lesson-1':
        module_name = r.text_entry('Enter module name')
        new_chap = True
except Exception:
    new_chap = False

# Get some extra data
file_number = r.integer_entry('Lesson number')
lesson_name = r.text_entry('Lesson name')
lesson_unit = r.text_entry('Lesson unit EX: (Unit 3)')

# Check if the lesson already exists
if os.path.exists(CURRENT_COURSE + '/' + file_name):
    r.error('Sorry! A file already exists with that name! Try again.')
    exit(1)

# Get some extra data
today = date.today()
now = datetime.now()
today_date = today.strftime('%b %d %Y %a')
current_time = now.strftime(' (%H:%M:%S)')

# Transform from the inputted unit to the folder unit name
# Example: Unit 10 - unit-10
lesson_unit_folder_name = lesson_unit.replace(' ', '-')
lesson_unit_folder_name = lesson_unit_folder_name.lower()

# Check if the folder exists. If it doesn't, we simply create it
if not os.path.isdir('{}/{}'.format(CURRENT_COURSE, lesson_unit_folder_name)):
    os.makedirs('{}/{}'.format(CURRENT_COURSE, lesson_unit_folder_name))

# Write all of the information to the file that the user wants to create
with open(CURRENT_COURSE + '/' + file_name, 'w') as new_file:
    new_file.write('\\lesson{' + str(file_number) + '}{' + today_date + current_time + '}{' + lesson_name + '}' + '{' + lesson_unit + '}')
    new_file.write('\n\n\n\n\\newpage')

# Add the file to the `source-lesson.tex` file to input it into the master.tex
with open(CURRENT_COURSE + '/source-lessons.tex', 'a') as source_file:
    # If we are creating the first lesson of the unit, the we will
    # Add the Unit name and the Unit number in the unit-info.tex file
    # And then we will source it in the source-lessons.tex
    if new_chap:
        with open(CURRENT_COURSE + '/unit-info.tex', 'w') as unit_info_file:
            unit_info_file.write('\\chapter{}')
        source_file.write('\\input{' + lesson_unit + '/unit-info}\n')
    source_file.write('\\input{' + file_name[:-4] + '}\n')
