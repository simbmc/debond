'''
Created on 24.10.2016

@author: Yingxiong
'''
from multilinear_editor import MultilinearEditor
from kivy.uix.boxlayout import BoxLayout
from 


class BondEditor(BoxLayout):
    
    def __init__(self, **kwargs):
        super(BondEditor, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.create_graph()
        self.create_panel()
        
    def creat_graph(self):
