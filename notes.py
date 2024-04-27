#!/usr/bin/env python3

# nautilus 文件备注的脚本

import subprocess
import random,sys,os,re

tmp_file = '/tmp/' + ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 8)) + '.txt'

# 提取属性
proc = subprocess.run(
        f"gio info --attributes=metadata::annotation '{sys.argv[1]}' | sed '{{1,4 d; 5 s/  metadata::annotation: //}}'",
        check=True,
        shell=True,
        stdout=subprocess.PIPE,
    )

attribute = proc.stdout.decode("utf-8")
# 特殊字符处理
attribute = re.sub(r'\\\$', r'\$', attribute)
attribute = re.sub(r'\\-', r'-', attribute)
print(attribute, file=open(tmp_file, 'w'), end='')

# zenity需要设备这个环境变量
os.environ['GTK_PATH'] = ''
proc = subprocess.run(
        f'zenity --text-info --title=备注 --editable --width=500 --height=300 --filename={tmp_file}',
        check=True,
        shell=True,
        stdout=subprocess.PIPE,
    )
os.remove(tmp_file)
newAttribute = proc.stdout.decode("utf-8")
# 特殊字符处理
newAttribute = re.sub(r'(["`\-$])', r'\\\1',newAttribute)

# 设置新的属性
proc = subprocess.run(
        f'gio set -t string "{sys.argv[1]}" metadata::annotation "{newAttribute}"',
        check=True,
        shell=True,
        stdout=subprocess.PIPE,
    )

