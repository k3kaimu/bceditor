# -*- coding: utf-8 -*-

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, ReferenceListProperty
from kivy.graphics import RenderContext, Color, Ellipse, Line, Rectangle
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.uix.listview import ListView, ListItemButton, CompositeListItem, ListItemLabel
from kivy.adapters.listadapter import ListAdapter
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from block import *
from charactor import *
from kivy.graphics.instructions import InstructionGroup
from kivy.animation import Animation
from map import *
import random
import json
import jsonenc
from os.path import dirname, abspath, join

from wakopy import Block, Map, Charactor;

import sys

class RectWidget(Widget):

    def __init__(self, **kwargs):
        self.instlist = []
        Widget.__init__(self, **kwargs)

    def add(self, inst):
        self.instlist += [inst]
        self.canvas.add(inst)

    def on_size(self, *arg):
        for e in self.instlist:
            try:
                e.size = self.size
            except: pass

    def on_pos(self, *arg):
        for e in self.instlist:
            try:
                e.pos = self.pos
            except: pass

    def removeFromCanvas(self):
        for e in self.instlist:
            self.canvas.remove(e)


class NullBlockWidget(Block, RectWidget):
    source = "img/null.png"

    def __init__(self, **kwargs):
        Block.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Rectangle(**kwargs))


class RightBlockWidget(RightBlock, RectWidget):
    source = "img/right.png"

    def __init__(self, **kwargs):
        RightBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = RightBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class LeftBlockWidget(LeftBlock, RectWidget):
    source = "img/left.png"

    def __init__(self, **kwargs):
        LeftBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = LeftBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class UpBlockWidget(UpBlock, RectWidget):
    source = "img/up.png"

    def __init__(self, **kwargs):
        UpBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = UpBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class DownBlockWidget(DownBlock, RectWidget):
    source = "img/down.png"

    def __init__(self, **kwargs):
        DownBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = DownBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class StartBlockWidget(StartBlock, RectWidget):
    source = "img/start.png"

    def __init__(self, **kwargs):
        StartBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = StartBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))

    # def ApplayCharactor(self, map, chara):
    #     StartBlock.ApplayCharactor(self, map, chara)


class EndBlockWidget(EndBlock, RectWidget):
    source = "img/end.png"

    def __init__(self, **kwargs):
        EndBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = EndBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class RightTurnBlockWidget(RightTurnBlock, RectWidget):
    source = "img/turnright.png"

    def __init__(self, **kwargs):
        RightTurnBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = RightTurnBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class LeftTurnBlockWidget(LeftTurnBlock, RectWidget):
    source = "img/turnleft.png"

    def __init__(self, **kwargs):
        LeftTurnBlock.__init__(self)
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = LeftTurnBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class PythonBlockWidget(PythonBlock, RectWidget):
    source = "img/python.png"

    def __init__(self, **kwargs):
        PythonBlock.__init__(self, kwargs['fn'])
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = PythonBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


class ConditionBlockWidget(ConditionBlock, RectWidget):
    source = "img/if.png"

    def __init__(self, **kwargs):
        ConditionBlock.__init__(self, kwargs['incblock'], kwargs['block'])
        RectWidget.__init__(self, **kwargs)
        RectWidget.add(self, Color(1, 1, 1, 1))
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = kwargs['incblock'].source
        RectWidget.add(self, Rectangle(**kwargs))
        kwargs['source'] = ConditionBlockWidget.source
        RectWidget.add(self, Rectangle(**kwargs))


    def ApplyCharactor(self, map, chara):
        super().ApplyCharactor(map, chara)


class CharactorWidget(Charactor, RectWidget):
    source = "img/d3.png"

    def __init__(self, **kwargs):
        Charactor.__init__(self)
        RectWidget.__init__(self, **kwargs)
        kwargs['source'] = CharactorWidget.source
        RectWidget.add(self, Rectangle(**kwargs))
        self.mapInstance = kwargs['mapInstance']

    def Move(self,map):
        Charactor.Move(self,map)
        self.pos = self.mapInstance.GetRectPos(self.cpos)

class FlowChartViewer(Map, Widget):
    yBias = NumericProperty(0)
    outlabel = ObjectProperty(None)

    #ブロックの設定のモード
    BLOCK_SET_MODE      = 1
    BLOCK_SELECT_MODE   = 2
    block_state = BLOCK_SET_MODE
    block_on_push = None

    def __init__(self, **kwargs):
        self.builded = False
        self.divW = 5
        self.divH = 5
        self.vertLines = []
        self.horiLines = []
        self.charaWidget = None
        wh = int(min(self.width // self.divW, (self.height - self.yBias) // self.divH))
        self.blockSize = wh
        self.xMergin = (self.width - wh * self.divW) // 2
        self.yMergin = ((self.height - self.yBias) - wh * self.divH) // 2

        Widget.__init__(self, **kwargs)
        Map.__init__(self)

        with self.canvas:
            for x in range(self.divW):
                for y in range(self.divH):
                    self.SetBlock([x, y], NullBlockWidget(pos=self.GetRectPos([x, y]),
                                                          size=[wh, wh]))

            for i in range(self.divH+1):
                Color(0.3, 0.3, 0.3)
                self.vertLines += [Line(points=self.GetRectPos([0, i]) + self.GetRectPos([self.divW, i]),
                                        width=2)]

            for i in range(self.divW+1):
                Color(0.3, 0.3, 0.3)
                self.horiLines += [Line(points=self.GetRectPos([i, 0]) + self.GetRectPos([i, self.divH]),
                                        width=2)]
        self.builded = True

    def GetRectPos(self, pos):
        x = pos[0]
        y = pos[1]
        wh = self.blockSize
        return [self.xMergin + wh * x, self.yMergin + wh * y + self.yBias]


    def on_size(self, *args):
        wh = int(min(self.width // self.divW, (self.height - self.yBias) // self.divH))
        self.blockSize = wh
        self.xMergin = (self.width - self.divW * wh) // 2
        self.yMergin = ((self.height - self.yBias) - self.divH * wh) // 2

        for x in range(self.divW):
            for y in range(self.divH):
                t = self.GetBlock([x, y])
                t.pos = self.GetRectPos([x, y])
                t.size = [wh, wh]

        for i in range(self.divH+1):
            self.vertLines[i].points = self.GetRectPos([0, i]) + self.GetRectPos([self.divW, i])

        for i in range(self.divW+1):
            self.horiLines[i].points = self.GetRectPos([i, 0]) + self.GetRectPos([i, self.divH])


    def on_touch_up(self, touch):
        if BlockListView.selectedBlockGenerator == None: return True;

        xx = int(touch.x - self.xMergin) // self.blockSize
        yy = int(touch.y - self.yMergin - self.yBias) // self.blockSize

        if xx < 0 or yy < 0 or xx >= self.divW or yy >= self.divH:
            return False

        if FlowChartViewer.block_state == FlowChartViewer.BLOCK_SET_MODE:
            before = self.GetBlock([xx, yy])
            after = BlockListView.selectedBlockGenerator(before)
            # print(self.CharaMap)
            # print(after.source)
            after.pos = before.pos
            after.size = before.size
            self.SetBlock([xx, yy], after)

        elif FlowChartViewer.block_state == FlowChartViewer.BLOCK_SELECT_MODE:
            before = self.GetBlock([xx, yy])
            if not isinstance( before , NullBlockWidget ):
                #選択しているブロックにする
                if self.block_on_push != None:
                    FlowChartViewer.block_on_push(before)

        self.redraw()

        return True;


    def redraw(self):
        self.canvas.clear()

        for i in range(self.divW):
            for j in range(self.divH):
                if isinstance(self.GetBlock([i, j]), RectWidget):
                    for e in self.GetBlock([i, j]).instlist:
                        self.canvas.add(e)

        for i in range(self.divH+1):
            self.canvas.add(Color(0.3, 0.3, 0.3))
            self.canvas.add(self.vertLines[i])

        for i in range(self.divW+1):
            self.canvas.add(Color(0.3, 0.3, 0.3))
            self.canvas.add(self.horiLines[i])

        if self.charaWidget != None:
            # print("redraw", self.charaWidget.rect.pos)
            for e in self.charaWidget.instlist:
                self.canvas.add(e)

        try:
            file = open("log.txt","r",encoding="utf-8")
            self.outlabel.text = ""
            for line in file.readlines():
                line = line.replace('\ufeff', '')
                self.outlabel.text += line
        finally:
            pass

        self.canvas.ask_update()

    def IsInRange(self):
        #範囲外の処理を書く
        if self.charaWidget != None:
            for i in range(2):
                if self.charaWidget.cpos[i] < 0 or self.charaWidget.cpos[i] > 4:
                    return False
        return True

    def DeleteBlock(self, block):
        Map.DeleteBlock(self, block)

        if self.builded:
            self.redraw()

    def SetBlock(self, pos_, block):
        if block == None:
            block = NullBlockWidget(pos=self.GetRectPos(pos_),
                                    size=[self.blockSize, self.blockSize])
        Map.SetBlock(self, pos_, block)

        if self.builded:
            # print("OK")
            self.redraw()


    def ApplyMapCharactor(self, chara):
        x = chara.cpos[0]
        y = chara.cpos[1]
        if not isinstance(self.GetBlock([x, y]), NullBlockWidget):
            self.GetBlock([x, y]).ApplyCharactor(self, chara)

        self.charaWidget = chara
        self.redraw()

    def SetCharactorInitPosition(self, chara):
        super().SetCharactorInitPosition(chara)
        self.charaWidget = chara;
        self.charaWidget.pos = self.GetRectPos(chara.cpos)
        self.redraw()


Factory.register("FlowChartViewer", cls=FlowChartViewer)


class BlockItemButton(ListItemButton, FloatLayout):
    def __init__(self, **kwargs):
        super(BlockItemButton, self).__init__(kwargs);


def generatePythonBlock(blk_unused):
    popup = None
    pyw = PythonBlockWidget(fn="")

    def loadFile(path, filename):
        fn = join(path, filename[0])
        pyw.filename = fn
        popup.dismiss()

    def cancel():
        popup.dismiss()

    # chooser.path = os.path.dirname(os.path.abspath(__file__))
    popup = showFileChooserPopUp("Load file", loadFile, cancel, ["*.py"])

    return pyw


def generateConditionBlock(beforeBlock):
    cbw = ConditionBlockWidget(incblock=beforeBlock, block=None)

    #ブロックの選択の結果を返す
    def selectBlock(block):
        cbw.setBlock(block)
        FlowChartViewer.block_state = FlowChartViewer.BLOCK_SET_MODE
        FlowChartViewer.block_on_push = None

    FlowChartViewer.block_state = FlowChartViewer.BLOCK_SELECT_MODE
    FlowChartViewer.block_on_push = selectBlock

    return cbw


def setSelectedBlockGenerator(inst):
    BlockListView.selectedBlockGenerator = inst


class BlockListView(ListView):
    selectedBlockGenerator = None

    # data = [{'text' : str(i), 'is_selected': False, 'source': 'testimage.png'} for i in range(8)]
    data = {'0': {'gen': lambda blk: NullBlockWidget(),      'img': 'img/null.png'},
            '1': {'gen': lambda blk: RightBlockWidget(),     'img': RightBlockWidget.source },
            '2': {'gen': lambda blk: LeftBlockWidget(),      'img': LeftBlockWidget.source },
            '3': {'gen': lambda blk: UpBlockWidget(),        'img': UpBlockWidget.source },
            '4': {'gen': lambda blk: DownBlockWidget(),      'img': DownBlockWidget.source },
            '5': {'gen': lambda blk: StartBlockWidget(),     'img': StartBlockWidget.source },
            '6': {'gen': lambda blk: EndBlockWidget(),       'img': EndBlockWidget.source },
            '7': {'gen': lambda blk: RightTurnBlockWidget(), 'img': RightTurnBlockWidget.source },
            '8': {'gen': lambda blk: LeftTurnBlockWidget(),  'img': LeftTurnBlockWidget.source },
            '9': {'gen': generatePythonBlock,    'img': PythonBlockWidget.source },
            '10': {'gen': generateConditionBlock, 'img': ConditionBlockWidget.source }
            }

    args_converter = \
        lambda row_index, rec: \
            {'text': "",
             'size_hint_y': None,
             'cls_dicts': [{'cls': ListItemButton,
                            'kwargs': {'text': rec['img'],
                                       'background_normal': rec['img'],
                                       'selected_color': [1, 1, 0, 1],
                                       'deselected_color': [1, 1, 1, 1],
                                       'on_press': lambda inst: setSelectedBlockGenerator(rec['gen']) }},
                           {'cls': ListItemLabel,
                            'kwargs': {'text': "",
                                       'is_representing_cls': True, 'size': [50, 50]}},
                           ]}


    def __init__(self, **kwargs):
        item_strings = ["{0}".format(index) for index in range(11)]

        dict_adapter = DictAdapter(sorted_keys=item_strings,
                                    data=BlockListView.data,
                                    args_converter=BlockListView.args_converter,
                                    selection_mode='single',
                                    allow_empty_selection=False,
                                    cls=CompositeListItem)

        super(BlockListView, self).__init__(adapter=dict_adapter)


class ExecButton(Button):
    mapInstance = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.chara = None
        super().__init__(**kwargs)

    def on_press(self, *arg):
        if self.chara == None:
            self.chara = CharactorWidget(size=[self.mapInstance.blockSize, self.mapInstance.blockSize], mapInstance=self.mapInstance)
            self.mapInstance.SetCharactorInitPosition(self.chara)
            self.mapInstance.redraw()
            # Clock.schedule_interval(self.updateCharactor, 0.8)
            self.updateCharactor()
        # else:
            # self.chara.step(1, self.mapInstance)
            # self.mapInstance.redraw()

    def updateCharactor(self, *args):
        def setNextAnimation():
            if self.mapInstance.charaWidget != None:
                self.chara.step(1, self.mapInstance)
                if isinstance(self.mapInstance.GetBlock(self.chara.cpos), EndBlock):
                    return
                elif not self.mapInstance.IsInRange():

                    def okpush(inst):
                        sys.exit()
                    def restartpush(inst):
                        self.chara = None
                        self.mapInstance.charaWidget = None
                        self.mapInstance.redraw()
                        self.popup.dismiss()

                    layout = BoxLayout(orientation='vertical')
                    layout.add_widget(Button(text="end", multiline=False, on_press=okpush))
                    layout.add_widget(Button(text="restart", multiline=False, on_press=restartpush))

                    self.popup = Popup(title='warnnig',
                                  content=layout,
                    size_hint=(None, None), size=(300, 200))
                    self.popup.open()

                    return
                else:
                    Clock.schedule_once(self.updateCharactor)

        anim = Animation(pos=self.mapInstance.GetRectPos([
             self.chara.cpos[0] + self.chara.vec[0],
             self.chara.cpos[1] + self.chara.vec[1]
        ]), t='out_bounce')
        anim.bind(on_complete=lambda *args: setNextAnimation())
        anim.start(self.chara)


class RestartButton(Button):
    execButton = ObjectProperty(None)
    mapInstance = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_press(self, *arg):
        self.execButton.chara = None
        self.mapInstance.charaWidget = None
        self.mapInstance.redraw()


class SaveButton(Button):
    mapInstance = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_press(self, *arg):
        jsonstr = json.dumps(self.mapInstance, cls=jsonenc.WidgetEncoder)

        popup = None
        def saveMap(path, filename):
            fn = join(path, filename[0])
            f = None
            try:
                f = open(fn, 'w')
                f.write(jsonstr)
            finally:
                if f != None:
                    f.close()
                popup.dismiss()

        def cancel():
            popup.dismiss()

        popup = showSaveFileChooserPopup("Save file", saveMap, cancel)


class LoadButton(Button):
    mapInstance = ObjectProperty(None)
    chooser = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_press(self, *arg):
        popup = None

        def loadMap(path, filename):
            fn = join(path, filename[0])
            f = None
            try:
                f = open(fn, 'r')
                jsonenc.widgetDecoder(self.mapInstance, f.read().rstrip())
            finally:
                if f != None:
                    f.close()
                popup.dismiss()

        def cancel():
            popup.dismiss()

        # chooser.path = os.path.dirname(os.path.abspath(__file__))
        popup = showFileChooserPopUp("Load file", loadMap, cancel, ["*.json"])


class FlowChart(FloatLayout):
    viewer = ObjectProperty(None)
    blockList = ObjectProperty(None)
    execButton = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FlowChart, self).__init__(**kwargs)
        open('log.txt','w',encoding='utf-8').close()


    def on_size(self, *args):
        if not self.viewer: return
        self.viewer.size = [self.width - 200, self.height]


    def on_touch_up(self, touch):
        # print(touch.x, touch.y)
        return super().on_touch_up(touch)

    def on_touch_down(self, touch):
        # print(touch.x, touch.y)
        return super().on_touch_down(touch)


class LoadDialog(FloatLayout):
    filechooser = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


def showFileChooserPopUp(title, loadfunc, cancelfunc, filters):
    popup = None

    content = LoadDialog(load=loadfunc, cancel=cancelfunc)
    content.filechooser.path = dirname(abspath(__file__))
    content.filechooser.filters = filters
    popup = Popup(title=title, content=content, size_hint=(0.9, 0.9))
    popup.open()
    return popup


class SaveDialog(FloatLayout):
    filechooser = ObjectProperty(None)
    textinput = ObjectProperty(None)
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


def showSaveFileChooserPopup(title, savefunc, cancelfunc):
    popup = None
    content = None

    def saveCaller(selection, touch):
        savefunc(content.filechooser.path, [content.textinput.text])

    content = SaveDialog(load=saveCaller, cancel=cancelfunc)
    content.filechooser.path = dirname(abspath(__file__))
    popup = Popup(title=title, content=content, size_hint=(0.9, 0.9))
    popup.open()
    return popup


Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)


class FlowChartApp(App):
    def build(self):
        return FlowChart()


if __name__ == '__main__':
    FlowChartApp().run()
