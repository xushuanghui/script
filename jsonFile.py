#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os 
import sys
import commands
import subprocess
import json
import shutil
import time

print "------- start ----------"
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

CURRENT_PATH = sys.path[0]
PROJECT_DIR = os.environ['PWD']
if len(sys.argv) >= 2 :
    PROJECT_DIR = sys.argv[1]

print 'ProjectDir------>%s'%PROJECT_DIR
os.chdir(CURRENT_PATH)
ROOT_DIR = os.path.dirname(PROJECT_DIR)
print 'RootDir------>%s'%ROOT_DIR
SETTING_MODEL_PATH = ROOT_DIR + '/settings_model'
print 'settingModelPath------>%s'%SETTING_MODEL_PATH
def getNewCommitId(originPath ,destinationPath):
    if (os.path.exists(destinationPath)):
        os.chdir(destinationPath)
        a = commands.getoutput('git rev-parse HEAD')
        os.chdir(originPath)
        return a
    pass

def getFileMap(path):
    dic = {}
    for root, dirs, files in os.walk(path):
        for file in files :
            if file.endswith('.js') or file.endswith('.json') :
                dic[file] = root + '/' + file
                pass
            pass
        pass
    
    return dic

def moveSettingModelFileToWorkSpace() :    
    if (not os.path.exists(SETTING_MODEL_PATH)) :
        p = subprocess.Popen(['git', 'clone', '--progress', 'git@git.2dfire-inc.com:background_manage_new/settings_model.git', SETTING_MODEL_PATH,], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = p.stdout.readline()
            if output == '' and p.poll() is not None:
                break
            if output:
                print output.strip()
        pass
    print ('读取config...')
    fileOpen = open(CURRENT_PATH + '/config', 'r')
    
    content = fileOpen.read()
    fileOpen.close()

    contentDic = json.loads(content,encoding="utf-8")

    # storCommitId = contentDic['commitId']

    # newCommitId = getNewCommitId(currentPath, settingModelPath)

    files = getFileMap(SETTING_MODEL_PATH)

    value = contentDic['fileMap']
    print ('移动文件...')
    error = 0
    for resourcePath, destinatioFiles in value.items() :
        for file in destinatioFiles :
            if file in files :
                path = files[file]
                try:
                    print "copy " + path 
                    print " to "
                    print  ROOT_DIR + resourcePath
                    print "\n"
                    shutil.copy(path, ROOT_DIR + resourcePath)
                except IOError as e:
                    error += 1
                    print str(e) + 'when copy ' + path
            pass
        pass

    print "------- error:%d----------"%error
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print "------- done ----------"
    print '\n\n\n'
    pass


if __name__ == '__main__' :
    moveSettingModelFileToWorkSpace()

    pass