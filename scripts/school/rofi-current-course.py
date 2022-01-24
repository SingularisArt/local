#!/usr/bin/env python3

import os
import sys
import yaml

HOME = os.path.expanduser('~')

sys.path.insert(0, '{}/ ~/Singularis/local/scripts/school/')

from config import rofi, ROOT, CURRENT_COURSE

classes = [os.path.join(ROOT, o) for o in os.listdir(ROOT)
           if os.path.isdir(os.path.join(ROOT, o))]
titles = []


for current_class in classes:
    try:
        info = open('{}/info.yaml'.format(current_class))
        file_info = yaml.load(info, Loader=yaml.FullLoader)

        titles.append("<b><span color='blue'>{: <{}}</span></b> <span color='grey'>(</span><i><span color='yellow'>{}</span></i><span color='grey'>)</span>".format(
            file_info['title'],
            25,
            file_info['short']
        ))
    except Exception:
        pass

titles = sorted(titles)
classes = sorted(classes)

key, index, selected = rofi('Select class', titles, [
    '-lines', 5,
    '-markup-rows',
    '-kb-row-down', 'Down',
    '-kb-custom-1', 'Ctrl+n'
])

current_class = os.path.realpath(CURRENT_COURSE)
current_class = os.path.basename(os.path.normpath(current_class))
current_class = current_class.replace('-', ' ')
current_class = current_class.replace('hs', 'Honors')
current_class = current_class.title()

new_class = os.path.basename(os.path.normpath(classes[index]))
new_class = new_class.replace('-', ' ')
new_class = new_class.replace('hs', 'Honors')
new_class = new_class.title()

os.system('''notify-send "Change Class" """<span color=\'blue\'>{}</span> ➡️ <span color=\'blue\'>{}</span>
"""'''.format(current_class, new_class))

if os.path.isdir(CURRENT_COURSE):
    os.remove(CURRENT_COURSE)
os.symlink(classes[index], CURRENT_COURSE)
