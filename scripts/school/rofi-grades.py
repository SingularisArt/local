#!/usr/bin/env python3

"""
Author: Hashem A. Damrah
Date: 2022-02-09 03:15
"""

from bs4 import BeautifulSoup
from rofi import Rofi
import pandas as pd
import requests
import operator
import yaml
import sys
import os
import re


class Grades:
    def __init__(self):
        """This function initializes the class"""

        self.home = os.path.expanduser("~")
        sys.path.insert(0, "{}/Singularis/local/scripts/school/".format(self.home))

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

        self.headers = {
            "authority": "bakercharters.instructure.com",
            "cache-control": "max-age=0",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "_ga=GA1.2.776452699.1644355646; _gid=GA1.2.383447782.1644355646; _gat=1; log_session_id=57974abe9683873403e2457fb10a1fb4; _legacy_normandy_session=Hct16IcwPy_1YnailbhACg+Rz_Do0cIzMRZFgOCR3BIRpMSUyaWOFZ2aDwqfUvPdLZCPq_0_UvcqSVu4aEXEQaS0fYbXA9tek0UPnXd6tXKW0Crpgtsy1Zo-ofHYIJMCBLHSSAuPyN7PiqB2dXWJLsmXU365e7tslr5wZmhFxIlChnvk6mXnOExGutwF1qVa6ep0ZP-kqCMRmgdpcgCs7fveNeuimLqomfv-W4BDBmoL3yhKm657smI2IpFBGUDLbieneclLDw8ekeNnV8r7m36BdFnboJWP-tGv90u4BaB0cvg54iVjMLcKK1w6KEUHyp3KnERwxTH2bVk_w4-f3tfpEW4j_Ae5zJKwNm_pwGCabrBMuo_leK4EI3HrrFuYvaheMMH-e3NNzqxz_gmlW3dNNBXyxlarmqmmq0hlt2nc-NCI8qRLTBRSk4RN-GympE.y3XdOsrlkT6p8FVMr3fNFq1Mjus.YgORSw; canvas_session=Hct16IcwPy_1YnailbhACg+Rz_Do0cIzMRZFgOCR3BIRpMSUyaWOFZ2aDwqfUvPdLZCPq_0_UvcqSVu4aEXEQaS0fYbXA9tek0UPnXd6tXKW0Crpgtsy1Zo-ofHYIJMCBLHSSAuPyN7PiqB2dXWJLsmXU365e7tslr5wZmhFxIlChnvk6mXnOExGutwF1qVa6ep0ZP-kqCMRmgdpcgCs7fveNeuimLqomfv-W4BDBmoL3yhKm657smI2IpFBGUDLbieneclLDw8ekeNnV8r7m36BdFnboJWP-tGv90u4BaB0cvg54iVjMLcKK1w6KEUHyp3KnERwxTH2bVk_w4-f3tfpEW4j_Ae5zJKwNm_pwGCabrBMuo_leK4EI3HrrFuYvaheMMH-e3NNzqxz_gmlW3dNNBXyxlarmqmmq0hlt2nc-NCI8qRLTBRSk4RN-GympE.y3XdOsrlkT6p8FVMr3fNFq1Mjus.YgORSw; _csrf_token=sh%2BvAcnZMpHJB6Bapgpn7yf8iC2phUJDqKzNTKqTFr7hV%2F5Ore5m3KhAzx6QbF%2BoEa7CatO1dQrFx5sEy9Fi0w%3D%3D",
        }

        self.src, self.soup = self.get_src()
        (
            self.classes,
            self.grades,
            self.classes_and_grades,
        ) = self.get_classes_and_grades()

    def get_src(self):
        result = requests.get(
            "https://bakercharters.instructure.com/grades", headers=self.headers
        )
        src = result.content
        soup = BeautifulSoup(src, "lxml")

        return src, soup

    def get_classes_and_grades(self):
        links = self.soup.find_all("a")
        classes = []

        for link in links:
            try:
                link_id = re.search(
                    r"/courses/([0-9]+)/grades/([0-9]+)", link.attrs["href"]
                )
                link_id = link_id.group(1)
                classes.append(link.text)
            except Exception:
                pass

        grades = self.soup.find_all("td", {"class": "percent"})
        cleaned_grades = []

        for grade in grades:
            grade = (
                grade.text.replace("        ", "").replace("\n", "").replace(
                    "    ", "")
            )
            cleaned_grades.append(grade)

        grades = cleaned_grades

        classes_and_grades = {}

        for key in classes:
            for grade in grades:
                classes_and_grades[key] = grade
                grades.remove(grade)
                break

        classes_and_grades = sorted(
            classes_and_grades.items(), key=operator.itemgetter(0)
        )

        return classes, grades, classes_and_grades

    def output_info(self):
        information = ''
        for class_and_grade in self.classes_and_grades:
            for x, class_or_grade in enumerate(class_and_grade):
                try:
                    information += "{} - {}\n".format(class_or_grade,
                                                      class_and_grade[x + 1])
                except Exception:
                    pass

        self.r.error(information)


grades = Grades()
grades.output_info()
