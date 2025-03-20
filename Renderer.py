import pygame
import numpy as np
import copy
import time
import random

#Pygame init
pygame.init()
WindowSize = (600,600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("PyRenderer")

#Functions
def RotateObject(Object):
    YTheta = np.radians(CameraYDegrees)
    XTheta = np.radians(CameraXDegrees)

    CosY = np.cos(YTheta)
    SinY = np.sin(YTheta)
    CosX = np.cos(XTheta)
    SinX = np.sin(XTheta)

    RotatedObject = []
    for Point in Object["Polygon"]:
        X = Point[0] - CameraX
        Y = Point[1] - CameraY
        Z = Point[2] - CameraZ

        YRotatedX = X * CosY + Z * SinY
        YRotatedZ = -X * SinY + Z * CosY

        XRotatedY = Y * CosX - YRotatedZ * SinX
        XRotatedZ = Y * SinX + YRotatedZ * CosX

        RotatedObject.append((YRotatedX, XRotatedY, XRotatedZ))
    return RotatedObject

def Object2D(MovedObject):
    Polygon2D = []
    ClippedPolygon = []
    Polygon = MovedObject["Polygon"]
    for Line in range(len(Polygon)):
        Point1 = Polygon[Line]
        Point2 = Polygon[(Line+1) % len(Polygon)]

        if Point1[2] >= 0:
            ClippedPolygon.append(Point1)

        if Point1[2] * Point2[2] < 0:
            T = Point1[2] / (Point1[2] - Point2[2])
            NewX = Point1[0] + T * (Point2[0] - Point1[0])
            NewY = Point1[1] + T * (Point2[1] - Point1[1])
            NewZ = 0

            ClippedPolygon.append((NewX,NewY,NewZ))
            
    for Point in ClippedPolygon:
            
        X = Point[0]
        Y = Point[1]
        Z = (Point[2] +0.01)/250

        W = Z/D
        if(W > 0):
            Polygon2D.append((((X*F)/W)+300,-((Y*F)/W)+300))
    return Polygon2D

def DrawObject(Object2D):
    try:
        pygame.draw.polygon(Window,Object2D["Color"],Object2D["Polygon"],1)
    except:
        pass
#Transform .obj in list
Polygons = []
Vertex = []
Normals = []
Colors = {}
LastColor = (255,255,255)
LastColorName = ""

MtlArchive = open("Chevrolet_Camaro_SS_Low.mtl")
MtlContent = MtlArchive.read()
Lines = MtlContent.split("\n")
for Line in Lines:
    if "newmtl " in Line:
        Line = Line.split(" ")
        LastColorName = Line[1]
        
    
    if "Kd " in Line:
        Line = Line.split(" ")
        Colors[str(LastColorName)] = (int(float(Line[1])*255),int(float(Line[2])*255),int(float(Line[3])*255))

ObjArchive = open("Chevrolet_Camaro_SS_Low.obj")
ObjContent = ObjArchive.read()
ObjContent = ObjContent.replace("  "," ")
Lines = ObjContent.split("\n")
for Line in Lines:
    if "v " in Line:
        Line = Line.split(" ")
        Vertex.append((float(Line[1]),float(Line[2]),float(Line[3])))
    
    if "vn " in Line:
        Line = Line.split(" ")
        Normals.append((float(Line[1]), float(Line[2]), float(Line[3])))
    
    if "usemtl " in Line:
        Line = Line.split(" ")
        LastColor = Colors[str(Line[1])]

    if "f " in Line:
        ObjPolygon = {"Polygon":[],"Color":LastColor, "Normals":[]}
        LineParts = Line.split(" ")
        for Part in LineParts[1:]:
            Part = Part.split("/")
            ObjPolygon["Polygon"].append(Vertex[int(Part[0])-1])
            ObjPolygon["Normals"].append(Normals[int(Part[2]) - 1])
        Polygons.append(ObjPolygon)
#Variable definitions
Running = True
RotatedObjects = copy.deepcopy(Polygons)
Objects2D = copy.deepcopy(Polygons)
D = 1
F = 1
CameraX = 0
CameraY = 0
CameraZ = 0
CameraYDegrees = 0
CameraXDegrees = 0
RotationVelocity = 45
LastTime = pygame.time.get_ticks() / 1000
DeltaTime = 1

#Main loop
while Running:
    #Inputs
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
    
    Keys = pygame.key.get_pressed()
    move_speed = 1 * DeltaTime
    theta = np.radians(CameraYDegrees)

    forward_x = np.sin(theta) * move_speed
    forward_z = np.cos(theta) * move_speed

    right_x = np.cos(theta) * move_speed
    right_z = -np.sin(theta) * move_speed

    if Keys[pygame.K_w]:
        CameraX -= forward_x
        CameraZ += forward_z
    if Keys[pygame.K_s]:
        CameraX += forward_x
        CameraZ -= forward_z
    if Keys[pygame.K_a]:
        CameraX -= right_x
        CameraZ += right_z
    if Keys[pygame.K_d]:
        CameraX += right_x
        CameraZ -= right_z
    if Keys[pygame.K_LSHIFT]:
        CameraY -= move_speed
    if Keys[pygame.K_SPACE]: 
        CameraY += move_speed
    
    if Keys[pygame.K_RIGHT]:
        CameraYDegrees -= RotationVelocity * DeltaTime
    
    if Keys[pygame.K_LEFT]:
        CameraYDegrees += RotationVelocity * DeltaTime

    if Keys[pygame.K_UP]:
        CameraXDegrees -= RotationVelocity * DeltaTime
    
    if Keys[pygame.K_DOWN]:
        CameraXDegrees += RotationVelocity * DeltaTime

    #Functions calling
    for i in range(len(Polygons)):
        RotatedObjects[i]["Polygon"] = RotateObject(Polygons[i])
        Objects2D[i]["Polygon"] = Object2D(RotatedObjects[i])
        Objects2D[i]["Color"] = Polygons[i]["Color"]
        DrawObject(Objects2D[i])

    #Window settings
    CurrentTime = pygame.time.get_ticks() / 1000
    DeltaTime = CurrentTime - LastTime
    LastTime = CurrentTime
    CameraYDegrees %= 360
    CameraXDegrees %= 360
    pygame.time.wait(0)
    pygame.display.flip()
    Window.fill((0,0,0))
pygame.quit()