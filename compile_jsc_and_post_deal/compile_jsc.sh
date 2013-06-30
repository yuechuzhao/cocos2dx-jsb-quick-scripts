#!/bin/bash
PROJECT_NAME=testProject
PROJECT_ROOT=${COCOS2DX_ROOT}/projects/${PROJECT_NAME}

if [ -d $PROJECT_ROOT ];
then
    # do make bytes
    python ${COCOS2DX_CONSOLE_ROOT}/cocos2d.py jscompile -d ${PROJECT_ROOT}/Published-iOS -d ${PROJECT_ROOT}/Published-Android -s ${COCOS2DX_ROOT}/scripting/javascript/bindings/js -s ${PROJECT_ROOT}/Resources/js -j ${PROJECT_ROOT}/ScriptOutConf/compiler_config_${PROJECT_NAME}.json -c
    # do copy
    cp -r -f ${PROJECT_ROOT}/Published-iOS/game.min.jsc ${PROJECT_ROOT}/Published-Android

else
    echo "Project not exist"
fi
