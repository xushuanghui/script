#!/usr/bin/python
# -*- coding: utf-8 -*-
# 将#import <A.h>改为#import <A/A.h>

import io
import os
import re
import string

# 获取所有文件名
def get_file_names(path):
    filesPath = [];
    fileNames = [];
    for roots, dirs, files in os.walk(path):
        for name in files:
            if (name.endswith('h') | name.endswith('m')):
                path = os.path.join(roots, name);
                filesPath.append(path);
                fileNames.append(name);

    return filesPath, fileNames;


def getHeaderModule(filePath):
    files,fileNames = get_file_names(filePath);
    # print files;
    module = set();
    for filePath in files:
        a = open(filePath);
        s = a.read();
        strs = str(s);

        mi = re.findall(r'(?<=#import [\s*"])\w*\.h', strs);
        if len(mi) > 0:
            module = module | set(mi);
    return module, fileNames, files;




if __name__ == '__main__':
    root_path = raw_input('输入root路径(多个用空格隔开):');
    root_paths = root_path.split(' ');

    allImportFiles = set();
    allIncludefileNames = [];
    allFilePaths = [];

    for rootPath in root_paths:
        module1,fileNames1, filePaths = getHeaderModule(rootPath);
        allImportFiles = allImportFiles | module1;
        allIncludefileNames = allIncludefileNames + fileNames1;
        allFilePaths = allFilePaths + filePaths;
        pass

    allNoInFile = allImportFiles - set(allIncludefileNames);

    print(allNoInFile);

    resuleFile = {};
    other_path = raw_input('输入引用Pods路径（当前pod中example中的pods文件路径建议先pod update一下）:');
    allOtherFilePath, allOtherFileName = get_file_names(other_path);
    for fileName in allNoInFile:
        for filePath in allOtherFilePath:
            if (fileName in filePath):
                mi = re.findall(r'(?<=/Pods/)\w*', filePath);
                if len(mi) > 0 and str(mi[0]) != 'Headers':
                    resuleFile[fileName] = mi[0]+'/'+fileName
                    break;
            pass
        pass
    print resuleFile;

    for key in resuleFile:
        for filePath in allFilePaths:
            #读写文件  如果用read 再write只会追加
            a = open(filePath);
            # print a.readlines();
            s = a.read();
            # print(s)
            strs = str(s);
            pattern = r'#import\s*"'+key+'"';
            replace_str = '#import <'+resuleFile[key] +'>';
            mi = re.findall(pattern, strs);
            if len(mi) > 0:
                print('正在修改' + filePath + '文件的' + mi[0] + '为' + replace_str);
                newS = re.sub(pattern, replace_str, strs)
                b = open(filePath,'w+');
                b.write(newS);
                b.close();
            a.close();
    print ('修改完成')