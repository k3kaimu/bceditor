# -*- coding: utf-8 -*-

import json
import gui
import map
import block


class WidgetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, gui.FlowChartViewer):
            blcks = []
            for x in range(obj.divW):
                submap = []
                for y in range(obj.divH):
                    submap += [self.widgetEncode(obj.GetBlock([x, y]), obj)]
                blcks += [submap]

            return blcks
        else:
            json.JSONEncoder.default(self, obj)

    def widgetEncode(self, blk, map):
        if isinstance(blk, gui.NullBlockWidget):          return ['N']
        elif isinstance(blk, gui.RightBlockWidget):       return ['R']
        elif isinstance(blk, gui.LeftBlockWidget):        return ['L']
        elif isinstance(blk, gui.UpBlockWidget):          return ['U']
        elif isinstance(blk, gui.DownBlockWidget):        return ['D']
        elif isinstance(blk, gui.StartBlockWidget):       return ['S']
        elif isinstance(blk, gui.EndBlockWidget):         return ['E']
        elif isinstance(blk, gui.RightTurnBlockWidget):   return ['RT']
        elif isinstance(blk, gui.LeftTurnBlockWidget):    return ['LT']
        elif isinstance(blk, gui.PythonBlockWidget):      return ['P', blk.filename]
        elif isinstance(blk, gui.ConditionBlockWidget):
            checkedBlock = None
            for x in range(map.divW):
                for y in range(map.divH):
                    if blk.checker != None:
                        if map.GetBlock([x, y]).detecter == blk.checker.detecter:
                            checkedBlock = map.GetBlock([x, y])

            return ['C', self.widgetEncode(blk.incBlock, map)[0], str(map.GetBlockPos(checkedBlock)), str(blk.checker.loopCount)]
        else: assert(0)


def widgetDecoder(map, string):
    arr = eval(string)

    for i in range(map.divW):
        for j in range(map.divH):
            elem = arr[i][j]

            p = map.GetRectPos([i, j])
            s = [map.blockSize, map.blockSize]

            def decodeElem(e):
                if e[0] == 'N':
                    return gui.NullBlockWidget(pos=p, size=s)
                elif e[0] == 'R':
                    return gui.RightBlockWidget(pos=p, size=s)
                elif e[0] == 'L':
                    return gui.LeftBlockWidget(pos=p, size=s)
                elif e[0] == 'U':
                    return gui.UpBlockWidget(pos=p, size=s)
                elif e[0] == 'D':
                    return gui.DownBlockWidget(pos=p, size=s)
                elif e[0] == 'S':
                    return gui.StartBlockWidget(pos=p, size=s)
                elif e[0] == 'E':
                    return gui.EndBlockWidget(pos=p, size=s)
                elif e[0] == 'RT':
                    return gui.RightTurnBlockWidget(pos=p, size=s)
                elif e[0] == 'LT':
                    return gui.LeftTurnBlockWidget(pos=p, size=s)
                elif e[0] == 'P':
                    return gui.PythonBlockWidget(pos=p, size=s, fn=e[1])
                elif e[0] == 'C':
                    incBlock = decodeElem([e[1]])
                    cd = gui.ConditionBlockWidget(pos=p, size=s, incblock=incBlock, block=None)
                    # cd.checker.loopCount = eval(e[3])
                    return cd
                else:
                    assert(0)

            map.SetBlock([i, j], decodeElem(elem))

    for i in range(map.divW):
        for j in range(map.divH):
            if isinstance(map.GetBlock([i, j]), gui.ConditionBlockWidget):
                blk = map.GetBlock(eval(arr[i][j][2]))
                map.GetBlock([i, j]).setBlock(blk, eval(arr[i][j][3]))
                # map.GetBlock([i, j]).checker = blk.detecter.CreateBlockChecker()
                # map.GetBlock([i, j]).loopCount = eval(arr[i][j][3])

    map.redraw()

