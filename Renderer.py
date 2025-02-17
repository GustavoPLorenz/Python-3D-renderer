import pygame
import numpy as np
import copy
import time

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
    for Line in Object["Object"]:
        RotatedLine = []
        for Point in Line:
            X = Point[0] - CameraX
            Y = Point[1] - CameraY
            Z = Point[2] - CameraZ

            YRotatedX = X * CosY + Z * SinY
            YRotatedZ = -X * SinY + Z * CosY

            XRotatedY = Y * CosX - YRotatedZ * SinX
            XRotatedZ = Y * SinX + YRotatedZ * CosX

            RotatedLine.append((YRotatedX, XRotatedY, XRotatedZ))
        RotatedObject.append(RotatedLine)
    return RotatedObject

def Object2D(MovedObject):
    Object2D = []
    for Line in MovedObject["Object"]:
        Line2D = []
        if Line[0][2] * Line[1][2] < 0:

            Line[0] = list(Line[0])
            Line[1] = list(Line[1])

            T = Line[0][2] / (Line[0][2] - Line[1][2])

            YRotatedX = Line[0][0] + T * (Line[1][0] - Line[0][0])
            NewY = Line[0][1] + T * (Line[1][1] - Line[0][1])

            if Line[0][2] < 0:
                Line[0] = [YRotatedX, NewY, 0]
            else:
                Line[1] = [YRotatedX, NewY, 0]

        for Point in Line:
            
            X = Point[0]
            Y = Point[1]
            Z = (Point[2] +0.01)/250

            W = Z/D
            if(W > 0):
                Line2D.append((((X*F)/W)+300,-((Y*F)/W)+300))
        Object2D.append(Line2D)
    return Object2D

def DrawObject(Object2D):
    for Line in Object2D["Object"]:
        try:
            pygame.draw.polygon(Window,Object2D["Color"],Line, 1)
        except:
            pass

#Variable definitions
Running = True
Objects = [{}]

#Transform .obj in list
Archive = open("Car.obj")
Content = Archive.read()
Lines = Content.split("\n")
Vertex = []
for Line in Lines:
    if len(Line) >= 1 :
        LineParts = Line.split(" ")
        if LineParts[0] == "v":
            
            X = float(LineParts[1])
            Y = float(LineParts[2])
            Z = float(LineParts[3])

            Vertex.append((X,Y,Z))
ObjObject = []
for Line in Lines:
    ObjLine = []
    if len(Line) >= 1:
        LineParts = Line.split(" ")
        if LineParts[0] == "f":
            for VertexPosition in LineParts[1:-1]:
                VertexNumber = int(VertexPosition.split("/")[0]) - 1
                ObjLine.append(Vertex[VertexNumber])
            ObjObject.append(ObjLine)
Objects[0] = {
    "Name": "Teste",
    "Color": (255,255,255),
    "Object": ObjObject
}
            
RotatedObjects = copy.deepcopy(Objects)
Objects2D = copy.deepcopy(Objects)
D = 1
F = 1
CameraX = 0
CameraY = 0
CameraZ = 0
CameraYDegrees = 0
CameraXDegrees = 0
RotationVelocity = 45
LastTime = pygame.time.get_ticks() / 1000

#Main loop
while Running:
    #Inputs
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
    
    Keys = pygame.key.get_pressed()
    move_speed = 0.01
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
    for i in range(len(Objects)):
        RotatedObjects[i]["Object"] = RotateObject(Objects[i])
        Objects2D[i]["Object"] = Object2D(RotatedObjects[i])
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
