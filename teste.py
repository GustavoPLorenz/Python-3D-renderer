import pygame
import numpy as np
import math

# Configurações iniciais
WIDTH, HEIGHT = 800, 600
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ponto que será rotacionado
point = np.array([1, 0, 0])

# Ponto ao redor do qual o ponto vai girar (ponto pivô)
pivot = np.array([0, 0, 0])

# Distância da câmera para projeção
distance = 5

def rotate_point_3d(point, pivot, theta, axis):
    """ Rotaciona um ponto em torno de um ponto pivô em 3D usando matrizes """
    theta = math.radians(theta)  # Converte para radianos
    x, y, z = point - pivot  # Translada para a origem do pivô
    
    if axis == 'x':
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)]
        ])
    elif axis == 'y':  # Rotação no eixo Y (plano XZ)
        rotation_matrix = np.array([
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)]
        ])
    elif axis == 'z':
        rotation_matrix = np.array([
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1]
        ])
    else:
        return point  # Retorna o mesmo ponto se o eixo for inválido
    
    # Aplica a rotação
    rotated_point = np.dot(rotation_matrix, [x, y, z])
    
    # Translada de volta para a posição original do pivô
    return rotated_point + pivot

def project_3d_to_2d(point):
    """ Projeta um ponto 3D para 2D usando perspectiva """
    x, y, z = point
    if z + distance == 0:
        return WIDTH // 2, HEIGHT // 2  # Evita divisão por zero
    
    factor = distance / (z + distance)  # Fator de projeção
    x_2d = int(WIDTH // 2 + x * factor * 100)  # Ajuste de escala
    y_2d = int(HEIGHT // 2 - y * factor * 100)  # Inverter y para alinhar
    
    return x_2d, y_2d

# Loop principal
running = True
angle = 0

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotaciona o ponto em torno do pivô no eixo Y (plano XZ)
    rotated_point = rotate_point_3d(point, pivot, angle, axis='y')

    # Converte o ponto 3D para 2D
    projected_point = project_3d_to_2d(rotated_point)

    # Desenha o ponto pivot
    pivot_projected = project_3d_to_2d(pivot)
    pygame.draw.circle(screen, WHITE, pivot_projected, 10)

    # Desenha o ponto rotacionado
    pygame.draw.circle(screen, (0, 255, 0), projected_point, 15)

    # Atualiza a tela
    pygame.display.flip()

    # Incrementa o ângulo para a rotação contínua
    angle += 1
    if angle >= 360:
        angle = 0

    clock.tick(60)  # Mantém 60 FPS

pygame.quit()
