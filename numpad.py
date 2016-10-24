'''
Created on 01.03.2016

@author: mkennert
'''
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

# from ownComponents.ownLabel import OwnLabel


class Numpad(GridLayout):

    '''
    the class numpad was developed to give the user the possibility
    to input a value
    '''

    # parent-component of the keyboard
    p = ObjectProperty()

    # strings
    plusStr, minusStr = StringProperty('+'), StringProperty('-')
    defaultStr = StringProperty('')
    confirmStr, cancelStr = StringProperty('ok'), StringProperty('cancel')
    dotStr, backStr = StringProperty('.'), StringProperty('<<')

    '''
    constructor
    '''

    def __init__(self, **kwargs):
        super(Numpad, self).__init__(**kwargs)
        self.cols = 1
        self.create_numfield_with_sign()

    '''
    the method create_numfield create the gui
    of the numpad
    '''

    def create_numfield_with_sign(self):
        self.create_btns()
        self.lblTextinput = Label(text=self.defaultStr)
        self.numfieldLayout = GridLayout(cols=4)
        for i in range(1, 10):
            cur = Button(text=str(i))
            cur.bind(on_press=self.appending)
            self.numfieldLayout.add_widget(cur)
            if i == 3:
                self.numfieldLayout.add_widget(self.btnPlus)
            elif i == 6:
                self.numfieldLayout.add_widget(self.btnMinus)
            elif i == 9:
                self.numfieldLayout.add_widget(self.btnCancel)
        self.numfieldLayout.add_widget(self.btnDot)
        self.numfieldLayout.add_widget(self.btnZero)
        self.numfieldLayout.add_widget(self.btnDelete)
        self.numfieldLayout.add_widget(self.btnOK)
        self.add_widget(self.lblTextinput)
        self.add_widget(self.numfieldLayout)

    '''
    create and bind all btns of the numpad
    '''

    def create_btns(self):
        # create the btns
        self.btnZero = Button(text=str(0))
        self.btnOK = Button(text=self.confirmStr)
        self.btnCancel = Button(text=self.cancelStr)
        self.btnPlus = Button(text=self.plusStr)
        self.btnMinus = Button(text=self.minusStr)
        self.btnDelete = Button(text=self.backStr)
        self.btnDot = Button(text=self.dotStr)
        # bind the btns
        self.btnMinus.bind(on_press=self.set_sign)
        self.btnOK.bind(on_press=self.finished)
        self.btnCancel.bind(on_press=self.cancel)
        self.btnDot.bind(on_press=self.appending)
        self.btnZero.bind(on_press=self.appending)
        self.btnDelete.bind(on_press=self.delete)
        self.btnPlus.bind(on_press=self.set_sign)

    '''
    set the sign of the input-value
    '''

    def set_sign(self, btn):
        if self.lblTextinput.text == '':
            self.lblTextinput.text = btn.text
            return
        if btn.text == self.plusStr:
            if self.lblTextinput.text[0] == self.minusStr:
                self.lblTextinput.text = self.plusStr + \
                    self.lblTextinput.text[1:]
            elif not self.lblTextinput.text[0] == self.plusStr:
                self.lblTextinput.text = self.plusStr + self.lblTextinput.text
        else:
            if self.lblTextinput.text[0] == self.plusStr:
                self.lblTextinput.text = self.minusStr + \
                    self.lblTextinput.text[1:]
            elif not self.lblTextinput.text[0] == self.minusStr:
                self.lblTextinput.text = self.minusStr + self.lblTextinput.text

    '''
    the method finished close the popup when the user
    is finished and made a correctly input
    '''

    def finished(self, button):
        # try to cast the string in a floatnumber
        try:
            # proofs whether you can cast the input
            x = float(self.lblTextinput.text)
            self.lblTextinput.text = self.lblTextinput.text
            self.p.finished_numpad()
            self.reset_text()
        # if the value is not a float
        # the lblTextinput will be reset
        except ValueError:
            self.reset_text()

    '''
    the method appending appends the choosen digit at the end.
    the method is called when the user use the keyboard
    '''

    def appending(self, button):
        self.lblTextinput.text += button.text

    '''
    the method delete delete the digit at the end.
    the method is called when the press the button '<<'
    '''

    def delete(self, button):
        self.lblTextinput.text = self.lblTextinput.text[:-1]

    '''
    the method reset_text reset the text of the label
    the method must be called from the developer when
    the text must be deleted
    '''

    def reset_text(self):
        self.lblTextinput.text = ''

    '''
    cancel the numpad input
    '''

    def cancel(self, btn):
        self.p.close_numpad()
        self.reset_text()
