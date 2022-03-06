#!/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Jan 23 2022 Sun (00:45:44)
This class is used to create a rofi menu for the user to select a command
to execute.
The commands source a selected number of lessons from my notes directory
which is located ~/Documents/notes/.
Then, the user is given the option to open the compiled pdf.
"""

import os
import sys
import ntpath
from rofi import Rofi


class SourceLessons:
    def __init__(self):
        """ This function initializes the class """

        self.home = os.path.expanduser('~')
        sys.path.insert(0, '{}/Singularis/local/scripts/school/'.format(
                            self.home))

        from config import tex_types, new_chap, discourage_folders, rofi
        from config import EDITOR, VIEWER, TERMINAL, NOTES_DIR, ROOT
        from config import CURRENT_COURSE, SOURCE_LESSONS_LOCATION

        self.tex_types = tex_types
        self.new_chap = new_chap
        self.discourage_folders = discourage_folders

        self.rofi = rofi
        self.r = Rofi()

        self.editor = EDITOR
        self.viewer = VIEWER
        self.terminal = TERMINAL
        self.notes_dir = NOTES_DIR
        self.root = ROOT
        self.current_course = CURRENT_COURSE
        self.source_lesson_location = SOURCE_LESSONS_LOCATION

        self.options = [
            "<i><b><span color='yellow'>Current lesson</span></b></i>",
            "<i><b><span color='yellow'>Last two lessons</span></b></i>",
            "<i><b><span color='yellow'>All lessons in Unit</span></b></i>",
            "<i><b><span color='yellow'>All Lessons From A Specific Unit</span></b></i>",
            "<i><b><span color='yellow'>All lessons</span></b></i>",
        ]

        self.index = 0
        self.selected = self.options[self.index]

        self.unit_info_name = 'unit-info.tex'
        self.folders_head, self.folders_tail = self.get_all_folders()
        self.units_head, self.units_tail = self.get_all_units()
        self.lessons_head, self.lessons_tail, \
            self.all_lessons = self.get_all_lessons()

        self.last_lesson_head, \
            self.last_lesson_tail, \
            self.second_to_last_lesson_head, \
            self.second_to_last_lesson_tail, \
            self.last_unit_name, \
            self.last_unit_number = self.get_latest_lesson(
                    self.lessons_head)

    def get_all_folders(self):
        """
        This function returns all of the folders in a list.
        It returns them in this order
        folder_head, folder_tail
        folder_head: This is the absolute path to the folder
        folder_tail: This is just the name for the folder
        """
        folders_head = []
        folders_tail = []
        sub_folders = sorted([f.path for f in os.scandir(self.current_course)
                              if f.is_dir()])

        for folder in sub_folders:
            sub_folder_head, sub_folder_tail = ntpath.split(folder)
            if sub_folder_tail not in self.discourage_folders:
                folders_head.append('{}/{}'.format(sub_folder_head,
                                    sub_folder_tail))
                folders_tail.append(sub_folder_tail)

        return folders_head, folders_tail

    def get_all_units(self):
        """
        This function returns all of the units in a list.
        It returns them in this order
        unit_head: This is the absolute path to the unit
        unit_tail: This is just the name for the unit
        """
        units_head = []
        units_tail = []

        for folder in self.folders_head:
            unit_head, unit_tail = ntpath.split(folder)
            units_head.append('{}/{}'.format(unit_head, unit_tail))
            units_tail.append(unit_tail)

        return units_head, units_tail

    def get_all_lessons(self):
        """
        This function returns all of the lessons in a list.
        It returns them in this order
        lesson_head: list: This is the absolute path to the lesson
        lesson_tail: list: This is just the name for the lesson
        all_lessons: dict: {'unit-1': ['lesson-1.tex', 'lesson-2.tex', ...]}
        """
        lessons_head = []
        lessons_tail = []
        all_lessons = {}

        for unit in self.units_head:
            lessons = sorted([os.path.join(unit, f) for f in os.listdir(unit)
                              if os.path.isfile(os.path.join(unit, f))])

            for lesson in lessons:
                lesson_head, lesson_tail = ntpath.split(lesson)

                lessons_head.append('{}/{}'.format(lesson_head, lesson_tail))
                lessons_tail.append(lesson_tail)

        try:
            size = len(lessons_tail)
            lessons_tail_splited = [idx + 1 for idx, val in
                                    enumerate(lessons_tail)
                                    if val == self.unit_info_name]

            lessons_tail_new = [lessons_tail[i: j] for i, j in
                                zip([0] + lessons_tail_splited,
                                    lessons_tail_splited +
                                    ([size] if lessons_tail_splited[-1] != size
                                        else []))]

            for x, lesson in enumerate(lessons_tail_new):
                all_lessons[self.units_tail[x]] = lesson
        except Exception:
            self.r.error('No lessons found')
            sys.exit(1)

        return lessons_head, lessons_tail, all_lessons

    def get_latest_lesson(self, lessons: list) -> str:
        """
        This function gets you the last two lessons.
        It returns them in this order
        latest_lesson_head: This is the absolute path to the last lesson
        latest_lesson_tail: This is the name of the last lesson
        second_to_last_lesson_head: This is the absolute path to the second to
            last lesson
        second_to_last_lesson_tail: This is the name of the
            second to last lesson
        :param lessons list: This is a list with all of the lessons
        """
        if ntpath.split(lessons[-1])[1] == self.unit_info_name:
            latest_lesson_head = ntpath.split(lessons[-2])[0]
            latest_lesson_tail = ntpath.split(lessons[-2])[1]
        else:
            latest_lesson_head = ntpath.split(lessons[-1])[0]
            latest_lesson_tail = ntpath.split(lessons[-2])[1]

        if ntpath.split(lessons[-2])[1] == self.unit_info_name:
            latest_lesson_head = ntpath.split(lessons[-3])[0]
            latest_lesson_tail = ntpath.split(lessons[-3])[1]
        else:
            if ntpath.split(lessons[-2])[1] == latest_lesson_tail:
                second_to_last_lesson_head = ntpath.split(lessons[-3])[0]
                second_to_last_lesson_tail = ntpath.split(lessons[-3])[1]
            else:
                second_to_last_lesson_head = ntpath.split(lessons[-2])[0]
                second_to_last_lesson_tail = ntpath.split(lessons[-2])[1]

        last_unit_name = ntpath.split(latest_lesson_head)[1]
        last_unit_number = last_unit_name[5:]

        return latest_lesson_head, \
            latest_lesson_tail, \
            second_to_last_lesson_head, \
            second_to_last_lesson_tail, \
            last_unit_name, \
            last_unit_number

    def source_current_lesson(self):
        lesson_string = '\\input{' + self.last_unit_name + '/' + \
                self.last_lesson_tail + '}\n'
        with open(self.source_lesson_location, 'w') as source_lessons_file:
            source_lessons_file.write('% Unit {} Started\n'.format(
                self.last_unit_number))
            source_lessons_file.write(lesson_string)
            source_lessons_file.write('% Unit {} Ended'.format(
                self.last_unit_number))

    def source_last_two_lessons(self):
        lesson_string = '\\input{' + self.last_unit_name + '/' + \
            self.second_to_last_lesson_tail + '}\n'
        lesson_string += '\\input{' + self.last_unit_name + '/' + \
            self.last_lesson_tail + '}\n'
        with open(self.source_lesson_location, 'w') as source_lessons_file:
            source_lessons_file.write('% Unit {} Started\n'.format(
                self.last_unit_number))
            source_lessons_file.write(lesson_string)
            source_lessons_file.write('% Unit {} Ended'.format(
                self.last_unit_number))

    def source_all_lessons_in_unit(self):
        with open(self.source_lesson_location, 'w') as source_lessons_file:
            source_lessons_file.write('% Unit {} Started\n'.format(
                self.last_unit_number))
            lesson_string = '\\input{' + self.last_unit_name + '/' + \
                self.unit_info_name + '}\n'

            source_lessons_file.write(lesson_string)

            for lesson in self.lessons_head:
                lesson_head, lesson_tail = ntpath.split(lesson)
                unit_head, unit_tail = ntpath.split(lesson_head)

                if unit_tail == self.last_unit_name:
                    if lesson_tail != self.unit_info_name:
                        lesson_string = '\\input{' + unit_tail + '/' + \
                                lesson_tail + '}\n'
                        source_lessons_file.write(lesson_string)

            source_lessons_file.write('% Unit {} Ended'.format(
                self.last_unit_number))

    def source_specific_unit(self):
        units_style = []
        units = []
        for u in self.units_tail:
            units.append(u)
            units_style.append(
                    f"<i><b><span color='yellow'>Unit {u[5:]}</span></b></i>"
            )

        key, index, selected = self.rofi('Select Unit',
                                         units_style,
                                         ['-scroll-method', 1,
                                          '-lines', 5,
                                          '-markup-rows'])
        with open(self.source_lesson_location, 'w') as source_lessons_file:
            source_lessons_file.write('% Unit {} Started\n'.format(
                units[index][5:]))
            input_string = '\\input{' + units[index] + \
                           '/' + self.unit_info_name + '}'
            source_lessons_file.write('{}\n'.format(input_string))

            unit_path = "{}/{}".format(self.current_course, units[index])
            lessons = [f for f in os.listdir(unit_path) if os.path.isfile(
                       os.path.join(unit_path, f))]

            for lesson in sorted(lessons):
                if lesson != self.unit_info_name:
                    input_string = '\\input{' + units[index] + \
                                   '/' + lesson + '}'
                    source_lessons_file.write('{}\n'.format(input_string))

            source_lessons_file.write('% Unit {} Ended\n'.format(
                units[index][5:]))

    def source_all_lessons(self):
        with open(self.source_lesson_location, 'w') as source_lessons_file:
            for x, lesson in enumerate(self.all_lessons.values()):
                current_unit = self.units_tail[x]

                source_lessons_file.write('% Unit {} Started\n'.format(
                    current_unit[5:]))

                lesson_string = '\\input{' + current_unit + '/' + \
                    self.unit_info_name + '}\n'

                source_lessons_file.write(lesson_string)

                for les in lesson:
                    if les != self.unit_info_name:
                        lesson_string = '\\input{' + self.units_tail[x] + \
                                '/' + les + '}\n'
                        source_lessons_file.write(lesson_string)

                if self.units_tail[x] == self.units_tail[-1]:
                    source_lessons_file.write('% Unit {} Ended'.format(
                        current_unit[5:]))
                else:
                    source_lessons_file.write('% Unit {} Ended\n\n\n'.format(
                        current_unit[5:]))

    def check_selection(self):
        if self.selected == self.options[0]:
            self.source_current_lesson()
        elif self.selected == self.options[1]:
            self.source_last_two_lessons()
        elif self.selected == self.options[2]:
            self.source_all_lessons_in_unit()
        elif self.selected == self.options[3]:
            self.source_specific_unit()
        elif self.selected == self.options[4]:
            self.source_all_lessons()


lesson = SourceLessons()

key, index, selected = lesson.rofi('Select Item, or type a range',
                                   lesson.options,
                                   ['-scroll-method', 1,
                                    '-lines', 5,
                                    '-markup-rows'])


lesson.selected = selected

lesson.check_selection()

os.chdir(lesson.current_course)
cwd = os.getcwd()

os.system('pdflatex master.tex')
os.system('pdflatex master.tex')
os.system('rubber --clean master')


key, index, selected = lesson.rofi('Finished',
                                   ['Open PDF', 'Exit'],
                                   ['-lines', 1, '-markup-rows'])


if selected == 'Open PDF':
    os.system('{} {}/master.pdf'.format(lesson.viewer, cwd))
else:
    sys.exit()
