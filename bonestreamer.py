from pykinect import nui, audio
from pykinect.nui import JointId
from Tkinter import Tk
from classes import skeleton_window, layout_manager, skeleton_server, systray_icon_manager
import ctypes, win32gui, win32gui_struct, win32api, sqlite3, base64, StringIO, ImageFilter
from PIL import Image

myappid = 'RW.Bonestreamer.ClientApp.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

kinect = nui.Runtime()

kinect.skeleton_engine.enabled = True

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

objs = {
     'SkeletonWindow': False,
     'SkeletonServer': False,
     'positions': ['ok'],
     'mouse_control_bool': False,
     'skeleton_stream': True,
     'video_stream': False,
     'open_video': lambda: kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color),
     'video_data': False,
     'kinect': kinect,
     'image_filter': []
}

classes = {
     'SkeletonServer': skeleton_server.SkeletonServer,
     'SkeletonWindow': skeleton_window.SkeletonWindow,
}

filter_map = {
    'blur': ImageFilter.BLUR,
    'contour': ImageFilter.CONTOUR, 
    'detail': ImageFilter.DETAIL, 
    'edge_enhance': ImageFilter.EDGE_ENHANCE, 
    'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE, 
    'emboss': ImageFilter.EMBOSS, 
    'find_edges': ImageFilter.FIND_EDGES, 
    'smooth': ImageFilter.SMOOTH, 
    'smooth_more': ImageFilter.SMOOTH_MORE, 
    'sharpen': ImageFilter.SHARPEN
}

skeleton_server.objs = objs
skeleton_server.classes = classes
 
window_width = win32api.GetSystemMetrics(0)
window_height = win32api.GetSystemMetrics(1)

def video_frame_ready(video_frame):
    if objs['video_stream'].get() == 1:
        image = Image.fromstring('RGBA', (640, 480), video_frame.image.bits)
                      
        if len(objs['image_filter']) > 0:
            for filter in objs['image_filter']:
                image = image.filter(filter_map[filter])
        
        output = StringIO.StringIO()
        image.save(output, format='JPEG')
        objs['video_data'] = base64.b64encode(output.getvalue())
    else:
        objs['video_data'] = False

def skeleton_frame_ready(skeleton_frame):
    global objs, window_width, window_height
    skeletons = skeleton_frame.SkeletonData
    print 'frame ready'
    def scaledBones():
        return list({
               'ankle_left': getScaled(data, JointId.AnkleLeft),
               'ankle_right': getScaled(data, JointId.AnkleRight),
               'elbow_left': getScaled(data, JointId.ElbowLeft),
               'elbow_right': getScaled(data, JointId.ElbowRight),
               'foot_left': getScaled(data, JointId.FootLeft),
               'foot_right': getScaled(data, JointId.FootRight),
               'hand_left': getScaled(data, JointId.HandLeft),
               'hand_right': getScaled(data, JointId.HandRight),   
               'head': getScaled(data, JointId.Head),   
               'hip_center': getScaled(data, JointId.HipCenter), 
               'hip_left': getScaled(data, JointId.HipLeft), 
               'hip_right': getScaled(data, JointId.HipRight),
               'knee_left': getScaled(data, JointId.KneeLeft),
               'knee_right': getScaled(data, JointId.KneeRight),
               'shoulder_center': getScaled(data, JointId.ShoulderCenter),
               'shoulder_left': getScaled(data, JointId.ShoulderLeft),  
               'shoulder_right': getScaled(data, JointId.ShoulderRight),
               'spine': getScaled(data, JointId.Spine),
               'wrist_left': getScaled(data, JointId.WristLeft),
               'wrist_right': getScaled(data, JointId.WristRight),
         } for data in skeletons)
         
    def unScaledBones():
        return list({
               'ankle_left': getUnscaled(data, JointId.AnkleLeft),
               'ankle_right': getUnscaled(data, JointId.AnkleRight),
               'elbow_left': getUnscaled(data, JointId.ElbowLeft),
               'elbow_right': getUnscaled(data, JointId.ElbowRight),
               'foot_left': getUnscaled(data, JointId.FootLeft),
               'foot_right': getUnscaled(data, JointId.FootRight),
               'hand_left': getUnscaled(data, JointId.HandLeft),
               'hand_right': getUnscaled(data, JointId.HandRight),   
               'head': getUnscaled(data, JointId.Head),   
               'hip_center': getUnscaled(data, JointId.HipCenter), 
               'hip_left': getUnscaled(data, JointId.HipLeft), 
               'hip_right': getUnscaled(data, JointId.HipRight),
               'knee_left': getUnscaled(data, JointId.KneeLeft),
               'knee_right': getUnscaled(data, JointId.KneeRight),
               'shoulder_center': getUnscaled(data, JointId.ShoulderCenter),
               'shoulder_left': getUnscaled(data, JointId.ShoulderLeft),  
               'shoulder_right': getUnscaled(data, JointId.ShoulderRight),
               'spine': getUnscaled(data, JointId.Spine),
               'wrist_left': getUnscaled(data, JointId.WristLeft),
               'wrist_right': getUnscaled(data, JointId.WristRight),
         } for data in skeletons)
    
    def getScaled(data, which): 
        point = skeleton_to_depth_image( data.SkeletonPositions[which], window_width, window_height)
        return {
               'x': point[0], 
               'y': point[1]
        }
          
    def getUnscaled(data, which):
        return {
               'x': data.SkeletonPositions[which].x,  
               'y': data.SkeletonPositions[which].y,  
               'z': data.SkeletonPositions[which].z
        }


    if objs['mouse_control_bool'] == True:
        objs['positions'] = scaledBones()
        for x in objs['positions']:
            if x['hand_right']['x'] > 0:
                win32api.SetCursorPos(
                    (
                        int(x['hand_right']['x']), 
                        int(x['hand_right']['y']) 
                    )
                )
    elif objs['SkeletonWindow'] != False:
        objs['positions'] = scaledBones()
        objs['SkeletonWindow'].draw()
    else:
        objs['positions'] = unScaledBones()

kinect.skeleton_frame_ready += skeleton_frame_ready
kinect.video_frame_ready += video_frame_ready

root = Tk()
frame = layout_manager.Main(root, objs, classes)

root.mainloop()   