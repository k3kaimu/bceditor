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
from kivy.uix.textinput import TextInput

class BlockChecker:

    #BlockDetecterの中身を使って条件を満たしているかを判断
    #満たしていたらCheckでTrueを返す。

    def __init__(self,detecter):
        self.detecter = detecter
        self.loopCount = 0

    #チェックしたい項目を設定
    def SetCheckItem(self, val=None):
        if val == None:
            self.onSetCheckItem()
        else:
            self.loopCount = val

    def onSetCheckItem(self):

        def setText(inst):
            self.loopCount = int(inst.text)

        popup = Popup(title='set loop count',
                    content=TextInput(text="loop count", multiline=False, on_text_validate=setText),
                    size_hint=(None, None), size=(300, 100))
        popup.open()

    def Check(self,map,chara):
        if self.detecter.loopCount == self.loopCount:
            return True
        return False

class BlockDetecter:
    def __init__(self):
        self.loopCount = 0

    #ブロックが実行された時に呼び出される。
    def Detect(self,map,chara):
        self.onDetect(map,chara)

    def onDetect(self,map,chara):
        self.loopCount+=1;

    #自分を判断するチェッカーを作成
    def CreateBlockChecker(self, val=None):
        checker = self.onCreateBlockChecker()
        checker.SetCheckItem(val)
        return checker

    def onCreateBlockChecker(self):
        return BlockChecker(self)

class Block:

    def __init__(self):
        #IF用の検出器
        self.detecter = BlockDetecter()

    @property
    def Detecter(self):
        return self.detecter

    # @Detecter.setter
    # def Detecter(self,detecter):
    #     self.detecter = detecter

    #キャラクタの動作に影響を与える
    def ApplyCharactor(self,map,chara):
        try:
            file = open('log.txt','a',encoding='utf-8')
            sys.stdout = file
            self.onApplyCharactor(map,chara)
            self.detecter.Detect(map,chara)
            sys.stdout = sys.__stdout__
            file.close()
        finally:
            sys.stdout = sys.__stdout__
            file.close()

    def onApplyCharactor(self,map,chara):
        pass

    #キャラクタの更新
    def Update(self,map,chara):
        self.onUpdate(map,chara)

    def onUpdate(self,map,chara):
        pass

class RightBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        print("light_block")
        chara.vec[0] = 1
        chara.vec[1] = 0


class DownBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        chara.vec[0] = 0
        chara.vec[1] = -1

class LeftBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        chara.vec[0] = -1
        chara.vec[1] = 0

class UpBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        print("up_block")
        chara.vec[0] = 0
        chara.vec[1] = 1

class RightTurnBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        copyVec = [None, None]
        copyVec[:] = chara.vec[:]
        chara.vec[0] = copyVec[1]
        chara.vec[1] = -copyVec[0]

class LeftTurnBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        copyVec = [None, None]
        copyVec[:] = chara.vec[:]
        chara.vec[0] = -copyVec[1]
        chara.vec[1] = copyVec[0]

class PythonBlock(Block):

    def __init__(self,fn):
        Block.__init__(self)
        self.filename = fn

    #オーバーライド
    def onApplyCharactor(self,map,chara):

        fileString = None
        try:
            fileString = open(self.filename,'r',encoding='utf-8')
            string = fileString.read()
            string = string.replace('\ufeff', '')
            exec(string)
        finally:
            if fileString != None:
                fileString.close()

        # finally:
        #     fileString.close()

class ConditionBlock(Block):

    def __init__(self,incblock,block,val=None):
        Block.__init__(self)
        if block != None:
            self.checker = block.Detecter.CreateBlockChecker(val)
        else:
            self.checker = None
        self.incBlock = incblock

    def setBlock(self,block,val=None):
        self.checker = block.Detecter.CreateBlockChecker(val)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        self.incBlock.ApplyCharactor(map,chara)

    #オーバーライド
    def onUpdate(self,map,chara):
        self.incBlock.Update(map,chara)
        if self.checker != None:
            if self.checker.Check(map,chara):
                print("delete")
                map.DeleteBlock(self)

class StartBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        chara.vec[0] = 0
        chara.vec[1] = -1

class EndBlock(Block):

    def __init__(self):
        Block.__init__(self)

    #オーバーライド
    def onApplyCharactor(self,map,chara):
        #終了処理を書く
        print("終了")
        pass
