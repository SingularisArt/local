#!/usr/bin/env python3

import os
import sys
import yaml


class ChangeCourse:
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

        self.classes = sorted(self.get_classes())
        self.titles = sorted(self.get_titles())

    def get_classes(self):
        return sorted([os.path.join(self.root, o)
                       for o in os.listdir(self.root)
                       if os.path.isdir(os.path.join(self.root, o))])

    def get_titles(self):
        titles = []
        file_info = ''

        for current_class in self.classes:
            try:
                info = open('{}/info.yaml'.format(current_class))
                file_info = yaml.load(info, Loader=yaml.FullLoader)

                titles.append("<b><span color='blue'>{: <{}}</span></b>"
                              "<span color='grey'>(</span><i>"
                              "<span color='yellow'>{}</span></i>"
                              "<span color='grey'>)</span>".format(
                                        file_info['title'],
                                        25,
                                        file_info['short']))
            except Exception:
                pass

        return titles


def main():
    course = ChangeCourse()

    key, index, selected = course.rofi('Select class', course.titles, [
        '-lines', 5,
        '-markup-rows',
        '-kb-row-down', 'Down',
        '-kb-custom-1', 'Ctrl+n'
    ])

    current_class = os.path.realpath(course.current_course)
    current_class = os.path.basename(os.path.normpath(current_class))
    current_class = current_class.replace('-', ' ')
    current_class = current_class.replace('hs', 'Honors')
    current_class = current_class.title()

    new_class = os.path.basename(os.path.normpath(course.classes[index]))
    new_class = new_class.replace('-', ' ')
    new_class = new_class.replace('hs', 'Honors')
    new_class = new_class.title()

    if os.path.isdir(course.current_course):
        os.remove(course.current_course)
    os.symlink(course.classes[index], course.current_course)


if __name__ == '__main__':
    main()
