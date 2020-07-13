'''
This code has opengl visualization of 3D skeletons, including floor visualization and mouse+keyboard control
See the main function for demo codes.

showSkeleton: visualize 3D human body skeletons. This can handle holden's formation, 3.6m formation, and domeDB
setSpeech: to set speechAnnotation. Should be called before showSkeleton

renderscene: main function to render scenes using openGL

Note: this visualizer is assuming centimeter metric (joint, mesh).

Hanbyul Joo (jhugestar@gmail.com)
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import json
import numpy as np
from PIL import Image, ImageOps
import numpy as np

import sys, math

import threading

import time
#from time import time

#import pickle
#import cPickle as pickle
import _pickle as pickle


#-----------
# Global Variables
#-----------
#g_camView_fileName = '/ssd/camInfo/camInfo.pkl'
g_camView_fileName = './camInfo/camInfo.pkl'

g_fViewDistance = 50.
# g_Width = 1280
# g_Height = 720
# g_Width = 1920
# g_Height = 1080
g_Width = 1000
g_Height = 1280

g_nearPlane = 0.01        #original
# g_nearPlane = 1000          #cameramode
g_farPlane = 5000.

g_show_fps = False

g_action = ""
g_xMousePtStart = g_yMousePtStart = 0.

g_xTrans = 0.
g_yTrans = 0.
g_zTrans = 0.
g_zoom = 434
g_xRotate = -44.
g_yRotate = -39.
g_zRotate = 0.
g_xrot = 0.0
g_yrot = 0.0
# the usual screen dimension variables and lighting

# Generic Lighting values and coordinates
g_ambientLight = (0.35, 0.35, 0.35, 1.0)
g_diffuseLight = (0.75, 0.75, 0.75, 0.7)
g_specular = (0.2, 0.2, 0.2, 1.0)
g_specref = (0.5, 0.5, 0.5, 1.0)


# To visualize in Dome View point
#g_viewMode = 'camView'#free' #'camView'
g_viewMode = 'free' #'camView'
g_bOrthoCam = False     #If true, draw by ortho camera mode
from collections import deque
#g_camid = deque('00',maxlen=2)
g_camid = deque('27',maxlen=2)


g_onlyDrawHumanIdx = -1


# To save rendered scene into file
g_stopMainLoop = False
g_winID = None

g_bSaveToFile = False
g_bSaveToFile_done = False      #If yes, file has been saved

# g_savedImg = None       # Keep the save image as a global variable, if ones want to obtain this
# g_haggling_render = False       #Automatically Load next seqeucne, when frames are done
g_bSaveOnlyMode = False  #If true, load camera turn on save mode and exit after farmes are done
g_saveFolderName = None

"Visualization Options"
g_bApplyRootOffset = False
ROOT_OFFSET_DIST = 160
#ROOT_OFFSET_DIST = 30

""" Mesh Drawing Option """

#A tutorial for VAO and VBO: https://www.khronos.org/opengl/wiki/Tutorial2:_VAOs,_VBOs,_Vertex_and_Fragment_Shaders_(C_/_SDL)
g_vao= None
g_vertex_buffer= None
g_normal_buffer= None
g_tangent_buffer = None
g_index_buffer = None

g_hagglingSeqName= None
# global vts_num

# global SMPL_vts
# global face_num

# global SMPLModel
g_saveFrameIdx = 0
# global MoshParam


g_bGlInitDone = False       #To initialize opengl only once

BACKGROUND_IMAGE_PLANE_DEPTH=3000


######################################################
#  MTC Camera view
g_camView_K = None
g_camView_K_list = None #if  each mesh uses diff K.... very ugly
g_bShowBackground = True

g_backgroundTextureID = None
g_textureData = None
# g_textureImgOriginal = None  #Original Size

g_renderOutputSize = None  #(width, height) If not None, crop the output to this size
######################################################
#  Visualizeation Option

g_bShowFloor = True
g_bShowWiredMesh = False

g_bRotateView = False   #Rotate view 360 degrees
g_rotateView_counter = 0
g_rotateInterval = 2

g_bShowSkeleton = True
g_bShowMesh = True





########################################################
# 3D keypoints Visualization Setting
g_skeletons = None # list of np.array. skeNum x  (skelDim, skelFrames)
g_skeletons_GT = None
g_trajectory = None # list of np.array. skeNum x  (trajDim:3, skelFrames)
HOLDEN_DATA_SCALING = 5


g_faces = None #(faceNum, skelDim, skelFrames)
g_faceNormals = None
g_bodyNormals = None
g_hands = None #(handNum, skelDim, skelFrames)
g_hands_left = None
g_hands_right = None

g_posOnly = None

g_meshes = None

g_cameraPoses = None
g_cameraRots = None
g_ptCloud =None
g_ptCloudColor =None
g_ptSize = 2


g_frameLimit = -1
g_frameIdx = 0
g_lastframetime = g_currenttime = time.time()
g_fps = 0

g_speech = None # list of np.array. humanNum x  speechUnit, where elmenet is a dict with 'indicator', 'word', 'root' with a size of (1, skelFrames)
g_speechGT = None # list of np.array. humanNum x  speechUnit, , where elmenet is a dict with 'indicator', 'word', 'root' with a size of (1, skelFrames)

# Original
# g_colors = [ (0, 255, 127), (209, 206, 0), (0, 0, 128), (153, 50, 204), (60, 20, 220),
#     (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
#     (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]

# g_colors = [ (0, 255, 127), (170, 170, 0), (0, 0, 128), (153, 50, 204), (60, 20, 220),
#     (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
#     (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]

# g_colors = [ (250,0,0), (255,0, 0 ), (0, 255, 127), (209, 206, 0), (0, 0, 128), (153, 50, 204), (60, 20, 220),
#     (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
#     (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]


#GT visualization (by red)
g_colors = [ (255,0,0), (0, 255, 127), (170, 170, 0), (0, 0, 128), (153, 50, 204), (60, 20, 220),
    (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
    (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]

#Custom (non brl) originalPanoptic data
g_colors = [(0, 255, 127), (255,0,0), (170, 170, 0), (0, 0, 128), (153, 50, 204), (60, 20, 220),
    (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
    (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]


#RGB order!!
g_colors = [ (0,0,255), (255,0,0), (0, 255, 127), (170, 170, 0), (0, 0, 128), (153, 50, 204), (60, 20, 220),
    (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
    (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]


# g_colors = [(0, 255, 127), (255,0,0), (170, 170, 0)  , (0, 0, 128), (153, 50, 204), (60, 20, 220),
#      (0, 128, 0), (180, 130, 70), (147, 20, 255), (128, 128, 240), (154, 250, 0), (128, 0, 0),
#      (30, 105, 210), (0, 165, 255), (170, 178, 32), (238, 104, 123)]


import timeit



#######################################v
# Parametric Mesh Models
g_faceModel = None

########################################################3
# Opengl Setting
def init():
    #global width
    #global height

    glClearColor(1.0, 1.0, 1.0, 1.0)
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    #glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, g_ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, g_diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, g_specular)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, g_specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    # # #Mesh Rendering
    global g_vao
    global g_vertex_buffer
    global g_normal_buffer
    global g_tangent_buffer
    global g_index_buffer

    g_vao = glGenVertexArrays(1)
    # glBindVertexArray(g_vao)

    g_vertex_buffer = glGenBuffers(40)
    # #glBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer)

    g_normal_buffer = glGenBuffers(40)
    # #glBindBuffer(GL_ARRAY_BUFFER, g_normal_buffer)

    g_tangent_buffer = glGenBuffers(40)
    # #glBindBuffer(GL_ARRAY_BUFFER, g_tangent_buffer)

    g_index_buffer = glGenBuffers(40)
    # # #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, g_index_buffer)


    #Create Background Texture
    global g_backgroundTextureID
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)       #So that texture doesnt have to be power of 2
    g_backgroundTextureID = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, g_backgroundTextureID)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, 1920, 1080, 0, GL_RGB, GL_FLOAT, 0)
    #glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB, width, height, 0, GL_BGR, GL_UNSIGNED_BYTE, data);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # glEnable(GL_CULL_FACE)
    # glCullFace(GL_BACK)


def init_minimum():
    #global width
    #global height

    glClearColor(1.0, 1.0, 1.0, 1.0)
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, g_ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, g_diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, g_specular)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, g_specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)


"""Render text on bottom left corner"""
def RenderText(testStr):

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0.0, glutGet(GLUT_WINDOW_WIDTH), 0.0, glutGet(GLUT_WINDOW_HEIGHT))
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    # glRasterPos2i(10, 10)

    glPushMatrix()
    glColor4f(1,1,1,1)
    glClearDepth(1)
    if testStr is not None:
        glRasterPos2d(5,5)
        for c in testStr:
            #glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
    raster_pos = glGetIntegerv(GL_CURRENT_RASTER_POSITION)
    glPopMatrix()

    glClearDepth(0.99)
    glColor4f(.3,.3,.3,.8)
    glPushMatrix()
    glBegin(GL_QUADS)
    glVertex2i(0, 25)
    glVertex2i(raster_pos[0]+5, 25)
    glVertex2i(raster_pos[0]+5, 0)
    glVertex2i(0, 0)
    glEnd()
    glPopMatrix()
    glClearDepth(1)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()


def RenderDomeFloor():
    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_FILL)
    # glPolygonMode(GL_FRONT, GL_FILL)
    gridNum = 10
    width = 200
    halfWidth =width/2
    # g_floorCenter = np.array([0,0.5,0])

    # g_floorCenter = np.array([0,500,0])
    g_floorCenter = np.array([0,100,0])
    g_floorAxis1 = np.array([1,0,0])
    g_floorAxis2 = np.array([0,0,1])

    origin = g_floorCenter - g_floorAxis1*(width*gridNum/2 ) - g_floorAxis2*(width*gridNum/2)
    axis1 =  g_floorAxis1 * width
    axis2 =  g_floorAxis2 * width
    for y in range(gridNum+1):
        for x in range(gridNum+1):

            if (x+y) % 2 ==0:
                glColor(1.0,1.0,1.0,1.0) #white
            else:
                # glColor(0.95,0.95,0.95,0.3) #grey
                glColor(0.3,0.3,0.3,0.5) #grey

            p1 = origin + axis1*x + axis2*y
            p2 = p1+ axis1
            p3 = p1+ axis2
            p4 = p1+ axis1 + axis2


            glBegin(GL_QUADS)
            glVertex3f(   p1[0], p1[1], p1[2])
            glVertex3f(   p2[0], p2[1], p2[2])
            glVertex3f(   p4[0], p4[1], p4[2])
            glVertex3f(   p3[0], p3[1], p3[2])
            glEnd()


def setFree3DView():
    glTranslatef(0,0,g_zoom)

    glRotatef( -g_yRotate, 1.0, 0.0, 0.0)
    glRotatef( -g_xRotate, 0.0, 1.0, 0.0)

    glRotatef( g_zRotate, 0.0, 0.0, 1.0)
    glTranslatef( g_xTrans,  0.0, 0.0 )
    glTranslatef(  0.0, g_yTrans, 0.0)
    glTranslatef(  0.0, 0, g_zTrans)


# g_hdCams = None
# def load_panoptic_cameras():
#     global g_hdCams
#     with open('/media/posefs3b/Users/xiu/domedb/171204_pose3/calibration_171204_pose3.json') as f:
#         rawCalibs = json.load(f)
#     cameras = rawCalibs['cameras']
#     allPanel = map(lambda x:x['panel'],cameras)
#     hdCamIndices = [i for i,x in enumerate(allPanel) if x==0]
#     g_hdCams = [cameras[i] for i in hdCamIndices]

# def setPanopticCameraView(camid):
#     if g_hdCams==None:
#         load_cameras()

#     if camid>=len(g_hdCams):
#         camid = 0
#     cam = g_hdCams[camid]
#     invR = np.array(cam['R'])
#     invT = np.array(cam['t'])
#     camMatrix = np.hstack((invR, invT))
#     # denotes camera matrix, [R|t]
#     camMatrix = np.vstack((camMatrix, [0, 0, 0, 1]))
#     #camMatrix = numpy.linalg.inv(camMatrix)
#     K = np.array(cam['K'])
#     #K = K.flatten()
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     Kscale = 1920.0/g_Width
#     K = K/Kscale
#     ProjM = np.zeros((4,4))
#     ProjM[0,0] = 2*K[0,0]/g_Width
#     ProjM[0,2] = (g_Width - 2*K[0,2])/g_Width
#     ProjM[1,1] = 2*K[1,1]/g_Height
#     ProjM[1,2] = (-g_Height+2*K[1,2])/g_Height

#     ProjM[2,2] = (-g_farPlane-g_nearPlane)/(g_farPlane-g_nearPlane)
#     ProjM[2,3] = -2*g_farPlane*g_nearPlane/(g_farPlane-g_nearPlane)
#     ProjM[3,2] = -1

#     glLoadMatrixd(ProjM.T)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0)
#     glMultMatrixd(camMatrix.T)


# def load_MTC_default_camera():
#     global g_Width,  g_Height

#     camRender_width = 1920
#     camRender_height = 1080

#     g_Width = camRender_width
#     g_Height = camRender_height


# 3x3 intrinsic camera matrix
def setCamView_K(K):
    global g_camView_K
    g_camView_K = K


# 3x3 intrinsic camera matrix
# Set a default camera matrix used for MTC
def setCamView_K_DefaultForMTC():
    global g_camView_K

    K = np.array([[2000, 0, 960],[0, 2000, 540],[0,0,1]])       #MTC default camera. for 1920 x 1080 input image
    g_camView_K = K


#Show the world in a camera cooridnate (defined by K)
def setCameraView():

    # camRender_width = 1920
    # camRender_height = 1080

    # global g_Width,  g_Height
    # if camRender_width != g_Width or  camRender_height!=g_Height:
    #     g_Width = camRender_width
    #     g_Height = camRender_height
    #     #reshape(g_Width, g_Height)
    #     glutReshapeWindow(g_Width,g_Height)

    # invR = np.array(cam['R'])
    # invT = np.array(cam['t'])
    invR = np.eye(3)
    invT = np.zeros((3,1))
    # invT[2] = 400
    camMatrix = np.hstack((invR, invT))
    # denotes camera matrix, [R|t]
    camMatrix = np.vstack((camMatrix, [0, 0, 0, 1]))
    #camMatrix = numpy.linalg.inv(camMatrix)
    # K = np.array(cam['K'])
    # K = np.array(cam['K'])
    # K = np.array([[2000, 0, 960],[0, 2000, 540],[0,0,1]])       #MTC default camera
    # global g_camView_K
    # g_camView_K = K
    #K = K.flatten()

    if g_camView_K is None:
        print("## Warning: no K is set, so I use a default cam parameter defined for MTC")
        setCamView_K_DefaultForMTC()
    K = g_camView_K.copy()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Kscale = 1920.0/g_Width
    Kscale = 1.0 #1920.0/g_Width        :: why do we need this?
    K = K/Kscale
    ProjM = np.zeros((4,4))
    ProjM[0,0] = 2*K[0,0]/g_Width
    ProjM[0,2] = (g_Width - 2*K[0,2])/g_Width
    ProjM[1,1] = 2*K[1,1]/g_Height
    ProjM[1,2] = (-g_Height+2*K[1,2])/g_Height

    ProjM[2,2] = (-g_farPlane-g_nearPlane)/(g_farPlane-g_nearPlane)
    ProjM[2,3] = -2*g_farPlane*g_nearPlane/(g_farPlane-g_nearPlane)
    ProjM[3,2] = -1

    glLoadMatrixd(ProjM.T)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0)
    glMultMatrixd(camMatrix.T)


def SetOrthoCamera(bOrtho=True):
    global g_bOrthoCam
    g_bOrthoCam = bOrtho

#Show the world in a camera cooridnate (defined by K)
def setCameraViewOrth():

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    texHeight,texWidth =   g_textureData.shape[:2]
    # texHeight,texWidth =   1024, 1024
    texHeight*=0.5
    texWidth*=0.5
    # texHeight *=BACKGROUND_IMAGE_PLANE_DEPTH
    # texWidth *=BACKGROUND_IMAGE_PLANE_DEPTH

    glOrtho(-texWidth, texWidth, -texHeight, texHeight, -1500, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0)
    # glMultMatrixd(camMatrix.T)

def setRenderOutputSize(imWidth, imHeight):
    global g_renderOutputSize
    g_renderOutputSize = (imWidth, imHeight)

def setWindowSize(new_width, new_height):
    global g_Width, g_Height

    if new_height>1600:    #Max height of screen
        new_width = int(new_width *0.7)
        new_height = int(new_height *0.7)

    if new_width != g_Width or  new_height!=g_Height:
        g_Width = new_width
        g_Height =new_height
        #reshape(g_Width, g_Height)

        if g_bGlInitDone:
            glutReshapeWindow(g_Width,g_Height)
            

def reshape(width, height):
    #lightPos = (-50.0, 50.0, 100.0, 1.0)
    nRange = 250.0
    global g_Width, g_Height
    g_Width = width
    g_Height = height
    glViewport(0, 0, g_Width, g_Height)

    # # Set perspective (also zoom)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # #gluPerspective(zoom, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
    # gluPerspective(65, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
    # print("here: {}".format(float(g_Width)/float(g_Height)))


def SaveScenesToFile():
    #global g_Width, g_Height, g_bSaveToFile, g_fameIdx, g_hagglingSeqName
    # global g_bSaveToFile
    global g_saveFrameIdx

    glReadBuffer(GL_FRONT)
    img = glReadPixels(0, 0, g_Width, g_Height, GL_RGBA, GL_UNSIGNED_BYTE, outputType=None)
    img = Image.frombytes("RGBA", (g_Width, g_Height), img)
    img = ImageOps.flip(img)

    if False:
        pix = np.array(img)
        import viewer2D
        viewer2D.ImShow(pix)


    #Crop and keep the original size
    # if g_textureImgOriginal is not None and g_viewMode=='camView':
    #     width, height = img.size
    #     img = img.crop( (0,0,g_textureImgOriginal.shape[1], g_textureImgOriginal.shape[0]))     #top, left, bottom, right where origin seems top left

    if g_renderOutputSize is not None and g_viewMode=='camView':
        width, height = g_renderOutputSize
        img = img.crop( (0,0,width, height))     #top, left, bottom, right where origin seems top left


    #img.save('/ssd/render_general/frame_{}.png'.format(g_frameIdx), 'PNG')
    if g_saveFolderName is not None:
        folderPath = g_saveFolderName
    else:# g_haggling_render == False:
        # folderPath = '/home/hjoo//temp/render_general/'
        folderPath = '/home/hjoo//temp/render_general/'
    # else:
    #     if g_meshes == None and g_hagglingFileList == None: #Initial loading
    #         LoadHagglingData_Caller() #Load New Scene
    #     folderPath = '/hjoo/home/temp/render_mesh/' + g_hagglingSeqName
    #     if os.path.exists(folderPath) == False:
    #         os.mkdir(folderPath)

    if os.path.exists(folderPath) == False:
        os.mkdir(folderPath)
    # img.save('{0}/scene_{1:08d}.png'.format(folderPath,g_saveFrameIdx), 'PNG')
    img = img.convert("RGB")
    fileNameOut = '{0}/scene_{1:08d}.jpg'.format(folderPath,g_saveFrameIdx)
    img.save(fileNameOut, "JPEG")

    print(fileNameOut)

    #Done saving
    global g_bSaveToFile_done
    g_bSaveToFile_done = True
    g_saveFrameIdx+=1


    # global g_savedImg = img     #save rendered one into gobal variable

    # if g_frameIdx+1 >= g_frameLimit:
    #     if g_haggling_render == False:
    #         g_bSaveToFile = False
    #     else:
    #         bLoaded = LoadHagglingData_Caller() #Load New Scene
    #         if bLoaded ==False:
    #             g_bSaveToFile = False

        #cur_ind += 1
        #print(cur_ind)

    #glutPostRedisplay()


def SaveCamViewInfo():
    global g_Width, g_Height
    global g_nearPlane,g_farPlane
    global g_zoom,g_yRotate,g_xRotate, g_zRotate, g_xTrans, g_yTrans, g_zTrans

    fileName = '/ssd/camInfo/camInfo.pkl'
    if os.path.exists('/ssd/camInfo/') == False:
            os.mkdir('/ssd/camInfo/')

    if os.path.exists('/ssd/camInfo/archive/') == False:
        os.mkdir('/ssd/camInfo/archive/')

    if os.path.exists(fileName):
        #resave it
        for i in range(1000):
            newName = '/ssd/camInfo/archive/camInfo_old{}.pkl'.format(i)
            if os.path.exists(newName) == False:
                import shutil
                shutil.copy2(fileName,newName)
                break

    camInfo = dict()
    camInfo['g_Width'] = g_Width
    camInfo['g_Height']  =g_Height
    camInfo['g_nearPlane'] = g_nearPlane
    camInfo['g_farPlane'] = g_farPlane
    camInfo['g_zoom'] = g_zoom
    camInfo['g_yRotate'] = g_yRotate
    camInfo['g_xRotate'] =g_xRotate
    camInfo['g_zRotate'] = g_zRotate
    camInfo['g_xTrans'] = g_xTrans
    camInfo['g_yTrans'] = g_yTrans

    pickle.dump( camInfo, open(fileName, "wb" ) )

    print('camInfo')


def LoadCamViewInfo():
    global g_Width, g_Height
    global g_nearPlane,g_farPlane
    global g_zoom,g_yRotate,g_xRotate, g_zRotate, g_xTrans, g_yTrans
    global g_camView_fileName
    fileName = g_camView_fileName
    if not os.path.exists(fileName):
        print("No cam info: {}".format(fileName))
        return

    camInfo = pickle.load( open( fileName, "rb" ) , encoding='latin1')
    g_yTrans = camInfo['g_Width']
    g_Height = camInfo['g_Height']
    g_nearPlane = camInfo['g_nearPlane']
    g_farPlane = camInfo['g_farPlane']
    g_zoom = camInfo['g_zoom']
    g_yRotate = camInfo['g_yRotate']
    g_xRotate = camInfo['g_xRotate']
    g_zRotate = camInfo['g_zRotate']
    g_xTrans = camInfo['g_xTrans']
    g_yTrans= camInfo['g_yTrans']

    reshape(g_Width, g_Height)


def PuttingObjectCenter():
    global g_zoom, g_xTrans, g_yTrans, g_zTrans
    global g_xRotate, g_yRotate, g_zRotate
    if (g_skeletons is not None) and len(g_skeletons)>0:


        g_xRotate =0
        g_yRotate =0
        g_zRotate =0

        if g_skeletonType == 'smplcoco':
            g_xTrans = -(g_skeletons[0][9,0] + g_skeletons[0][12,0] )*0.5
            g_yTrans = -(g_skeletons[0][10,0] + g_skeletons[0][13,0] )*0.5
            g_zTrans = -(g_skeletons[0][11,0] + g_skeletons[0][14,0] )*0.5
            g_zoom = 300
        else: #Adam
            g_xTrans = -g_skeletons[0][0,0]
            g_yTrans = -g_skeletons[0][1,0]# 0#100
            g_zTrans = -g_skeletons[0][2,0]
            g_zoom = 300

    elif g_meshes is not None and len(g_meshes)>0:

        g_xRotate =0
        g_yRotate =0
        g_zRotate =0

        g_xTrans = -g_meshes[0]['ver'][0,1767,0]
        g_yTrans = -g_meshes[0]['ver'][0,1767,1]
        g_zTrans = -g_meshes[0]['ver'][0,1767,2]

        # print("{} {} {}".format(g_xTrans, g_yTrans, g_zTrans))
        g_zoom = 300


def keyboard(key, x, y):
    global g_stopMainLoop,g_frameIdx,g_show_fps
    global g_ptSize


    if isinstance(key, bytes):
        key = key.decode()  #Python3: b'X' -> 'X' (bytes -> str)
    if key == chr(27) or key == 'q':
        #sys.exit()
        g_stopMainLoop= True
        g_frameIdx = 0
        # glutIdleFunc(0); # Turn off Idle function if used.
        # glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE,GLUT_ACTION_CONTINUE_EXECUTION)
        # glutLeaveMainLoop()
        # glutDestroyWindow(g_winID) # Close open windows
    elif key == 'p':
        #global width, height
        glReadBuffer(GL_FRONT)
        img = glReadPixels(0, 0, g_Width, g_Height, GL_RGBA, GL_UNSIGNED_BYTE, outputType=None)
        img = Image.frombytes("RGBA", (g_Width, g_Height), img)
        img = ImageOps.flip(img)
        img.save('temp.jpg', 'JPG')

    elif key == 's':
        g_frameIdx = 0

    elif key == 't':
        global g_xRotate,g_yRotate,g_zRotate
        g_xRotate =0
        g_yRotate =-90
        g_zRotate =0
        print('showTopView')
    # elif key == 'r':
    #        global g_bSaveToFile
    #        g_frameIdx = 0
    #        g_bSaveToFile = True

    elif key == 'w':
        global g_bShowWiredMesh
        g_bShowWiredMesh = not g_bShowWiredMesh

    elif key == 'h':        #Load Next Haggling Data
            LoadHagglingData_Caller()
    elif key =='o':
        global g_bApplyRootOffset
        g_bApplyRootOffset = not g_bApplyRootOffset

    elif key =='f':
        global g_bShowFloor
        g_bShowFloor = not g_bShowFloor

    elif key =='V':
        SaveCamViewInfo()

    elif key =='v':
        LoadCamViewInfo()

    # elif key =='c':
    #     g_xRotate =0
    #     g_yRotate =0
    #     g_zRotate =180

    elif key =='c':     #put the target human in the center
       PuttingObjectCenter()
    elif key=='+':
        g_ptSize +=1
    elif key=='-':
        # global g_ptSize
        if g_ptSize >=2:
            g_ptSize -=1
    elif key =='R':     #rotate cameras
        global g_bRotateView, g_rotateView_counter

        g_bRotateView = not g_bRotateView
        g_rotateView_counter =0

    elif key =='j':  #Toggle joint
        global g_bShowSkeleton
        g_bShowSkeleton = not g_bShowSkeleton
    elif key =='m':
        global g_bShowMesh
        g_bShowMesh = not g_bShowMesh
    elif key =='b':
        global g_bShowBackground
        g_bShowBackground = not g_bShowBackground

    # elif key =='C':
    #     g_xRotate =0
    #     g_yRotate =0
    #     g_zRotate =0
    elif key == 'C':
        print('Toggle camview / freeview')
        global g_viewMode, g_nearPlane
        if g_viewMode=='free':
            g_viewMode = 'camView'
            g_nearPlane = 500          #cameramode
        else:
            g_viewMode ='free'
            g_nearPlane = 0.01        #original

    # elif key>='0' and key<='9':
    #     g_camid.popleft()
    #     g_camid.append(key)
    #     print('camView: CamID:{}'.format(g_camid))

    elif key =='0':
        glutReshapeWindow(1920,720)

    elif key =='z': # Toggle fps printing
        g_show_fps = not g_show_fps

    glutPostRedisplay()


def mouse(button, state, x, y):
    global g_action, g_xMousePtStart, g_yMousePtStart
    if (button==GLUT_LEFT_BUTTON):
        if (glutGetModifiers() == GLUT_ACTIVE_SHIFT):
            g_action = "TRANS"
        else:
            g_action = "MOVE_EYE"
    #elif (button==GLUT_MIDDLE_BUTTON):
    #    action = "TRANS"
    elif (button==GLUT_RIGHT_BUTTON):
        g_action = "ZOOM"
    g_xMousePtStart = x
    g_yMousePtStart = y

def motion(x, y):
    global g_zoom, g_xMousePtStart, g_yMousePtStart, g_xRotate, g_yRotate, g_zRotate, g_xTrans, g_zTrans
    if (g_action=="MOVE_EYE"):
        g_xRotate += x - g_xMousePtStart
        g_yRotate -= y - g_yMousePtStart
    elif (g_action=="MOVE_EYE_2"):
        g_zRotate += y - g_yMousePtStart
    elif (g_action=="TRANS"):
        g_xTrans += x - g_xMousePtStart
        g_zTrans += y - g_yMousePtStart
    elif (g_action=="ZOOM"):
        g_zoom -= y - g_yMousePtStart
        # print(g_zoom)
    else:
        print("unknown action\n", g_action)
    g_xMousePtStart = x
    g_yMousePtStart = y

    print ('xTrans {},  yTrans {}, zoom {} xRotate{} yRotate {} zRotate {}'.format(g_xTrans,  g_yTrans,  g_zoom,  g_xRotate,  g_yRotate,  g_zRotate))
    glutPostRedisplay()

def setBackgroundTexture(img):
    global g_textureData#, g_textureImgOriginal
    g_textureData = img

    #In MTC, the background should be always 1920x1080
    # g_textureData = np.ones( (1080, 1920, 3), dtype=img.dtype)*0     #dtype==np.unit8
    # g_textureData[:img.shape[0],:img.shape[1] ] = img
    # g_textureImgOriginal = img  #keep the original image


    # import cv2
    # cv2.imshow('here??',img)
    # cv2.waitKey(0)

def SetCameraPoses(camRots, camPoses):
    global g_cameraPoses,g_cameraRots
    
    g_cameraPoses = camPoses
    g_cameraRots = camRots


""" ptCloud: N,3 """
def SetPtCloud(ptCloud, ptCloudColor = None):
    global g_ptCloud, g_ptCloudColor
    g_ptCloud = ptCloud
    g_ptCloudColor = ptCloudColor

def DrawBackgroundOrth():

    if g_textureData is None:
        return

    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)

    # glUseProgram(0)

    glBindTexture(GL_TEXTURE_2D, g_backgroundTextureID)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1920, 1080, 0, GL_RGB, GL_UNSIGNED_BYTE, g_textureData)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 480, 640, 0, GL_RGB, GL_UNSIGNED_BYTE, g_textureData.data)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, g_textureData.shape[1], g_textureData.shape[0], 0, GL_BGR, GL_UNSIGNED_BYTE, g_textureData.data)
    texHeight,texWidth =   g_textureData.shape[:2]
    texHeight*=0.5
    texWidth*=0.5

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    # d = BACKGROUND_IMAGE_PLANE_DEPTH
    d = 10

    glTexCoord2f(0, 0)
    # #Eigen::Map<Eigen::Matrix<double, 3, 3, Eigen::RowMajor>> K(m_options.m_pK);
    P = np.array([-texWidth, -texHeight, d])
    # P = np.matmul(K_inv,P)
    # P = P / P[2]
    glVertex3f(P[0] , P[1] , P[2] );  # K^{-1} [0, 0, 1]^T

    glTexCoord2f(1, 0)
    # P = [1920, 0, 1]
    P = [texWidth, -texHeight, d]
    glVertex3f(P[0] , P[1] , P[2] );  # K^{-1} [0, 0, 1]^T

    glTexCoord2f(1, 1)
    # P = [1920, 1080, 1]
    P = [texWidth, texHeight, d]
    # P = np.matmul(K_inv,P)
    # P = P / P[2]
    # glVertex3f(P[0] * d, P[1] * d, P[2] * d)
    glVertex3f(P[0] , P[1] , P[2] );  # K^{-1} [0, 0, 1]^T

    glTexCoord2f(0, 1)
    # P = [0, 1080, 1]
    P = [-texWidth, texHeight, d]
    # glVertex3f(P[0] * d, P[1] * d, P[2] * d)
    glVertex3f(P[0] , P[1] , P[2] );  # K^{-1} [0, 0, 1]^T
    glEnd()

    glEnable(GL_LIGHTING)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)



def DrawBackground():

    if g_camView_K is None or g_textureData is None:
        return

    K_inv = np.linalg.inv(g_camView_K)

    glDisable(GL_CULL_FACE)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)

    # glUseProgram(0)

    glBindTexture(GL_TEXTURE_2D, g_backgroundTextureID)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1920, 1080, 0, GL_RGB, GL_UNSIGNED_BYTE, g_textureData)
    # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 480, 640, 0, GL_RGB, GL_UNSIGNED_BYTE, g_textureData.data)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, g_textureData.shape[1], g_textureData.shape[0], 0, GL_BGR, GL_UNSIGNED_BYTE, g_textureData.data)
    texHeight,texWidth =   g_textureData.shape[:2]

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    d = BACKGROUND_IMAGE_PLANE_DEPTH

    glTexCoord2f(0, 0)
    # #Eigen::Map<Eigen::Matrix<double, 3, 3, Eigen::RowMajor>> K(m_options.m_pK);
    P = np.array([0, 0, 1])
    P = np.matmul(K_inv,P)
    P = P / P[2]
    glVertex3f(P[0] * d, P[1] * d, P[2] * d);  # K^{-1} [0, 0, 1]^T

    glTexCoord2f(1, 0)
    # P = [1920, 0, 1]
    P = [texWidth, 0, 1]

    P = np.matmul(K_inv,P)
    P = P / P[2]
    glVertex3f(P[0] * d, P[1] * d, P[2] * d);  # K^{-1} [0, 0, 1]^T

    glTexCoord2f(1, 1)
    # P = [1920, 1080, 1]
    P = [texWidth, texHeight, 1]
    P = np.matmul(K_inv,P)
    P = P / P[2]
    glVertex3f(P[0] * d, P[1] * d, P[2] * d)

    glTexCoord2f(0, 1)
    # P = [0, 1080, 1]
    P = [0, texHeight, 1]
    P = np.matmul(K_inv,P)
    P = P / P[2]
    glVertex3f(P[0] * d, P[1] * d, P[2] * d)
    glEnd()

    glEnable(GL_LIGHTING)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)


def specialkeys(key, x, y):
    global g_xrot
    global g_yrot
    global g_cur_ind
    if key == GLUT_KEY_UP:
        g_xrot -= 2.0
    if key == GLUT_KEY_DOWN:
        g_xrot += 2.0
    # if key == GLUT_KEY_LEFT:
    #     cur_ind -=1
    # if key == GLUT_KEY_RIGHT:
    #     cur_ind +=1
    glutPostRedisplay()

from multiprocessing import Pool

def init_gl_util():
    global g_bGlInitDone, g_lastframetime, g_currenttime, g_fps

    g_lastframetime = g_currenttime
    g_currenttime = time.time()
    refresh_fps = 0.15
    g_fps = (1-refresh_fps)*g_fps + refresh_fps*1/(g_currenttime-g_lastframetime)

    if g_bGlInitDone==False:
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE) #GLUT_MULTISAMPLE is required for anti-aliasing
        #glutInitDisplayMode(GLUT_RGB |GLUT_DOUBLE|GLUT_DEPTH)
        glutInitWindowPosition(100,100)
        glutInitWindowSize(g_Width,g_Height)

        global g_winID
        g_winID = glutCreateWindow("Visualize human skeleton")
        init()
        # init_minimum()
        glutReshapeFunc(reshape)
        glutDisplayFunc(renderscene)
        glutKeyboardFunc(keyboard)
        glutMouseFunc(mouse)
        glutMotionFunc(motion)
        glutSpecialFunc(specialkeys)
        # glutIdleFunc(idlefunc)
        glutIdleFunc(renderscene)

        #Ver 1: Infinite loop (termination is not possible)
        #glutMainLoop()

        #Ver 2: for better termination (by pressing 'q')
        g_bGlInitDone = True
    else:
        glutReshapeWindow(g_Width, g_Height)     #Just doing resize
        # glutReshapeWindow(int(g_Width*0.5), int(g_Height*0.5))     #Just doing resize


def init_gl(maxIter=-10):
    # Init_Haggling()
    # global width
    # global height
    # Setup for double-buffered display and depth testing
    init_gl_util()

    global g_stopMainLoop
    g_stopMainLoop=False
    while True:
        glutPostRedisplay()
        if bool(glutMainLoopEvent)==False:
            continue
        glutMainLoopEvent()
        if g_stopMainLoop:
            break
        if maxIter>0:
            maxIter -=1
            if maxIter<=0:
                g_stopMainLoop = True

    # print("Escaped glut loop")


#g_faces should be: #(faceNum, faceDim, faceFrames)
def DrawFaces():
    #global g_colors
    #global g_faces, g_faceNormals, g_frameIdx#, g_normals

    if g_faces is None:
        return

    #g_frameLimit = g_faces.shape[2]

    for humanIdx in range(len(g_faces)):

        if(g_frameIdx >= g_faces[humanIdx].shape[1]):
            continue

        if g_onlyDrawHumanIdx>=0 and humanIdx!=g_onlyDrawHumanIdx:
            continue

        face3D = g_faces[humanIdx][:, g_frameIdx]  #210x1
        drawface_70(face3D, g_colors[humanIdx % len(g_colors)])

        if g_faceNormals is not None and len(g_faceNormals)> humanIdx:

            if g_faceNormals[humanIdx].shape[1]<=g_frameIdx:
                print("Warning: g_faceNormals[humanIdx].shape[2]<=g_frameId")
                continue

            normal3D = g_faceNormals[humanIdx][:,g_frameIdx]  #3x1
            #drawfaceNormal_70(normal3D, face3D, g_colors[humanIdx % len(g_colors)])
            #drawfaceNormal_70(normal3D, face3D, [0, 255, 255])
            eyeCenterPoint = 0.5 *(face3D[(45*3):(45*3+3)] + face3D[(36*3):(36*3+3)])
            #drawNormal(normal3D, eyeCenterPoint, [0, 255, 0],normalLength=25)
            drawNormal(normal3D, eyeCenterPoint, [0, 255, 255],normalLength=25)

        #drawbody_joint_ptOnly(face3D, g_colors[humanIdx])
    #g_frameIdx +=1

    #if g_frameIdx>=g_frameLimit:
    #    g_frameIdx =0


#g_faces should be: #(faceNum, faceDim, faceFrames)
def DrawHands():
    #global g_colors
    #global g_hands_left,g_hands_right, g_frameIdx#, g_normals


    #g_frameLimit = g_faces.shape[2]

    if g_hands_left is not None:
        for humanIdx in range(len(g_hands_left)):
            if g_onlyDrawHumanIdx>=0 and humanIdx!=g_onlyDrawHumanIdx:
               continue

            if(g_frameIdx >= g_hands_left[humanIdx].shape[1]):
                continue

            hand3D = g_hands_left[humanIdx][:, g_frameIdx]  #210x1
            drawhand_21(hand3D, g_colors[humanIdx % len(g_colors)])
            #drawbody_joint_ptOnly(face3D, g_colors[humanIdx])

    if g_hands_right is not None:
        for humanIdx in range(len(g_hands_right)):
            if g_onlyDrawHumanIdx>=0 and humanIdx!=g_onlyDrawHumanIdx:
               continue

            if(g_frameIdx >= g_hands_right[humanIdx].shape[1]):
                continue

            hand3D = g_hands_right[humanIdx][:, g_frameIdx]  #210x1
            drawhand_21(hand3D, g_colors[humanIdx % len(g_colors)])
            #drawbody_joint_ptOnly(face3D, g_colors[humanIdx])

    #g_frameIdx +=1

    #if g_frameIdx>=g_frameLimit:
    #    g_frameIdx =0


# Face keypoint orders follow Openpose keypoint output
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md
# Face outline points (0-16) are unstable
face_edges = np.array([ #[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10],[11,12],[12,13],[14,15],[15,16], #outline (ignored)
                [17,18],[18,19],[19,20],[20,21], #right eyebrow
                [22,23],[23,24],[24,25],[25,26], #left eyebrow
                [27,28],[28,29],[29,30],   #nose upper part
                [31,32],[32,33],[33,34],[34,35], #nose lower part
                [36,37],[37,38],[38,39],[39,40],[40,41],[41,36], #right eye
                [42,43],[43,44],[44,45],[45,46],[46,47],[47,42], #left eye
                [48,49],[49,50],[50,51],[51,52],[52,53],[53,54],[54,55],[55,56],[56,57],[57,58],[58,59],[59,48], #Lip outline
                [60,61],[61,62],[62,63],[63,64],[64,65],[65,66],[66,67],[67,60] #Lip inner line
                ])
#joints70: 3x70 =210 dim
def drawface_70(joints,  color):

    glLineWidth(2.0)
    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    #for i in range(len(joints)/3):
    #    glPushMatrix()
    #    glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
    #    glutSolidSphere(0.5, 10, 10)
    #    glPopMatrix()

    # connMat_coco19 = g_connMat_smc19
    #Visualize Bones
    for conn in face_edges:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]

        x1 = joints[3*conn[1]]
        y1 = joints[3*conn[1]+1]
        z1 = joints[3*conn[1]+2]

        glBegin(GL_LINES)
        glVertex3f(x0, y0, z0)
        glVertex3f(x1,y1,z1)
        glEnd()


# g_meshColor = (0.4, 0.4, 0.7) #Blue Default (R,G,B)
g_meshColor = (0.53, 0.53, 0.8)   #prediction: blue
def SetMeshColor(colorName='blue'):
    global g_meshColor
    if colorName=='blue':
        # g_meshColor = (0.4, 0.4, 0.)   #prediction: blue
        g_meshColor = (0.53, 0.53, 0.8)   #prediction: blue
        # glColor3f(0.53, 0.53, 0.8)
    elif colorName=='red':
        g_meshColor = (0.7, 0.5, 0.5)   #targer: red
    else:
        assert False


g_firsttime = True
""" With normal"""
def DrawMeshes():

    global g_colors, g_firsttime
    global g_meshes, g_frameIdx#, g_normals

    global g_vao
    global g_vertex_buffer
    global g_normal_buffer
    global g_tangent_buffer
    global g_index_buffer

    # MESH_SCALING = 100.0  #from meter (model def) to CM (panoptic def)
    # MESH_SCALING = 1.0  #from meter (model def) to CM (panoptic def)

    if g_meshes is None:
        return

    #g_meshes[humanIdx]['ver']: frames x 6890 x 3
    for humanIdx in range(len(g_meshes)):

        if(g_frameIdx >= g_meshes[humanIdx]['ver'].shape[0]):
            continue

        # if(humanIdx==0 or humanIdx==1):       #Debug
        #     continue

        SMPL_vts = g_meshes[humanIdx]['ver'][g_frameIdx,:,: ]  #6890x3
        SMPL_inds = g_meshes[humanIdx]['f']
        SMPL_vts = SMPL_vts.flatten() #* MESH_SCALING
        SMPL_vts = SMPL_vts.astype(np.float32)
        SMPL_inds = SMPL_inds.flatten()
        vts_num = int(len(SMPL_vts) / 3)
        face_num = int(len(SMPL_inds) / 3)

        if 'normal' in g_meshes[humanIdx].keys() and g_meshes[humanIdx]['normal'] is None:
            here=0
        if 'normal' in g_meshes[humanIdx].keys() and len(g_meshes[humanIdx]['normal'])>0:
            SMPL_normals = g_meshes[humanIdx]['normal'][g_frameIdx,:,: ]
            SMPL_normals = SMPL_normals.flatten().astype(np.float32)
            tangent = np.zeros(SMPL_normals.shape)
            tangent.astype(np.float32)
            normal_num = len(SMPL_normals) / 3
        else :
            SMPL_normals = None

        #Vertex Array
        glBindVertexArray(g_vao)

        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, g_vertex_buffer[humanIdx])
        glBufferData(GL_ARRAY_BUFFER, len(SMPL_vts) * sizeof(ctypes.c_float), (ctypes.c_float * len(SMPL_vts))(*SMPL_vts), GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        if SMPL_normals is not None:
            #this is not needed.. .but normal should be the third attribute...
            if True:#g_firsttime:
                glEnableVertexAttribArray(1)
                glBindBuffer(GL_ARRAY_BUFFER, g_tangent_buffer[humanIdx])
                glBufferData(GL_ARRAY_BUFFER, len(tangent) * sizeof(ctypes.c_float), (ctypes.c_float * len(tangent))(*tangent), GL_STATIC_DRAW)
                glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

            glEnableVertexAttribArray(2)
            glBindBuffer(GL_ARRAY_BUFFER, g_normal_buffer[humanIdx])
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
            #glBufferData(GL_ARRAY_BUFFER, len(SMPL_normals) * sizeof(ctypes.c_float), (ctypes.c_float * len(SMPL_normals))(*SMPL_normals), GL_STATIC_DRAW)
            #glBufferData(GL_ARRAY_BUFFER, len(SMPL_normals) * sizeof(ctypes.c_float), (ctypes.c_float * len(SMPL_normals))(*SMPL_normals), GL_STATIC_DRAW)
            glBufferData(GL_ARRAY_BUFFER,
                            len(SMPL_normals) * sizeof(ctypes.c_float),
                            SMPL_normals,
                            GL_STATIC_DRAW)

        if True:#g_firsttime:
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, g_index_buffer[humanIdx])
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(ctypes.c_uint) * len(SMPL_inds), (ctypes.c_uint * len(SMPL_inds))(*SMPL_inds), GL_STATIC_DRAW)

        g_firsttime = False
        # set the dimensions of the position attribute, so it consumes 2 floats at a time (default is 4)

        #Draw by vertex array
        glPushMatrix()

        # if humanIdx ==0:
        #     #glColor3f(0.5, 0.2, 0.2)   #targer: red
        #     glColor3f(0.4, 0.4, 0.7)   #prediction: blue
        # elif humanIdx ==1:
        #     glColor3f(0.5, 0.2, 0.2)   #targer: red
        #     #glColor3f(0.0, 0.8, 0.3)   #buyer
        # elif humanIdx ==2:
        #     glColor3f(0.0, 0.8, 0.3)   #buyer
        #     #glColor3f(0.5, 0.5, 0)   #another: yellow
        # else:
        # #elif humanIdx ==2:
        #     glColor3f(0.5, 0.5, 0)   #another: yellow
        # glColor3f(0.6, 0.6, 0.4)   #another: yellow

        if False:#humanIdx ==1:        #Second one red
            glColor3f(0.5, 0.2, 0.2)   #targer: red
            # glColor3f(0.4, 0.4, 0.7)   #prediction: blue
        else:
        #     glColor3f(0.4, 0.4, 0.7)   #prediction: blue
            glColor3f(g_meshColor[0],g_meshColor[1],g_meshColor[2])
            # glColor3f(0.53, 0.53, 0.8)
        # glColor3f(g_meshColor[0],g_meshColor[1],g_meshColor[2])

        #glColor3f(0.8, 0.8, 0.8)
        glLineWidth(.5)

        if SMPL_normals is not None and g_bShowWiredMesh==False:
            glPolygonMode(GL_FRONT, GL_FILL)
            glPolygonMode(GL_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT, GL_LINE)
            glPolygonMode(GL_BACK, GL_LINE)
        # for vao_object in g_vao_object_list:
        #     glBindVertexArray(vao_object)
        #     glDrawElements(GL_TRIANGLES, face_num * 3, GL_UNSIGNED_INT, None)
        if g_bApplyRootOffset:
            #glTranslatef(40*humanIdx,0,0)
            glTranslatef(ROOT_OFFSET_DIST*humanIdx,0,0)

        glDrawElements(GL_TRIANGLES, face_num * 3, GL_UNSIGNED_INT, None)
        # glPolygonMode(GL_FRONT, GL_FILL)
        # glPolygonMode(GL_BACK, GL_FILL)
        glPopMatrix()

        glDisableVertexAttribArray(0)

        if SMPL_normals is not None:
            glDisableVertexAttribArray(1)
            glDisableVertexAttribArray(2)

    g_firsttime = False
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)    #Unbind


#normal3D: 3 dim
#rootPt: 3x1
def drawNormal(normal3D, rootPt,  color, normalLength=40):

    glLineWidth(2.0)
    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])

    #neckPoint = joints[(0*3):(0*3+3)]
    normalEndPoint = rootPt+ normal3D * normalLength

    glBegin(GL_LINES)
    glVertex3f(rootPt[0], rootPt[1], rootPt[2])
    glVertex3f(normalEndPoint[0], normalEndPoint[1], normalEndPoint[2])
    glEnd()

    glPushMatrix()
    glTranslate(normalEndPoint[0], normalEndPoint[1], normalEndPoint[2])
    glutSolidSphere(1, 10, 10)
    glPopMatrix()


g_connMat_hand21 = [ [0,1], [1,2], [2,3], [3,4],
                     [0,5], [5,6], [6,7], [7,8],
                     [0,9], [9,10], [10,11],[11,12],
                     [0,13], [13,14], [14, 15], [15, 16],
                     [0, 17], [17, 18], [18, 19], [19, 20]]
g_connMat_hand21 = np.array(g_connMat_hand21, dtype=int)
#joints70: 3x70 =210 dim
def drawhand_21(joints,  color, normal=None):

    # #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    # for i in range(len(joints)/3):

    #     glPushMatrix()
    #     glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
    #     glutSolidSphere(1, 10, 10)
    #     glPopMatrix()

    connMat_coco19 = g_connMat_hand21
    #Visualize Bones
    for conn in connMat_coco19:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]]
        y1 = joints[3*conn[1]+1]
        z1 = joints[3*conn[1]+2]


        if (x0==0) or (x1==0):
            continue

        x1 -= x0
        y1 -= y0
        z1 -= z0

        if abs(x1) >20 or abs(y1)>20 or abs(z1)>20:
            continue

        if g_bSimpleHead and conn[0] == 0 and conn[1]==1:
            x1 = x1*0.5
            y1 = y1*0.5
            z1 = z1*0.5

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(0.5, length, 10, 10)
        glPopMatrix()


# draw human location only
def DrawPosOnly():
    global g_colors
    global g_frameIdx#, g_normals
    global g_speech,g_speechGT
    global g_bApplyRootOffset

    global g_posOnly
    global g_bodyNormals, g_faceNormals

    #print(g_frameIdx)
    if g_posOnly is None:
        return

    for humanIdx in range(len(g_posOnly)):

        if(g_frameIdx >= g_posOnly[humanIdx].shape[1]):
            continue

        # if(humanIdx==1):
        #     continue


        skel = g_posOnly[humanIdx][:, g_frameIdx]
        # normal = g_normals[skelIdx, :, g_idx]
        color = g_colors[humanIdx % len(g_colors)]
        glColor3ub(color[0], color[1], color[2])


        glPushMatrix()
        glTranslate(skel[0], skel[1], skel[2])

        if humanIdx==0:#or humanIdx==1:
            glutSolidCube(10)
        elif False:#humanIdx==1:#or humanIdx==1:
            glutWireSphere(10,10,10)
        else:
            glutSolidSphere(10,10,10)
        glPopMatrix()

        #Draw body normal
        if g_bodyNormals is not None and len(g_bodyNormals)> humanIdx:

            if g_bodyNormals[humanIdx].shape[1]>g_frameIdx:
                normal3D = g_bodyNormals[humanIdx][:,g_frameIdx]  #3x1
                #drawbodyNormal(normal3D, skel, [255, 0, 0])
                drawNormal(normal3D, skel, [255, 0, 0])


        #Draw face normal
        if g_faceNormals is not None and len(g_faceNormals)> humanIdx:

            if g_faceNormals[humanIdx].shape[1]>g_frameIdx:
                normal3D = g_faceNormals[humanIdx][:,g_frameIdx]  #3x1
                drawNormal(normal3D, skel, [0, 255, 0], normalLength = 30)


        #Draw Speaking Info
        if g_speech is not None and g_skeletons is None:    #If g_skeletons is valid, draw speech there
            if len(g_speech[humanIdx]['indicator'])>g_frameIdx:
                draw_speaking_general(skel, g_speech[humanIdx]['indicator'][g_frameIdx], g_speech[humanIdx]['word'][g_frameIdx],  g_colors[humanIdx % len(g_colors)], offset=[0,0,23])





#g_trajectory: a list of np.array. skeNum x  (trajDim:3, frames)
def DrawTrajectory():
    global g_colors
    global g_trajectory, g_frameIdx#, g_normals


    if g_trajectory is None:
        return

    for humanIdx in range(len(g_trajectory)):

        if(g_frameIdx >= g_trajectory[humanIdx].shape[1]):
            continue

        color = g_colors[humanIdx % len(g_colors)]

        glLineWidth(2.0)

        #Visualize Joints
        glColor3ub(color[0], color[1], color[2])

        glPushMatrix()
        if g_bApplyRootOffset:
            #glTranslatef(40*humanIdx,0,0)
            glTranslatef(ROOT_OFFSET_DIST*humanIdx,0,0)

        #Visualize All Trajctory locations
        #interval=10
        for idx in range(0,g_trajectory[humanIdx].shape[1]-interval, interval):

            # root location
            x0 = g_trajectory[humanIdx][0,idx]
            y0 = g_trajectory[humanIdx][1,idx]
            z0 = g_trajectory[humanIdx][2,idx]

            x1 = g_trajectory[humanIdx][0,idx+interval]
            y1 = g_trajectory[humanIdx][1,idx+interval]
            z1 = g_trajectory[humanIdx][2,idx+interval]

            glBegin(GL_LINES)
            glVertex3f(x0, y0, z0)
            glVertex3f(x1,y1,z1)
            glEnd()

        """
        #Visualize current location and normal dirctio
        # x0, y0, z0 for the root location
        x0 = g_trajectory[humanIdx][0,g_frameIdx]
        y0 = g_trajectory[humanIdx][1,g_frameIdx]
        z0 = g_trajectory[humanIdx][2,g_frameIdx]

        x1 = g_trajectory[humanIdx][3,g_frameIdx]
        y1 = g_trajectory[humanIdx][4,g_frameIdx]
        z1 = g_trajectory[humanIdx][5,g_frameIdx]

        glBegin(GL_LINES)
        glVertex3f(x0, y0, z0)
        glVertex3f(x1,y1,z1)
        glEnd()
        """

        glPopMatrix()
        # drawface_70(face3D, g_colors[humanIdx % len(g_colors)])

        # if g_faceNormals is not None and len(g_faceNormals)> humanIdx:

        #     if g_faceNormals[humanIdx].shape[1]<=g_frameIdx:
        #         print("Warning: g_faceNormals[humanIdx].shape[2]<=g_frameId")
        #         continue

        #     normal3D = g_faceNormals[humanIdx][:,g_frameIdx]  #3x1
        #     #drawfaceNormal_70(normal3D, face3D, g_colors[humanIdx % len(g_colors)])
        #     #drawfaceNormal_70(normal3D, face3D, [0, 255, 255])
        #     eyeCenterPoint = 0.5 *(face3D[(45*3):(45*3+3)] + face3D[(36*3):(36*3+3)])
        #     drawNormal(normal3D, eyeCenterPoint, [0, 255, 255])


#g_skeletons should be: #(skeNum, skelDim, skelFrames)
def DrawSkeletons():
    global g_colors
    global g_skeletons, g_frameIdx#, g_normals
    global g_speech,g_speechGT
    global g_bApplyRootOffset
    global g_bodyNormals
    #print(g_frameIdx)
    if g_skeletons is None:
        return

    #frameLimit = g_skeletons.shape[2]
    #frameLens = [l.shape[1] for l in g_skeletons]
    #g_frameLimit = min(frameLens)

    #for humanIdx in range(g_skeletons.shape[0]):
    for humanIdx in range(len(g_skeletons)):

        if g_onlyDrawHumanIdx>=0 and humanIdx!=g_onlyDrawHumanIdx:
            continue
        # if skelIdx ==0:
        #     # if g_idx+time_offset>=g_skeletons.shape[2]:
        #     #     continue
        #     skel = g_skeletons[skelIdx, :, g_idx+time_offset]
        #     # normal = g_normals[skelIdx, :, g_idx+time_offset]
        # else:
        #skel = g_skeletons[humanIdx, :, g_frameIdx]
        if(g_frameIdx >= g_skeletons[humanIdx].shape[1]):
            continue

        # if(humanIdx==0 or humanIdx==1):
        #     continue

        skel = g_skeletons[humanIdx][:, g_frameIdx]
        # normal = g_normals[skelIdx, :, g_idx]

        if g_bApplyRootOffset:
            skel = skel.copy()
            #skel[0::3] = skel[0::3]+ 70 *humanIdx
            skel[0::3] = skel[0::3]+ ROOT_OFFSET_DIST *humanIdx

        # if skel.shape[0]==42: #Coco19's first 14 (LSP 14?) in HMR
        #     drawbody_joint14(skel, g_colors[humanIdx % len(g_colors)])
        if skel.shape[0]==78:       #SMPlCOCO19 + headtop (19) + (leftFoot --toe20 pink21 heel22) + (rightFoot--toe23-pink24-heel25)
            drawbody_SMPLCOCO_TotalCap26(skel, [0,255,0])
        elif skel.shape[0]==57:
            if g_skeletonType is not None and g_skeletonType=='smplcoco':
                drawbody_SMPLCOCO19(skel, g_colors[humanIdx % len(g_colors)])   #from HMR, SMPL->COCO19 regression. Same as MTC20's first 19.
            else:
                drawbody_SMC19(skel, g_colors[humanIdx % len(g_colors)]) #Panoptic Studio (SMC19) with 19 joints. Note SMC21 includes headtop
        elif g_skeletonType=='spin' and skel.shape[0]==72: #SPIN 24 (without openpose, 24 superset)
            drawbody_jointSpin24(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==42: #LSP14joints also used in HMR
            drawbody_LSP14(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==51: #simpler human36m (17joints)
            drawbody_joint17_human36m(skel, [0,255,0])#g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==72: #SMPL LBS skeleton
            drawbody_joint24_smplLBS(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==96: #human36m (32joints)
            drawbody_joint32_human36m(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==66: #Holden's converted form (21joints)
            drawbody_joint22(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==93: #CMU Mocap Raw data (31joints)
            drawbody_joint31(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==186: #Adam model (62 joints: 22 for body 20x2 for fingers)
            drawbody_jointAdam(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==147: #SPIN 49 (25 openpose +  24 superset)
            drawbody_jointSpin49(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==249: #FRL Pitts social mocap seuqence with fingers
            drawbody_FRLSocialmocap(skel, g_colors[humanIdx % len(g_colors)])


        else:
            drawbody_joint_ptOnly(skel, g_colors[humanIdx % len(g_colors)])



        if g_bodyNormals is not None and len(g_bodyNormals)> humanIdx:

            if g_bodyNormals[humanIdx].shape[1]<=g_frameIdx:
                print("Warning: g_bodyNormals[humanIdx].shape[2]<=g_frameId")
                continue

            normal3D = g_bodyNormals[humanIdx][:,g_frameIdx]  #3x1
            #drawbodyNormal(normal3D, skel, [255, 0, 0])
            rootPt = skel[(0*3):(0*3+3)]

            if skel.shape[0]==66:
                i=12
                rootPt = skel[(3*i):(3*i+3)]
            # drawNormal(normal3D, rootPt, [0, 255, 255])
            #drawNormal(normal3D, rootPt, [255, 0, 0])

            # if g_onlyDrawHumanIdx>=0 and humanIdx!=g_onlyDrawHumanIdx:
            drawNormal(normal3D, rootPt, [0, 255, 0])

        # if g_faceNormals is not None and len(g_faceNormals)> humanIdx:

        #     if g_faceNormals[humanIdx].shape[1]<=g_frameIdx:
        #         print("Warning: g_bodyNormals[humanIdx].shape[2]<=g_frameId")
        #         continue

        #     normal3D = g_faceNormals[humanIdx][:,g_frameIdx]  #3x1
        #     #drawbodyNormal(normal3D, skel, [255, 0, 0])
        #     rootPt = skel[(0*3):(0*3+3)]

        #     if skel.shape[0]==66:
        #         i=13
        #         rootPt = skel[(3*i):(3*i+3)]
        #     # drawNormal(normal3D, rootPt, [0, 255, 255])
        #     drawNormal(normal3D, rootPt, [0, 255, 0])

        #Draw Speeking Annotation
        if skel.shape[0]==57 and g_speech is not None: #Coco19
            if(g_frameIdx < len(g_speech[humanIdx]['word'])):
                #draw_speaking_joint19(skel, g_speech[humanIdx]['indicator'][g_frameIdx], g_speech[humanIdx]['word'][g_frameIdx],  g_colors[humanIdx % len(g_colors)])
                draw_speaking_joint19(skel, g_speech[humanIdx]['indicator'][g_frameIdx], None,  g_colors[humanIdx % len(g_colors)])

        if skel.shape[0]==66 and g_speech is not None: #Holden's
            if(len(g_speech)> humanIdx and  g_frameIdx < len(g_speech[humanIdx]['word'])):
                #draw_speaking_joint22(skel, g_speech[humanIdx][g_frameIdx],None,  g_colors[humanIdx % len(g_colors)])
                i=13
                facePt = skel[(3*i):(3*i+3)]
                draw_speaking_general(facePt, g_speech[humanIdx]['indicator'][g_frameIdx], g_speech[humanIdx]['word'][g_frameIdx],  [0, 0, 255], offset=[0,-43,0])

        if skel.shape[0]==66 and g_speechGT is not None: #Holden's
            if(g_frameIdx < len(g_speechGT[humanIdx]['word'])):
                #draw_speaking_joint22(skel, g_speechGT[humanIdx][g_frameIdx],"GT: Speaking", [255, 0, 0], 40)
                i=13
                facePt = skel[(3*i):(3*i+3)]
                draw_speaking_general(facePt, g_speechGT[humanIdx]['indicator'][g_frameIdx], g_speechGT[humanIdx]['word'][g_frameIdx],  g_colors[humanIdx % len(g_colors)], offset=[0,-33,0])




#g_skeletons should be: #(skeNum, skelDim, skelFrames)
def DrawSkeletonsGT():
    global g_colors
    global g_skeletons_GT, g_frameIdx#, g_normals
    global g_speech,g_speechGT
    global g_bApplyRootOffset
    global g_bodyNormals
    #print(g_frameIdx)
    if g_skeletons_GT is None:
        return

    #frameLimit = g_skeletons.shape[2]
    #frameLens = [l.shape[1] for l in g_skeletons]
    #g_frameLimit = min(frameLens)

    #for humanIdx in range(g_skeletons.shape[0]):
    for humanIdx in range(len(g_skeletons_GT)):
        # if skelIdx ==0:
        #     # if g_idx+time_offset>=g_skeletons.shape[2]:
        #     #     continue
        #     skel = g_skeletons[skelIdx, :, g_idx+time_offset]
        #     # normal = g_normals[skelIdx, :, g_idx+time_offset]
        # else:
        #skel = g_skeletons[humanIdx, :, g_frameIdx]
        if(g_frameIdx >= g_skeletons_GT[humanIdx].shape[1]):
            continue

        skel = g_skeletons_GT[humanIdx][:, g_frameIdx]
        # normal = g_normals[skelIdx, :, g_idx]

        if g_bApplyRootOffset:
            skel = skel.copy()
            #skel[0::3] = skel[0::3]+ 70 *humanIdx
            skel[0::3] = skel[0::3]+ ROOT_OFFSET_DIST *humanIdx

        if skel.shape[0]==78:       #SMPlCOCO19 + headtop (19) + (leftFoot --toe20 pink21 heel22) + (rightFoot--toe23-pink24-heel25)
            drawbody_SMPLCOCO_TotalCap26(skel, [0,255,0])
        elif skel.shape[0]==57: #Panoptic Studio (SMC19) with 19 joints. Note SMC21 includes headtop
            drawbody_SMC19(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==96: #human36
            drawbody_joint32_human36m(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==66: #Holden's converted form
            drawbody_joint22(skel, g_colors[humanIdx % len(g_colors)])
        elif skel.shape[0]==93: #CMU Mocap Raw data (31joints)
            drawbody_joint31(skel, g_colors[humanIdx % len(g_colors)])
        else:
            drawbody_joint_ptOnly(skel, g_colors[humanIdx % len(g_colors)])

        # if False:#g_bodyNormals is not None and len(g_bodyNormals)> humanIdx:

        #     if g_bodyNormals[humanIdx].shape[1]<=g_frameIdx:
        #         print("Warning: g_bodyNormals[humanIdx].shape[2]<=g_frameId")
        #         continue

        #     normal3D = g_bodyNormals[humanIdx][:,g_frameIdx]  #3x1
        #     #drawbodyNormal(normal3D, skel, [255, 0, 0])
        #     rootPt = skel[(0*3):(0*3+3)]
        #     drawNormal(normal3D, rootPt, [255, 0, 0])


        # #Draw Speeking Annotation
        # if skel.shape[0]==57 and g_speech is not None: #Coco19
        #     if(g_frameIdx < len(g_speech[humanIdx]['word'])):
        #         draw_speaking_joint19(skel, g_speech[humanIdx]['indicator'][g_frameIdx], g_speech[humanIdx]['word'][g_frameIdx],  g_colors[humanIdx % len(g_colors)])

        # # if skel.shape[0]==66 and g_speech is not None: #Holden's
        # #     if(g_frameIdx < len(g_speech[humanIdx])):
        # #         draw_speaking_joint22(skel, g_speech[humanIdx][g_frameIdx],None,  g_colors[humanIdx % len(g_colors)])

        # # if skel.shape[0]==66 and g_speechGT is not None: #Holden's
        # #     if(g_frameIdx < len(g_speechGT[humanIdx])):
        # #         draw_speaking_joint22(skel, g_speechGT[humanIdx][g_frameIdx],"GT: Speaking", [255, 0, 0], 40)



#LSP14 format (used in HMR)
# Right ankle 1
# Right knee 2
# Right hip 3
# Left hip 4
# Left knee 5
# Left ankle 6
# Right wrist 7
# Right elbow 8
# Right shoulder 9
# Left shoulder 10
# Left elbow 11
# Left wrist 12
# Neck 13
# Head top 14
g_connMat_lsp14 = [ [13,3], [3,2], [2,1], #Right leg
                     [13,4], [4,5], [5,6], #Left leg
                     [13,10], [10,11], [11,12], #Left Arm
                     [13,9], [9,8], [8,7], #Right shoulder
                     [13,14]    #Nect -> Headtop
                     ]
g_connMat_lsp14 = np.array(g_connMat_lsp14, dtype=int) - 1 #zero Idx

#LSP14 format (used in HMR)
def drawbody_LSP14(joints,  color):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        if g_bSimpleHead and (i>=15 or i==1):
            continue
        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    connMat = g_connMat_lsp14
    #Visualize Bones
    for conn in connMat:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0


        if g_bSimpleHead and conn[0] == 0 and conn[1]==1:
            x1 = x1*0.5
            y1 = y1*0.5
            z1 = z1*0.5

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()




#In Zero index
#This is regressed joint from SMPL model defined from HMR
#MTC20 is exactly same as this except it has one more joint on spine (19)
g_connMat_smplcoco19 = [ [12,2], [2,1], [1,0], #Right leg
                     [12,3], [3,4], [4,5], #Left leg
                     [12,9], [9,10], [10,11], #Left Arm
                     [12,8], [8,7], [7,6], #Right shoulder
                      [12,14],[14,16],[16,18],  #Neck(12)->Nose(14)->rightEye(16)->rightEar(18)
                      [14,15],[15,17],   #Nose(14)->leftEye(15)->leftEar(17).
                      [14,13] #Nose->headTop(13)
                     ]
g_connMat_smplcoco19 = np.array(g_connMat_smplcoco19, dtype=int)  #zero Idx
def drawbody_SMPLCOCO19(joints,  color, normal=None):


    bBoneIsLeft =  [ 0,0,0,
            1, 1, 1,
            1,1,1,
            0,0,0,
            1,0,0,
            1,1,
            1] #To draw left as different color. Torso is treated as left


    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        # if i!=2:
        #     continue
        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    connMat = g_connMat_smplcoco19
    #Visualize Bones
    for i, conn in enumerate(connMat):
        if bBoneIsLeft[i]:          #Left as a color
            glColor3ub(color[0], color[1], color[2])
        else:       #Right as black
            glColor3ub(0,0,0)

        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()

    # Visualize Normals
    if normal is not None:
        i=1
        facePt = joints[(3*i):(3*i+3)]
        normalPt = facePt + normal*50

        glColor3ub(0, 255, 255)
        glPushMatrix()
        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()




#Panoptic Studio's Skeleton Output (AKA SMC19). Note SM21 has headTop(19) and spine(20)
g_bSimpleHead = False
if g_bSimpleHead==False:
    g_connMat_smc19 = [ [1,2], [1,4], [4,5], [5,6], [1,3], [3,7], [7,8], [8,9], [3,13],[13,14], [14,15], [1,10], [10, 11], [11, 12], [2, 16], [16, 17], [2, 18], [18, 19] ]
else:
    g_connMat_smc19 = [ [1,2], [1,4], [4,5], [5,6], [1,3], [3,7], [7,8], [8,9], [3,13],[13,14], [14,15], [1,10], [10, 11], [11, 12]]
g_connMat_smc19 = np.array(g_connMat_smc19, dtype=int) - 1 #zero Idx
def drawbody_SMC19(joints,  color, normal=None):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        if g_bSimpleHead and (i>=15 or i==1):
            continue
        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    connMat = g_connMat_smc19
    #Visualize Bones
    for conn in connMat:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0


        if g_bSimpleHead and conn[0] == 0 and conn[1]==1:
            x1 = x1*0.5
            y1 = y1*0.5
            z1 = z1*0.5

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()

    # Visualize Normals
    if normal is not None:
        i=1
        facePt = joints[(3*i):(3*i+3)]
        normalPt = facePt + normal*50

        glColor3ub(0, 255, 255)
        glPushMatrix()
        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()



#Panoptic Studio's Skeleton Output (AKA SMC19). Note SM21 has headTop(19) and spine(20)
def drawbody_SMPLCOCO_TotalCap26(joints,  color, normal=None):
    connMat = [ [12,2], [2,1], [1,0], #Right leg
                     [12,3], [3,4], [4,5], #Left leg
                     [12,9], [9,10], [10,11], #Left Arm
                     [12,8], [8,7], [7,6], #Right shoulder
                      [12,14],[14,16],[16,18],  #Neck(12)->Nose(14)->rightEye(16)->rightEar(18)
                      [14,15],[15,17],   #Nose(14)->leftEye(15)->leftEar(17).
                      [14,13], #Nose->headMidle(13)
                      [12,19],       #headTop19
                      [5,20], [5,21], [5,22],       #leftFoot
                      [0,23], [0,24], [0,25]       #rightFoot
                     ]
    connMat = np.array(connMat, dtype=int)  #zero Idx

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        if g_bSimpleHead and (i>=15 or i==1):
            continue
        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    #Visualize Bones
    for conn in connMat:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0


        if g_bSimpleHead and conn[0] == 0 and conn[1]==1:
            x1 = x1*0.5
            y1 = y1*0.5
            z1 = z1*0.5

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()

    # Visualize Normals
    if normal is not None:
        i=1
        facePt = joints[(3*i):(3*i+3)]
        normalPt = facePt + normal*50

        glColor3ub(0, 255, 255)
        glPushMatrix()
        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()



g_connMat_coco14 = [ [13,3], [3,2], [2,1], #Right leg
                     [13,4], [4,5], [5,6], #Left leg
                     [13,10], [10,11], [11,12], #Left Arm
                     [13,9], [9,8], [8,7], #Right shoulder
                     ]
g_connMat_coco14 = np.array(g_connMat_coco14, dtype=int) - 1 #zero Idx

def drawbody_joint14(joints,  color, normal=None):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        if g_bSimpleHead and (i>=15 or i==1):
            continue
        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    connMat_coco14 = g_connMat_coco14
    #Visualize Bones
    for conn in connMat_coco14:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0


        if g_bSimpleHead and conn[0] == 0 and conn[1]==1:
            x1 = x1*0.5
            y1 = y1*0.5
            z1 = z1*0.5

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()

    # Visualize Normals
    if normal is not None:
        i=1
        facePt = joints[(3*i):(3*i+3)]
        normalPt = facePt + normal*50

        glColor3ub(0, 255, 255)
        glPushMatrix()
        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()


def RenderString(str):
    glRasterPos3d(0,-2,0)
    for c in str:
        #glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


def draw_speaking_joint19(joints, bSpeak, word,  color, normal=None):

    # Visualize Speaking signal
    if bSpeak:
        i=1
        facePt = joints[(3*i):(3*i+3)]
        normalPt = facePt + np.array([0,-1,0])*20

        #glColor3ub(0, 255, 255)
        glColor3ub(color[0], color[1], color[2])

        glPushMatrix()

        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        #Render String
        if word is not None:
            RenderString(word)
        else:
            RenderString('speaking')


        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()



def draw_speaking_joint22(joints, bSpeak, word,  color, offset=20, normal=None):

    # Visualize Speaking signal
    if bSpeak:
        i=13
        facePt = joints[(3*i):(3*i+3)]
        normalPt = facePt + np.array([0,-1,0])*offset

        #glColor3ub(0, 255, 255)
        glColor3ub(color[0], color[1], color[2])

        glPushMatrix()

        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        #Render String
        if word is not None:
            RenderString(word)
        else:
            RenderString('speaking')


        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()

"""
    flagLength: show info on the upright direction
    offset: show info on the designated location
"""
def draw_speaking_general(facePt, bSpeak, word,  color, offsetLength=20, offset=None):

    # Visualize Speaking signal
    if bSpeak:
        #facePt = joints[(3*i):(3*i+3)]

        if offset is None:
            normalPt = facePt + np.array([0,-1,0])*offsetLength
        else:
            normalPt = facePt + offset

        #glColor3ub(0, 255, 255)
        glColor3ub(color[0], color[1], color[2])

        glPushMatrix()

        glTranslate(normalPt[0], normalPt[1], normalPt[2])
        glutSolidSphere(1, 10, 10)
        #Render String
        if word is not None:
            RenderString(word)
        else:
            RenderString('speaking')


        glPopMatrix()

        glBegin(GL_LINES)
        glVertex3f(facePt[0], facePt[1], facePt[2])
        glVertex3f(normalPt[0], normalPt[1],  normalPt[2])
        glEnd()

def drawbody_joint_ptOnly(joints,  color, normal=None):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()



#Human 36m DB's mocap data. 32 joints
g_connMat_joint32_human36m = [ [0,1],[1,2],[2,3],[3,4],[4,5], #RightLeg: root(0), rHip(1), rKnee(2), rAnkle(3), rFootMid(4), rFootEnd(5)
                     [0,6],[6,7],[7,8],[8,9], [9,10], #LeftLeg: root, lHip(6), lKnee(7), lAnkle(8), lFootMid(9), lFootEnd(10)
                     [11,12], [12,13], [13,14], [14,15], #root2(11), spineMid(12), neck(13), nose(14), head(15) #0,11 are the same points?
                     [16,17], [17,18], [18,19], [20,21], [20,22],   #Left Arms. neck(16==13), lshoulder(17),  lElbow(18), lWrist (19=20), lThumb(21), lMiddleFinger(22)
                     [24,25], [25,26], [26,27], [27,29], [27,30]   #Right Arm, neck(24==13), rshoulder(25),  rElbow(26), rWrist (27=28), rThumb(29), rMiddleFinger(30)
                     ]

def drawbody_joint32_human36m(joints,  color, normal=None):

    bBoneIsLeft = [0 ,0, 0, 0, 0,
                    1, 1, 1, 1, 1,
                    1, 1, 1, 1,
                    1, 1, 1, 1, 1,
                    0, 0, 0, 0, 0] #To draw left as different color. Torso is treated as left

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])

    for i in range(int(len(joints)/3)):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    #Visualize Bones
    for i, conn in enumerate(g_connMat_joint32_human36m):
        if bBoneIsLeft[i]:          #Left as a color
            glColor3ub(color[0], color[1], color[2])
        else:       #Right as black
            glColor3ub(0,0,0)
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()


# Simpler version of Human 36m DB's mocap data. with 17 joints
# 5 for torso + neck (root, spine, nect, nose, headtop)
g_connMat_joint17_human36m = [ [0,1],[1,2],[2,3],#,#root(0), rHip(1), rKnee(2), rAnkle(3)
                     [0,4],[4,5],[5,6],#,[8,9], [9,10], #root(0, lHip(4), lKnee(5), lAnkle(6)
                      [0,7], [7,8], [8,9], [9,10], #root(0, spineMid(7), neck(8), nose(9), head(10) #0,11 are the same points?
                     [8,11], [11,12], [12,13], #Left Arms. neck(8). lshoulder(11),  lElbow(12), lWrist (13)
                     [8,14], [14,15], [15,16] #Right Arm, neck(8), rshoulder(14),  rElbow(15), rWrist (16)
                     ]
def drawbody_joint17_human36m(joints,  color, normal=None):

    bBoneIsLeft = [0 ,0, 0,
                    1, 1, 1,
                    1, 1, 1, 1,
                    1, 1, 1,
                    0, 0, 0] #To draw left as different color. Torso is treated as left


    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    #Visualize Bones
    for i, conn in enumerate(g_connMat_joint17_human36m):
        if bBoneIsLeft[i]:          #Left as a color
            glColor3ub(color[0], color[1], color[2])
        else:       #Right as black
            glColor3ub(0,0,0)

        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()


#SMPL 24 joints used for LBS
g_connMat_joint24_smpl = [ [0,3],[3,6],[6,9],[9,12],[12,15],  #root-> torso -> head
                     [9,13],[13,16],[16,18],[18,20],[20,22], #Nect-> left hand
                     [9,14], [14,17], [17,19], [19,21], [21,23],  #Nect-> right hand
                     [0,1], [1,4], [4,7], [7,10], # left Leg
                     [0,2], [2,5], [5,8], [8,11] #right leg
                     ]
def drawbody_joint24_smplLBS(joints, color, normal=None):

    bBoneIsLeft = [1,1,1,1,1,
                    1,1,1,1,1,
                    0,0,0,0,0,
                    0,0,0,0,
                    1,1,1,1] #To draw left as different color. Torso is treated as left


    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    #Visualize Bones
    for i, conn in enumerate(g_connMat_joint24_smpl):
        if True:#bBoneIsLeft[i]:          #Left as a color
            glColor3ub(color[0], color[1], color[2])
        else:       #Right as black
            glColor3ub(0,0,0)

        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()


# g_connMat_coco31 = [ [0,1],[1,2],[2,3],[3,4],[4,5], #root(0), rHip(1), rKnee(2), rAnkle(3), RFootMid(4), rFootEnd(5)
#                      [0,6],[6,7],[7,8],[8,9], [9,10], #root, lHip(6), lKnee(7), lAnkle(8), lFootMid(9), lFootEnd(10)
#                      [11,12], [12,13], [13,14], [14,15], #root2(11), spineMid(12), neck(13), nose(14), head(15) #0,11 are the same points?
#                      [16,17], [17,18], [18,19], [18,19], [20,21], [20,22] ,
#                      [24,25], [25,26], [26,27], [27,29], [27,30] ]

#Note that left right of torso are flipped, compared human36m format
g_connMat_coco31 = [ [0,1],[1,2],[2,3],[3,4],[4,5], #root(0), lHip(1), lKnee(2), lAnkle(3), lFootMid(4), lFootEnd(5)
                     [0,6],[6,7],[7,8],[8,9], [9,10], #root, rHip(6), rKnee(7), lAnkle(8), lFootMid(9), lFootEnd(10)
                     [11,12], [12,13], [14,15],[15,16], #root2(11), lowerback(12), spine(13=14), neck(15), head(16) #(0,11), (13=14) are the same points
                     [17,18],[18,19],[19,20],[21,22],   # spine2(14=17), lShoulder(18), lElbow(19), lWrist(20==21), lHand(22), LThumb(23, not valid and same as 20)
                     [24,25],[25,26],[26,27],[28,29]   # spine2(14=24), rShoulder(25), rElbow(26), rWrist(27==28), rHand(29), rThumb(30, not valid and same as 27)
                     ]
# g_connMat_coco31 = [ [0,18]
#                       ]
def drawbody_joint31(joints,  color, normal=None):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(int(len(joints)/3)):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    #Visualize Bones
    for conn in g_connMat_coco31:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()

# Adam model
# Body (22) + Lhand (20) +  Rhand
g_connMat_Adam = [ [0,1], [1,4], [4,7], [7,10], #left leg
                    [0,2], [2,5], [5,8], [8,11], #right leg
                    [9,13], [13,16], [16,18], [18,20],   #left arm
                    [9,14], [14,17], [17,19], [19,21],   #right arm
                    [0,3], [3,6], [6,9], [9,12], [12,15],   #torso -> head

                    [20,22], [22,23], [23,24], [24,25],     #LeftHand Thumb
                    [20,26], [26,27], [27,28], [28,29],
                    [20,30], [30,31], [31,32], [32,33],
                    [20,34], [34,35], [35,36], [36,37],
                    [20,38], [38,39], [39,40], [40,41],     #Left Pinky


                    [21,42], [42,43], [43,44], [44,45],     #RightHand Thumb
                    [21,46], [46,47], [47,48], [48,49],
                    [21,50], [50,51], [51,52], [52,53],
                    [21,54], [54,55], [55,56], [56,57],
                    [21,58], [58,59], [59,60], [60,61]     #Right Pinky
                    ]
def drawbody_jointAdam(joints,  color, normal=None, ignore_root=False):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(1,int(len(joints)/3)):
    # for i in range(22):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])

        if i<22:
            glutSolidSphere(2, 10, 10)
        else:
            glutSolidSphere(0.5, 10, 10)
        glPopMatrix()

    connMat_adam = g_connMat_Adam
    #Visualize Bones
    for conn in connMat_adam:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        if conn[1]<22:    #body
            glutSolidCone(2, length, 10, 10)
        else:
            glutSolidCone(0.4, length, 10, 10)
        glPopMatrix()

    #Spine to ground projection
    conn = [0,1]
    x0 = joints[3*conn[0]]
    y0 = joints[3*conn[0]+1]
    z0 = joints[3*conn[0]+2]
    # x1, y1, z1 is the vector points from the base to the target
    x1 = joints[3*conn[1]]
    y1 = joints[3*conn[1]+1]
    z1 = joints[3*conn[1]+2]

    glBegin(GL_LINES)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y1, z1)
    glEnd()


def drawbody_jointSpin49(joints,  color, normal=None, ignore_root=False):

    skelSize = 10

    #Openpose25 + SPIN global 24
    link_openpose = [  [8,1], [1,0] , [0,16] , [16,18] , [0,15], [15,17],
                [1,2],[2,3],[3,4],      #Right Arm
                [1,5], [5,6], [6,7],       #Left Arm
                [8,12], [12,13], [13,14], [14,21], [14,19], [14,20],
                [8,9], [9,10], [10,11], [11,24], [11,22], [11,23]
                ]

    link_spin24 =[  [14,16], [16,12], [12,17] , [17,18] ,
                [12,9],[9,10],[10,11],      #Right Arm
                [12,8], [8,7], [7,6],       #Left Arm
                [14,3], [3,4], [4,5],
                [14,2], [2,1], [1,0]
                ]
    link_spin24 = np.array(link_spin24) + 25

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(1,int(len(joints)/3)):
    # for i in range(22):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])

        glutSolidSphere(skelSize, 10, 10)
        glPopMatrix()

    # #Visualize Bones
    # glColor3ub(0,0,255)
    # for conn in link_openpose:
    #     # x0, y0, z0 is the coordinate of the base point
    #     x0 = joints[3*conn[0]]
    #     y0 = joints[3*conn[0]+1]
    #     z0 = joints[3*conn[0]+2]
    #     # x1, y1, z1 is the vector points from the base to the target
    #     x1 = joints[3*conn[1]] - x0
    #     y1 = joints[3*conn[1]+1] - y0
    #     z1 = joints[3*conn[1]+2] - z0

    #     length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
    #     theta = math.degrees(math.acos(z1/length))
    #     phi = math.degrees(math.atan2(y1, x1))

    #     glPushMatrix()
    #     glTranslate(x0, y0, z0)
    #     glRotatef(phi, 0, 0, 1)
    #     glRotatef(theta, 0, 1, 0)
    #     glutSolidCone(0.4, length, 10, 10)
    #     glPopMatrix()

    #Visualize Bones
    # glColor3ub(255,0,0)
    glColor3ub(color[0], color[1], color[2])
    for conn in link_spin24:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(skelSize, length, 10, 10)

        glPopMatrix()

    #Spine to ground projection
    conn = [0,1]
    x0 = joints[3*conn[0]]
    y0 = joints[3*conn[0]+1]
    z0 = joints[3*conn[0]+2]
    # x1, y1, z1 is the vector points from the base to the target
    x1 = joints[3*conn[1]]
    y1 = joints[3*conn[1]+1]
    z1 = joints[3*conn[1]+2]

    glBegin(GL_LINES)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y1, z1)
    glEnd()


def drawbody_FRLSocialmocap(joints,  color, normal=None, ignore_root=False):

    skelSize = 0.5

    # parents = [-1,  0,  1,  2,  3,  4,  5,  6,  7,  7,  7,  7, 11, 11, 11, 14, 15,
    #     16, 17, 18, 18, 17, 17, 16, 16, 15, 15,  5, 27, 28, 29, 30, 31, 32,
    #     33, 34, 35, 33, 37, 38, 33, 40, 41, 33, 43, 44, 33, 46, 47, 48,  5,
    #     50, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 57, 62, 63, 57, 65, 66,
    #     57, 68, 69, 57, 71, 72,  4,  1, 75, 76, 77,  1, 79, 80, 81]

    # joints_name = ['body_world', 'b_root', 'b_spine0', 'b_spine1', 'b_spine2', 'b_spine3', 'b_neck0', 'b_head', 'b_head_null', 'b_l_eye', 'b_r_eye', 'b_jaw', 'b_jaw_null', 'b_teeth', 'b_tongue0', 'b_tongue1', 'b_tongue2', 'b_tongue3', 'b_tongue4', 'b_l_tongue4_1', 'b_r_tongue4_1', 'b_l_tongue3_1', 'b_r_tongue3_1', 'b_l_tongue2_1', 'b_r_tongue2_1', 'b_r_tongue1_1', 'b_l_tongue1_1', 'b_r_shoulder', 'p_r_scap', 'b_r_arm', 'b_r_arm_twist', 'b_r_forearm', 'b_r_wrist_twist', 'b_r_wrist',
    #  'b_r_index1', 'b_r_index2', 'b_r_index3', 'b_r_ring1', 'b_r_ring2', 'b_r_ring3', 'b_r_middle1', 'b_r_middle2', 'b_r_middle3', 'b_r_pinky1', 'b_r_pinky2', 'b_r_pinky3', 'b_r_thumb0', 'b_r_thumb1', 'b_r_thumb2', 'b_r_thumb3', 
    # 'b_l_shoulder', 'p_l_delt', 'p_l_scap', 'b_l_arm', 'b_l_arm_twist', 'b_l_forearm', 'b_l_wrist_twist', 'b_l_wrist',
    #  'b_l_thumb0', 'b_l_thumb1', 'b_l_thumb2', 'b_l_thumb3', 'b_l_index1', 'b_l_index2', 'b_l_index3', 'b_l_middle1', 'b_l_middle2', 'b_l_middle3', 'b_l_ring1', 'b_l_ring2', 'b_l_ring3', 'b_l_pinky1', 'b_l_pinky2', 'b_l_pinky3',
    #  'p_navel', 'b_r_upleg', 'b_r_leg', 'b_r_foot_twist', 'b_r_foot', 'b_l_upleg', 'b_l_leg', 'b_l_foot_twist', 'b_l_foot']
    
    #34 -49 :right hand
    #58 - 73: left hand
    # link_body = [[1,0],  [2,1],  [3,2],  [4,3],  [5,4],  [6,5],  [7,6],  [8,7],  [9,7],  [10,7],  [11,7], [12,11], [13,11], [14,11], [15,14], [16,15],
    #     [17,16], [18,17], [19,18], [20,18], [21,17], [22,17], [23,16], [24,16], [25,15], [26,15],  [27,5], [28,27], [29,28], [30,29], [31,30], [32,31], [33,32],[34,33],
    #     [50,5], [51,50], [52,50], [53,52], [54,53], [55,54], [56,55], [57,56],

    #      [74,4],  [75,1], [76,75], [77,76], [78,77],  [79,1], [80,79], [81,80], [82,81]
    #     ]
    link_body = [  [2,1],  [3,2],  [4,3],  [5,4],  [6,5],  [7,6],  [8,7],  [11,7],# [12,11], [13,11], [14,11], [15,14], [16,15],[17,16], [18,17], [19,18], [20,18], [21,17], [22,17], [23,16], [24,16], [25,15], [26,15],
      [27,5], [28,27], [29,28], [30,29], [31,30], [32,31], [33,32],[34,33],
      [50,5], [51,50], [52,51], [53,52], [54,53], [55,54], [56,55], [57,56],
    [74,4], [75,1], [76,75], [77,76], [78,77],  [79,1], [80,79], [81,80], [82,81]     #Legs
    ]
    link_body = np.array(link_body)

    link_hand = [ [58,57], [59,58], [60,59], [61,60], [62,57], [63,62], [64,63], [65,57], [66,65], [67,66], [68,57], [69,68], [70,69], [71,57], [72,71], [73,72], #left hand
         [35, 34], [36,35], [37,33], [38,37], [39,38], [40,33], [41, 40], [42,41], [43,33], [44,43], [45,44], [46,33], [47,46], [48,47], [49,48], #right hand
    ]
    link_hand = np.array(link_hand)


    link_face = [ [9,10], [9,13], [10,13], [9,11], [10,11], [13,11] ]
    link_face = np.array(link_face)
    



    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(1,int(len(joints)/3)):
    # for i in range(22):
        if i in [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]:
            continue
        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])

        glutSolidSphere(skelSize, 10, 10)
        glPopMatrix()

    # #Visualize Bones
    # glColor3ub(0,0,255)
    # for conn in link_openpose:
    #     # x0, y0, z0 is the coordinate of the base point
    #     x0 = joints[3*conn[0]]
    #     y0 = joints[3*conn[0]+1]
    #     z0 = joints[3*conn[0]+2]
    #     # x1, y1, z1 is the vector points from the base to the target
    #     x1 = joints[3*conn[1]] - x0
    #     y1 = joints[3*conn[1]+1] - y0
    #     z1 = joints[3*conn[1]+2] - z0

    #     length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
    #     theta = math.degrees(math.acos(z1/length))
    #     phi = math.degrees(math.atan2(y1, x1))

    #     glPushMatrix()
    #     glTranslate(x0, y0, z0)
    #     glRotatef(phi, 0, 0, 1)
    #     glRotatef(theta, 0, 1, 0)
    #     glutSolidCone(0.4, length, 10, 10)
    #     glPopMatrix()

    #Visualize Bones
    # glColor3ub(255,0,0)
    glColor3ub(color[0], color[1], color[2])
    for conn in link_body:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[1]]
        y0 = joints[3*conn[1]+1]
        z0 = joints[3*conn[1]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[0]] - x0
        y1 = joints[3*conn[0]+1] - y0
        z1 = joints[3*conn[0]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(skelSize*3, length, 10, 10)

        glPopMatrix()

    
     #Visualize Bones
    # glColor3ub(255,0,0)
    glColor3ub(color[0], color[1], color[2])
    for conn in link_hand:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[1]]
        y0 = joints[3*conn[1]+1]
        z0 = joints[3*conn[1]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[0]] - x0
        y1 = joints[3*conn[0]+1] - y0
        z1 = joints[3*conn[0]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(skelSize, length, 10, 10)

        glPopMatrix()


    #Visualize Bones
    # glColor3ub(255,0,0)
    glColor3ub(color[0], color[1], color[2])
    glLineWidth(5)
    for conn in link_face:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[1]]
        y0 = joints[3*conn[1]+1]
        z0 = joints[3*conn[1]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[0]] 
        y1 = joints[3*conn[0]+1]
        z1 = joints[3*conn[0]+2]

        glBegin(GL_LINES)
        glVertex3f(x0, y0, z0)
        glVertex3f(x1, y1, z1)
        glEnd()



    # #Spine to ground projection
    # conn = [0,1]
    # x0 = joints[3*conn[0]]
    # y0 = joints[3*conn[0]+1]
    # z0 = joints[3*conn[0]+2]
    # # x1, y1, z1 is the vector points from the base to the target
    # x1 = joints[3*conn[1]]
    # y1 = joints[3*conn[1]+1]
    # z1 = joints[3*conn[1]+2]

    # glBegin(GL_LINES)
    # glVertex3f(x0, y0, z0)
    # glVertex3f(x1, y1, z1)
    # glEnd()



def drawbody_jointSpin24(joints,  color, normal=None, ignore_root=False):

    link_spin24 =[  [14,16], [16,12], [12,17] , [17,18] ,
                [12,9],[9,10],[10,11],      #Right Arm
                [12,8], [8,7], [7,6],       #Left Arm
                [14,3], [3,4], [4,5],
                [14,2], [2,1], [1,0]
                ]
    link_spin24 = np.array(link_spin24)

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(1,int(len(joints)/3)):
    # for i in range(22):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])

        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    #Visualize Bones
    # glColor3ub(255,0,0)
    glColor3ub(color[0], color[1], color[2])
    for conn in link_spin24:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        if length>0.001:
            theta = math.degrees(math.acos(z1/length))
            phi = math.degrees(math.atan2(y1, x1))

            glPushMatrix()
            glTranslate(x0, y0, z0)
            glRotatef(phi, 0, 0, 1)
            glRotatef(theta, 0, 1, 0)
            glutSolidCone(2, length, 10, 10)

            glPopMatrix()

    #Spine to ground projection
    conn = [0,1]
    x0 = joints[3*conn[0]]
    y0 = joints[3*conn[0]+1]
    z0 = joints[3*conn[0]+2]
    # x1, y1, z1 is the vector points from the base to the target
    x1 = joints[3*conn[1]]
    y1 = joints[3*conn[1]+1]
    z1 = joints[3*conn[1]+2]

    glBegin(GL_LINES)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y1, z1)
    glEnd()







# D. Holden's Data type
# root (3pts on the floor) + 21joints
parents = np.array([-1,0,1,2,3,4,1,6,7,8,1,10,11,12,12,14,15,16,12,18,19,20])

g_connMat_coco22 = [ [1,2], [2,3], [3,4], [4,5],    #right leg
                     [1,6], [6,7], [7,8], [8,9],    #left leg
                     [1,10], [10,11], [11,12], [12,13], #spine, head
                      [12,14], [14,15], [15,16], [16,17], #right arm
                       [12,18] , [18,19], [19,20], [20,21]] #left arm
#g_connMat_coco22 = np.array(g_connMat_coco22, dtype=int) - 1 #zero Idx
def drawbody_joint22(joints,  color, normal=None, ignore_root=False):

    #Visualize Joints
    glColor3ub(color[0], color[1], color[2])
    for i in range(1,int(len(joints)/3)):

        glPushMatrix()
        glTranslate(joints[3*i], joints[3*i+1], joints[3*i+2])
        glutSolidSphere(2, 10, 10)
        glPopMatrix()

    connMat_coco22 = g_connMat_coco22
    #Visualize Bones
    for conn in connMat_coco22:
        # x0, y0, z0 is the coordinate of the base point
        x0 = joints[3*conn[0]]
        y0 = joints[3*conn[0]+1]
        z0 = joints[3*conn[0]+2]
        # x1, y1, z1 is the vector points from the base to the target
        x1 = joints[3*conn[1]] - x0
        y1 = joints[3*conn[1]+1] - y0
        z1 = joints[3*conn[1]+2] - z0

        length = math.sqrt(x1*x1 + y1*y1 + z1*z1)
        theta = math.degrees(math.acos(z1/length))
        phi = math.degrees(math.atan2(y1, x1))

        glPushMatrix()
        glTranslate(x0, y0, z0)
        glRotatef(phi, 0, 0, 1)
        glRotatef(theta, 0, 1, 0)
        glutSolidCone(2, length, 10, 10)
        glPopMatrix()




    #Spine to ground projection
    conn = [0,1]
    x0 = joints[3*conn[0]]
    y0 = joints[3*conn[0]+1]
    z0 = joints[3*conn[0]+2]
    # x1, y1, z1 is the vector points from the base to the target
    x1 = joints[3*conn[1]]
    y1 = joints[3*conn[1]+1]
    z1 = joints[3*conn[1]+2]

    glBegin(GL_LINES)
    glVertex3f(x0, y0, z0)
    glVertex3f(x1, y1, z1)
    glEnd()

    # # Visualize Normals
    # if normal is not None:
    #     i=1
    #     facePt = joints19[(3*i):(3*i+3)]
    #     normalPt = facePt + normal*50

    #     glColor3ub(0, 255, 255)
    #     glPushMatrix()
    #     glTranslate(normalPt[0], normalPt[1], normalPt[2])
    #     glutSolidSphere(1, 10, 10)
    #     glPopMatrix()

    #     glBegin(GL_LINES);
    #     glVertex3f(facePt[0], facePt[1], facePt[2]);
    #     glVertex3f(normalPt[0], normalPt[1],  normalPt[2]);
    #     glEnd()


# The following is for drawbody_joint73 (Holden's format)
sys.path.append('../motion/')
from Quaternions import Quaternions

# skel_list is a list of skeletonElement
# each skeletonElement: (73,frameNum)
# D. Holden's Data type
# Joints73: 73 dim = 22joint*3 + 3 (X_velocity,Z_velocity,Rot_Velocity) +  4 (footStep)
# Input
#   - initRot: Quaternion for the first frame in global coordinate
#   - initTrans: 3x1 vector or np array
def set_Holden_Data_73(skel_list, ignore_root=False, initRot = None, initTrans=None, bIsGT= False):
    #global HOLDEN_DATA_SCALING

    skel_list_output = []
    #footsteps_output = []

    for ai in range(len(skel_list)):
        anim = np.swapaxes(skel_list[ai].copy(), 0, 1)  # frameNum x 73

        if anim.shape[1]==73:
            joints, root_x, root_z, root_r = anim[:,:-7], anim[:,-7], anim[:,-6], anim[:,-5]
        elif anim.shape[1]==69:
            joints, root_x, root_z, root_r = anim[:,:-3], anim[:,-3], anim[:,-2], anim[:,-1]
        joints = joints.reshape((len(joints), -1, 3)) #(frameNum,66) -> (frameNum, 22, 3)

        if initRot is None:
            rotation = Quaternions.id(1)
        else:
            rotation = initRot[ai]
        offsets = []

        if initTrans is None:
            translation = np.array([[0,0,0]])   #1x3
        else:
            translation = np.array(initTrans[ai])
            if translation.shape[0]==3:
                translation = np.swapaxes(translation,0,1)


        if not ignore_root:
            for i in range(len(joints)):
                joints[i,:,:] = rotation * joints[i]
                joints[i,:,0] = joints[i,:,0] + translation[0,0]
                joints[i,:,2] = joints[i,:,2] + translation[0,2]
                rotation = Quaternions.from_angle_axis(-root_r[i], np.array([0,1,0])) * rotation
                offsets.append(rotation * np.array([0,0,1]))
                translation = translation + rotation * np.array([root_x[i], 0, root_z[i]])

        #joints dim:(frameNum, 22, 3)
        #Scaling
        joints[:,:,:] = joints[:,:,:] * HOLDEN_DATA_SCALING#5 #m -> cm
        joints[:,:,1] = joints[:,:,1] *-1 #Flip Y axis

        #Reshaping
        joints = joints.reshape(joints.shape[0], joints.shape[1]*joints.shape[2]) # frameNum x 66
        joints =  np.swapaxes(joints, 0, 1)  # 66  x frameNum

        skel_list_output.append(joints)
        #footsteps_output.append(anim[:,-4:])


    #adjust length
    length = min( [ i.shape[1] for i in skel_list_output])
    skel_list_output = [ f[:,:length] for f in skel_list_output ]

    skel_list_output = np.asarray(skel_list_output)
    #return skel_list_output #(skelNum, 66, frameNum)
    #showSkeleton(skel_list_output)
    setSkeleton(skel_list_output, bIsGT)


# traj_list is a list of 3 dim tran+rot infor
# each trajectory data: (3,frameNum)
# D. Holden's Data type
# 3 dim = 3 (X_velocity,Z_velocity,Rot_Velocity)
def set_Holden_Trajectory_3(traj_list, initRot = None, initTrans=None ):

    global HOLDEN_DATA_SCALING

    traj_list_output = []

    for ai in range(len(traj_list)):

        root_x, root_z, root_r = traj_list[ai][0,:], traj_list[ai][1,:], traj_list[ai][2,:]

        if initRot is None:
            rotation = Quaternions.id(1)
        else:
            rotation = initRot[ai]
        offsets = []

        if initTrans is None:
            translation = np.array([[0,0,0]])   #1x3
        else:
            translation = np.array(initTrans[ai])
            if translation.shape[0]==3:
                translation = np.swapaxes(translation,0,1)

        # joints = np.array([0,0,0])
        # joints = np.repeat(joints, )
        # joints = joints.reshape((len(joints), -1, 3)) #(frameNum,66) -> (frameNum, 22, 3)
        joints = np.zeros((len(root_x),2,3))        #(frames, 2,3) for original and directionPt
        joints[:,1,2] = 10 #Normal direction

        for i in range(len(joints)):
            joints[i,:,:] = rotation * joints[i]
            joints[i,:,0] = joints[i,:,0] + translation[0,0]
            joints[i,:,2] = joints[i,:,2] + translation[0,2]
            rotation = Quaternions.from_angle_axis(-root_r[i], np.array([0,1,0])) * rotation
            offsets.append(rotation * np.array([0,0,1]))
            translation = translation + rotation * np.array([root_x[i], 0, root_z[i]])

        #Reshaping
        joints = joints.reshape(joints.shape[0], joints.shape[1]*joints.shape[2]) # (frameNum,jointDim,3) -> (frameNum, jointDim*3)
        joints =  np.swapaxes(joints, 0, 1)  # jointDim*3  x frameNum

        joints = joints*HOLDEN_DATA_SCALING
        traj_list_output.append(joints)

    traj_list_output = np.asarray(traj_list_output)
    setTrajectory(traj_list_output)         #(trajNum, joitnDim*3, frames)

"""
    input:
     - speech_list: list of speechData
     - speechData: {'indicator': i, 'word': w}
     - i: frames of binary value
"""
def setSpeech_binary(speech_list):

    global g_speech#,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    for i, _ in enumerate(speech_list):
        if len(speech_list[i].shape) ==1:
            no = [None] * len(speech_list[i])
            speech_list[i] = {'indicator': speech_list[i], 'word':no}

    g_speech = speech_list #List of 2dim np.array

"""
    input:
     - speech_list: list of speechData
     - speechData: {'indicator': i, 'word': w}
     - i: frames of binary value
"""
def setSpeechGT_binary(speech_list):

    global g_speechGT#,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    for i, _ in enumerate(speech_list):
        if len(speech_list[i].shape) ==1:
            no = [None] * len(speech_list[i])
            speech_list[i] = {'indicator': speech_list[i], 'word':no}

    g_speechGT = speech_list #List of 2dim np.array

"""
    input:
     - speech_list: list of speechData
     - speechData: {'indicator': i, 'word': w}
     - i: frames of binary value
"""
def setSpeech(speech_list):

    global g_speech#,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    g_speech = speech_list #List of 2dim np.array

    # #g_frameLimit = g_skeletons.shape[2]
    # frameLens = [l.shape[1] for l in g_skeletons]
    # g_frameLimit = min(frameLens)


"""
    input:
     - speech_list: list of speechData
     - speechData: {'indicator': i, 'word': w}
     - i: frames of binary value
     - root_list: the root location to draw the speech data. same size as speech data
"""
def setSpeech_withRoot(speech_list, root_list):

    global g_speech#,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    g_speech = speech_list #List of 2dim np.array

    #Set root location
    for u,r in zip(g_speech,root_list):
        u['root'] = r

    # #g_frameLimit = g_skeletons.shape[2]
    # frameLens = [l.shape[1] for l in g_skeletons]
    # g_frameLimit = min(frameLens)



"""
    input:
     - speech_list: list of speechData
     - speechData: {'indicator': i, 'word': w}
     - i: frames of binary value
"""
def setSpeechGT(speech_list):

    global g_speechGT#,g_frameLimit #nparray: (skelNum, skelDim, frameNum)


    g_speechGT = speech_list #List of 2dim np.array

    # #g_frameLimit = g_skeletons.shape[2]
    # frameLens = [l.shape[1] for l in g_skeletons]
    # g_frameLimit = min(frameLens)



#Input: face_list (faceNum, dim, frames): nparray or list of arrays (dim, frames)
def showFace(face_list):

    #Add Skeleton Data
    global g_faces,g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    #g_faces = np.asarray(face_list)  #no effect if face_list is already np.array
    g_faces  = face_list

    frameLens = [l.shape[1] for l in g_faces]
    g_frameLimit = max(g_frameLimit,min(frameLens))
    #init_gl()



def setFace(face_list):

    global g_faces,g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    g_faces  = face_list

    # frameLens = [l.shape[1] for l in g_faces]
    # g_frameLimit = max(g_frameLimit,min(frameLens))
    setFrameLimit()




"""faceNormal_list: each element should have 3xframe"""
def setFaceNormal(faceNormal_list):

    global g_faceNormals,g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    #g_faceNormals  = faceNormal_list
    g_faceNormals  = [ x.copy() for x in faceNormal_list]


    frameLens = [l.shape[1] for l in g_faceNormals if len(l)>0]
    maxFrameLength = max(frameLens)
    for i, p in enumerate(g_faceNormals):
        if len(p)==0:
            newData = np.zeros((3, maxFrameLength))
            g_faceNormals[i] = newData
        elif p.shape[0]==2:
            newData = np.zeros((3, p.shape[1]))
            newData[0,:] = p[0,:]
            newData[1,:] = 0 #some fixed number
            newData[2,:] = p[1,:]

            g_faceNormals[i] = newData



    g_frameLimit = max(g_frameLimit,min(frameLens))


"""bodyNormal_list: each element should have 3xframe"""
def setBodyNormal(bodyNormal_list):

    global g_bodyNormals,g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    #g_bodyNormals  = bodyNormal_list
    g_bodyNormals  = [ x.copy() for x in bodyNormal_list]

    frameLens = [l.shape[1] for l in g_bodyNormals  if len(l)>0]
    maxFrameLength = max(frameLens)


    for i, p in enumerate(g_bodyNormals):
        if len(p)==0:
            newData = np.zeros((3, maxFrameLength))
            g_bodyNormals[i] = newData
        elif p.shape[0]==2:
            newData = np.zeros((3, p.shape[1]))
            newData[0,:] = p[0,:]
            newData[1,:] = 0 #some fixed number
            newData[2,:] = p[1,:]

            g_bodyNormals[i] = newData

        elif p.shape[0]==3:
            g_bodyNormals[i] = p





    g_frameLimit = max(g_frameLimit,min(frameLens))


"""pos_list: each element should have 3xframe"""
#Input: skel_list (skelNum, dim, frames): 
def setPosOnly(pos_list):
    global g_posOnly,g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    g_posOnly  = [ x.copy() for x in pos_list]

    for i, p in enumerate(g_posOnly):
        if p.shape[0]==2:
            newData = np.zeros((3, p.shape[1]))
            newData[0,:] = p[0,:]
            #newData[1,:] = -100 #some fixed number
            newData[1,:] = 0 #some fixed number
            newData[2,:] = p[1,:]

            g_posOnly[i] = newData

    frameLens = [l.shape[1] for l in g_posOnly]
    g_frameLimit = max(g_frameLimit,min(frameLens))




def setHand_left(hand_list):

    global g_hands_left, g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    g_hands_left  = hand_list

    frameLens = [l.shape[1] for l in g_hands_left]
    g_frameLimit = max(g_frameLimit,min(frameLens))


def setHand_right(hand_list):

    global g_hands_right, g_frameLimit#nparray: (faceNum, faceDim, frameNum)

    g_hands_right  = hand_list

    frameLens = [l.shape[1] for l in g_hands_right]
    g_frameLimit = max(g_frameLimit,min(frameLens))


#Input: skel_list (skelNum, dim, frames): nparray or list of arrays (dim, frames)
def setTrajectory(traj_list):
    #Add Skeleton Data
    global g_trajectory,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    # if len(skel_list)>1:
    #     lens = [len(l) for l in skel_list]
    #     minLeng=max(lens)

    #     for i in range(0,len(skel_list)):
    #         skel_list[i] = skel_list[i][:,:minLeng]

    #g_skeletons = np.asarray(skel_list)  #no effect if skel_list is already np.array
    g_trajectory = traj_list #List of 2dim np.array

    #g_frameLimit = g_skeletons.shape[2]
    frameLens = [l.shape[1] for l in g_trajectory]
    g_frameLimit = max(g_frameLimit,min(frameLens))


def addSkeleton(skel_list, bIsGT = False, jointType=None):
    if g_skeletons is not None:
        setSkeleton(g_skeletons+ skel_list, bIsGT, jointType)
    else:
        setSkeleton(skel_list, bIsGT, jointType)

#Input: skel_list (skelNum, dim, frames): nparray or list of arrays (dim, frames)
def setSkeleton(skel_list, bIsGT = False, jointType=None):
    global g_skeletons,g_frameLimit #nparray: (skelNum, skelDim, frameNum)
    global g_skeletons_GT,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    if bIsGT==False:
        global g_skeletonType
        g_skeletonType = jointType

    if jointType =='smpl':
        print("Use smplcoco instead of smpl!")
        assert(False)

    if isinstance(skel_list,list) == False and len(skel_list.shape)==2:
        skel_list = skel_list[np.newaxis,:]

    if bIsGT==False:
        #Add Skeleton Data

        # if len(skel_list)>1:
        #     lens = [len(l) for l in skel_list]
        #     minLeng=max(lens)

        #     for i in range(0,len(skel_list)):
        #         skel_list[i] = skel_list[i][:,:minLeng]

        #g_skeletons = np.asarray(skel_list)  #no effect if skel_list is already np.array
        g_skeletons = skel_list #List of 2dim np.array


        #g_frameLimit = g_skeletons.shape[2]
        # frameLens = [l.shape[1] for l in g_skeletons]
        # g_frameLimit = max(g_frameLimit,min(frameLens))

    else:
         #Add Skeleton Data
        g_skeletons_GT = skel_list #List of 2dim np.array


        #g_frameLimit = g_skeletons.shape[2]
        # frameLens = [l.shape[1] for l in g_skeletons_GT]
        # g_frameLimit = max(g_frameLimit,min(frameLens))

    setFrameLimit()



#Input: skel_list (skelNum, dim, frames): nparray or list of arrays (dim, frames)
def showSkeleton(skel_list):

    #Add Skeleton Data
    global g_skeletons,g_frameLimit #nparray: (skelNum, skelDim, frameNum)

    # if len(skel_list)>1:
    #     lens = [len(l) for l in skel_list]
    #     minLeng=max(lens)

    #     for i in range(0,len(skel_list)):
    #         skel_list[i] = skel_list[i][:,:minLeng]

    #g_skeletons = np.asarray(skel_list)  #no effect if skel_list is already np.array
    g_skeletons = skel_list #List of 2dim np.array


    #g_frameLimit = g_skeletons.shape[2]
    frameLens = [l.shape[1] for l in g_skeletons]
    g_frameLimit = max(g_frameLimit,min(frameLens))

    # init_gl()


#Input: skel_list peopelNum x {'ver': vertexInfo, 'f': faceInfo}
#: vertexInfo should be (frames x vertexNum x 3 )
#: if vertexInfo has (vertexNum x 3 ), this function automatically changes it to (1 x vertexNum x 3)
#: faceInfo should be (vertexNum x 3 )
#'normal': if missing, draw mesh by wireframes
def setMeshData(mesh_list, bComputeNormal = False):

    global g_meshes

    #g_skeletons = np.asarray(skel_list)  #no effect if skel_list is already np.array

    ##
    g_meshes = mesh_list

    if len(g_meshes)==0:
        return

    if len(g_meshes)>40:
        print("Warning: too many meshes ({})".format(len(g_meshes)))
        g_meshes =g_meshes[:40]


    if len(g_meshes)==0:
        return

    if len(g_meshes)>40:
        print("Warning: too many meshes ({})".format(len(g_meshes)))
        g_meshes =g_meshes[:40]


    for element in g_meshes:
        if len(element['ver'].shape) ==2:
            # print("## setMeshData: Warning: input size should be (N, verNum, 3). Current input is (verNum, 3). I am automatically fixing this.")
            element['ver'] = element['ver'][np.newaxis,:,:]
            if 'normal' in element.keys():
                element['normal'] = element['normal'][np.newaxis,:,:]

    #Auto computing normal
    if bComputeNormal:
        # print("## setMeshData: Computing face normals automatically.")
        for element in g_meshes:
            element['normal'] = ComputeNormal(element['ver'],element['f']) #output: (N, 18540, 3)

    #g_frameLimit = g_skeletons.shape[2]
    #mesh_list[0]['ver'].shape
    # frameLens = [l['ver'].shape[0] for l in g_meshes]
    # g_frameLimit = max(g_frameLimit,min(frameLens))

    setFrameLimit()

# Length computation doesn't look correct for skeletons
# def setFrameLimit():
#     global g_frameLimit
#     g_frameLimit = 0

#     if g_meshes is not None:
#         frameLens = [1] + [l['ver'].shape[0] for l in g_meshes]
#         g_frameLimit = max(g_frameLimit,min(frameLens))

#     if g_skeletons is not None:
#         frameLens = [1] + [l.shape[1] for l in g_skeletons]
#         g_frameLimit = max(g_frameLimit,min(frameLens))

#     if g_skeletons_GT is not None:
#         frameLens = [1] + [l.shape[1] for l in g_skeletons_GT]
#         g_frameLimit = max(g_frameLimit,min(frameLens))

#     if g_faces is not None:
#         frameLens = [1] + [l.shape[1] for l in g_faces]
#         g_frameLimit = max(g_frameLimit,min(frameLens))

# Getting back to the original code
def setFrameLimit():
    global g_frameLimit
    g_frameLimit = 0

    if g_meshes is not None:
        frameLens = [l['ver'].shape[0] for l in g_meshes] 
        g_frameLimit = max(g_frameLimit,min(frameLens))

    if g_skeletons is not None:
        frameLens = [l.shape[1] for l in g_skeletons] 
        g_frameLimit = max(g_frameLimit,min(frameLens))

    if g_skeletons_GT is not None:
        frameLens = [l.shape[1] for l in g_skeletons_GT] 
        g_frameLimit = max(g_frameLimit,min(frameLens))

    if g_faces is not None:
        frameLens = [l.shape[1] for l in g_faces] 
        g_frameLimit = max(g_frameLimit,min(frameLens))


def resetFrameLimit():
    global g_frameLimit
    g_frameLimit =0


def addMeshData(mesh_list, bComputeNormal = False):
    if g_meshes is not None:
        setMeshData(g_meshes + mesh_list, bComputeNormal) #TODO: no need to compute normal for already added one..
    else:
        setMeshData(mesh_list, bComputeNormal)




"""
    input:
     - list of faceParam, where each element has np array of (200 x frames)
"""
def setFaceParmData(faceParam_list, bComputeNormal = True):
    global g_faceModel

    if g_faceModel is None:
        import scipy.io as sio
        g_faceModel = sio.loadmat('/ssd/data/totalmodel/face_model_totalAligned.mat')

    #check the dimension. If dim <200, padding zeros
    for i,f in enumerate(faceParam_list):
        if (f.shape[0]<200):
            newData = np.zeros ( (200,f.shape[1]) )
            newData[:f.shape[0],:] = f
            faceParam_list[i] = newData

    faceParam_list = [ {'face_exp': f} for f in faceParam_list]

    faceMesh_list = GetFaceMesh(g_faceModel,faceParam_list, bComputeNormal= bComputeNormal)
    etMeshData( faceMesh_list)


"""
    input:
     - list of faceParam, where each element has np array of (200 x frames)
"""
def setFaceParmDataWithTrans(faceParam_list, bComputeNormal = True, trans= None, rot = None):
    global g_faceModel

    if g_faceModel is None:
        import scipy.io as sio
        g_faceModel = sio.loadmat('/ssd/data/totalmodel/face_model_totalAligned.mat')

    #check the dimension. If dim <200, padding zeros
    for i,f in enumerate(faceParam_list):
        if (f.shape[0]<200):
            newData = np.zeros ( (200,f.shape[1]) )
            newData[:f.shape[0],:] = f
            faceParam_list[i] = newData

    #faceParam_list = [ {'face_exp': f} for f in faceParam_list]
    faceParam_list_new =[]
    for i in range(len(faceParam_list)):
        data = dict()
        data['face_exp'] = faceParam_list[i]    #(200,frames)
        if trans is not None:
            data['trans'] = trans[i]        #(3,frames)

            frameLen = min( data['face_exp'].shape[1], data['trans'].shape[1] )
            data['face_exp'] = data['face_exp'][:,:frameLen]
            data['trans'] = data['trans'][:,:frameLen] *0.01

            ROT_PIVOT = np.array([0.003501, 0.475611, 0.115576])
            ROT_PIVOT[2] -=0.1
            #faceMassCenter = np.array([-0.002735  , -1.44728992,  0.2565446 ])#*100
            data['rot_pivot'] = data['trans']*0 + ROT_PIVOT[:,np.newaxis]




        if rot is not None:
            data['rot'] = rot[i]

            frameLen = min( data['face_exp'].shape[1], data['rot'].shape[1] )
            data['face_exp'] = data['face_exp'][:,:frameLen]
            if trans is not None:
                 data['trans'] = data['trans'][:,:frameLen]
            data['rot'] = data['rot'][:,:frameLen]

        faceParam_list_new.append(data)


    #faceMesh_list = GetFaceMesh(g_faceModel,faceParam_list, bComputeNormal= bComputeNormal)
    faceMesh_list = GetFaceMesh(g_faceModel,faceParam_list_new, bComputeNormal= bComputeNormal,bApplyTrans=(trans is not None),bApplyRot=(rot is not None), bApplyRotFlip=(rot is not None))
    etMeshData( faceMesh_list)

'''
# D. Holden's format
'''
def demo_holden_data():
    # X = np.load('/ssd/codes/holden_synthesis/motionsynth_code/data/processed/data_cmu.npz')['clips'] #(17944, 240, 73)
    #X = np.load('/ssd/codes/holden_synthesis/motionsynth_code/data/processed/data_edin_kinect.npz')['clips'] #(17944, 240, 73)
    X = np.load('/ssd/codes/holden_synthesis/motionsynth_code/data/processed/data_edin_locomotion.npz')['clips'] #(17944, 240, 73)
    #X = np.load('/ssd/codes/holden_synthesis/motionsynth_code/data/processed/data_hdm05.npz')['clips'] #(17944, 240, 73)
    #X = np.load('/ssd/codes/holden_synthesis/motionsynth_code/data/processed/data_mhad.npz')['clips'] #(17944, 240, 73)
    X = np.swapaxes(X, 1, 2).astype(np.float32) #(17944, 73, 240)
    #set_Holden_Data_73([ X[0,:,:], X[1,:,:], X[2,:,:] ], ignore_root=True)
    set_Holden_Data_73([ X[0,:,:], X[1,:,:], X[2,:,:] ], ignore_root=False)

    set_Holden_Trajectory_3([ X[0,-7:-4,:], X[1,-7:-4,:], X[2,-7:-4,:] ])

'''
# D. Holden's format of Panoptic Studio Data
'''
def demo_holdenFormat_panoptic():
    datasetName = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed/data_hagglingSellers_speech_body_bySequence_white_noGa_testing_tiny.pkl'
    pkl_file = open(datasetName, 'rb')
    X = pickle.load(pkl_file, encoding='latin1')
    pkl_file.close()

    X_data = X['data']      #X_data[0]: (subjectNum:3, frames, featureDim:73)
    X_speech = X['speech']
    X_initInfo = X['initInfo']

    sceneIdx=0
    bodyData = [ X_data[sceneIdx][0,:,:], X_data[sceneIdx][1,:,:], X_data[sceneIdx][2,:,:] ]  #(frames, 73)

    # #Apply global rot,trans information of the original seqeunce
    # for i,X in enumerate(bodyData):
    #     skel_22  = np.reshape(bodyData[i][0,:-7],(-1,22,3)).copy()  #(frames,22,3)
    #     initTrans = X_initInfo[i]['pos'][1,:]       #(22,3) -> (3,)
    #     initRot = X_initInfo[i]['rot']      #qs values of a quaternion

    #     #initRot = np.repeat(initRot,numFrames,axis=0)
        #initRot = Quaternions(initRot)[:,np.newaxis]    #(frames,1)

        #skel_22 = initRot*skel_22     #Quaternion x (frames,22,3)
        # skel_22[0,:,0] += initTrans[0]
        # skel_22[0-,:,2] += initTrans[2]      #ignoring Y

        #bodyData[i][0,:-7] = np.reshape(skel_22,(-1,22*3))



    for i,X in enumerate(bodyData):
        bodyData[i] =  np.swapaxes(X, 0, 1).astype(np.float32) #(73, frames)

    initTrans = [X_initInfo[sceneIdx][0]['pos'], X_initInfo[sceneIdx][1]['pos'], X_initInfo[sceneIdx][2]['pos']]

    initRot = [X_initInfo[sceneIdx][0]['rot'], X_initInfo[sceneIdx][1]['rot'], X_initInfo[sceneIdx][2]['rot']]
    initRot = [ Quaternions(x) for x in initRot ]

    set_Holden_Data_73(bodyData, ignore_root=False, initRot=initRot, initTrans= initTrans, bIsGT= True)
    set_Holden_Trajectory_3([ bodyData[0][-7:-4,:], bodyData[1][-7:-4,:], bodyData[2][-7:-4,:] ], initRot=initRot, initTrans= initTrans)


    # set_Holden_Data_73(bodyData, ignore_root=False)
    # set_Holden_Trajectory_3([ bodyData[0][-7:-4,:], bodyData[1][-7:-4,:], bodyData[2][-7:-4,:] ])
    #set_Holden_Trajectory_3([  bodyData[0][-7:-4,:] ] )


'''
    Input:
        face_list:  faceNum x element['face70'](210, frames)
    Output:
        faceNormal_list:
        face_list:  faceNum x (3, frames)
'''
def ComputeFaceNormal(face_list):
    ##Compute face normal
    faceNormal_list =[]
    for s in face_list:
        leftEye = s['face70'][(45*3):(45*3+3),:].transpose() #210xframes
        rightEye = s['face70'][(36*3):(36*3+3),:].transpose() #210xframes
        nose = s['face70'][(33*3):(33*3+3),:].transpose() #210xframes

        left2Right = rightEye - leftEye
        right2nose = nose - rightEye

        from sklearn.preprocessing import normalize
        left2Right = normalize(left2Right, axis=1)
        #Check: np.linalg.norm(left2Right,axis=1)
        right2nose = normalize(right2nose, axis=1)

        faceNormal = np.cross(left2Right,right2nose)
        faceNormal[:,1] = 0 #Project on x-z plane, ignoring y axis
        faceNormal = normalize(faceNormal, axis=1)
        faceNormal_list.append(faceNormal.transpose())

    return faceNormal_list


'''
    Input:
        body_list:  bodyNum x element['joints19'](21, frames)
    Output:
        faceNormal_list:
        face_list:  bodyNum x (3, frames)
'''
def ComputeBodyNormal_panoptic(body_list):
     #Compute Body Normal
    bodyNormal_list =[]
    for s in body_list:
        leftShoulder = s['joints19'][(3*3):(3*3+3),:].transpose() #210xframes
        rightShoulder = s['joints19'][(9*3):(9*3+3),:].transpose() #210xframes
        bodyCenter = s['joints19'][(2*3):(2*3+3),:].transpose() #210xframes

        left2Right = rightShoulder - leftShoulder
        right2center = bodyCenter - rightShoulder

        from sklearn.preprocessing import normalize
        left2Right = normalize(left2Right, axis=1)
        #Check: np.linalg.norm(left2Right,axis=1)
        right2center = normalize(right2center, axis=1)

        bodyNormal = np.cross(left2Right,right2center)
        bodyNormal[:,1] = 0 #Project on x-z plane, ignoring y axis
        bodyNormal = normalize(bodyNormal, axis=1)
        bodyNormal_list.append(bodyNormal.transpose())
    return bodyNormal_list

'''
# Panoptic Studio Data
'''
def demo_panoptic_data_haggling():

    #fileName = '170224_haggling_b2_group3.pkl'  #interesting
    #fileName = '170221_haggling_m1_group0.pkl'
    #fileName = '170228_haggling_b1_group9.pkl'
    fileName = '170228_haggling_b1_group6.pkl'
    #fileName = '170221_haggling_b1_group3.pkl'
    #fileName = '170221_haggling_b1_group3.pkl'

    ##read face
    seqPath = 'data/haggling/panopticDB_face_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    setFace([motionData['subjects'][0]['face70'], motionData['subjects'][1]['face70'], motionData['subjects'][2]['face70']])
    ##Compute face normal
    setFaceNormal([motionData['subjects'][0]['normal'], motionData['subjects'][1]['normal'], motionData['subjects'][2]['normal']])

    ##read hand
    seqPath = 'data/haggling/panopticDB_hand_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    if 'hand_left' in motionData:
        setHand_left([motionData['hand_left'][0]['hand21'], motionData['hand_left'][1]['hand21'], motionData['hand_left'][2]['hand21']])

    if 'hand_right' in motionData:
        setHand_right([motionData['hand_right'][0]['hand21'], motionData['hand_right'][1]['hand21'], motionData['hand_right'][2]['hand21']])

    #read speech
    seqPath = 'data/haggling/panopticDB_speech_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    setSpeech([motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]])

    #read body
    seqPath = 'data/haggling/panopticDB_body_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    setSkeleton([motionData['subjects'][0]['joints19'], motionData['subjects'][1]['joints19'], motionData['subjects'][2]['joints19']])


    """Visualize formations"""
    #Visualize Pos only
    setPosOnly([motionData['subjects'][0]['joints19'][:3,:], motionData['subjects'][1]['joints19'][:3,:], motionData['subjects'][2]['joints19'][:3,:]])

    
    #Visualize Body Normal
    setBodyNormal([motionData['subjects'][0]['bodyNormal'], motionData['subjects'][1]['bodyNormal'], motionData['subjects'][2]['bodyNormal']])
    setFaceNormal([motionData['subjects'][0]['faceNormal'], motionData['subjects'][1]['faceNormal'], motionData['subjects'][2]['faceNormal']])

    show()



'''
# Panoptic Studio Data
'''
def demo_panoptic_data_haggling_meshes():
    #import pickle #this is slower

    fileName = '170221_haggling_b1_group0.pkl'  #interesting
    #fileName = '170221_haggling_m1_group0.pkl'

    ##read face
    # seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_face_pkl_hagglingProcessed/' +fileName
    # motionData = pickle.load( open( seqPath, "rb" ) )
    # setFace([motionData['subjects'][0]['face70'], motionData['subjects'][1]['face70'], motionData['subjects'][2]['face70']])

    ##Compute face normal
    #setFaceNormal([motionData['subjects'][0]['normal'], motionData['subjects'][1]['normal'], motionData['subjects'][2]['normal']])

    # ##read hand
    # seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_hand_pkl_hagglingProcessed/' +fileName
    # motionData = pickle.load( open( seqPath, "rb" ) )
    # if 'hand_left' in motionData:
    #     setHand_left([motionData['hand_left'][0]['hand21'], motionData['hand_left'][1]['hand21'], motionData['hand_left'][2]['hand21']])

    # if 'hand_right' in motionData:
    #     setHand_right([motionData['hand_right'][0]['hand21'], motionData['hand_right'][1]['hand21'], motionData['hand_right'][2]['hand21']])


    #read body
    # seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_pkl_hagglingProcessed/' +fileName
    # motionData = pickle.load( open( seqPath, "rb" ) )
    # setSkeleton([motionData['subjects'][0]['joints19'], motionData['subjects'][1]['joints19'], motionData['subjects'][2]['joints19']])

    #Read body, holden's format
    fileName_npz = fileName.replace('pkl','npz')
    X = np.load('/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed/panoptic_npz/' + fileName_npz)['clips'] #(17944, 240, 73)
    X = np.swapaxes(X, 1, 2).astype(np.float32) #(17944, 73, 240)
    set_Holden_Data_73([ X[0,:,:], X[1,:,:], X[2,:,:] ], ignore_root=True)

    #Read Face mesh
    ##read face mesh parameter
    seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl_hagglingProcessed/' +fileName
    faceData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')

    import scipy.io as sio
    faceModel = sio.loadmat('/ssd/data/totalmodel/face_model_totalAligned.mat')

    ## Debug: visualize just a short clip
    visLength = 100
    for f in faceData['subjects']:
        f['face_exp'] =  f['face_exp'][:,:visLength]
        f['face_id'] =  f['face_id'][:,:visLength]
        f['rot'] =  f['rot'][:,:visLength]
        f['rot_pivot'] =  f['rot_pivot'][:,:visLength]
        f['trans'] =  f['trans'][:,:visLength]


    #faceMesh_list = GetFaceMesh(faceModel,faceData['subjects'], bApplyRot = True, bApplyTrans = True)
    faceMesh_list = GetFaceMesh(faceModel,faceData['subjects'], bApplyRot = False, bApplyTrans = False)
    etMeshData( faceMesh_list)

    #read speech
    seqPath = '/ssd/codes/haggling_audio/panopticDB_pkl_speech_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    speechData = [motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]]
    #setSpeech([motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]])
    speech_rootData = [faceMesh_list[0]['centers'], faceMesh_list[1]['centers'], faceMesh_list[2]['centers']]
    speech_rootData =np.multiply(speech_rootData, 100.0) #meter to cm
    setSpeech_withRoot(speechData,speech_rootData)


def getFaceRootCenter():
    global g_meshes

    speech_rootData = []

    for f in g_meshes:

        speech_rootData.append(f['centers'])
    return speech_rootData




#Todo: move this to Utility.py
# vertices: frames x meshVerNum x 3
# trifaces: facePolygonNum x 3 = 22800 x 3
def ComputeNormal(vertices, trifaces):

    if vertices.shape[0] > 5000:
        print('ComputeNormal: Warning: too big to compute {0}'.format(vertices.shape) )
        return

    #compute vertex Normals for all frames
    U = vertices[:,trifaces[:,1],:] - vertices[:,trifaces[:,0],:]  #frames x faceNum x 3
    V = vertices[:,trifaces[:,2],:] - vertices[:,trifaces[:,1],:]  #frames x faceNum x 3
    originalShape = U.shape  #remember: frames x faceNum x 3

    U = np.reshape(U, [-1,3])
    V = np.reshape(V, [-1,3])
    faceNormals = np.cross(U,V)     #frames x 13776 x 3
    from sklearn.preprocessing import normalize

    if np.isnan(np.max(faceNormals)):
        print('ComputeNormal: Warning nan is detected {0}')
        return
    faceNormals = normalize(faceNormals)

    faceNormals = np.reshape(faceNormals, originalShape)

    vertex_normals = np.zeros(vertices.shape) #(frames x 11510) x 3
    for fIdx, vIdx in enumerate(trifaces[:,0]):
       vertex_normals[:,vIdx,:] += faceNormals[:,fIdx,:]
    for fIdx, vIdx in enumerate(trifaces[:,1]):
        vertex_normals[:,vIdx,:] += faceNormals[:,fIdx,:]
    for fIdx, vIdx in enumerate(trifaces[:,2]):
        vertex_normals[:,vIdx,:] += faceNormals[:,fIdx,:]

    # # Computing vertex normals, much faster (and obscure) replacement
    # index = np.vstack((np.ravel(trifaces), np.repeat(np.arange(len(trifaces)), 3))).T
    # index_sorted = index[index[:,0].argsort()]
    # vertex_normals = np.add.reduceat(faceNormals[:,index_sorted[:, 1],:][0],
    #     np.concatenate(([0], np.cumsum(np.unique(index_sorted[:, 0],
    #     return_counts=True)[1])[:-1])))[None, :]

    originalShape = vertex_normals.shape
    vertex_normals = np.reshape(vertex_normals, [-1,3])
    vertex_normals = normalize(vertex_normals)
    vertex_normals = np.reshape(vertex_normals,originalShape)

    return vertex_normals


def ComputeNormal_gpu(vertices, trifaces):
    import torch
    import torch.nn.functional as F

    if vertices.shape[0] > 5000:
        print('ComputeNormal: Warning: too big to compute {0}'.format(vertices.shape) )
        return

    #compute vertex Normals for all frames
    #trifaces_cuda = torch.from_numpy(trifaces.astype(np.long)).cuda()
    vertices_cuda = torch.from_numpy(vertices.astype(np.float32)).cuda()

    U_cuda = vertices_cuda[:,trifaces[:,1],:] - vertices_cuda[:,trifaces[:,0],:]  #frames x faceNum x 3
    V_cuda = vertices_cuda[:,trifaces[:,2],:] - vertices_cuda[:,trifaces[:,1],:]  #frames x faceNum x 3
    originalShape = list(U_cuda.size())  #remember: frames x faceNum x 3

    U_cuda = torch.reshape(U_cuda, [-1,3])#.astype(np.float32)
    V_cuda = torch.reshape(V_cuda, [-1,3])#.astype(np.float32)

    faceNormals = U_cuda.cross(V_cuda)
    faceNormals = F.normalize(faceNormals,dim=1)

    faceNormals = torch.reshape(faceNormals, originalShape)

    # trifaces has duplicated vertex index, so cannot be parallazied
    # vertex_normals = torch.zeros(vertices.shape,dtype=torch.float32).cuda() #(frames x 11510) x 3
    # for fIdx, vIdx in enumerate(trifaces[:,0]):
    #    vertex_normals[:,vIdx,:] += faceNormals[:,fIdx,:]
    # for fIdx, vIdx in enumerate(trifaces[:,1]):
    #     vertex_normals[:,vIdx,:] += faceNormals[:,fIdx,:]
    # for fIdx, vIdx in enumerate(trifaces[:,2]):
    #     vertex_normals[:,vIdx,:] += faceNormals[:,fIdx,:]

    # Computing vertex normals, much faster (and obscure) replacement
    index = np.vstack((np.ravel(trifaces), np.repeat(np.arange(len(trifaces)), 3))).T
    index_sorted = index[index[:,0].argsort()]
    vertex_normals = np.add.reduceat(faceNormals[:,index_sorted[:, 1],:][0],
        np.concatenate(([0], np.cumsum(np.unique(index_sorted[:, 0],
        return_counts=True)[1])[:-1])))[None, :]
    vertex_normals = torch.from_numpy(vertex_normals).float().cuda()

    vertex_normals = F.normalize(vertex_normals,dim=2)
    vertex_normals = vertex_normals.data.cpu().numpy()  #(batch, chunksize, dim)

    return vertex_normals


#####################################################
### FaceOnly Model Visualization (todo. move this to another file)
# Input:
# - bApplyRot: if True, apply global face orientation
# Output:
# - 'ver': (frames, 11510, 3)
# - 'normal': (frames, 11510, 3)
# - 'f': (22800,3)
# - 'centers': (frames,3)
from modelViewer.batch_lbs import batch_rodrigues


import scipy.io as sio
def GetFaceMesh(faceModel, faceParam_list, bComputeNormal = True, bApplyRot = False, bApplyTrans = False, bShowFaceId = False, bApplyRotFlip=False):

    MoshParam_list = []

    v_template = faceModel['v_template'] #11510 x 3
    v_template_flat = v_template.flatten()  #(34530,)
    v_template_flat = v_template_flat[:,np.newaxis] #(34530,1)  for broadcasting

    trifaces = faceModel['trifaces']  #22800 x 3

    U_id = faceModel['U_id'] #34530 x 150
    U_exp = faceModel['U_exp'] #34530 x 200


    for i, faceParam in enumerate(faceParam_list):

        print('processing: humanIdx{0}/{1}'.format(i, len(faceParam_list) ))
        #faceParam = faceParam_all[humanIdx]


        #Debug: only use the first 5
        faceParam['face_exp'][5:,:]=0

        """Computing face vertices for all frames simultaneously"""
        face_exp_component = np.matmul(U_exp, faceParam['face_exp']) #(34,530 x 200)  x  (200 x frames)

        v_face_allFrames = v_template_flat + face_exp_component  #(34530 x frames). Ignore face Identity information

        if bShowFaceId:
            face_id_component = np.matmul(U_id, faceParam['face_id']) #(34,530 x 150)  x  (150 x frames)
            v_face_allFrames += face_id_component #(34530 x frames)
            #v_face_allFrames = v_template_flat+ face_id_component +face_exp_component  #(34530 x frames)

        v_face_allFrames = v_face_allFrames.swapaxes(0,1) # (frames, 34530)
        v_face_allFrames = np.reshape(v_face_allFrames,[v_face_allFrames.shape[0], -1, 3]) # (frames, 11510, 3)


        faceMassCenter = np.zeros((3,faceParam['face_exp'].shape[1]))#*0.0 #(3, frames)
        if 'rot_pivot' in faceParam.keys():


            rot_pivot = np.swapaxes(faceParam['rot_pivot'],0,1) #(frames,3)
            rot_pivot = np.expand_dims(rot_pivot,1)  #(frames,1, 3)

            v_face_allFrames = v_face_allFrames - rot_pivot     # (frames, 11510, 3)

        if bApplyRot:
            #Apply rotationsvf
            global_rot = None
            #computing global rotation
            global_rot =  batch_rodrigues(np.swapaxes(faceParam['rot'],0,1)) #input (Nx3), output: (N,3,3)



            #global_rot *( v_face_allFrames - rot_pivot)
            for f in range(v_face_allFrames.shape[0]):

                pts = np.swapaxes(v_face_allFrames[f,:,:],0,1) # (3,11510)

                if bApplyRotFlip:
                    #Flip
                    rot = np.array( [ 0, -1, 0,  1,  0,  0, 0, 0, 1])
                    rot = np.reshape(rot,(3,3))
                    pts =  np.matmul( rot, pts)  # (3,3)  x (11510,3) =>(3,11510)
                    pts =  np.matmul( rot, pts)  # (3,3)  x (11510,3) =>(3,11510)
                    pts *= 0.94


                # rot = np.array( [ 0, -1,  0, 1,  0,  0,0,  0,  1])
                # rot = np.reshape(rot,(3,3))
                rot = global_rot[f,:,:]
                pts =  np.matmul( rot, pts)  # (3,3)  x (11510,3) =>(3,11510)

                v_face_allFrames[f,:,:] = pts.transpose()
        else:   #Rotate 180 degrees to flip y axis
            #global_rot =  batch_rodrigues(np.swapaxes(faceParam['rot'],0,1)) #input (Nx3), output: (N,3,3)

            #global_rot *( v_face_allFrames - rot_pivot)
            for f in range(v_face_allFrames.shape[0]):

                pts = np.swapaxes(v_face_allFrames[f,:,:],0,1) # (3,11510)

                #rot = np.array( [ 1, 0, 0,  0, 1,  0,  0, 0, -1])
                #rot = np.array( [ 1, 0, 0,  0, 1,  0,  0, 0, -1])
                rot = np.array( [ 0, -1, 0,  1,  0,  0, 0, 0, 1])
                #rot = np.array( [ 0, 1, 0,  1,  0,  0, 0, 0, 1])
                rot = np.reshape(rot,(3,3))
                #rot = global_rot[f,:,:]
                pts =  np.matmul( rot, pts)  # (3,3)  x (11510,3) =>(3,11510)
                pts =  np.matmul( rot, pts)  # (3,3)  x (11510,3) =>(3,11510)

                #trans = np.array([[0.0,-1.5,0.2]])
                trans = np.array([[0.0,-1,0.2]])
                v_face_allFrames[f,:,:] = pts.transpose() +trans


        if bApplyTrans:
            trans = np.swapaxes(faceParam['trans'],0,1) #(frames,3)
            trans = np.expand_dims(trans,1)  #(frames,1, 3)
            v_face_allFrames = v_face_allFrames + trans     # (frames, 11510, 3)


            faceMassCenter += faceParam['trans'] #(3, frames)


        if bComputeNormal==False:
            #Debug. no normal
            faceMassCenter = v_face_allFrames[:,5885,:] #5885th vertex. around the head top.
            MoshParam = {'ver': v_face_allFrames, 'normal': [], 'f': trifaces, 'centers': faceMassCenter}  # support rendering two models together
            MoshParam_list.append(MoshParam)
            continue


        # # CPU version
        start = time.time()
        vertex_normals = ComputeNormal(v_face_allFrames, trifaces)
        print("CPU: normal computing time: {}".format( time.time() - start))

        # GPU version
        # start = time.time()
        # vertex_normals = ComputeNormal_gpu(v_face_allFrames, trifaces)
        # print("GPU: normal computing time: {}".format( time.time() - start))


        faceMassCenter = v_face_allFrames[:,5885,:] #5885th vertex. around the head top.
        #faceMassCenter = np.swapaxes(faceMassCenter,0,1) # (3,frames) - >(frames,3)

        MoshParam = {'ver': v_face_allFrames, 'normal': vertex_normals, 'f': trifaces, 'centers': faceMassCenter}  # support rendering two models together
        MoshParam_list.append(MoshParam)

    return MoshParam_list

"""Visualization of Face model from facewarehouse fitting results"""
def demo_panoptic_faceModel_pkl():

    """Load Face data"""
    import scipy.io as sio
    # faceModel = sio.loadmat('/ssd/data/totalmodel/face_model_totalAligned.mat')
    faceModel = sio.loadmat('models/face_model_totalAligned.mat')
    # v_template = faceModel['v_template'] #11510 x 3
    # trifaces = faceModel['trifaces']  #22800 x 3

    # U_id = faceModel['U_id'] #34530 x 150
    # U_exp = faceModel['U_exp'] #34530 x 200
    # v_template_flat = v_template.flatten()  #(34530,)
    # v_template_flat = v_template_flat[:,np.newaxis] #(34530,1)  for broadcasting

    #Load Face Data
    pklfile = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl/170224_haggling_a1.pkl'
    with open(pklfile, 'rb') as f:
        faceParam_all = pickle.load(f, encoding='latin1')

    # targetHuman = [0,1,2]
    #targetHuman = [3,4,5]
    #targetHuman = [6,7,8]

    targetHuman = [9, 10, 11]

    start = time.time()

    faceParam_selected =[]
    for humanIdx in targetHuman:
        faceParam_selected.append(faceParam_all[humanIdx])

    MoshParam_list = GetFaceMesh(faceModel,faceParam_selected)
    etMeshData( MoshParam_list)

    init_gl()

"""Visualization of Face model from facewarehouse fitting results"""
def demo_panoptic_faceModel_pkl_haggling():

    #import pickle #this is slower

    #fileName = '170224_haggling_b2_group3.pkl'  #interesting
    fileName = '170407_haggling_a2_group3_facemesh.pkl'

    ##read face mesh parameter
    # seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl_hagglingProcessed/' +fileName
    seqPath = 'samples/' +fileName
    faceData = pickle.load( open( seqPath, "rb" ), encoding='latin1')

    #Debug: visualize just a short clip
    visLength = 10
    for f in faceData['subjects']:
        f['face_exp'] =  f['face_exp'][:,:visLength]
        f['face_id'] =  f['face_id'][:,:visLength]
        f['rot'] =  f['rot'][:,:visLength]
        f['rot_pivot'] =  f['rot_pivot'][:,:visLength]
        f['trans'] =  f['trans'][:,:visLength]

    import scipy.io as sio
    # faceModel = sio.loadmat('/ssd/data/totalmodel/face_model_totalAligned.mat')
    faceModel = sio.loadmat('models/face_model_totalAligned.mat')

    #faceMesh_list = GetFaceMesh(faceModel,faceData['subjects'], bApplyRot = True, bApplyTrans = True)
    faceMesh_list = GetFaceMesh(faceModel,faceData['subjects'],  bComputeNormal = True, bApplyRot = False, bApplyTrans = False)
    etMeshData( faceMesh_list)

    # #read speech
    # seqPath = '/ssd/codes/haggling_audio/panopticDB_pkl_speech_hagglingProcessed/' +fileName
    # motionData = pickle.load( open( seqPath, "rb" ) )
    # #setSpeech([motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]])
    # speechData = [motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]]
    # speech_rootData = [faceMesh_list[0]['centers'], faceMesh_list[1]['centers'], faceMesh_list[2]['centers']]
    # speech_rootData =np.multiply(speech_rootData, 100.0) #meter to cm

    # setSpeech_withRoot(speechData,speech_rootData)

    init_gl()
    ##glvis.smpl_render_test.main()

### End of Face Mesh Model (todo. move this to another file)
#####################################################


""" Visualization of ADAM model with Panoptic Studio Dataset """
def demo_panoptic_AdamModel_multiFrames():

    from modelViewer.batch_adam import ADAM

    """Load Adam data"""
    adamWrapper = ADAM()

    # """Check All Adam fitting files"""
    # import glob
    # datadir = '/ssd/data/panoptic-toolbox/data_haggling/170224_haggling_a1/hdPose3d_Adam_stage0'
    # adamParamFiles = glob.glob(os.path.join(datadir, '*pkl'))
    # adamParamFiles.sort()

    #seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_adamMesh_pkl/170221_haggling_m1.pkl'
    seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_adamMesh_pkl_hagglingProcessed_stage1/170221_haggling_b1_group0.pkl'
    adamParam_all = pickle.load( open( seqPath, "rb" ) , encoding='latin1')

    """Load Facefitting files"""
    fileName = '170221_haggling_b1_group0.pkl'

    ##read face mesh parameter
    seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl_hagglingProcessed/' +fileName
    faceData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')



    start = time.time()
    #targetHuman = [0,1,2]

    # faceParam_selected =[]
    # for humanIdx in targetHuman:
    #     faceParam_selected.append(adamParam_all[humanIdx])

    meshes =[]
    frameStart = 0
    frameEnd = 200
    #for faceParam in faceParam_selected:
    for adamParam in adamParam_all['subjects']:

        betas = np.swapaxes(adamParam['betas'],0,1)[frameStart:frameEnd]  #Frames  x30
        faces = np.swapaxes(adamParam['faces'],0,1)[frameStart:frameEnd]  #Frames  200


        for faceParam in faceData['subjects']:
            if faceParam['humanId'] == adamParam['humanId']:
                faces = faceParam['face_exp']
                faces = np.swapaxes(faces,0,1)[frameStart:frameEnd]  #Frames  200
                break

        pose = np.swapaxes(adamParam['pose'],0,1)[frameStart:frameEnd]  #Frames  186
        trans = np.swapaxes(adamParam['trans'],0,1)[frameStart:frameEnd]  #Frames  x3
        startTime = time.time()
        v , j = adamWrapper(betas,pose,faces) #v:(frameNum, 18540, 3), j: (frameNum, 62, 3)
        print('time: {}'.format(time.time()-startTime))
        v += np.expand_dims(trans, axis=1)  # no translation in their LBS. trans: (humanNumn,30) ->(humanNumn,1, 30)

        v *=0.01

        normals = ComputeNormal(v, adamWrapper.f)
        meshes.append( {'ver': v, 'normal': normals, 'f': adamWrapper.f})  # support rendering two models together

    etMeshData( meshes)

    init_gl()


def LoadFrankMesh():

    if(os.path.exists("frank_default_mesh.pkl")):
        frank = pickle.load(open( "frank_default_mesh.pkl", "rb" ) , encoding='latin1')
        return frank

    import objLoader
    ## Load Adam Model
    # import pywavefront
    # scene = pywavefront.Wavefront('/ssd/data/totalmodel/nofeetmesh_byTomas.obj')
    mesh = objLoader.OBJ('/ssd/data/totalmodel/nofeetmesh_byTomas.obj')
    faces = [ x[0] for x in mesh.faces]
    faces = np.array(faces)
    faces = faces-1 #zero index

    vertices = np.array(mesh.vertices)

    # normals = mesh.normals
    # normals = np.array(normals)
    # from sklearn.preprocessing import normalize
    # normalize(normals)

    #calculating normals
    from sklearn.preprocessing import normalize
    normals = np.zeros(vertices.shape)
    U = vertices[faces[:,1]] - vertices[faces[:,0]]
    V = vertices[faces[:,2]] - vertices[faces[:,1]]

    Nor = np.cross(U,V)
    Nor = normalize(Nor)

    normals[faces[:,0]] += Nor
    normals[faces[:,1]] += Nor
    normals[faces[:,2]] += Nor
    normals = normalize(normals)

    #Save as pkl
    frank =  {'vertices': vertices, 'normals':normals , 'faces': faces}
    # pickle.dump( frank, open( "frank_default_mesh.pkl", "wb" ) )
    return frank

def LoadAdamModel():

    if(os.path.exists("adamModel_348.pkl")):
        adam = pickle.load(open( "adamModel_348.pkl", "rb" ) , encoding='latin1')
        return adam


    frank = pickle.load(open( "frank_default_mesh.pkl", "rb" ) , encoding='latin1')
    import scipy.io as sio
    # adamModel = sio.loadmat('/ssd/data/totalmodel/adam_v1_plus2.mat')
    # adamModel = sio.loadmat('/ssd/data/totalmodel/adam_v1_plus2.mat')
    adamModel_info = sio.loadmat('/ssd/data/totalmodel/adam_blendshapes_348_delta_norm_bugfixed.mat')

    #adamModel_info['mu'] #55620 x 1 where 55620 = 18540 *3
    #adamModel_info['Uw1']  #55620 x 348

    #adamModel_info['Ds']  #348 x 1
    ADAM_SHAPE_COEFF_NUM = 30

    adam = dict()
    adam['mu'] = adamModel_info['mu'] #55620 x 1
    adam['faces'] = frank['faces'] #36946 x 3
    adam['U'] = adamModel_info['Uw1'][:,ADAM_SHAPE_COEFF_NUM] #55620 x ADAM_SHAPE_COEFF_NUM
    pickle.dump( adam, open( "adamModel_348.pkl", "wb" ) )

    return adam




#####################################################
### Haggling video rendering/generation

def LoadHagglingDataKeypoints(fileName):
    global g_hagglingSeqName
    g_hagglingSeqName = fileName[:-4]
    ##read face
    seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_face_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    if 'subjects' in motionData.keys() and len(motionData['subjects'])==3:
        setFace([motionData['subjects'][0]['face70'], motionData['subjects'][1]['face70'], motionData['subjects'][2]['face70']])
    else:
        setFace(None)


    ##read hand
    seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_hand_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    if 'hand_left' in motionData:
        if len(motionData['hand_left'])==3:
            setHand_left([motionData['hand_left'][0]['hand21'], motionData['hand_left'][1]['hand21'], motionData['hand_left'][2]['hand21']])
        else:
            setHand_left(None)


    if 'hand_right' in motionData:
        if len(motionData['hand_right'])==3:
            setHand_right([motionData['hand_right'][0]['hand21'], motionData['hand_right'][1]['hand21'], motionData['hand_right'][2]['hand21']])
        else:
            setHand_right(None)

    #read speech
    seqPath = '/ssd/codes/haggling_audio/panopticDB_pkl_speech_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    setSpeech([motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]])

    #read body
    seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_pkl_hagglingProcessed/' +fileName
    motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
    setSkeleton([motionData['subjects'][0]['joints19'], motionData['subjects'][1]['joints19'], motionData['subjects'][2]['joints19']])

    #Visualize Body Normal
    setBodyNormal([motionData['subjects'][0]['bodyNormal'], motionData['subjects'][1]['bodyNormal'], motionData['subjects'][2]['bodyNormal']])
    setFaceNormal([motionData['subjects'][0]['faceNormal'], motionData['subjects'][1]['faceNormal'], motionData['subjects'][2]['faceNormal']])


g_adamWrapper = None
def LoadHagglingData(fileName):
    global g_hagglingSeqName
    g_hagglingSeqName = fileName[:-4]

    bLoadFace = False
    bLoadAdam = True
    bLoadSkeleton = False
    bLoadKeypoints = False


    fileName_pkl = fileName.replace('npz','pkl')

    if bLoadFace :
        """Load Face data"""
        global g_faceModel
        if g_faceModel is None:
            import scipy.io as sio
            g_faceModel = sio.loadmat('/ssd/data/totalmodel/face_model_totalAligned.mat')

        ##read face mesh parameter
        seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl_hagglingProcessed/' +fileName_pkl

        faceData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')

        FaceParam_list = GetFaceMesh(g_faceModel,faceData['subjects'])
        setMeshData( FaceParam_list)

        # #read speech
        # seqPath = '/ssd/codes/haggling_audio/panopticDB_pkl_speech_hagglingProcessed/' +fileName
        # motionData = pickle.load( open( seqPath, "rb" ) )
        # setSpeech([motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]])

        #read speech
        seqPath = '/ssd/codes/haggling_audio/panopticDB_pkl_speech_hagglingProcessed/' +fileName_pkl
        motionData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')
        speechData = [motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]]
        #setSpeech([motionData['speechData'][0], motionData['speechData'][1], motionData['speechData'][2]])
        speech_rootData = [FaceParam_list[0]['centers'], FaceParam_list[1]['centers'], FaceParam_list[2]['centers']]
        speech_rootData =np.multiply(speech_rootData, 100.0) #meter to cm
        setSpeech_withRoot(speechData,speech_rootData)

    if bLoadSkeleton:
        """Load Skeleton data (Holden's format)"""

        #Read body, holden's format
        #fileName_npz = fileName.replace('pkl','npz')
        X = np.load('/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed/panoptic_npz/' + fileName)['clips'] #(17944, 240, 73)
        X = np.swapaxes(X, 1, 2).astype(np.float32) #(17944, 73, 240)
        set_Holden_Data_73([ X[0,:,:], X[1,:,:], X[2,:,:] ], ignore_root=True)
    if bLoadKeypoints:
        LoadHagglingDataKeypoints(fileName_pkl)

    if bLoadAdam:

        from modelViewer.batch_adam import ADAM
        global g_adamWrapper

        """Load Adam data"""
        if g_adamWrapper==None:
            g_adamWrapper = ADAM()

        fileName_pkl = fileName.replace('npz','pkl')

        seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_adamMesh_pkl_hagglingProcessed_stage1/' +fileName_pkl
        adamParam_all = pickle.load( open( seqPath, "rb" ) , encoding='latin1')

         ##read face mesh parameter
        seqPath = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl_hagglingProcessed/' +fileName_pkl
        faceData = pickle.load( open( seqPath, "rb" ) , encoding='latin1')

        start = time.time()
        meshes =[]
        frameStart = 0
        frameEnd = -1

        #for faceParam in faceParam_selected:
        for adamParam in adamParam_all['subjects']:

            betas = np.swapaxes(adamParam['betas'],0,1)[frameStart:frameEnd]  #Frames  x30
            faces = np.swapaxes(adamParam['faces'],0,1)[frameStart:frameEnd]  #Frames  200

            for faceParam in faceData['subjects']:
                if faceParam['humanId'] == adamParam['humanId']:
                    faces = faceParam['face_exp']
                    faces = np.swapaxes(faces,0,1)[frameStart:frameEnd]  #Frames  200

                    break

            pose = np.swapaxes(adamParam['pose'],0,1)[frameStart:frameEnd]  #Frames  186
            trans = np.swapaxes(adamParam['trans'],0,1)[frameStart:frameEnd]  #Frames  x3
            startTime = time.time()

            #Align the length
            frameNum = min([pose.shape[0], faces.shape[0], betas.shape[0], trans.shape[0]])
            pose = pose[:frameNum]
            faces = faces[:frameNum]
            betas = betas[:frameNum]
            trans = trans[:frameNum]


            v , j = g_adamWrapper(betas,pose,faces) #v:(frameNum, 18540, 3), j: (frameNum, 62, 3)
            print('time: {}'.format(time.time()-startTime))
            v += np.expand_dims(trans, axis=1)  # no translation in their LBS. trans: (humanNumn,30) ->(humanNumn,1, 30)

            v *=0.01

            normals = ComputeNormal(v, g_adamWrapper.f)
            meshes.append( {'ver': v, 'normal': normals, 'f': g_adamWrapper.f})  # support rendering two models together


        setMeshData( meshes)


g_hagglingFileList = None
g_hagglingFileListIdx = -1
def LoadHagglingData_Caller():

    global g_hagglingFileList,g_hagglingFileListIdx,g_frameIdx

    if g_hagglingFileList==None: #If initial calling
        #directory = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_faceMesh_pkl_hagglingProcessed/'
        # directory = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_pkl_hagglingProcessed/'
        #directory = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed_panoptic/panopticDB_adamMesh_pkl_hagglingProcessed/'
        #g_hagglingFileList =  [f for f in sorted(list(os.listdir(directory))) if os.path.isfile(os.path.join(directory,f)) and f.endswith('.pkl')]

        #directory = '/ssd/codes/haggling_audio/panopticDB_pkl_speech_hagglingProcessed/'
        directory = '/ssd/codes/pytorch_motionSynth/motionsynth_data/data/processed/panoptic_npz/'
        g_hagglingFileList =  [f for f in sorted(list(os.listdir(directory))) if os.path.isfile(os.path.join(directory,f)) and f.endswith('.npz')]

        hagglingFileList_final = list()
        for f in g_hagglingFileList:
            seqName = f[:-4]
            if not os.path.exists('/ssd/render_mesh/'+seqName):
                hagglingFileList_final.append(f)

        g_hagglingFileList = hagglingFileList_final


        g_hagglingFileListIdx =-1


    g_hagglingFileListIdx +=1
    if g_hagglingFileListIdx>=len(g_hagglingFileList):
        print("g_hagglingFileListIdx>=len(g_hagglingFileList)")
        return False

    fileName = g_hagglingFileList[g_hagglingFileListIdx]
    print(fileName)
    LoadHagglingData(fileName)
    g_frameIdx =0

    return True

#Save all the frames, and exit opengl when all frames are saved
def setSaveOnlyMode(mode):
    global g_bSaveOnlyMode
    g_bSaveOnlyMode = mode

def setSave(mode):
    global g_bSaveToFile
    g_bSaveToFile = mode

def setSaveFolderName(folderName):
    global g_saveFolderName
    g_saveFolderName = folderName



""" Using pywavefront"""
def LoadObjMesh(filename):

    import pywavefront
    mesh = pywavefront.Wavefront(filename, collect_faces=True)

    faces = np.array(mesh.mesh_list[0].faces)   # (#Faces, 3). Zero-based
    # faces = faces-1

    vertices = np.array(mesh.vertices)  # (#Vertices, 3)

    #Compute Normals
    vertices = vertices[np.newaxis,:]  #1 x meshVerNum x 3
    normal_all = ComputeNormal(vertices,faces)

    #Save as pkl
    meshModel =  {'vertices': vertices, 'normals':normal_all , 'faces': faces}
    return meshModel


def setupRotationView():
    global g_bShowFloor,g_zoom
    glutReshapeWindow(1000,1000)
    g_bShowFloor = False
    # g_zoom = 220
    g_zoom = 2220



def DrawPyramid(camWidth,camHeight,camDepth,lineWith=1):

	# glColorMaterial(GL_FRONT, GL_DIFFUSE);
	# glEnable(GL_COLOR_MATERIAL);
	# glColor4f(color.first.x,color.first.y,color.first.z,color.second);

    glLineWidth(lineWith)

    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(camWidth*0.5,camHeight*0.5,camDepth*1)
    glVertex3f(0,0,0)
    glVertex3f(camWidth*0.5,camHeight*-0.5,camDepth*1)
    glVertex3f(0,0,0)
    glVertex3f(camWidth*-0.5,camHeight*0.5,camDepth*1)
    glVertex3f(0,0,0)
    glVertex3f(camWidth*-0.5,camHeight*-0.5,camDepth*1)
    glEnd()
	

    glBegin( GL_LINE_STRIP)
    glVertex3f(camWidth*0.5,camHeight*0.5,camDepth*1)
    glVertex3f(camWidth*-0.5,camHeight*0.5,camDepth*1)
    glVertex3f(camWidth*-0.5,camHeight*-0.5,camDepth*1)
    glVertex3f(camWidth*0.5,camHeight*-0.5,camDepth*1) 
    glVertex3f(camWidth*0.5,camHeight*0.5,camDepth*1) 
    glEnd()
    glDisable(GL_COLOR_MATERIAL)

    glBegin( GL_QUADS)
    # glColor4f(color.first.x,color.first.y,color.first.z,color.second*0.1)
    glVertex3f(camWidth*0.5,camHeight*0.5,camDepth*1)
    glVertex3f(camWidth*-0.5,camHeight*0.5,camDepth*1)
    glVertex3f(camWidth*-0.5,camHeight*-0.5,camDepth*1)
    glVertex3f(camWidth*0.5,camHeight*-0.5,camDepth*1) 
    glVertex3f(camWidth*0.5,camHeight*0.5,camDepth*1) 
    glEnd()
    # glDisable(GL_COLOR_MATERIAL)

def DrawPtCloud():
    # glColor3f(0,1,0)

    glPointSize(g_ptSize); 
    glBegin(GL_POINTS)
    for i in range(g_ptCloud.shape[0]):
        if g_ptCloudColor is not None:
            glColor3f(g_ptCloudColor[i,0],g_ptCloudColor[i,1],g_ptCloudColor[i,2])
        glVertex3f(g_ptCloud[i,0],g_ptCloud[i,1],g_ptCloud[i,2])
    glEnd()
	


def DrawCameras():
    if g_cameraPoses is None:
        return

    for i in range(len(g_cameraPoses)):

        glPushMatrix()

        glTranslatef(g_cameraPoses[i,0],g_cameraPoses[i,1],g_cameraPoses[i,2])
        glMultMatrixd(g_cameraRots[i])
        glutSolidSphere(1, 10, 10)
        DrawPyramid(10, 10, 10)
            
        glPopMatrix()

def renderscene():

    start = timeit.default_timer()
    # global xrot
    # global yrot
    # global view_dist
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #Some anti-aliasing code (seems not working, though)
    glEnable (GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable (GL_LINE_SMOOTH)
    glHint (GL_LINE_SMOOTH_HINT, GL_NICEST)
    # glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_MULTISAMPLE)
    # glHint(GL_MULTISAMPLE_FILTER_HINT_NV, GL_NICEST)


    # Set up viewing transformation, looking down -Z axis
    glLoadIdentity()
    #gluLookAt(0, 0, -g_fViewDistance, 0, 0, 0, -.1, 0, 0)   #-.1,0,0
    gluLookAt(0,0,0, 0, 0, 1, 0, -1, 0)


    if g_viewMode=='camView':       #Set View Point in MTC Camera View
        # camidlist = ''.join(g_camid)
        # camid = int(camidlist)
        if g_bOrthoCam:
            setCameraViewOrth()
        else:
            setCameraView()

    else:#Free Mode
        # Set perspective (also zoom)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #gluPerspective(zoom, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)
        gluPerspective(65, float(g_Width)/float(g_Height), g_nearPlane, g_farPlane)         # This should be called here (not in the reshpe)
        glMatrixMode(GL_MODELVIEW)
        # Render the scene

        setFree3DView()
        glColor3f(0,1,0)


        # glutSolidSphere(3, 10, 10)        #Draw Origin

    #This should be drawn first, without depth test (it should be always back)
    if g_bShowBackground:
        if g_bOrthoCam:
            DrawBackgroundOrth()
        else:
            DrawBackground()

    glEnable(GL_LIGHTING)
    glEnable(GL_CULL_FACE)
    #drawbody(bodyDatas[cur_ind], connMat_coco19)
    #drawbody_haggling(m_landmarks[:, cur_ind], connMat_coco19)
    #if g_bSaveToFile:


    # #Debug
    # glColor3f(1,0,0)
    # glutSolidTeapot(100, 10, 10)
    # RenderDomeFloor()
    # glutSwapBuffers()
    # return

    # glUseProgram(0)
    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_FILL)

    if g_bShowSkeleton:
        DrawSkeletons()
        DrawSkeletonsGT()
    DrawTrajectory()

    DrawFaces()
    DrawHands()

    if g_bShowMesh:
        DrawMeshes()
    DrawPosOnly()


    glDisable(GL_LIGHTING)
    glDisable(GL_CULL_FACE)


    DrawCameras()
    if g_ptCloud is not None:
        DrawPtCloud()


    if g_bShowFloor:
        RenderDomeFloor()

    global g_frameIdx#, g_frameLimit
    global g_fps, g_show_fps
    if g_show_fps:
        RenderText("{0} fps".format(int(np.round(g_fps,0))))

    # swap the screen buffers for smooth animation
    glutSwapBuffers()

    if g_bRotateView:
        global g_xRotate, g_rotateView_counter, g_saveFrameIdx

        # g_rotateInnterval = 2.0
        g_xRotate += g_rotateInterval

        # print("{0}/rotview_{1:04d}.jpg".format("RENDER_DIR",g_rotateView_counter))

        g_saveFrameIdx = g_rotateView_counter
        g_rotateView_counter+=1


    if g_bSaveToFile:
        SaveScenesToFile()

    g_frameIdx +=1
    #time.sleep(1)
    if g_frameIdx>=g_frameLimit:
        #global g_bSaveOnlyMode
        if g_bSaveOnlyMode:
            #exit opengl
            global g_stopMainLoop
            g_stopMainLoop= True
            g_frameIdx = 0
        else:
            g_frameIdx =0

    if False:
        #Ensure 30fps
        stop = timeit.default_timer()
        time_sec = stop - start
        sleepTime = 0.03333 -time_sec
        if sleepTime>0:
            time.sleep(sleepTime)

    # #Ensure 60fps
    # stop = timeit.default_timer()
    # time_sec = stop - start
    # sleepTime = 0.06666 -time_sec
    # if sleepTime>0:
    #     time.sleep(sleepTime)
    # #print('Time: ', stop - start)


def show_SMPL_sideView(bSaveToFile = False, bResetSaveImgCnt=True, countImg = True):
    show_SMPL_cameraView(bSaveToFile, bResetSaveImgCnt, countImg, False)

def show_SMPL_youtubeView(bSaveToFile = False, bResetSaveImgCnt=True, countImg = True, zoom = 230):
    show_SMPL(bSaveToFile = bSaveToFile, bResetSaveImgCnt = bResetSaveImgCnt, countImg = countImg, zoom = zoom, mode = 'youtube')

def show_SMPL_cameraView(bSaveToFile = False, bResetSaveImgCnt=True, countImg = True, bShowBG = True):
    show_SMPL(bSaveToFile = bSaveToFile, bResetSaveImgCnt = bResetSaveImgCnt, countImg = countImg, bShowBG = bShowBG, mode = 'camera')

# This is to render scene in camera view (especially MTC output)
def show_SMPL(bSaveToFile = False, bResetSaveImgCnt = True, countImg = True, bShowBG = True, zoom = 230, mode = 'camera'):
    init_gl_util()

    if mode == 'init':
        #Setup for rendering
        keyboard('c',0,0)

    global g_bSaveToFile, g_bSaveToFile_done, g_bShowSkeleton, g_bShowFloor, g_viewMode, g_saveFrameIdx

    g_bSaveToFile_done = False
    g_bSaveToFile = bSaveToFile
    g_bShowSkeleton = False
    g_bShowFloor = False

    if mode == 'youtube':
        bShowBG = True
        global g_xTrans,  g_yTrans, g_zoom, g_xRotate, g_yRotate, g_zRotate
        if False:   #Original
            g_xTrans=  -86.0
            g_yTrans= 0.0
            g_zoom= zoom
            g_xRotate = 34.0
            g_yRotate= -32.0
            g_zRotate= 0.0
            g_viewMode = 'free'
        else:   # New
            g_xTrans=  -0.7
            g_yTrans= 3.86
            g_zoom= zoom #230
            g_xRotate = 29
            g_yRotate= -41
            g_zRotate= 0.0
            g_viewMode = 'free'
    elif mode == 'camera' or mode == 'init':
        g_viewMode = 'camView'

    global g_bShowBackground
    g_bShowBackground = bShowBG

    if bResetSaveImgCnt:
        g_saveFrameIdx = 0 #+= 1      #always save as: scene_00000000.png
    elif countImg:
        g_saveFrameIdx +=1

    if mode == 'init':
        global g_stopMainLoop
        g_stopMainLoop=False
        # while True:
        while g_rotateView_counter*g_rotateInterval<360:
            glutPostRedisplay()
            if bool(glutMainLoopEvent)==False:
                continue
            glutMainLoopEvent()
            break
            if g_stopMainLoop:
                break
    else:
        if g_bSaveToFile:
            while g_bSaveToFile_done == False:
                glutPostRedisplay()
                if bool(glutMainLoopEvent)==False:
                    continue
                glutMainLoopEvent()
        else:
            for i in range(3):   ##Render more than one to be safer
                glutPostRedisplay()
                if bool(glutMainLoopEvent)==False:
                    continue
                glutMainLoopEvent()



#For easier use.
#skel should be a skeleton in a single frame
#Input: skel should be a vector (N,)
def VisSkeleton_single(skel):

    skel = skel[:,np.newaxis]       #(N, 1)
    setSkeleton( [skel] , jointType='smplcoco')#(skelNum, dim, frames)
    show()

def SetNearPlane(p):
    global g_nearPlane
    g_nearPlane = p


#Aliasing since the "init_gl" is a bit ugly name
def show(maxIter=-10):
    init_gl(maxIter)


def loadBodyData(seqName="171204_pose1_sample"):
    '''
    output:
        bodyData[humanId]['bValid']
        bodyData[humanId]['scores']
        bodyData[humanId]['joints19']
        bodyData[humanId]['startFrame']
    '''

    #The motion data of all people in this sequence is saved here
    motionData = list()

    seqPath = seqName  + '/hdPose3d_stage1_coco19'
    seqPathFull=[ os.path.join(seqPath,f) for f in sorted(list(os.listdir(seqPath))) ]

    for i, frameFilePath  in enumerate(seqPathFull):
        
        #Extract frameIdx from fileName
        fileName = os.path.basename(frameFilePath)
        numStartIdx = fileName.find('_') + 1
        frameIdx = int(fileName[numStartIdx:numStartIdx+8]) #Always, body3DScene_%08d.json
    
        print(frameFilePath)
        with open(frameFilePath) as cfile:

            jsonData = json.load(cfile)

            for pose in jsonData['bodies']:
                humanId = pose['id']
                #print(humanId)
                #Add new human dic
                if humanId >= len(motionData):
                    while humanId >= len(motionData):
                        motionData.append(dict())   #add blank dict
                        motionData[-1]['bValid'] = False
                    
                    #Initialze Currnet Human Data
                    motionData[humanId]['bValid'] = True
                    motionData[humanId]['scores'] = np.empty((19,0),float)
                    motionData[humanId]['joints19'] = np.empty((57,0),float) #57 = 19x3
                    motionData[humanId]['startFrame'] = frameIdx
                    
                joints19 = np.array(pose['joints19']) #(76,)
                joints19 = joints19.reshape(-1,4) #19x4 where last column has recon. scores
                scores = joints19[:,3:4] #19x1
                joints19 = joints19[:,:3] #19x3
                joints19 = joints19.flatten()[:,np.newaxis] #(57,1)

                #Append. #This assume that human skeletons exist continuously. Will be broken if drops happen. No this results are happening?
                localIdx = frameIdx - motionData[humanId]['startFrame'] #zero based inx
                #assert(motionData[humanId]['joints19'].shape[1] ==localIdx)
                if motionData[humanId]['joints19'].shape[1] != localIdx:
                    print('{0} vs {1}'.format(motionData[humanId]['joints19'].shape[1],localIdx))
                    assert(False)

                motionData[humanId]['joints19']  = np.append(motionData[humanId]['joints19'],joints19, axis=1) #(57, frames)
                motionData[humanId]['scores']  = np.append(motionData[humanId]['scores'],scores, axis=1) #(19, frames)

    #You may want to save it as pkl file
    # pickle.dump( motionData, open( "{0}/{1}.pkl".format(outputFolder,seqName), "wb" ) )
    return motionData


def loadFaceData(seqName):

    #The motion data of all people in this sequence is saved here
    motionData = list()

    seqPath = seqName  + '/hdFace3d'
    seqPathFull=[ os.path.join(seqPath,f) for f in sorted(list(os.listdir(seqPath))) if os.path.isfile(os.path.join(seqPath,f))]

    for i, frameFilePath  in enumerate(seqPathFull):
        
        #Extract frameIdx from fileName
        fileName = os.path.basename(frameFilePath)
        numStartIdx = fileName.find('_') + 3 #'_HD...#
        frameIdx = int(fileName[numStartIdx:numStartIdx+8]) #Always, body3DScene_%08d.json
    
        print(frameFilePath)
        with open(frameFilePath) as cfile:
 
            jsonData = json.load(cfile)

            for pose in jsonData['people']:
                humanId = pose['id']
                if humanId<0:
                    continue

                faceData = pose['face70']

                validityCheck = np.mean(faceData['averageScore'])
                if validityCheck<0.001:
                    continue

                #print(humanId)
                #Add new human dic
                if humanId >= len(motionData):
                    while humanId >= len(motionData):
                        motionData.append(dict())   #add blank dict
                        motionData[-1]['bValid'] = False
                    
                    #Initialze Currnet Human Data
                    motionData[humanId]['bValid'] = True
                    motionData[humanId]['scores'] = np.empty((70,0),float)
                    motionData[humanId]['reproErrors'] = np.empty((70,0),float)
                    motionData[humanId]['visibilityCnt'] = np.empty((70,0),int)
                    motionData[humanId]['face70'] = np.empty((210,0),float) #210 = 70x3
                    motionData[humanId]['startFrame'] = frameIdx
                    motionData[humanId]['bValidFrame'] = np.empty((1,0),bool)  #Validity signal

                elif motionData[humanId]['bValid']==False:       #Already added, but was not valid
                    #Initialze Currnet Human Data
                    motionData[humanId]['bValid'] = True
                    motionData[humanId]['scores'] = np.empty((70,0),float)
                    motionData[humanId]['reproErrors'] = np.empty((70,0),float)
                    motionData[humanId]['visibilityCnt'] = np.empty((70,0),int)
                    motionData[humanId]['face70'] = np.empty((210,0),float) #210 = 70x3
                    motionData[humanId]['startFrame'] = frameIdx
                    motionData[humanId]['bValidFrame'] = np.empty((1,0),bool)  #Validity signal
                    
                    
                face70 = np.array(faceData['landmarks']) #(210,)
                face70 = face70.flatten()[:,np.newaxis] #(210,1)

                scores = np.array(faceData['averageScore'])  #(70,)
                scores = scores[:,np.newaxis] #(70,1)
                reproError = np.array(faceData['averageReproError'])  #(70,)
                reproError = reproError[:,np.newaxis] #(70,1)
                visibility = np.array(faceData['visibility'])
                visibilityCnt = np.array([len(x) for x in visibility]) #(70,)
                visibilityCnt = visibilityCnt[:,np.newaxis] #(70,1)

                #Append. 
                localIdx = frameIdx - motionData[humanId]['startFrame'] #zero based inx
                #assert(motionData[humanId]['joints19'].shape[1] ==localIdx)
                if motionData[humanId]['face70'].shape[1] != localIdx:
                    #print('{0} vs {1}'.format(motionData[humanId]['face70'].shape[1],localIdx))

                    #Add invalid
                    while motionData[humanId]['face70'].shape[1] !=localIdx:

                        #print('adding: {0} vs {1}'.format(motionData[humanId]['face70'].shape[1],localIdx))

                        motionData[humanId]['face70']  = np.append(motionData[humanId]['face70'], np.zeros((210,1),dtype=float), axis=1) #(210, frames)
                        motionData[humanId]['scores']  = np.append(motionData[humanId]['scores'], np.zeros((70,1),dtype=float), axis=1) #(70, frames)

                        motionData[humanId]['reproErrors']  = np.append(motionData[humanId]['reproErrors'], np.zeros((70,1),dtype=float), axis=1) #(70, frames)
                        motionData[humanId]['visibilityCnt']  = np.append(motionData[humanId]['scores'], np.zeros((70,1),dtype=int), axis=1) #(70, frames)
                        motionData[humanId]['bValidFrame'] = np.append(motionData[humanId]['bValidFrame'], False)  #Validity signal

                motionData[humanId]['face70']  = np.append(motionData[humanId]['face70'],face70, axis=1) #(210, frames)
                motionData[humanId]['scores']  = np.append(motionData[humanId]['scores'],scores, axis=1) #(70, frames)
                motionData[humanId]['reproErrors']  = np.append(motionData[humanId]['reproErrors'],reproError, axis=1) #(70, frames)
                motionData[humanId]['visibilityCnt']  = np.append(motionData[humanId]['scores'],scores, axis=1) #(70, frames)
                motionData[humanId]['bValidFrame'] = np.append(motionData[humanId]['bValidFrame'], True)  #Validity signal

                # if motionData[humanId]['face70'].shape[1] == 1045:
                #     print('{0} vs {1}'.format(motionData[humanId]['face70'].shape[1],localIdx+1))
                

    #print(motionData)
    # pickle.dump( motionData, open( "{0}/{1}.pkl".format(outputFolder,seqName), "wb" ) )
    return motionData

def loadHandData(seqName):

    #The motion data of all people in this sequence is saved here
    motionData_left = list()     #Left hand
    motionData_right = list()   #Right hand

    seqPath = seqName  + '/hdHand3d'
    seqPathFull=[ os.path.join(seqPath,f) for f in sorted(list(os.listdir(seqPath))) if os.path.isfile(os.path.join(seqPath,f)) and f.endswith('.json') ]

    for i, frameFilePath  in enumerate(seqPathFull):
        #Extract frameIdx from fileName
        fileName = os.path.basename(frameFilePath)
        numStartIdx = fileName.find('_') + 3 #'_HD...#
        frameIdx = int(fileName[numStartIdx:numStartIdx+8]) #Always, body3DScene_%08d.json
    
        print(frameFilePath)
        with open(frameFilePath) as cfile:
 
            jsonData = json.load(cfile)

            for target in ('left','right'):
                
                for pose in jsonData['people']:
                    humanId = pose['id']
                    if humanId<0:
                        continue

                    if target=='left':
                        if not ('left_hand' in pose):
                            continue
                        handData = pose['left_hand']
                        motionData = motionData_left #just reference copy. No deep copy is done
                    else: 
                        if not ('right_hand' in pose):
                                continue
                        handData = pose['right_hand']
                        motionData = motionData_right #just reference copy. No deep copy is done

                    validityCheck = np.mean(handData['averageScore'])
                    if validityCheck<0.001:
                        continue

                    #print(humanId)
                    #Add new human dic
                    if humanId >= len(motionData):
                        while humanId >= len(motionData):
                            motionData.append(dict())   #add blank dict
                            motionData[-1]['bValid'] = False
                        
                        #Initialze Currnet Human Data
                        motionData[humanId]['bValid'] = True
                        motionData[humanId]['scores'] = np.empty((21,0),float)
                        motionData[humanId]['reproErrors'] = np.empty((21,0),float)
                        motionData[humanId]['visibilityCnt'] = np.empty((21,0),int)
                        motionData[humanId]['hand21'] = np.empty((63,0),float) #63 = 21x3
                        motionData[humanId]['startFrame'] = frameIdx
                        motionData[humanId]['bValidFrame'] = np.empty((1,0),bool)  #Validity signal

                    elif motionData[humanId]['bValid']==False:       #Already added, but was not valid
                        #Initialze Currnet Human Data
                        motionData[humanId]['bValid'] = True
                        motionData[humanId]['scores'] = np.empty((21,0),float)
                        motionData[humanId]['reproErrors'] = np.empty((21,0),float)
                        motionData[humanId]['visibilityCnt'] = np.empty((21,0),int)
                        motionData[humanId]['hand21'] = np.empty((63,0),float) #63 = 21x3
                        motionData[humanId]['startFrame'] = frameIdx
                        motionData[humanId]['bValidFrame'] = np.empty((1,0),bool)  #Validity signal
                        
                        
                    hand21 = np.array(handData['landmarks']) #(63,)
                    hand21 = hand21.flatten()[:,np.newaxis] #(63,1)

                    scores = np.array(handData['averageScore'])  #(21,)
                    scores = scores[:,np.newaxis] #(21,1)
                    reproError = np.array(handData['averageReproError'])  #(21,)
                    reproError = reproError[:,np.newaxis] #(21,1)
                    visibility = np.array(handData['visibility'])
                    visibilityCnt = np.array([len(x) for x in visibility]) #(21,)
                    visibilityCnt = visibilityCnt[:,np.newaxis] #(21,1)

                    #Append. 
                    localIdx = frameIdx - motionData[humanId]['startFrame'] #zero based inx
                    #assert(motionData[humanId]['joints19'].shape[1] ==localIdx)
                    if motionData[humanId]['hand21'].shape[1] != localIdx:
                        #print('{0} vs {1}'.format(motionData[humanId]['hand21'].shape[1],localIdx))

                        #Add invalid (if there existing missing frames where no hand exists)
                        while motionData[humanId]['hand21'].shape[1] !=localIdx:

                            #print('adding: {0} vs {1}'.format(motionData[humanId]['hand21'].shape[1],localIdx))

                            motionData[humanId]['hand21']  = np.append(motionData[humanId]['hand21'], np.zeros((63,1),dtype=float), axis=1) #(63, frames)
                            motionData[humanId]['scores']  = np.append(motionData[humanId]['scores'], np.zeros((21,1),dtype=float), axis=1) #(21, frames)

                            motionData[humanId]['reproErrors']  = np.append(motionData[humanId]['reproErrors'], np.zeros((21,1),dtype=float), axis=1) #(21, frames)
                            motionData[humanId]['visibilityCnt']  = np.append(motionData[humanId]['scores'], np.zeros((21,1),dtype=int), axis=1) #(21, frames)
                            motionData[humanId]['bValidFrame'] = np.append(motionData[humanId]['bValidFrame'], False)  #Validity signal

                    motionData[humanId]['hand21']  = np.append(motionData[humanId]['hand21'],hand21, axis=1) #(63, frames)
                    motionData[humanId]['scores']  = np.append(motionData[humanId]['scores'],scores, axis=1) #(21, frames)
                    motionData[humanId]['reproErrors']  = np.append(motionData[humanId]['reproErrors'],reproError, axis=1) #(21, frames)
                    motionData[humanId]['visibilityCnt']  = np.append(motionData[humanId]['scores'],scores, axis=1) #(21, frames)
                    motionData[humanId]['bValidFrame'] = np.append(motionData[humanId]['bValidFrame'], True)  #Validity signal

                    # if motionData[humanId]['face70'].shape[1] == 1045:
                    #     print('{0} vs {1}'.format(motionData[humanId]['face70'].shape[1],localIdx+1))
                    

    #print(motionData)
    # pickle.dump( {'left': motionData_left, 'right':motionData_right}, open( "{0}/{1}.pkl".format(outputFolder,seqName), "wb" ) )
    return motionData_left, motionData_right

if __name__ == '__main__':
    # demo_panoptic_data_haggling()

    seqName = "171204_pose1_sample"

    bodyData = loadBodyData(seqName)
    faceData = loadFaceData(seqName)
    handData_left,handData_right = loadHandData(seqName)

    #Set data on visualizer
    humanId = 0
    setSkeleton( [ bodyData[humanId]['joints19'] ] )
    setFace([ faceData[humanId]['face70'] ])
    setHand_left([handData_left[humanId]['hand21'] ])
    setHand_right([handData_right[humanId]['hand21'] ])
    
    show()


