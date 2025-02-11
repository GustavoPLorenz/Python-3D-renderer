import pygame
import numpy as np
import logging

# Configuração do logging (log mais compacto)
logging.basicConfig(
    filename="debug_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s"
)

# Inicializa o Pygame
pygame.init()
WindowSize = (600, 600)
Window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("PyRenderer")

# Parâmetros da câmera
CameraX = 0
CameraY = 0
CameraZ = -3
CameraYDegrees = 0

F = 100  # Fator de projeção

# Definição do objeto (um cubo)
Objects = [{
    "Name": "Cube",
    "Object": [
        [(0, 0, 5), (1, 0, 5)],
        [(0, 0, 5), (0, 1, 5)],
        [(0, 0, 5), (0, 0, 6)],
        [(1, 0, 5), (1, 1, 5)],
        [(1, 0, 5), (1, 0, 6)],
        [(0, 1, 5), (1, 1, 5)],
        [(0, 1, 5), (0, 1, 6)],
        [(1, 1, 5), (1, 1, 6)],
        [(0, 1, 6), (1, 1, 6)],
        [(0, 1, 6), (0, 0, 6)],
        [(1, 0, 6), (1, 1, 6)],
        [(1, 0, 6), (0, 0, 6)]
    ],
}]

def get_object_center(obj):
    """Calcula o centro do objeto em coordenadas mundiais."""
    xs, ys, zs = [], [], []
    for line in obj["Object"]:
        for point in line:
            xs.append(point[0])
            ys.append(point[1])
            zs.append(point[2])
    return sum(xs)/len(xs), sum(ys)/len(ys), sum(zs)/len(zs)

def ViewTransform(Object):
    """Transforma os pontos do objeto do espaço mundial para o espaço da câmera."""
    theta = np.radians(CameraYDegrees)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    TransformedObject = {"Name": Object["Name"], "Object": []}
    for line in Object["Object"]:
        new_line = []
        for point in line:
            x = point[0] - CameraX
            y = point[1] - CameraY
            z = point[2] - CameraZ
            x_new = x * cos_theta + z * sin_theta
            z_new = -x * sin_theta + z * cos_theta
            new_line.append((x_new, y, z_new))
        TransformedObject["Object"].append(new_line)
    return TransformedObject

def Object2D(Object):
    """Projeta os pontos 3D no plano 2D usando projeção em perspectiva."""
    Object2D = {"Name": Object["Name"], "Object": []}
    for line in Object["Object"]:
        new_line = []
        for point in line:
            x, y, z = point
            if z <= 0:
                continue
            scale = F / z
            new_line.append(((x * scale) + 300, (y * scale) + 300))  # Centraliza na tela
        Object2D["Object"].append(new_line)
    return Object2D

def DrawObject(Object2D):
    """Desenha o objeto na tela."""
    for line in Object2D["Object"]:
        if len(line) == 2:
            pygame.draw.line(Window, (0, 255, 0), line[0], line[1])

Running = True
frame_count = 0

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    Keys = pygame.key.get_pressed()
    pressed_keys = []
    move_speed = 0.001
    rotate_speed = 0.05

    if Keys[pygame.K_w]:
        CameraZ += move_speed
        pressed_keys.append("W")
    if Keys[pygame.K_s]:
        CameraZ -= move_speed
        pressed_keys.append("S")
    if Keys[pygame.K_a]:
        CameraX -= move_speed
        pressed_keys.append("A")
    if Keys[pygame.K_d]:
        CameraX += move_speed
        pressed_keys.append("D")
    if Keys[pygame.K_LSHIFT]:
        CameraY -= move_speed
        pressed_keys.append("SHIFT")
    if Keys[pygame.K_SPACE]:
        CameraY += move_speed
        pressed_keys.append("SPACE")
    if Keys[pygame.K_LEFT]:
        CameraYDegrees += rotate_speed
        pressed_keys.append("LEFT")
    if Keys[pygame.K_RIGHT]:
        CameraYDegrees -= rotate_speed
        pressed_keys.append("RIGHT")

    # Apenas grava log a cada 10 frames para reduzir o tamanho do arquivo
    if frame_count % 10 == 0:
        cube_center = get_object_center(Objects[0])
        logging.debug(f"Camera: ({CameraX:.3f}, {CameraY:.3f}, {CameraZ:.3f}), Rotation: {CameraYDegrees:.1f}°, Keys: {pressed_keys}")
        logging.debug(f"Cube Center (world): {cube_center}")

    transformed_obj = ViewTransform(Objects[0])
    projected_obj = Object2D(transformed_obj)
    DrawObject(projected_obj)

    pygame.display.flip()
    Window.fill((0, 0, 0))

    frame_count += 1  # Incrementa o contador de frames

pygame.quit()
