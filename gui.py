## @file
## @brief native client GUI

# https://github.com/ponyatov/pyFORTH/blob/master/FORTH.py

## @defgroup gui Native client GUI
## @frief wxWidgets
## @{

import wx, wx.stc, threading

from sym import *
from forth import *

import time

## generic GUI window
class GUI_window(wx.Frame):
    
    ## @name initialization
    
    ## define constructor parameters to default values specific for our app
    ## @param[in] title window title
    ## @param[in] filename file name will be used on save console content
    def __init__(self,parent=None,title='KB/wx',filename=sys.argv[0]+'.save'):
        wx.Frame.__init__(self,parent,title='%s:%s'%(title,filename))
        ## file name will be used for console content save/load
        self.filename = filename
        self.menu()
    ## initialize menu
    def menu(self):
        ## menu bar
        self.menubar = wx.MenuBar() ; self.SetMenuBar(self.menubar)
        
        ## file submenu
        self.file = wx.Menu() ; self.menubar.Append(self.file,'&File')
        ## file/save console content
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        self.Bind(wx.EVT_MENU,self.onSave,self.save)
        ## file/quit
        self.quit = self.file.Append(wx.ID_EXIT,'&Quit')
        self.Bind(wx.EVT_MENU,self.onQuit,self.quit)
        
    ## @name event callbacks
    
    ## quit event callback
    def onQuit(self,event): self.Close()
    ## save console content callback
    def onSave(self,event):
        with open(self.filename,'a') as F:
            print >>F,time.strftime('\n%H:%M:%S %d/%m/%Y',time.localtime()),
            print >>F,self.GetTitle() 

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
