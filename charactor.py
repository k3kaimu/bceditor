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

import sys

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

class Charactor:

    #charactorの位置
    '''
        self.pos;
        self.vec;
    '''

    def __init__(self):
        self.cpos = [-1,-1]
        self.vec = [-1,-1]

    #GUIの実行が押された時に呼ばれる。
    def step(self,stepCount,map):
        #標準入力の委託
        for i in range(stepCount):
            self.Move(map)
            map.ApplyMapCharactor(self)
            map.Update(self)

    #キャラクタの移動を行う
    def Move(self,map):
        self.cpos[0] += self.vec[0]
        self.cpos[1] += self.vec[1]

    def Print(self):
        print("座標：",self.cpos,"速度",self.vec)