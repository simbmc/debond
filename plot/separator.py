'''
Created on 26.09.2016

@author: Yingxiong
'''
from kivy.uix.widget import Widget
# from kivy.graphics import Rectangle
from kivy.lang import Builder

Builder.load_string("""
<Separator@Widget>:
    size_hint_y: None
    height: dp(6)
    color: 1, 1, 1, 1
    background_image: ''

    canvas:
        Color:
            rgba: root.color
        Rectangle:
            pos: self.pos
            size: self.size
            source: root.background_image
""")


class Separator(Widget):
    pass