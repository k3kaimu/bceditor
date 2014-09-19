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
from charactor import *

class Map:

    @property
    def CharaMap(self):
        return self.charaMap

    @CharaMap.setter
    def CharaMap(self,charamap):
        self.charaMap = charamap

    def __init__(self):
        self.CharaMap = [[None for j in range(5)] for i in range(5)]
        for i,iv in enumerate(self.charaMap):
            for j,jv in enumerate(self.charaMap[i]):
                self.SetBlock([i,j],None)

    #キャラクタにマップ上のブロックを適応
    def ApplyMapCharactor(self,chara):
        x = chara.pos[0]
        y = chara.pos[1]
        if self.charaMap[x][y] != None:
            self.charaMap[x][y].ApplyCharactor(self,chara)

    #ブロックをマップにセット
    def SetBlock(self,pos,block):
        x = pos[0]
        y = pos[1]

        pos = [None, None]
        #スタートブロックがすでにあれば消す
        if isinstance(block,StartBlock):
            if self.IsSetStartBlock(pos):
                self.SetBlock(pos, None)
        self.charaMap[x][y] = block

    #ブロックの取得
    def GetBlock(self,pos):
        return self.charaMap[pos[0]][pos[1]]

    # ブロック位置の取得
    def GetBlockPos(self, block):
        for i,iv in enumerate(self.charaMap):
            for j,jv in enumerate(self.charaMap[i]):
                if jv == block:
                    return [i, j]
        return [-1, -1]

    #スタートブロックがセットされているかを確認
    def IsSetStartBlock(self,pos):
        for i,iv in enumerate(self.charaMap):
            for j,jv in enumerate(self.charaMap[i]):
                if isinstance(jv,StartBlock):
                    pos[:] = [i,j]
                    return True
        return False

    #キャラクタの初期位置を取得
    def SetCharactorInitPosition(self,chara):
        pos = [0,0]
        if self.IsSetStartBlock(pos):
            chara.cpos = pos
            self.ApplyMapCharactor(chara)
            return True
        else:
            return False

    #マップの更新
    def Update(self,chara):
        for iv in self.charaMap:
            for jv in iv:
                if isinstance( jv , Block):
                    jv.Update(self,chara)

    #マップの要素を消す
    def DeleteBlock(self,block):
        for i,iv in enumerate(self.charaMap):
            for j,jv in enumerate(self.charaMap[i]):
                if jv == block:
                    self.SetBlock([i, j], None)

                    #アニメーションなどの要望はここから

