import win32api, time
from Tkinter import Canvas, ALL


class SkeletonWindow:
     def __init__(self, root, objs, classes):
          self.objs = objs
          self.classes = classes
          self.can = Canvas(root, width=1920, height=1080)
          self.can.create_line(0, 0, 50,50, fill='black')
          self.can.pack()
          self.alpha = 100
        

               
        
     def draw(self):
          data = self.objs['positions']
          self.can.delete(ALL)
        
          num = 0
          for skel in data:
               num+=1
            
               color = ''
            
               if num == 1: color = 'green'
               if num == 2: color = 'blue'
               if num == 3: color = 'red'
               if num == 4: color = 'orange'
               if num == 5: color = 'pink'
               if num == 6: color = 'black'
            
               #head
               self.can.create_oval(
                    (
                         ( skel['head']['x'] - 50),
                         ( skel['head']['y'] ),
                         ( skel['head']['x'] + 50),
                         ( skel['head']['y'] + 50)
                    ), fill=color
               )
               #shoulders
               self.can.create_line(
                    (
                         skel['shoulder_left']['x'],
                         skel['shoulder_left']['y'],
                         skel['shoulder_center']['x'],
                         skel['shoulder_center']['y'],
                    ), fill=color
               )
            
               self.can.create_line(
                    (
                         skel['shoulder_center']['x'],
                         skel['shoulder_center']['y'],
                         skel['shoulder_right']['x'],
                         skel['shoulder_right']['y'],
                    ), fill=color
               )
               
               #eldows
               self.can.create_line(
                    (
                         skel['elbow_left']['x'],
                         skel['elbow_left']['y'],
                         skel['shoulder_left']['x'],
                         skel['shoulder_left']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['elbow_right']['x'],
                         skel['elbow_right']['y'],
                         skel['shoulder_right']['x'],
                         skel['shoulder_right']['y'],
                    ), fill=color
               )
               #wrist
               self.can.create_line(
                    (
                         skel['wrist_left']['x'],
                         skel['wrist_left']['y'],
                         skel['elbow_left']['x'],
                         skel['elbow_left']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['wrist_right']['x'],
                         skel['wrist_right']['y'],
                         skel['elbow_right']['x'],
                         skel['elbow_right']['y'],
                    ), fill=color
               )
               #hand
               self.can.create_line(
                    (
                         skel['hand_left']['x'],
                         skel['hand_left']['y'],
                         skel['wrist_left']['x'],
                         skel['wrist_left']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['hand_right']['x'],
                         skel['hand_right']['y'],
                         skel['wrist_right']['x'],
                         skel['wrist_right']['y'],
                    ), fill=color
               )
               #hips
               self.can.create_line(
                    (
                         skel['hip_left']['x'],
                         skel['hip_left']['y'],
                         skel['hip_center']['x'],
                         skel['hip_center']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['hip_center']['x'],
                         skel['hip_center']['y'],
                         skel['hip_right']['x'],
                         skel['hip_right']['y'],
                    ), fill=color
               )
               #spine
               self.can.create_line(
                    (
                         skel['spine']['x'],
                         skel['spine']['y'],
                         skel['hip_center']['x'],
                         skel['hip_center']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['spine']['x'],
                         skel['spine']['y'],
                         skel['shoulder_center']['x'],
                         skel['shoulder_center']['y'],
                    ), fill=color
               )
               #hips to knees
               self.can.create_line(
                    (
                         skel['hip_left']['x'],
                         skel['hip_left']['y'],
                         skel['knee_left']['x'],
                         skel['knee_left']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['hip_right']['x'],
                         skel['hip_right']['y'],
                         skel['knee_right']['x'],
                         skel['knee_right']['y'],
                    ), fill=color
               )
               #ankle to knees
               self.can.create_line(
                    (
                         skel['ankle_left']['x'],
                         skel['ankle_left']['y'],
                         skel['knee_left']['x'],
                         skel['knee_left']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['ankle_right']['x'],
                         skel['ankle_right']['y'],
                         skel['knee_right']['x'],
                         skel['knee_right']['y'],
                    ), fill=color
               )
               #ankle to foot
               self.can.create_line(
                    (
                         skel['ankle_left']['x'],
                         skel['ankle_left']['y'],
                         skel['foot_left']['x'],
                         skel['foot_left']['y'],
                    ), fill=color
               )
               self.can.create_line(
                    (
                         skel['ankle_right']['x'],
                         skel['ankle_right']['y'],
                         skel['foot_right']['x'],
                         skel['foot_right']['y'],
                    ), fill=color
               )
            
            
          self.can.update_idletasks()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            