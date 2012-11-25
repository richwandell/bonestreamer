import win32api, re, sys, win32gui, webbrowser, sqlite3
from PIL import ImageTk, Image
from classes.systray_icon_manager import SystrayIconManager
from Tkinter import (OptionMenu, Checkbutton, Menu, 
END, Entry, Label, Button, Canvas, Listbox, StringVar, IntVar, PhotoImage, Toplevel, VERTICAL)
from ttk import *


'''
Main is the class for layout_manager module. 
Layout manger handles the majority of interface interactions for Bonestreamer
@author: Rich Wandell
@contact: richwandell@gmail.com
@note: I like compact code, but I wouldn't expect to find readable and concise coding style
conventions throughout the application. I tend to lean left when it comes to code.
'''
class Main:
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
     
    """
    Changes the port value when the select box is changed
    """
    def selectBoxChanged(self, event):
        if event == 'tcp':
            self.cur.execute("""
                   select value from settings
                   where type = 'port' 
                   and key = 'tcp'
            """)               
            self.broadcasting_tcp_port = self.cur.fetchone()[0]
            self.wgt['port_text'].delete(0, END)
            self.wgt['port_text'].insert(0, self.broadcasting_udp_port)                                             
        elif event == 'udp':               
            self.cur.execute("""
                 select value from settings
                 where type = 'port' 
                 and key = 'udp'
            """)
            self.broadcasting_udp_port = self.cur.fetchone()[0]
            self.wgt['port_text'].delete(0, END)
            self.wgt['port_text'].insert(0, self.broadcasting_udp_port)               
        else:
            self.cur.execute("select value from settings where type = 'port' and key = 'http' ")
            self.broadcasting_http_port = self.cur.fetchone()[0]               
            self.wgt['port_text'].delete(0, END)
            self.wgt['port_text'].insert(0, self.broadcasting_http_port)                                   
    """
       Event handler for the configure event
       This will set overrideredirect on the window when it is visible
    """
    def configure(self, event):
        if self.root.winfo_viewable() is 1:
            self.root.overrideredirect(True)          
          
    """
    Event handler for when the mouse is moved
    This method looks at the mouse x and y coordinates to find out if we are hovering over one of the custom made
    icons used in this app.
    @postcondition: Buttons will be highlighted or un-highlighted depending on whether or not
    the mouse x and y coordinates are over the buttons
    """     
    def mouseMoved(self, event):
        if event.x - 656 > 0 and event.x - 656 < 38 and event.y - 40 <= 0:
            self.wgt['canvas'].delete(self.wgt['canvas_close_icon'])
            self.wgt['canvas_close_icon'] = self.wgt['canvas'].create_image(676, 20, image = self.images['close_icon_hover'])
            self.wgt['canvas'].delete(self.wgt['canvas_minimize_icon'])
            self.wgt['canvas_minimize_icon'] = self.wgt['canvas'].create_image(636, 20, image=self.images['minimize_icon'])
        elif event.x - 616 > 0 and event.x - 616 < 38 and event.y - 40 <= 0:
            self.wgt['canvas'].delete(self.wgt['canvas_minimize_icon'])
            self.wgt['canvas_minimize_icon'] = self.wgt['canvas'].create_image(636, 20, image=self.images['minimize_icon_hover'])
            self.wgt['canvas'].delete(self.wgt['canvas_close_icon'])
            self.wgt['canvas_close_icon'] = self.wgt['canvas'].create_image(676, 20, image = self.images['close_icon'])
        elif event.x - 616 > 0 and event.x < 680 and event.y > 419:
            self.wgt['canvas'].delete(self.wgt['tux_xray_icon'])
            self.wgt['tux_xray_icon'] = self.wgt['canvas'].create_image(650, 450, image=self.images['tux_xray_icon_hover'])
        else:
            self.wgt['canvas'].delete(self.wgt['canvas_close_icon'])
            self.wgt['canvas'].delete(self.wgt['canvas_minimize_icon'])
            self.wgt['canvas_close_icon'] = self.wgt['canvas'].create_image(676, 20, image = self.images['close_icon'])
            self.wgt['canvas_minimize_icon'] = self.wgt['canvas'].create_image(636, 20, image=self.images['minimize_icon'])
            self.wgt['canvas'].delete(self.wgt['tux_xray_icon'])
            self.wgt['tux_xray_icon'] = self.wgt['canvas'].create_image(650, 450, image=self.images['tux_xray_icon'])
               
    """
    Event handler for when mouse is released
    @precondition: Frame is opaque
    @postcondition: Frame is fully visible
    """
    def mouseUp(self, event):
        self.root.attributes('-alpha', 1)
    """
    Event handler for when the mouse is dragged
    @param event: Tkinter event
    @note: This will move the frame around as if it were being dragged by 
    the native window chrome. 
    """
    def mouseDragged(self, event):
        self.root.attributes('-alpha', 0.5)
        x_distance = event.x - self.mouse_x
        y_distance = event.y - self.mouse_y
          
        dim, left, top = self.root.geometry().split("+")
                   
        self.root.geometry('%dx%d+%d+%d' % (700, 500, int(left) + int(x_distance), int(top) + int(y_distance) ) )
     
    """
    Event handler for when the mouse is clicked on the canvas
    if the mouse is over one of our custom icons, this method will 
    call the appropriate event handler
    """
    def mouseClicked(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        if event.x - 656 > 0 and event.x - 656 < 38 and event.y - 40 <= 0:
            self.closeApp()
        elif event.x - 616 > 0 and event.x - 616 < 38 and event.y - 40 <= 0:
            self.minimize()
        elif event.x - 616 > 0 and event.x < 680 and event.y > 419:
            self.showSkeletonWindow()
        elif event.x < 90 and event.x > 14 and event.y > 405 and event.y < 481:
            webbrowser.open_new("www.github.com/richwandell/bonestreamer")     
    """
    @todo: write this method
    """
    def showSkeletonWindow(self):
        self.objs['SkeletonWindow'] = self.classes['SkeletonWindow'](Toplevel(), self.objs, self.classes)
    """
    Minimizes the window by first setting override redirect to false
    which will give us back the taskbar icon
    then runs the iconify function
    """
    def minimize(self):
        self.root.overrideredirect(False)
        self.root.iconify()
               
    """
    Ends possible running threads and closes windows.
    """     
    def closeApp(self, thing=False):
        try: 
            self.objs['http_server'].server_close() 
        except Exception as e: 
            pass
        try: 
            self.objs['udp_server'].server_close()
        except Exception as e:
            pass
        try: 
            self.objs['tcp_server'].server_close()
        except Exception as e: 
            pass
        
        sys.exit(0)       
                   
    """
         Event handler for when the broadcasting button in clicked
    """
    def broadcastingButtonCallback(self, event):
        if self.broadcasting_status is 'off':
            event.widget.config(text='Stop Broadcasting')               
            status_text = 'Http: '+str(self.broadcasting_http_port)
            if self.broadcasting_type.get() == 'udp':
                status_text = 'UDP: '+str(self.broadcasting_udp_port)
            elif self.broadcasting_type.get() == 'tcp':
                status_text = 'TCP: '+str(self.broadcasting_tcp_port)               
            self.wgt['canvas_broadcasting_status'].config(text=status_text, foreground='green')               
            self.objs['SkeletonServer'] = self.classes['SkeletonServer']()
            self.objs['SkeletonServer'].server_type = self.broadcasting_type.get() 
            self.objs['SkeletonServer'].start()
            self.broadcasting_status = 'on'
        else:
            event.widget.config(text='Start Broadcasting')
            self.broadcasting_status = 'off'
            if self.broadcasting_type.get() == 'http':
                self.objs['http_server'].server_close()
            elif self.broadcasting_type.get() == 'udp':
                self.objs['udp_server'].server_close()
            else:
                self.objs['tcp_server'].server_close()                    
            self.wgt['canvas_broadcasting_status'].config(text="Not Broadcasting", foreground='red')
    """
          Event handler for pressing a key in the scale input boxes
          These input boxes are used to configure the auto scale feature of the 
          kinect for windows sdk
    """
    def keypress(self, event):
        if re.match(r'[a-zA-Z]', event.char):
            old = event.widget.get().replace(event.char, '')
            event.widget.delete(0, END)
            event.widget.insert(0, old)
          
        port_type = self.broadcasting_type.get()
        port_number = self.wgt['port_text'].get()
          
        self.cur.execute(
             " update settings set value = ? where type = 'port' and key = ? ",
             [str(port_number), str(port_type)]
        )
        self.conn.commit()

    """
          Centers the window in the middle of the screen
    """
    def center_window(self, w=300, h=200):
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
     
    """
    Creates all elements for the layout
    @param Widget root The root element that is need for adding elements to it  
    """     
    def createElements(self, root):
        self.images = {
             'close_icon': ImageTk.PhotoImage(Image.open('img/close_icon.png')),
             'close_icon_hover': ImageTk.PhotoImage(Image.open('img/close_icon_hover.png')),
             'minimize_icon': ImageTk.PhotoImage(Image.open('img/minimize_icon.png')),
             'minimize_icon_hover': ImageTk.PhotoImage(Image.open('img/minimize_icon_hover.png')),
             'bonestreamer_logo': ImageTk.PhotoImage(Image.open('img/bonestreamer1.png')), 
             'bonestreamer_background': ImageTk.PhotoImage(Image.open('img/bonestreamer_background.png')),
             'tux_xray_icon': ImageTk.PhotoImage(Image.open('img/tux-xray.png')),
             'tux_xray_icon_hover': ImageTk.PhotoImage(Image.open('img/tux-xray_hover.png')),
             'github_image': ImageTk.PhotoImage(Image.open('img/github-fork-me.png')),
             'hand_cursor': ImageTk.PhotoImage(Image.open("img/hand_cursor_left.png"))
        }          
        style = Style()
        style.configure(
             "main_frame.TFrame",
             relief='sunken'
        )
        self.wgt['canvas'] = Canvas(root, width=700, height=500, cursor='@img/Glass.cur' )
        self.wgt['bonestreamer_background'] = self.wgt['canvas'].create_image(350,250, image=self.images['bonestreamer_background'])
        self.wgt['canvas_close_icon'] = self.wgt['canvas'].create_image(676, 20, image = self.images['close_icon'])
        self.wgt['canvas_minimize_icon'] = self.wgt['canvas'].create_image(636, 20, image=self.images['minimize_icon'])
        self.wgt['bonestreamer_logo'] = self.wgt['canvas'].create_image(115, 50, image=self.images['bonestreamer_logo'])
        self.wgt['tux_xray_icon'] = self.wgt['canvas'].create_image(650, 450, image=self.images['tux_xray_icon'])
        self.wgt['hand_cursor'] = self.wgt['canvas'].create_image(350, 455, image=self.images['hand_cursor'])
        self.wgt['github_image'] = self.wgt['canvas'].create_image(70, 425, image=self.images['github_image'])          
        self.wgt['main_frame'] = Frame(root, style='main_frame.TFrame')          
        optionList = ("http", "udp", "http", "tcp")
        self.broadcasting_type = StringVar()          
        self.broadcasting_type.set(1)
        self.wgt['broadcasting_type'] = OptionMenu(
            self.wgt['main_frame'], 
            self.broadcasting_type, 
            *optionList,
            command=self.selectBoxChanged
        )
        self.wgt['canvas_broadcasting_status'] = Label(self.wgt['main_frame'], text='Not Broadcasting', foreground='red')
        self.wgt['broadcasting_type_label'] = Label(self.wgt['main_frame'], text='Server Type:', anchor='w')
        self.wgt['status_label'] = Label(self.wgt['main_frame'], text='Server Status:', anchor='w')
        self.wgt['broadcasting_button'] = Button(self.wgt['main_frame'], text='Start Broadcasting')
        
        self.wgt['port_label'] = Label(self.wgt['main_frame'], text='Port:', anchor='w')
        self.wgt['port_text'] = Entry(self.wgt['main_frame'])
        self.wgt['host_label'] = Label(self.wgt['main_frame'], text='Host:', anchor='w')
        self.wgt['host_text'] = Entry(self.wgt['main_frame'])
        
        self.wgt['enable_mouse_movement_button'] = Button(self.wgt['main_frame'], text='Enable Mouse Control')
        
        self.objs['skeleton_stream'] = IntVar()
        self.objs['skeleton_stream'].set(1)
        self.objs['video_stream'] = IntVar()
        self.objs['video_stream'].set(0)
        self.wgt['enable_skeleton_data'] = Checkbutton(self.wgt['main_frame'], text='Skeleton Stream', variable=self.objs['skeleton_stream'])
        self.wgt['enable_video_data'] = Checkbutton(self.wgt['main_frame'], text='Video Stream', variable=self.objs['video_stream']) 
        self.wgt['slider'] = Scale(self.wgt['main_frame'], from_=15, to=-15, orient=VERTICAL)
        self.wgt['slider'].set(self.objs['kinect'].camera.elevation_angle)
        
        self.wgt['image_filter_fieldset'] = LabelFrame(self.wgt['main_frame'], text="Image Filters")
        
        for x in ['blur','contour','detail','edge_enhance','edge_enhance_more','emboss','find_edges','smooth','smooth_more','sharpen']:            
            self.objs[x] = IntVar()
            self.objs[x].set(0)
            self.wgt[x] = Checkbutton(self.wgt['image_filter_fieldset'], text=x.replace("_", " "), variable=self.objs[x])
        
    """
    Positions the elements on the grid
    @param root: Tkinter root widget
    @postcondition: Everything in its riiiiiiight place (@author: Radiohead)
    """
    def positionElements(self, root):          
        self.wgt['canvas'].place(x=0, y=0)
        self.wgt['main_frame'].place(x=80, y=100)        
        self.wgt['slider'].place(x=500, y=5)        
        #row0
        self.wgt['status_label'].grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.wgt['canvas_broadcasting_status'].grid(row=0, column=1, padx=5, pady=5, sticky='W')
        self.wgt['broadcasting_type_label'].grid(row=1, column=0, padx=5, pady=5, sticky='W')          
        self.wgt['broadcasting_type'].config(width=25)          
        #row1
        self.wgt['broadcasting_type'].grid(row=1, column=1, padx=5, pady=5, sticky='W')
        self.wgt['enable_skeleton_data'].grid(row=1, column=2, padx=5, pady=5, sticky='W')
        #row2
        self.wgt['port_label'].grid(row=2, column=0, padx=5, pady=5, sticky='W')
        self.wgt['port_text'].grid(row=2, column=1, padx=5, pady=5, sticky='W')
        self.wgt['enable_video_data'].grid(row=2, column=2, padx=5, pady=5, sticky='W')        
        #row3
        self.wgt['host_label'].grid(row=3, column=0, padx=5, pady=5, sticky='W')
        self.wgt['host_text'].grid(row=3, column=1, pady=5, padx=5, sticky='W')        
        self.wgt['broadcasting_button'].grid(row=3, column=3, padx=5, pady=5, sticky='E')
        #row 4
        self.wgt['enable_mouse_movement_button'].grid(row=4, column=3, pady=5, padx=5, sticky='E')
        #row 5
        self.wgt['image_filter_fieldset'].grid(row=5, column=0, columnspan=5)
        self.wgt['image_filter_fieldset'].grid_forget()
        #row1 on image filter
        self.wgt['blur'].grid(row=1, column=0, padx=5, pady=5, sticky='W')
        self.wgt['contour'].grid(row=1, column=1, padx=5, pady=5, sticky='W')
        self.wgt['detail'].grid(row=1, column=2, padx=5, pady=5, sticky='W')
        self.wgt['edge_enhance'].grid(row=1, column=3, padx=5, pady=5, sticky='W')
        #row 2 on image filter
        self.wgt['edge_enhance_more'].grid(row=2, column=0, padx=5, pady=5, sticky='W') 
        self.wgt['emboss'].grid(row=2, column=1, padx=5, pady=5, sticky='W')
        self.wgt['find_edges'].grid(row=2, column=2, padx=5, pady=5, sticky='W')
        self.wgt['smooth'].grid(row=2, column=3, padx=5, pady=5, sticky='W')
        #row 3 on image filter
        self.wgt['smooth_more'].grid(row=3, column=0, padx=5, pady=5, sticky='W')
        self.wgt['sharpen'].grid(row=3, column=1, padx=5, pady=5, sticky='W')
    '''
    Event handler for the video stream checkbox
    @postcondition: Opens video connection to the kinect if it hasn't already been 
    opened. Also shows and hides the image filter panel.
    '''
    def videoStreamCheckEvent(self, event):
        if self.objs['video_stream'].get() == 0:
            try: self.objs['open_video']() 
            except: pass
            self.wgt['image_filter_fieldset'].grid(row=5, column=0, columnspan=5)
        else:
            self.wgt['image_filter_fieldset'].grid_forget()
    '''
    @todo: I don't remember what this is here for... Will fix later
    '''       
    def skeletonStreamCheckEvent(self, event):
        print self.objs['skeleton_stream'].get()
    """
    Binds events to the elements and sets up callbacks and initial values for entry widgets
    @param root: The root level tkinter widget
    """
    def bindEvents(self, root):
        self.wgt['broadcasting_button'].bind("<Button-1>", self.broadcastingButtonCallback)                             
        self.wgt['enable_video_data'].bind('<Button-1>', self.videoStreamCheckEvent)
        self.wgt['enable_skeleton_data'].bind('<Button-1>', self.skeletonStreamCheckEvent)
        self.wgt['canvas'].bind('<Motion>', self.mouseMoved)
        self.wgt['canvas'].bind('<Button-1>', self.mouseClicked)
        self.wgt['canvas'].bind('<B1-Motion>', self.mouseDragged)
        self.wgt['canvas'].bind('<ButtonRelease-1>', self.mouseUp)
        self.root.bind('<Configure>', self.configure)
        self.wgt['port_text'].bind('<KeyRelease>', self.keypress)
        self.wgt['enable_mouse_movement_button'].bind('<Button-1>', self.toggleMouseControl)
        self.wgt['slider'].bind('<ButtonRelease-1>', self.moveKinectHead)

        for x in ['blur','contour','detail','edge_enhance','edge_enhance_more','emboss','find_edges','smooth','smooth_more','sharpen']:
            setattr(self.wgt[x], 'widget_id', x)
            self.wgt[x].bind('<Button-1>', self.checkButtonFilterClicked)
    '''
    Event handler for image filter checkboxes
    @param event: The tkinter event
    '''
    def checkButtonFilterClicked(self, event):
        if event.widget.widget_id in self.objs['image_filter']:
            self.objs['image_filter'].remove(event.widget.widget_id)
        else:
            self.objs['image_filter'].append(event.widget.widget_id)
    '''
    Event handler for moving the slider up or down
    @param event: Tkinter event
    @postcondition: The kinect head will move up or down
    '''
    def moveKinectHead(self, event):
        self.objs['kinect'].camera.elevation_angle = int(self.wgt['slider'].get())
    '''
    Event handler for toggling mouse control on or off
    @param event: Tkinter event
    '''
    def toggleMouseControl(self, event):
        if self.objs['mouse_control_bool'] == False: 
            self.objs['mouse_control_bool'] = True 
        else: 
            self.objs['mouse_control_bool'] = False
    '''
    Slowly hides the window when minimize button is clicked
    '''
    def hideWindow(self, sysTrayIcon):
        start = 1
        while start > 0.0:
            self.root.attributes('-alpha', start)
            start = start - 0.0001
          
    def __init__(self, root, objs, classes):
        
        self.root = root
        self.objs = objs
        self.classes = classes
        self.x_scale = 1920
        self.y_scale = 1080
          
        self.broadcasting_type = 'udp'
        self.broadcasting_status = 'off'
        cur = self.cur
        cur.execute("select value from settings where type = 'port' and key = 'http' order by default_value limit 1")        
        self.broadcasting_http_port = cur.fetchone()[0]
        cur.execute("select value from settings where type = 'port' and key = 'udp' order by default_value limit 1")
        self.broadcasting_udp_port = cur.fetchone()[0]
        cur.execute("select value from settings where type = 'port' and key = 'tcp' order by default_value limit 1")
        self.broadcasting_tcp_port = cur.fetchone()[0]
          
        root.overrideredirect(True)
        
        root.winfo_toplevel().minsize(700,500)
        root.winfo_toplevel().maxsize(700,500)
        self.center_window(700,500)
          
        self.wgt = {}
        self.createElements(root)
        self.positionElements(root)
        self.bindEvents(root)
          
        self.wgt['port_text'].insert(0, self.broadcasting_http_port)
