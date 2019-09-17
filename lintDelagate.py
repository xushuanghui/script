#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

folder = "/Users/felix/Documents/GitLab/TDFDeprecateItems/TDFDeprecateItems/Classes/"

def scan_files(rootdir):
    filePaths = []
    for root, _, files in os.walk(rootdir):
        filePaths += list(map(lambda fn: os.path.join(root, fn), filter(typeObjC, files)))
    return filePaths


def lintProperty(file: str):
    lines = []
    with open(file, 'r') as f:
        for line in f.readlines():
            matches = re.compile(r'^@property\s+\(.*strong.*\).*id\<.*delegate').findall(line)
            if len(matches) > 0:
                print('FindErrorLine::' + file)
                print(line)
                newline = line.replace(r'strong', r'weak')
                lines.append(newline)
            else:
                lines.append(line)
    with open(file, 'w') as f:
        for line in lines:
            f.write(line)


def typeObjC(file: str):
    if len(file.split('.', 1)) == 1:
        return False
    fileType = file.split('.', 1)[1]
    return fileType == 'm' or fileType == 'h' or fileType == 'mm'


if __name__ == "__main__":
    files = scan_files(folder)
    for f in files:
        lintProperty(f)
    print("Done")
