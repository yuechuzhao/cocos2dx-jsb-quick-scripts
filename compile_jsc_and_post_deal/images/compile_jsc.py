#! /usr/bin/python2.7
# -*- coding: utf-8 -*-
'''
用来自动编译
'''
#!/bin/bash
# 以下是shell脚本，复制下来也可以一样用
#PROJECT_NAME=xxx
#PROJECT_ROOT=${COCOS2DX_ROOT}/projects/${PROJECT_NAME}

#if [ -d $PROJECT_ROOT ];
#then
    ## do make bytes
    #python ${COCOS2DX_CONSOLE_ROOT}/cocos2d.py jscompile -d ${PROJECT_ROOT}/Published-iOS -s ${COCOS2DX_ROOT}/scripting/javascript/bindings/js -s ${PROJECT_ROOT}/Resources/js -j ${PROJECT_ROOT}/ScriptOutConf/compiler_config_${PROJECT_NAME}.json -c

    ## do copy
    #cp -r -f ${PROJECT_ROOT}/Published-iOS/game.min.jsc ${PROJECT_ROOT}/Published-Android
#else
    #echo "Project not exist"
#fi



import sys, os
def do_cocos2d_jsc_compile(project_name):
    cocos2dx_root = os.environ.get("COCOS2DX_ROOT")
    project_root = "/".join([cocos2dx_root, "projects", project_name])
    if not os.path.exists(cocos2dx_root):
        print "cocos2d root not exist"
    #判断是否存在这个root
    elif not os.path.exists(project_root):
        print "Project not exists"
    else:
        cocos2dx_console_root = "%s/tools/cocos2d-console/console" % cocos2dx_root
        if not cocos2dx_console_root or not os.path.exists(cocos2dx_console_root):
            print "cocos2dx_console_root not exists"
        else:
            # 直接运行命令。不用python调用，那样会需要去看源代码
            js_binding_path = "%s/scripting/javascript/bindings/js" % cocos2dx_root
            src_path = "%s/Resources/js" % project_root
            dst_path_ios = "%s/Published-iOS" % project_root
            dst_path_android = "%s/Published-Android" % project_root
            config_file = "%s/ScriptOutConf/compiler_config_%s.json" % (project_root, project_name)
            
            # 检查是否存在
            args_names = ["js_binding_path", "src_path", "dst_path_ios", "dst_path_android", "config_file"]
            args = [js_binding_path, src_path, dst_path_ios, dst_path_android, config_file]
            i = 0
            for args_name in args_names:
                if not os.path.exists(args[i]) and not os.path.isfile(args[i]):
                    print "%s not exists: %s" % (args_name, args[i])
                    return 0
                i += 1

            # 命令
            custom_command = "python %s/cocos2d.py jscompile -d %s -s %s -s %s -j %s -c" % (cocos2dx_console_root,
                    dst_path_ios, js_binding_path, src_path, config_file)
            import subprocess
            subprocess.call(custom_command, shell=True)

            import shutil
            # 再复制到andorid文件夹
            android_jsc = "%s/game.min.jsc" % dst_path_android
            ios_jsc = "%s/game.min.jsc" % dst_path_ios
            shutil.copyfile(ios_jsc, android_jsc)
            print "copy jsc to ios && android succeed"


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] != "-c":
        print '''
        This is a command line tool for use cocos2d-console to compile
        -usage:
        --help: -h
        --compile: python compile_jsc.py -c -project_name
        You should set dirs like this:
        
        +cocos2dx_root
        -+project_root
        --+published-iOS
        --+published-Android
        --+Resources
        ---+js --Your js files should be here
        --+ScriptOutConf
        ---+compiler_config_${projectName}.json -- You compile json file should be here
        
        '''
    elif sys.argv[1] == "-c" and len(sys.argv) == 3: 
        project_name = sys.argv[2]
        do_cocos2d_jsc_compile(project_name)
