#!/usr/bin/env python3

from datetime import datetime
import ntpath
import sys
import re
import os

HOME = os.path.expanduser('~')

sys.path.insert(0, '{}/ ~/Singularis/local/scripts/school/')

from config import r, rofi, EDITOR, TERMINAL, CURRENT_COURSE

units = [os.path.join(CURRENT_COURSE, o) for o in os.listdir(CURRENT_COURSE)
         if os.path.isdir(os.path.join(CURRENT_COURSE, o))]
options = []
lesson_numbers = []
lesson_dates = []
lesson_names = []
lesson_units = []


def get_week(d=datetime.today()):
    return (int(d.strftime('%W')) + 52 - 5) % 52


if not os.path.isdir(CURRENT_COURSE):
    r.error('''
              You don\'t have a CURRENT_COURSE in your notes dir.
                              Please set that up!
              To do this, you can run `py rofi-current-course.py`
                            or run `WINDOWS+ALT+c`.
     Then, you choose the class that you want to set as your current class.
                   After all of that, you can run this file.
''')
    exit(1)

for unit in units:
    unit_head, unit_tail = ntpath.split(unit)

    lessons = [os.path.join(unit, o) for o in os.listdir(unit)
               if os.path.isfile(os.path.join(unit, o))]

    lessons = sorted(lessons)

    for lesson in lessons:
        lesson_head, lesson_tail = ntpath.split(lesson)

        if unit_tail != 'figures':
            with open(lesson, encoding="utf8", errors='ignore') as f:
                for line in f:
                    for count, _ in enumerate(f):
                        pass
                    try:
                        lesson_match = re.search(
                            r'\\lesson\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}',
                            line)

                        lesson_number = lesson_match.group(1)
                        lesson_date = lesson_match.group(2)
                        lesson_name = lesson_match.group(3)
                        lesson_unit = lesson_match.group(4)

                        lesson_numbers.append(lesson_number)
                        lesson_dates.append(lesson_date)
                        lesson_names.append(lesson_name)
                        lesson_units.append(lesson_unit.replace(
                            'U', 'u',).replace(' ', '-'))

                        if count <= 5:
                            lesson_unit += " File Empty"

                        options.append(
                            "<span color='red'>{number: >2}</span>. <b><span color='blue'>{title: <{fill}}</span></b> <i><span color='yellow' size='smaller'>{date}</span> <span color='green' size='smaller'>({week})</span></i>".format(
                                fill=35,
                                number=lesson_number,
                                title=lesson_name,
                                date=lesson_date,
                                week=lesson_unit
                            ))
                        break
                    except Exception:
                        pass

key, index, selected = rofi('Select lesson', options, [
    '-scroll-method', 1,
    '-lines', 5,
    '-markup-rows',
    '-kb-row-down', 'Down',
    '-kb-custom-1', 'Ctrl+n',
    '-keep-left'
])

os.system('nvim-ctrl "-e {}"'.format('{}/{}/lesson-{}.tex'.format(
    CURRENT_COURSE,
    lesson_units[index],
    lesson_numbers[index])))
