#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ultra-tkymx
#
# Created:     17/09/2014
# Copyright:   (c) ultra-tkymx 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from block import *
from map import *
from charactor import *

def main():
    map = Map()
    map.SetBlock([0,4],StartBlock())
    map.SetBlock([0,3],PythonBlock('C:\\Users\\ultra-tkymx\\Documents\\WakoPy\\extra\\extra.py'))
    map.SetBlock([0,3],PythonBlock('C:\\Users\\ultra-tkymx\\Documents\\WakoPy\\extra\\extra2.py'))
    map.SetBlock([0,2],RightBlock())
    map.SetBlock([1,2],UpBlock())
    map.SetBlock([1,2],ConditionBlock(map.GetBlock([1,2]),map.GetBlock([0,2])))
    chara = Charactor()
    map.SetCharactorInitPosition(chara)
    chara.Print()
    for i in range(5):
        chara.step(1,map)
        chara.Print()

if __name__ == '__main__':
    main()
