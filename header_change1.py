#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
import re
import string
import subprocess
import shutil
from git import Repo

GIT_REPO_GROUPS = {'AssemblyComponent': '2dfire-ios', 'ActivityForRestApp': '2dfire-ios', 'UnitSettingForRestApp': '2ye-iOS'}

CHECK_PODS = ['TDFMemberTag']
# 'TDFDeprecateItems', 'TDFBaseUI','TDFMemberTag','TDFWechatMarketingModule','TDFMGameCenter','TDFMemberManagement','TDFMemberPod', 'TDFJsonConfig','TDFMemberSystem', 'TDFMUniversalModule', 'TDFMActivityModule', 'AssemblyComponent', 'TDFMemberJsonConfigComponents','TDFMCouponModule', 'TDFMemDecoupleModule', 'TDFTinyApp', 'TDFTemplateParser', 'ActivityForRestApp'
NO_NEED_CHECK_POD = []

def err_message(message):
    err_message = '\033[0;31m' + message + '\033[0m'
    return err_message

def warn_message(message): 
    war_message = '\033[1;33m' + message + '\033[0m'
    return war_message

def noti_message(message): 
    noti_message = '\033[0;33m' + message + '\033[0m'
    return noti_message

def suc_message(message):
    suc_message = '\033[1;32m' + message + '\033[0m'
    return suc_message

# clone git repo

def exe_command(commands):
    p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            print output.strip()
    pass

def clone_repo(group,module):
    print module
    p = subprocess.Popen(['git', 'clone', '-b', 'develop' ,'--progress', 'git@git.2dfire.net:' + group + '/' + module + '.git'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() is not None:
            break
        if output:
            print output.strip()
    pass

def clone_repos(modules):
    for module in modules:
        if module in GIT_REPO_GROUPS.keys():
            clone_repo(GIT_REPO_GROUPS[module],module)
            pass
        else:
            clone_repo('ios',module)
            pass
        
        pass
    pass

# 获取所有文件名
def get_file_names(path, ignort_paths=['Pods', 'Base.lproj', 'Images.xcassets', 'en.lproj', 'Tests']):
    filesPath = [];
    fileNames = [];
    for roots, dirs, files in os.walk(path):
        if os.path.basename(roots) in ignort_paths:
            filesPath.append(roots);
            dirs[:] = [] # 忽略当前目录下的子目录
            continue;
        for name in files:
            path = os.path.join(roots, name);
            filesPath.append(path);
            fileNames.append(name);
    return filesPath, fileNames;

# 切换分支
def check_branch(git, pod_branch):
    does_exist = True
    try:
        git.checkout(pod_branch)
    except BaseException:
        does_exist = False
        pass
    else:
        pass

    
    if not does_exist :
        print (noti_message('%s分支不存在将从develop分支创建'%pod_branch))
        current_dev_commit = ''
        try:
            current_dev_commit = git.rev_parse('--verify', 'develop')
            print (noti_message('%s切换成功'%pod_branch))
            pass
        except BaseException as error:
            print(error)
            return False
        
        try:
            git.checkout(current_dev_commit,b=pod_branch)
            pass
        except BaseException as error:
            print(error)
            return False
        else:
            return True
        pass
    else:
        return True
    pass




# 找到podfile 文件路径执行pod update
def find_podfile_path(filesPath) :
    podfile_path = ''
    for path in filesPath:
        filepath, tmpfilename = os.path.split(path)
        if tmpfilename == 'Podfile':
            podfile_path = path;
            break;
        pass
    return podfile_path;

# 获取当前仓库分支名
def current_branch(path):
    try:
        repo = Repo(path)
        print(repo.active_branch)
    except BaseException as error:
        print (str(type(error)) + str(error))
        pass
    else:
        return repo.active_branch.name
    pass


def push(git): 
    remote_config = git.remote()
    if len(remote_config) > 0:
        try:
            print(git.pull())
        except BaseException as error_message:
            branchName = current_branch('./');
            # git.push('-u',branchName,'origin/'+branchName);
            exe_command(['git','push', '-u','origin',branchName]);
        
            print (error_message)
            pass
        else:
            print(git.push())
            pass
        pass
    else:
        
        print('该仓库没有对应远程仓库！')
        pass
    pass


def commit(git):
    git.add('.')
    while(1):
        commit_message = '头文件修改【自动提交信息】'
        if len(str(commit_message)) > 0: 
            print(git.commit('-m', str(commit_message)))
            break
        pass
    pass

def getHeaderModule(filesPath):
    module = set();
    allFilesPaht = [];
    for filePath in filesPath:
        if (filePath.endswith('h') | filePath.endswith('m')):
            allFilesPaht.append(filePath);
            a = open(filePath);
            s = a.read();
            strs = str(s);

            mi = re.findall(r'(?<=#import [\s*"])[\w+]*\.h', strs);
            if len(mi) > 0:
                module = module | set(mi);
            pass
    return module,allFilesPaht;


def change_umbrella(all_file_path):
    for path in all_file_path:
        a = open(path);
        s = a.read();
        strs = str(s);
        newS = strs;
        mi = re.findall(r'(?<=#import [\s*<])[\w+]*/[\w+]*(?=\.h)', strs);
        if len(mi) > 0:
            for fileName in mi:
                tem = fileName.split('/');
                # if tem[0] in PODS:
                if tem[0] != tem[1]:
                    print "======" + path + "======"
                    tem_be_replace_str = fileName;
                    tem_replace_str = tem[0]+'/'+tem[0]
                    newS = newS.replace('#import <'+tem_be_replace_str + '.h>', '#import <'+tem_replace_str + '.h>');
                    count = newS.count('#import <'+tem_replace_str + '.h>');
                    print count
                    if count > 1:
                        newS = newS.replace('#import <'+tem_replace_str + '.h>', '', count - 1)
                        pass
                    
                    print "======修改%s 为 %s======"%(tem_be_replace_str, tem_replace_str);


                    print "======end======"
                    pass
                    # pass
                pass
            pass
            b = open(path,'w+');
            b.write(newS);
            b.close();
        pass
        a.close();

def change_header(root_paths, other_path, allIncludefileNames):

    print ('将所有引号引用改为尖括号引用！')

    # 当前库所有import 的文件
    allImportFiles = set();
    # 当前库所有的文件
    allFilePaths = [];

    module1,filePaths = getHeaderModule(root_paths);

    allFilePaths += filePaths;

    allImportFiles = allImportFiles | module1;
    # 当前库所有引用的非当前库文件
    allNoInFile = allImportFiles - set(allIncludefileNames);

    print(allNoInFile);

    resuleFile = {};
    # pods 文件夹的所有文件
    allOtherFilePath, allOtherFileName = get_file_names(other_path, ignort_paths=[]);

    for fileName in allNoInFile:
        for filePath_ in allOtherFilePath:
            if (fileName == os.path.split(filePath_)[1]):
                mi = re.findall(r'(?<=/Pods/)[\w\+]*', filePath_);
                if len(mi) > 0 and str(mi[0]) != 'Headers':
                    resuleFile[fileName] = mi[0]+'/'+fileName
                    break;
            pass
        pass
    print resuleFile;

    for key in resuleFile:
        for tem_filepath in allFilePaths:
            #读写文件  如果用read 再write只会追加
            a = open(tem_filepath);
            # print a.readlines();
            s = a.read();
            # print(s)
            strs = str(s);
            pattern = r'#import\s*"'+key+'"';
            
            if '+' in key :
                listKey = key.split('+');
                pattern = r'#import\s*"%s\+%s"' % (listKey[0],listKey[1]);
                
            replace_str = '#import <'+resuleFile[key] +'>';
            mi = re.findall(pattern, strs);
            if len(mi) > 0:
                print('正在修改' + tem_filepath + '文件的' + mi[0] + '为' + replace_str);
                newS = re.sub(pattern, replace_str, strs)
                b = open(tem_filepath,'w+');
                b.write(newS);
                b.close();
            a.close();
    print ('修改完成')
    # change_umbrella(allFilePaths)



if __name__ == "__main__":
    if (os.path.exists('./ios_check')):
        shutil.rmtree('./ios_check')
        pass
    os.mkdir('ios_check')
    os.chdir('./ios_check')
    CURRENT_PATH = os.getcwd();

    clone_repos(CHECK_PODS);
    
    for moduleName in CHECK_PODS:
        path = CURRENT_PATH + '/' + moduleName;
        if os.path.exists(path):
            repo = Repo(path)
            # 切换分支
            check_branch(repo.git, 'feature/change_header')
            os.chdir(path)
            filesPath, fileNames = get_file_names('./');
            # 获取podfile 路径
            pod_file_path = find_podfile_path(filesPath);
            os.chdir(os.path.dirname(pod_file_path));
            # 执行pod update
            exe_command(['pod', 'update'])
            pods_path = os.getcwd();
            os.chdir(path)
            # 更改头文件
            change_header(filesPath, pods_path + '/Pods', fileNames);
            if len(repo.untracked_files) > 0 or repo.is_dirty():
                commit(repo.git)
                push(repo.git)
            
            pass
        pass
