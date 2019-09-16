#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re 
import glob

filePath = '/Users/shuanghui/Desktop/script/un_used_imagepath.txt'

def removeLinewith_en_th(file:str):
    lines = []
    unused_paths = []
    with open(file,'r') as f:
        for line in f.readlines():
            matches = re.compile(r'.*(_en|_th).*').findall(line)
            if len(matches) > 0:
                print('findLine_th_en==>'+line)
            else:
                lines.append(line)

    with open(file, 'w') as f:
        for line in lines:
            f.write(line)

    with open(file, 'r') as f:
        for line in f.readlines():
            matches = re.compile(r'.*\.imageset').findall(line)
            if len(matches) > 0:
                #  print ('remove==>'+line)
                os.system('rm -rf %s' % line)



if __name__ == "__main__":
    removeLinewith_en_th(filePath)
    print("Done")