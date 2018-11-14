## @file
## @brief native client GUI

# https://github.com/ponyatov/pyFORTH/blob/master/FORTH.py

## @defgroup gui Native client GUI
## @frief wxWidgets
## @{

import wx, wx.stc, threading

from sym import *
from forth import *

## generic GUI window
class GUI_window(wx.Frame):
    ## define constructor parameters to default values specific for our app
    def __init__(self,parent=None,title='KB/wx'):
        wx.Frame.__init__(self,parent,title=title)

## GUI works in a separate thread to let UI work in parallel with Forth VM
class GUI_thread(threading.Thread):
    ## construct main window
    def __init__(self):
        threading.Thread.__init__(self)
        ## wx application
        self.app = wx.App()
        ## main window
        self.main = GUI_window()
    ## activate GUI event loop thread
    def run(self):
        self.main.Show()
        self.app.MainLoop()

## singleton thread processes all GUI events
gui_thread = GUI_thread()

## start GUI system
def GUI(): gui_thread.start() ; gui_thread.join()
F << GUI

if __name__ == '__main__': GUI()

## @}
