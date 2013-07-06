#! /bin/bash
echo "Start compile and post deal"
python ${PWD}/compile_jsc.py -c $1
echo "-----------------"
echo "compile completed!"
echo "-----------------"
python ${PWD}/post_deal.py -d $1
echo "-----------------"
echo "post deal completed!"
echo "-----------------"

