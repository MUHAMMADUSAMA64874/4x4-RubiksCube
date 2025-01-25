import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Display settings
display_width = 800
display_height = 600
pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("4x4 Rubik's Cube")

# Colors for each face of the Rubik's Cube
WHITE = (1, 1, 1)
YELLOW = (1, 1, 0)
BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
RED = (1, 0, 0)
ORANGE = (1, 0.5, 0)

# Cube vertices
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# Cube edges
edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Cube faces
surfaces = (
    (0, 1, 2, 3),
    (3, 2, 6, 7),
    (6, 5, 4, 7),
    (4, 5, 1, 0),
    (1, 5, 6, 2),
    (4, 0, 3, 7)
)

# Colors for each face in the order: front, back, top, bottom, left, right
colors = [WHITE, YELLOW, BLUE, GREEN, RED, ORANGE]

# Function to draw a single smaller cube
def draw_single_cube():
    glBegin(GL_QUADS)
    for i, face in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3fv((0, 0, 0))
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Function to draw the 4x4 Rubik's Cube
def draw_rubiks_cube():
    spacing = 2.2  # Distance between the smaller cubes
    for x in range(4):
        for y in range(4):
            for z in range(4):
                glPushMatrix()
                glTranslatef((x - 1.5) * spacing, (y - 1.5) * spacing, (z - 1.5) * spacing)
                draw_single_cube()
                glPopMatrix()

# Smooth rotation variables
target_angle_x = 0
target_angle_y = 0
current_angle_x = 0
current_angle_y = 0
rotation_speed = 2  # Degrees per frame

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                target_angle_y -= 90
            elif event.key == pygame.K_RIGHT:
                target_angle_y += 90
            elif event.key == pygame.K_UP:
                target_angle_x -= 90
            elif event.key == pygame.K_DOWN:
                target_angle_x += 90

    # Update current angles smoothly
    if current_angle_x < target_angle_x:
        current_angle_x += rotation_speed
    elif current_angle_x > target_angle_x:
        current_angle_x -= rotation_speed

    if current_angle_y < target_angle_y:
        current_angle_y += rotation_speed
    elif current_angle_y > target_angle_y:
        current_angle_y -= rotation_speed

    # Clear screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up perspective projection and camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display_width / display_height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 20, 0, 0, 0, 0, 1, 0)

    # Rotate the cube
    glRotatef(current_angle_x, 1, 0, 0)
    glRotatef(current_angle_y, 0, 1, 0)

    # Draw the Rubik's Cube
    draw_rubiks_cube()

    # Update display
    pygame.display.flip()
    pygame.time.wait(10)
