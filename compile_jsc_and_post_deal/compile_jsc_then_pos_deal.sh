#! /bin/bash
echo "Start compile and post deal"
script_path=`dirname "$0"`
python ${script_path}/compile_jsc.py -c $1
echo "-----------------"
echo "compile completed!"
echo "-----------------"
python ${script_path}/post_deal.py -d $1
echo "-----------------"
echo "post deal completed!"
echo "-----------------"

