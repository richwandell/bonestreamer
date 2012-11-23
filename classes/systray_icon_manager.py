import itertools, glob, threading, sys
from classes.systrayicon import SysTrayIcon

class SystrayIconManager(threading.Thread):
    global objs, classes
     
    def closeApp(self, sysTrayIcon=False):
        objs['systray'].destroy()
          
    def hideWindow(self, sysTrayIcon):
        print 'hi'
    def showWindow(self, sysTrayIcon):
        print 'hi'
          
    def run(self):
        print objs
        self.createMenu()
          
    """
          TODO create a menu, maybe
    """   
    def createMenu(self):
        icon = 'bonestream.ico'
        hover_text = "Bonestream"
          
        def hello(sysTrayIcon): 
            print "Hello World."
               
        def simon(sysTrayIcon): 
            print "Hello Simon."
               
        def switch_icon(sysTrayIcon):
            print'hi'
    #               sysTrayIcon.icon = icons.next()
    #               sysTrayIcon.refresh_icon()
               
        menu_options = (
               (
                    'Minimize to tray', 
                    icon, 
                    self.hideWindow
               ), (
                    'Maximize', 
                    None, 
                    self.showWindow
               ), (
                   'A sub-menu', 
                   icon, 
                   (
                        (
                             'Say Hello to Simon', 
                             icon, 
                             simon
                        ),
                        (
                             'Switch Icon', 
                             icon, 
                             switch_icon
                        ),
                    )
               )
        )
          
        objs['systray'] = SysTrayIcon(icon, hover_text, menu_options, on_quit=self.closeApp, default_menu_index=1)