import pygame
import numpy as np
import copy

#Pygame init
pygame.init()
WindowSize = (600,600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("PyRenderer")

#Functions
def Object2D(Object):
    print(f"Calculating 2D Position: {Object["Name"]}")
    Object2D = []
    for Line in Object["Object"]:
        Line2D = []
        for Point in Line:
            X = Point[0]
            Y = Point[1]
            Z = (Point[2] +1)/50
            W = Z/D

            Line2D.append((((X*F)/W)+300,((Y*F)/W)+300))
        Object2D.append(Line2D)
    return Object2D

def DrawObject(Object2D):
    print(f"Drawing Object: {Object2D["Name"]}")
    for Line in Object2D["Object"]:
        pygame.draw.line(Window,(255,255,0),Line[0],Line[1])

#Variable definitions
Running = True
Objects = [{
    "Name" :"Object1",
    "Object":[
        [(0,0,0),(10,0,0)],
        [(0,0,0),(0,10,0)],
        [(0,0,0),(0,0,1)],
        [(10,0,0),(10,10,0)],
        [(10,0,0),(10,0,1)],
        [(0,10,0),(10,10,0)],
        [(0,10,0),(0,10,1)],
        [(10,10,0),(10,10,1)],
        [(0,10,1),(10,10,1)],
        [(0,10,1),(0,0,10)],
        [(10,0,1),(10,10,1)],
        [(10,0,1),(0,0,1)]
    ],
}]
Objects2D = copy.deepcopy(Objects)

D = 1
F = 1

#Main loop
while Running:
    #Inputs
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
    
    Objects2D[0]["Object"] = Object2D(Objects[0])
    DrawObject(Objects2D[0])

    #Window settings
    pygame.time.wait(0)
    pygame.display.flip()
    Window.fill((0,0,0))
pygame.quit()