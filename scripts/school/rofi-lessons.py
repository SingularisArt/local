#!/usr/bin/env python3

import re
import os
import sys
import ntpath
from datetime import datetime


class Lessons:
    def __init__(self):
        self.home = os.path.expanduser('~')
        sys.path.insert(0, '{}/Singularis/local/scripts/school/'.format(
                            self.home))

        from config import tex_types, new_chap, discourage_folders, rofi
        from config import EDITOR, TERMINAL, NOTES_DIR, ROOT
        from config import CURRENT_COURSE, SOURCE_LESSONS_LOCATION

        self.tex_types = tex_types
        self.new_chap = new_chap
        self.discourage_folders = discourage_folders

        self.rofi = rofi

        self.editor = EDITOR
        self.terminal = TERMINAL
        self.notes_dir = NOTES_DIR
        self.root = ROOT
        self.current_course = CURRENT_COURSE
        self.source_lesson_location = SOURCE_LESSONS_LOCATION

        self.units = sorted(self.get_units())
        self.options, \
            self.lesson_numbers, \
            self.lesson_dates, self.lesson_names, \
            self.lesson_units = self.get_lesson_info()

    def get_units(self):
        return [os.path.join(self.current_course, o)
                for o in os.listdir(self.current_course)
                if os.path.isdir(os.path.join(self.current_course, o))]

    def get_week(self, d=datetime.today()):
        return (int(d.strftime('%W')) + 52 - 5) % 52

    def get_lesson_info(self):
        options = []
        lesson_numbers = []
        lesson_dates = []
        lesson_names = []
        lesson_units = []

        for unit in self.units:
            unit_head, unit_tail = ntpath.split(unit)

            lessons = sorted([os.path.join(unit, o) for o in os.listdir(unit)
                              if os.path.isfile(os.path.join(unit, o))])

            for lesson in lessons:
                lesson_head, lesson_tail = ntpath.split(lesson)

                if lesson_tail in self.discourage_folders:
                    break
                with open(lesson, encoding="utf8",
                          errors='ignore') as lesson_file:
                    for line in lesson_file:
                        for count, _ in enumerate(lesson_file):
                            pass
                        lesson_match = re.search(
                            r'\\lesson\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}',
                            line)

                        try:
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
                                "<span color='red'>{number: >2}</span>. "
                                "<b><span color='blue'>{title: <{fill}}</span>"
                                "</b> <i><span color='yellow' size='smaller'>"
                                "{date}</span> <span color='green' "
                                "size='smaller'>({week})</span></i>".format(
                                    fill=35,
                                    number=lesson_number,
                                    title=lesson_name,
                                    date=lesson_date,
                                    week=lesson_unit
                                ))
                        except Exception:
                            pass

        return options, lesson_numbers, lesson_dates, \
            lesson_names, lesson_units


lesson = Lessons()

key, index, selected = lesson.rofi('Select lesson', lesson.options, [
    '-scroll-method', 1,
    '-lines', 5,
    '-markup-rows',
    '-kb-row-down', 'Down',
    '-kb-custom-1', 'Ctrl+n',
    '-keep-left'
])

os.system('xfce4-terminal -e "{} {}"'.format(lesson.editor,
          '{}/{}/lesson-{}.tex'.format(
            lesson.current_course,
            lesson.lesson_units[index],
            lesson.lesson_numbers[index])))
