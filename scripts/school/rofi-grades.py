#!/usr/bin/env python3

from bs4 import BeautifulSoup
from rofi import Rofi
import requests
import yaml
import sys
import os

HOME = os.path.expanduser('~')

sys.path.insert(0, '{}/ ~/Singularis/local/scripts/school/')

from config import rofi, EDITOR, TERMINAL, NOTES_DIR, ROOT, CURRENT_COURSE

r = Rofi()

classes = [os.path.join(ROOT, o) for o in os.listdir(ROOT)
           if os.path.isdir(os.path.join(ROOT, o))]

names = []
urls = []
grades = []
grade_string = ''

for classs in classes:
    info = open('{}/info.yaml'.format(classs))
    file_info = yaml.load(info, Loader=yaml.FullLoader)

    names.append(file_info['title'])
    urls.append(file_info['url'] + '/grades')

headers = {
    'authority': 'bakercharters.instructure.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="9"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://bakercharters.instructure.com/courses/16507',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.1062468772.1633320575; _gid=GA1.2.2078892401.1633320575; log_session_id=2101b217dcc42858b8ec1fc6533bc169; _legacy_normandy_session=NCXDzDcoUk0hrIdo5PJSZg+Ff8uQ9MngS96e-cfl0JAwl1pUU5hJDTozmv5FZMQ9BRwMDlQr26O0QvEK3SI4Q9cllFUGVDH28Dk6fmC8OpPNNiLnOqFYKn1JIpBRbHQqRVcPBQz9xh35KF5BzAqjLMqfG4sNakugUxm7nJ-gnYG84AMXnSeobAS-WKPSt-tMP1AueXMW-XYOO8N0fDO7Z8OHsT731rsc42iV_iP-JiR8WlCLqhZfEDy9a_fmwNbXORtPcYk09B25IJhptdXTsH5FkWK-eXHEAI83hZO0y1r8aO8WcSMK9yeRCnIydskXSA37cgmaoDDjmdhBjSXCLCrk9mFGm_QyjWa46S8roJL5VZiA0G8IFxnR4ratmSj1wJOfED1QblC4IbFxiDtYMvDsXhH3vBAcDHS-QqRQnsKlhRt9m1q1BgeKgCdZefKeVQ.QwlXzzybnZLXW3DNGzxtaYHy2Ms.YVqFWg; canvas_session=NCXDzDcoUk0hrIdo5PJSZg+Ff8uQ9MngS96e-cfl0JAwl1pUU5hJDTozmv5FZMQ9BRwMDlQr26O0QvEK3SI4Q9cllFUGVDH28Dk6fmC8OpPNNiLnOqFYKn1JIpBRbHQqRVcPBQz9xh35KF5BzAqjLMqfG4sNakugUxm7nJ-gnYG84AMXnSeobAS-WKPSt-tMP1AueXMW-XYOO8N0fDO7Z8OHsT731rsc42iV_iP-JiR8WlCLqhZfEDy9a_fmwNbXORtPcYk09B25IJhptdXTsH5FkWK-eXHEAI83hZO0y1r8aO8WcSMK9yeRCnIydskXSA37cgmaoDDjmdhBjSXCLCrk9mFGm_QyjWa46S8roJL5VZiA0G8IFxnR4ratmSj1wJOfED1QblC4IbFxiDtYMvDsXhH3vBAcDHS-QqRQnsKlhRt9m1q1BgeKgCdZefKeVQ.QwlXzzybnZLXW3DNGzxtaYHy2Ms.YVqFWg; _gat=1; _csrf_token=QtCI%2BA%2BCFgAmr6uXfy20bl%2BPr6xvJuTYC1fM0GlEWxYN4NmhXtdsYR%2FO3OFOaIM7OL7pnlligLdNNpmhEBw6Jw%3D%3D',
}

result = requests.get(urls[3], headers=headers)

src = result.content
soup = BeautifulSoup(src, 'lxml')

divs = soup.find_all('div', {'class': 'student_assignment final_grade'})

for div in divs:
    print(div.text)

print(urls[3])
grades.append(file_info['grade'] + '%')

for i, grade in enumerate(grades):
    grade_string += '''{}: {}
'''.format(names[i], grade)

r.error(grade_string)
