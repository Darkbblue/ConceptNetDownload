'''
测试打包回传功能
'''

import subprocess
from tools import transport

subprocess.run('mkdir m', shell=True)
subprocess.run('touch m/test.file', shell=True)

name = 't1'
transport.rename(name)
#transport.compress(name)
transport.deliver_content(name)
