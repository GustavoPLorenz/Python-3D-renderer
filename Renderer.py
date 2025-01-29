import pygame
import numpy as np

#Pygame init
pygame.init()
WindowSize = (600,600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("PyRenderer")

#Variable definitions
Running = True

#Main loop
while Running:
    #Inputs
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False

    #Window settings
    pygame.time.wait(1)
    pygame.display.flip()
    Window.fill((0,0,0))
pygame.quit()