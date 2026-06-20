from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500
rain_speed = 1  # Slower raindrop speed
rain_offset = 0  # Rain bending factor

# List to store raindrop positions
raindrops = [(random.randint(0, 500), random.randint(250, 500)) for _ in range(100)]

# Background color (night mode initially)
background_color = [0.0, 0.0, 0.0]

# Function to draw a house using only GL_POINTS, GL_LINES, GL_TRIANGLES
def draw_house():
    glColor3f(0, 0.5, 0.5)  # Updated house color
    glBegin(GL_QUADS)
    glVertex2f(-100, -100)
    glColor3f(1, 0.5, 0.5)
    glVertex2f(100, -100)
    glColor3f(1, 1, 1)
    glVertex2f(100, 50)
    glColor3f(1,0.5, 0)
    glVertex2f(-100, 50)
    glEnd()

    
    glColor3f(1, 0, 1) 
    glBegin(GL_TRIANGLES)
    glVertex2f(-150, 50)
    glColor3f(0.5, 0, 0.5)
    glVertex2f(150, 50)
    glColor3f(0, 0.5, 0.5)
    glVertex2f(0, 150)
    glEnd()

    glColor3f(0.3, 0.3, 0.3)  # Dark gray door
    glBegin(GL_QUADS)
    glVertex2f(-20, -100)
    glVertex2f(20, -100)
    glVertex2f(20, -30)
    glVertex2f(-20, -30)
    glEnd()

# Function to draw trees in the background
def draw_trees():
    for i in range(-475, 500, 45):
        glColor3f(0.4, 0.2, 0.0)  # Brown trunk
        glBegin(GL_QUADS)
        glVertex2f(i - 5, -100)
        glVertex2f(i + 5, -100)
        glVertex2f(i + 5, -50)
        glVertex2f(i - 5, -50)
        glEnd()

        glColor3f(0.0, 0.8, 0.0)  # Green leaves
        glBegin(GL_TRIANGLES)
        glVertex2f(i - 20, -50)
        glVertex2f(i + 20, -50)
        glVertex2f(i, 20)
        glEnd()

# Function to draw the ground
def draw_ground():
    glColor3f(1, 0.6, 0.0)  # Brown soil
    glBegin(GL_QUADS)
    glVertex2f(-500, -100)
    glColor3f(1, 0.6, 0.0)
    glVertex2f(500, -100)
    glColor3f(0.5, 0, 0.0)
    glVertex2f(500, -300)
    glColor3f(0.5, 0, 0.0)
    glVertex2f(-500, -300)
    glEnd()

def draw_rain():
    glColor3f(0.5, 0.5, 1.0)  # Light blue raindrops
    glLineWidth(2)  # Slightly thicker raindrops
    glBegin(GL_LINES)
    for x, y in raindrops:
        glVertex2f(x, y)
        glVertex2f(x, y - 30)  # Make the drops longer
    glEnd()


def keyboardListener(key, x, y):
    global background_color
    if key == b'd':  # Day mode
        background_color = [0.5, 0.8, 1.0]
    elif key == b'n':  # Night mode
        background_color = [0.0, 0.0, 0.0]
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_offset
    if key == GLUT_KEY_LEFT:
        rain_offset -= 1  # Move rain left smoothly
    elif key == GLUT_KEY_RIGHT:
        rain_offset += 1  # Move rain right smoothly
    glutPostRedisplay()


def animate():
    global raindrops
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        y -= rain_speed
        if y < -300:
            y = random.randint(100, 300)
            x = random.randint(-500, 500)
        raindrops[i] = (x, y)
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*background_color, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 500, 0, 0, 0, 0, 1, 0)
    draw_ground()
    draw_trees()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"House in Rain")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMainLoop()
