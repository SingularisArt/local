#!/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: Mar 06 2022 Sun (02:29:21)

OPTIONS:
    Current Lesson: This one will ask the user to select a unit. Then,
        from that unit, the program will source the last lesson.

    Last Two Lessons: This one will ask the user to select a unit.
        Then, from that unit, the program will source the two lessons.

    All Lessons From in Unit: This one will ask the user to select a
        unit Then, the program will ask if he wants to source all
        lessons. The user can specify a range of lessons to source. The
        program will only source the lessons that exist.

    Source Selected Units: This one will give the user the list of all the
        units available. The user can select the units he wants to source. Then
        the program sources all of the lessons in each of the unit selected.
        IT'S COMING SOON!

    All Lessons: This one will just source all of the lessons.
"""

import os
import sys
import ntpath
from config import Configuration


class SourceLessons(Configuration):
    """
    Class for different ways to source your lessons.
    It's inherited from the config.py/Configuration class

    Methods:
    --------

    """

    def __init__(self):
        Configuration.__init__(self)

        """ This function initializes the class """

        # The users options
        self.options = [
            "<i><b><span color='yellow'>Current lesson</span></b></i>",
            "<i><b><span color='yellow'>Last two lessons</span></b></i>",
            "<i><b><span color='yellow'>All lessons in Unit</span></b></i>",
            "<i><b><span color='yellow'>Select Multiple Units</span></b></i>",
            "<i><b><span color='yellow'>All lessons</span></b></i>",
        ]

        self.index = 0
        self.selected = self.options[self.index]

        # This gets all of the folders within the current course
        # The folders_head stores the absolute path to each folder
        # The folders_tail stores the folder name
        self.folders_head, self.folders_tail = self._get_all_folders()

        # This gets all of the units within the current course
        # The units_head stores the absolute path to each unit
        # The units_tail stores the unit folder name
        self.units_head, self.units_tail = self._get_all_units()

        # This gets all of the lessons within the current course
        # The lessons_head stores the absolute path to each lesson
        # The lessons_tail stores the lesson file name
        self.lessons_head, self.lessons_tail, \
            self.all_lessons = self._get_all_lessons()

        # This gets the last two lessons, and the last unit number along with
        # its name
        self.last_lesson_head, \
            self.last_lesson_tail, \
            self.second_to_last_lesson_head, \
            self.second_to_last_lesson_tail, \
            self.last_unit_name, \
            self.last_unit_number = self._get_latest_lesson(
                self.lessons_head)

    def _get_all_folders(self):
        """
        This function returns all of the folders in a list.
        It returns them in this order
        folder_head, folder_tail

        folder_head: This is the absolute path to the folder
        folder_tail: This is just the name for the folder
        """

        # The lists, which we will return later on.
        folders_head = []
        folders_tail = []

        # Getting all of the folders within our current course
        sub_folders = sorted([f.path for f in os.scandir(self.current_course)
                              if f.is_dir()])

        # Iterating through each folder
        for folder in sub_folders:
            # Splitting the folder into the name and absolute path
            sub_folder_head, sub_folder_tail = ntpath.split(folder)

            # Checking if the folder doesn't equal to one of the folders
            # that we don't want
            if sub_folder_tail not in self.discourage_folders:
                # Adds the folder to the list of folders we want to return
                folders_head.append('{}/{}'.format(sub_folder_head,
                                    sub_folder_tail))
                folders_tail.append(sub_folder_tail)

        return folders_head, folders_tail

    def _get_all_units(self):
        """
        This function returns all of the units in a list.
        It returns them in this order

        unit_head: This is the absolute path to the unit
        unit_tail: This is just the name for the unit
        """

        # The lists, which we will return later on.
        units_head = []
        units_tail = []

        # Iterating through all of the absolute path folders
        for folder in self.folders_head:
            # Splits the folder into the name and absolute path
            unit_head, unit_tail = ntpath.split(folder)

            # Adds the folder to the list of folders we want to return
            units_head.append('{}/{}'.format(unit_head, unit_tail))
            units_tail.append(unit_tail)

        return units_head, units_tail

    def _get_all_lessons(self):
        """
        This function returns all of the lessons in a list.
        It returns them in this order

        lesson_head: list: This is the absolute path to the lesson
        lesson_tail: list: This is just the name for the lesson
        all_lessons: dict:
            {'unit-1': ['lesson-1.tex', 'lesson-2.tex', ...], 'unit-2', [...]}
        """

        # The lists, which we will return later on.
        lessons_head = []
        lessons_tail = []

        # This stores the unit number as the key and the lessons within that
        # unit as the values within a list
        # This will be returned at the end of the function
        all_lessons = {}

        # Iterating through all of the units absolute path
        for unit in self.units_head:
            # Getting all of the lessons within that unit
            lessons = sorted([os.path.join(unit, f) for f in os.listdir(unit)
                              if os.path.isfile(os.path.join(unit, f))])

            # Iterating through the lessons we got
            for lesson in lessons:
                # splitting the lesson into the naame and absolute path
                lesson_head, lesson_tail = ntpath.split(lesson)

                # Appending all of the information respectfully
                lessons_head.append('{}/{}'.format(lesson_head, lesson_tail))
                lessons_tail.append(lesson_tail)

        # Try just in case there are any lessons
        try:
            # Get the amount of lessons
            size = len(lessons_tail)
            # Don't know exactly what this does
            lessons_tail_splited = [idx + 1 for idx, val in
                                    enumerate(lessons_tail)
                                    if val == self.unit_info_name]

            # Don't know exactly what this does
            lessons_tail_new = [lessons_tail[i: j] for i, j in
                                zip([0] + lessons_tail_splited,
                                    lessons_tail_splited +
                                    ([size] if lessons_tail_splited[-1] != size
                                        else []))]

            # Iterate through all of our lessons
            for x, lesson in enumerate(lessons_tail_new):
                # Add the unit as the key and lessons as the value in a list
                # form
                all_lessons[self.units_tail[x]] = lesson
        # Create an exception error if now lessons found
        except Exception:
            # Have rofi say no lessons found
            self.r.error('No lessons found')
            # Exit program
            sys.exit(1)

        return lessons_head, lessons_tail, all_lessons

    def _get_latest_lesson(self, lessons: list) -> str:
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

        if len(lessons) == 0:
            self.r.error('No lessons found')
            # sys.exit(1)
        elif len(lessons) == 1:
            latest_lesson_head = ntpath.split(lessons[-1])[0]
            latest_lesson_tail = ntpath.split(lessons[-1])[1]

            second_to_last_lesson_head = 'NONE'
            second_to_last_lesson_tail = 'NONE'

            last_unit_name = ntpath.split(latest_lesson_head)[1]
            last_unit_number = last_unit_name[5:]
        elif len(lessons) == 2:
            latest_lesson_head = ntpath.split(lessons[-1])[0]
            latest_lesson_tail = ntpath.split(lessons[-1])[1]

            second_to_last_lesson_head = ntpath.split(lessons[-2])[0]
            second_to_last_lesson_tail = ntpath.split(lessons[-2])[1]

            last_unit_name = ntpath.split(latest_lesson_head)[1]
            last_unit_number = last_unit_name[5:]
        elif len(lessons) >= 3:
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

    def _update_selection(self, selection):
        self.selected = selection

    def source_current_lesson(self):
        with open(self.source_lessons_location, 'w') as source_lessons_file:
            # It writes this as an example: % Unit 1 Started
            source_lessons_file.write('% Unit {} Started\n'.format(
                self.last_unit_number))

            # Source the last lesson
            source_lessons_file.write('\\input{' + self.last_unit_name + '/' +
                                      self.last_lesson_tail + '}\n')

            # It writes this as an example: % Unit 1 Ended
            source_lessons_file.write('% Unit {} Ended'.format(
                self.last_unit_number))

    def source_last_two_lessons(self):
        # We're checking if we have a second to last lesson
        if self.second_to_last_lesson_head != 'NONE':
            # If we do, then we're going to write the last and second last
            # lesson to the source file
            with open(self.source_lessons_location, 'w') as source_lessons_file:
                # It writes this as an example: % Unit 1 Started
                source_lessons_file.write('% Unit {} Started\n'.format(
                    self.last_unit_number))

                # Source second to last lesson
                source_lessons_file.write('\\input{' + self.last_unit_name +
                                          '/' + self.second_to_last_lesson_tail
                                          + '}\n')
                # Source last lesson
                source_lessons_file.write('\\input{' + self.last_unit_name +
                                          '/' + self.last_lesson_tail + '}\n')

                # It writes this as an example: % Unit 1 Ended
                source_lessons_file.write('% Unit {} Ended'.format(
                    self.last_unit_number))
        # If we don't, we'll just source the last lesson
        else:
            self.source_current_lesson()

    def source_all_lessons_in_unit(self, unit):
        with open(self.source_lessons_location, 'w') as source_lessons_file:
            # It writes this as an example: % Unit 1 Started
            source_lessons_file.write('% Unit {} Started\n'.format(
                unit[5:]))

            # It writes this as an example: \input{unit-1/unit-info.tex}
            input_string = '\\input{' + unit + \
                           '/' + self.unit_info_name + '}'
            source_lessons_file.write('{}\n'.format(input_string))

            # The path to the selected unit
            unit_path = "{}/{}".format(self.current_course, unit)
            # This is complicated to explain. When I just iterated through
            # a list of all the lessons, it would output something like this:
            # lesson-1.tex lesson-10.tex lesson-2.tex lesson-3.tex
            # It would make big leaps like that. So, we create a forloop using
            # this number and we check if the lessons exists. Example:
            # lesson-1.tex, lesson-2.tex, lesson-3.tex, lesson-4.tex
            # If that exists, then we will write this:
            # \input{unit-1/lesson-1.tex}
            lesson_range_to_source = 1000

            # Iterating through the lesson_range_to_source variable
            for i in range(lesson_range_to_source):
                # The path to the lesson
                lesson_name = "{}/lesson-{}.tex".format(unit_path, i)
                # Checking if the lesson exists
                if os.path.exists(lesson_name):
                    # If it does, then write it to the source_lessons file.
                    # Example: \input{unit-1/lesson-1.tex}
                    input_string = '\\input{' + unit + '/lesson-' + str(i) + \
                                   '.tex}\n'
                    source_lessons_file.write(input_string)

            # It writes this as an example: % Unit 1 Ended
            source_lessons_file.write('% Unit {} Ended\n'.format(unit[5:]))

    def source_range(self, lesson_range, unit_number):
        range_list = lesson_range.split('-')

        unit_info_path = self.current_course + '/source-lessons.tex'

        with open(unit_info_path, 'w') as source_lessons_file:
            source_lessons_file.write('% Unit {} Started\n'.format(
                unit_number[5:]))
            source_lessons_file.write('\\input{' + unit_number +
                                      '/' + self.unit_info_name + '}\n')

            for lesson_number in range(int(range_list[0]),
                                       int(range_list[1]) + 1):
                # Check if lesson exists
                if os.path.exists('{}/{}/lesson-{}.tex'.format(
                            self.current_course, unit_number, lesson_number)):
                    # Write to the source-lessons.tex file
                    string = '\\input{' + unit_number + '/lesson-' + \
                             str(lesson_number) + '.tex}\n'

                    source_lessons_file.write(string)

            source_lessons_file.write('% Unit {} Ended'.format(
                unit_number[5:]))

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

        unit = units[index]
        selection = ["<i><b><span color='yellow'>All Lessons</span></b></i>"]
        key, index, selected = self.rofi(
            'Select Option (You can also use a range. 1-{})'.format(
                len(self.all_lessons[unit]) - 1),
            selection,
            ['-scroll-method', 1,
             '-lines', 5,
             '-markup-rows']
        )

        if selected != selection[0]:
            self.source_range(selected, unit)
        else:
            self.source_all_lessons_in_unit(unit)

    def source_selected_units(self):
        self.r.status('Coming Soon ...')

    def source_all_lessons(self):
        with open(self.source_lessons_location, 'w') as source_lessons_file:
            for x, lesson in enumerate(self.all_lessons.values()):
                current_unit = self.units_tail[x]

                source_lessons_file.write('% Unit {} Started\n'.format(
                    current_unit[5:]))

                source_lessons_file.write('\\input{' + current_unit + '/' +
                                          self.unit_info_name + '}\n')

                for les in range(1000):
                    if os.path.exists('{}/{}/lesson-{}.tex'.format(
                            self.current_course, current_unit, les)):
                        source_lessons_file.write('\\input{' +
                                                  self.units_tail[x] +
                                                  '/lesson-' + str(les) +
                                                  '.tex}\n')

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
            self.source_specific_unit()
        elif self.selected == self.options[3]:
            self.source_selected_units()
        elif self.selected == self.options[4]:
            self.source_all_lessons()


lesson = SourceLessons()

_, _, selected = lesson.rofi('Select Option',
                             lesson.options,
                             ['-scroll-method', 1,
                              '-lines', 5,
                              '-markup-rows'])

lesson._update_selection(selected)

lesson.check_selection()
