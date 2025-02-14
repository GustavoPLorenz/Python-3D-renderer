import pygame
import numpy as np
import time

# Pygame init
pygame.init()
WindowSize = (600, 600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("Rotation Test")

# Função para salvar logs no arquivo
def SaveLog(text):
    with open("rotation_log.txt", "a") as file:
        file.write(text + "\n")

# Função para calcular a diferença angular corretamente
def AngleDifference(a, b):
    diff = (a - b + 180) % 360 - 180
    return diff if diff != -180 else 180

# Variáveis
Running = True
CameraYDegrees = 0
LastAngle = CameraYDegrees
LastTime = time.time()
RotationSpeed = 2  # Velocidade ajustável

# Limpa o arquivo de log antes de começar
open("rotation_log.txt", "w").close()

# Loop principal
while Running:
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False
    
    Keys = pygame.key.get_pressed()
    
    # Rotação sem compensação
    if Keys[pygame.K_RIGHT]:
        CameraYDegrees -= RotationSpeed
    if Keys[pygame.K_LEFT]:
        CameraYDegrees += RotationSpeed

    # Mantém o ângulo entre 0° e 360°
    CameraYDegrees = CameraYDegrees % 360  

    # Mede a velocidade da rotação corretamente
    CurrentTime = time.time()
    DeltaTime = CurrentTime - LastTime
    RotationVelocity = AngleDifference(CameraYDegrees, LastAngle) / DeltaTime if DeltaTime > 0 else 0

    # Registra no log
    SaveLog(f"Ângulo: {CameraYDegrees:.2f}° | Velocidade: {RotationVelocity:.2f}°/s")

    # Atualiza valores antigos
    LastAngle = CameraYDegrees
    LastTime = CurrentTime

    # Atualiza tela
    pygame.time.wait(10)
    pygame.display.flip()

pygame.quit()
