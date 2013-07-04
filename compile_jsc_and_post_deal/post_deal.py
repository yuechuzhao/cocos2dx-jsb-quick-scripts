#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
'''
删除不需要的js和js文件夹，复制特殊的资源（比如在spritesheet，在ios和android下使用pvr.ccz而在h5版本里面使用png）
'''
import json
import os
import shutil
import re

def str_match_reglist(name, reglist):
    """str match one regex of list or not
    """
    for reg in reglist:
        m = re.compile(reg)
        if m.match(name): return True
    return False

def del_file_by_reg_and_name_list(root, reglist, current_name_list):
    for path, dirnames, filenames in os.walk(root):
        # 删除符合要求的文件
        for filename in filenames:
            #print filename
            #print str_match_reglist(filename, reglist)
            if str_match_reglist(filename, reglist) or filename in current_name_list:
                os.remove(os.path.join(path, filename))

def deal_after_compile_jsc(project_name):
    cocos2dx_root = os.environ.get("COCOS2DX_ROOT")
    config_file = "%s/projects/%s/ScriptOutConf/post_deal_config.json" % (cocos2dx_root, project_name)
    json_conf = open(config_file, "r")
    deal_list = json.load(json_conf)
    project_root = "/".join([os.environ.get("COCOS2DX_ROOT"), "projects", project_name])
    if not os.path.exists(cocos2dx_root):
        print "cocos2d root not exist"
    #判断是否存在这个root
    elif not os.path.exists(project_root):
        print "Project not exists"
    else:
        proj_ios_root = "/".join([project_root, "Published-iOS"])
        proj_android_root = "/".join([project_root, "Published-Android"])
        # 先删除文件夹
        # TODO 错误处理
        for path in deal_list["del_dirs"]:
            del_dir = proj_ios_root + "/" + path
            if os.path.exists(del_dir): shutil.rmtree(del_dir)
            del_dir = proj_android_root + "/" + path
            if os.path.exists(del_dir): shutil.rmtree(del_dir)
        print "deleted required share files!"
        
        platforms = ["ios", "android"]
        for i in xrange(len(platforms)):
            platform = platforms[i]
            proj_platform_root = [proj_ios_root, proj_android_root][i]
            # 删除符合要求的文件
            del_file_by_reg_and_name_list(proj_platform_root, deal_list["del_files_by_re"], deal_list["del_files_%s" % platform])
            print "deleted required %s files!" % platform
        
            # 再复制
            print "Copy required resource files:"
            src_dir = os.path.join(project_root, deal_list["copy_files_dir_%s" % platform])
            print "Src: %s" % src_dir
            for path, dirnames, filenames in os.walk(src_dir):
                for dir_name in dirnames:
                    dst_dir = os.path.join(proj_platform_root, dir_name)
                    print "dst dir: %s" % dst_dir
                    if os.path.exists(dst_dir): os.rmdir(dst_dir)
                    shutil.copy(os.path.join(path, dir_name), proj_platform_root)
                for filename in filenames:
                    dst_file = os.path.join(proj_platform_root, filename)
                    print "dst file %s" % dst_file
                    if os.path.isfile(dst_file): os.remove(dst_file)
                    shutil.copy(os.path.join(path, filename), proj_platform_root)

            print "%s copy completed!" % platform


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1 or sys.argv[1] != "-d":
        print '''
        This is a command line tool for cocos2d-x javascript project post deals. It delete these things you don't need and copy these files you need add.
        -usage:
        --help: -h
        --deal: python post_deal.py -d -project_name
        You should set dirs like this:
        cocos2dx_root
        |project_root
        ||published-iOS
        ||published-Android
        ||need_to_cpy_dir ---this name you can define by your self
        ||ScriptOutConf
        ScriptOutConf/compiler_config_projectName.json -- You compile json file should be here
        '''
    elif sys.argv[1] == "-d" and len(sys.argv) == 3: 
        project_name = sys.argv[2]
        #deal_after_compile_jsc(project_name)
        deal_after_compile_jsc(project_name)
