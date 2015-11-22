# coding: utf-8
#!/usr/bin/env python

import os

path = '/Users/Tamazy/Dropbox/_Docs/TAL/App/summary2rouge/'
path2Rst = '/Users/Tamazy/Dropbox/_Docs/TAL/App/RST-DT/EXT-EDUS-30/'
path2Rouge = '/Users/Tamazy/Dropbox/_Docs/TAL/App/ROUGE-1.5.5/'

syscall = 'python ' + path + 'summary2rouge.py'
syscall += ' ' + path2Rouge
syscall += ' ' + path
syscall += ' -m'
syscall += ' ' + path2Rst + 'file1.shortabs.name1'
syscall += ' -s'
syscall += ' ' + path2Rst + 'file1.shortabs.name2'

#print syscall

os.system(syscall)

