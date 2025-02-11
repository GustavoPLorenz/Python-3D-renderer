import pygame
import numpy as np
import copy

#Pygame init
pygame.init()
WindowSize = (600,600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("PyRenderer")

#Functions
def RotateObject(Object):
    Theta = np.radians(CameraYDegrees)
    CosTheta = np.cos(Theta)
    SinTheta = np.sin(Theta)
    RotatedObject = []
    for Line in Object["Object"]:
        RotatedLine = []
        for Point in Line:
            X = Point[0] - CameraX
            Y = Point[1] - CameraY
            Z = Point[2] - CameraZ

            NewX = X * CosTheta + Z * SinTheta
            NewZ = -X * SinTheta + Z * CosTheta

            RotatedLine.append((NewX,Y,NewZ))
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

            NewX = Line[0][0] + T * (Line[1][0] - Line[0][0])
            NewY = Line[0][1] + T * (Line[1][1] - Line[0][1])

            if Line[0][2] < 0:
                Line[0] = [NewX, NewY, 0]
            else:
                Line[1] = [NewX, NewY, 0]

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
            pygame.draw.line(Window,Object2D["Color"],Line[0],Line[1])
        except:
            print("Linha não visivel")

#Variable definitions
Running = True
Objects = [{
        "Name": "Ground",
        "Color": (0,255,0),
        "Object": [
            [(-5, -1, 0), (5, -1, 0)],
            [(5, -1, 0), (5, -1, 10)],
            [(5, -1, 10), (-5, -1, 10)],
            [(-5, -1, 10), (-5, -1, 0)]
        ]
    },{
        "Name": "Tree",
        "Color":(120,64,8),
        "Object":[
            [(-0.5,-1,4.5),(0.5,-1,4.5)],
            [(-0.5,-1,5.5),(0.5,-1,5.5)],
            [(-0.5,-1,4.5),(-0.5,-1,5.5)],
            [(0.5,-1,5.5),(0.5,-1,4.5)],
            [(-0.5,3,4.5),(0.5,3,4.5)],
            [(-0.5,3,5.5),(0.5,3,5.5)],
            [(-0.5,3,4.5),(-0.5,3,5.5)],
            [(0.5,3,5.5),(0.5,3,4.5)],
            [(-0.5,-1,4.5),(-0.5,3,4.5)],
            [(0.5,-1,5.5),(0.5,3,5.5)],
            [(0.5,-1,4.5),(0.5,3,4.5)],
            [(-0.5,-1,5.5),(-0.5,3,5.5)],
        ]
    },{
        "Name": "Leaves",
        "Color":(0,50,0),
        "Object":[
            [(-1.5,3,3.5),(1.5,3,3.5)],
            [(-1.5,3,6.5),(1.5,3,6.5)],
            [(-1.5,3,3.5),(-1.5,3,6.5)],
            [(1.5,3,6.5),(1.5,3,3.5)],
            [(-1.5,3,3.5),(0,7,5)],
            [(-1.5,3,6.5),(0,7,5)],
            [(1.5,3,3.5),(0,7,5)],
            [(1.5,3,6.5),(0,7,5)],
        ]
    }
    ]


RotatedObjects = copy.deepcopy(Objects)
Objects2D = copy.deepcopy(Objects)
D = 1
F = 1
CameraX = 0
CameraY = 0
CameraZ = 0
CameraYDegrees = 0

#Main loop
while Running:
    #Inputs
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
    
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_w]:
        CameraZ +=0.003
    if Keys[pygame.K_s]:
        CameraZ -=0.003
    if Keys[pygame.K_LSHIFT]:
        CameraY -=0.003
    if Keys[pygame.K_SPACE]:
        CameraY +=0.003
    if Keys[pygame.K_d]:
        CameraX +=0.003
    if Keys[pygame.K_a]:
        CameraX -=0.003

    if Keys[pygame.K_RIGHT]:
        CameraYDegrees -=0.03
    if Keys[pygame.K_LEFT]:
        CameraYDegrees +=0.03
    
    #Functions calling
    for i in range(len(Objects)):
        RotatedObjects[i]["Object"] = RotateObject(Objects[i])
        Objects2D[i]["Object"] = Object2D(RotatedObjects[i])
        DrawObject(Objects2D[i])

    #Window settings
    pygame.time.wait(0)
    pygame.display.flip()
    Window.fill((0,0,0))
pygame.quit()