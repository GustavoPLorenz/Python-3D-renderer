import pygame
import numpy as np
import copy

#Pygame init
pygame.init()
WindowSize = (600,600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("PyRenderer")

#Functions
def MoveObject(RotatedObject):
    print(f"Moving: {RotatedObject["Name"]}")
    MovedObject = []
    for Line in RotatedObject["Object"]:
        MovedLine = []
        for Point in Line:
            
            MovedLine.append((Point[0]+CameraX,Point[1]+CameraY,Point[2]+CameraZ))   
        MovedObject.append(MovedLine) 
    return MovedObject

def Object2D(MovedObject):
    print(f"Calculating 2D Position: {MovedObject["Name"]}")
    Object2D = []
    for Line in MovedObject["Object"]:
        Line2D = []
        for Point in Line:
            X = Point[0]
            Y = Point[1]
            Z = (Point[2] +1)/250
            W = Z/D
            if(W > 0):
                Line2D.append((((X*F)/W)+300,((Y*F)/W)+300))
        Object2D.append(Line2D)
    return Object2D

def DrawObject(Object2D):
    print(f"Drawing Object: {Object2D["Name"]}")
    for Line in Object2D["Object"]:
        pygame.draw.line(Window,(0,255,0),Line[0],Line[1])

#Variable definitions
Running = True
Objects = [{
    "Name" :"Object1",
    "Object":[
        [(0,0,0),(1,0,0)],
        [(0,0,0),(0,1,0)],
        [(0,0,0),(0,0,1)],
        [(1,0,0),(1,1,0)],
        [(1,0,0),(1,0,1)],
        [(0,1,0),(1,1,0)],
        [(0,1,0),(0,1,1)],
        [(1,1,0),(1,1,1)],
        [(0,1,1),(1,1,1)],
        [(0,1,1),(0,0,1)],
        [(1,0,1),(1,1,1)],
        [(1,0,1),(0,0,1)]
    ],
}]
RotatedObjects = copy.deepcopy(Objects)
MovedObjects = copy.deepcopy(Objects)
Objects2D = copy.deepcopy(Objects)
D = 1
F = 1
CameraX = 1
CameraY = 1
CameraZ = 1

#Main loop
while Running:
    #Inputs
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
    
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_w]:
        CameraZ -=0.003
    if Keys[pygame.K_s]:
        CameraZ +=0.003
    if Keys[pygame.K_LSHIFT]:
        CameraY -=0.003
    if Keys[pygame.K_SPACE]:
        CameraY +=0.003
    if Keys[pygame.K_d]:
        CameraX -=0.003
    if Keys[pygame.K_a]:
        CameraX +=0.003
    
    #Functions calling
    for i in range(len(Objects)):
        MovedObjects[i]["Object"] = MoveObject(RotatedObjects[i])
        Objects2D[i]["Object"] = Object2D(MovedObjects[i])
        DrawObject(Objects2D[i])

    #Window settings
    pygame.time.wait(0)
    pygame.display.flip()
    Window.fill((0,0,0))
pygame.quit()