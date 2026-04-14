import pygame
import sys
from utils import OBJECT_EMPTY, OBJECT_HOUSE, OBJECT_HOSPITAL
from hc import hill_climbing

pygame.init()

WIDTH, HEIGHT = 700, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Editor de Matriz")

FONT = pygame.font.Font(None, 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)

# Inputs
input_filas = ""
input_columnas = ""

active_filas = False
active_columnas = False

rect_filas = pygame.Rect(50, 50, 140, 32)
rect_columnas = pygame.Rect(220, 50, 140, 32)

btn_generar = pygame.Rect(400, 50, 120, 32)

# Botones de objetos
btn_house = pygame.Rect(50, 100, 120, 32)
btn_hospital = pygame.Rect(200, 100, 120, 32)
btn_clear = pygame.Rect(350, 100, 120, 32)

# NUEVO botón simular
btn_simular = pygame.Rect(500, 100, 120, 32)

selected_object = OBJECT_HOUSE

# Matriz
filas = 0
columnas = 0
grid = []

def draw_text(text, x, y):
    txt_surface = FONT.render(text, True, BLACK)
    screen.blit(txt_surface, (x, y))

def create_grid(f, c):
    return [[OBJECT_EMPTY for _ in range(c)] for _ in range(f)]

def draw_grid():
    if filas <= 0 or columnas <= 0:
        return None

    cell_size = min(500 // columnas, 350 // filas)
    start_x = 50
    start_y = 180

    for i in range(filas):
        for j in range(columnas):
            x = start_x + j * cell_size
            y = start_y + i * cell_size

            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

            value = grid[i][j]
            if value is not None:
                txt = FONT.render(value, True, BLACK)
                screen.blit(txt, (x + cell_size//4, y + cell_size//4))

    return start_x, start_y, cell_size

# Loop
while True:
    screen.fill(WHITE)

    grid_info = draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            active_filas = rect_filas.collidepoint(event.pos)
            active_columnas = rect_columnas.collidepoint(event.pos)

            # Generar matriz
            if btn_generar.collidepoint(event.pos):
                try:
                    filas = int(input_filas)
                    columnas = int(input_columnas)
                    grid = create_grid(filas, columnas)
                except:
                    filas, columnas = 0, 0
                    grid = []

            # Selección de objetos
            if btn_house.collidepoint(event.pos):
                selected_object = OBJECT_HOUSE

            if btn_hospital.collidepoint(event.pos):
                selected_object = OBJECT_HOSPITAL

            if btn_clear.collidepoint(event.pos):
                selected_object = OBJECT_EMPTY

            # 🔥 BOTÓN SIMULAR
            if btn_simular.collidepoint(event.pos):
                if grid:
                    try:
                        nueva_matriz = hill_climbing(grid)
                        if nueva_matriz:
                            grid = nueva_matriz
                    except Exception as e:
                        print("Error en simulación:", e)

            # Click en la matriz
            if grid_info:
                start_x, start_y, cell_size = grid_info
                mx, my = event.pos

                if mx >= start_x and my >= start_y:
                    col = (mx - start_x) // cell_size
                    fila = (my - start_y) // cell_size

                    if 0 <= fila < filas and 0 <= col < columnas:
                        grid[fila][col] = selected_object

        if event.type == pygame.KEYDOWN:
            if active_filas:
                if event.key == pygame.K_BACKSPACE:
                    input_filas = input_filas[:-1]
                else:
                    input_filas += event.unicode

            if active_columnas:
                if event.key == pygame.K_BACKSPACE:
                    input_columnas = input_columnas[:-1]
                else:
                    input_columnas += event.unicode

    # Inputs
    pygame.draw.rect(screen, GRAY, rect_filas, 2)
    pygame.draw.rect(screen, GRAY, rect_columnas, 2)

    draw_text(input_filas, rect_filas.x + 5, rect_filas.y + 5)
    draw_text(input_columnas, rect_columnas.x + 5, rect_columnas.y + 5)

    draw_text("Filas", rect_filas.x, rect_filas.y - 25)
    draw_text("Columnas", rect_columnas.x, rect_columnas.y - 25)

    # Botón generar
    pygame.draw.rect(screen, YELLOW, btn_generar)
    draw_text("Generar", btn_generar.x + 10, btn_generar.y + 5)

    # Botones objetos
    pygame.draw.rect(screen, BLUE if selected_object == OBJECT_HOUSE else GRAY, btn_house)
    draw_text("Casa 🏠", btn_house.x + 5, btn_house.y + 5)

    pygame.draw.rect(screen, BLUE if selected_object == OBJECT_HOSPITAL else GRAY, btn_hospital)
    draw_text("Hospital 🏥", btn_hospital.x + 5, btn_hospital.y + 5)

    pygame.draw.rect(screen, BLUE if selected_object is OBJECT_EMPTY else GRAY, btn_clear)
    draw_text("Quitar ❌", btn_clear.x + 5, btn_clear.y + 5)

    # 🔥 Botón simular
    pygame.draw.rect(screen, GREEN, btn_simular)
    draw_text("Simular", btn_simular.x + 10, btn_simular.y + 5)

    pygame.display.flip()