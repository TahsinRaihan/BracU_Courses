from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

glutInit()
W_Width, W_Height = 800, 700

freeze = False  # To freeze/unfreeze points
global_speed = 0.1 

BOUNDARY_MIN_X, BOUNDARY_MAX_X = -W_Width // 2, W_Width // 2  # This ensures points stay within the window
BOUNDARY_MIN_Y, BOUNDARY_MAX_Y = -W_Height // 2, W_Height // 2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.random(), random.random(), random.random())  # Random color
        self.direction_x = random.choice([-1, 1])  # Random x direction
        self.direction_y = random.choice([-1, 1])  # Random y direction
        self.speed = global_speed
        self.blinking = False  # Blinking state
        self.visible = True  # Used for blinking

# To store all points
points = []

# Convert screen coordinates to OpenGL coordinates because mouse and opengl are not same
def convert_coordinate(x, y):
    cx = x - (W_Width / 2)  # Convert X to OpenGL space
    cy = (W_Height / 2) - y  # Convert Y to OpenGL space
    return cx, cy

def draw_point(point):
    if point.blinking and not point.visible:
        return  # Skip drawing if blinking is active
    glPointSize(10) 
    glBegin(GL_POINTS)
    glColor3f(*point.color)
    glVertex2f(point.x, point.y)
    glEnd()

def keyboardListener(key, x, y):
    global freeze
    if key == b' ':  # Spacebar to freeze/unfreeze
        freeze = not freeze
        print("Freeze:", freeze)
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global global_speed
    if freeze:  # Ignore input if frozen
        return
    if key == GLUT_KEY_UP:  # Increase speed
        global_speed *= 1.1
    elif key == GLUT_KEY_DOWN:  # Decrease speed
        global_speed /= 1.1
    for point in points:
        point.speed = global_speed  # Update each point's speed
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global points
    global freeze
    if freeze:  # Ignore input if frozen
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:  # Left click to start blinking for each point
        for point in points:
            point.blinking = not point.blinking
        print("Blinking toggled for all points")
        glutTimerFunc(500, blink_timer, 0)  # For continuous blinking
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:  # Right click to add a point
        cx, cy = convert_coordinate(x, y)  # Converted coordinates
        new_point = Point(cx, cy)
        points.append(new_point)
        print(f"New point added at ({cx}, {cy})")
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    for point in points:
        draw_point(point)
    glutSwapBuffers()

def animate():
    global points, freeze
    if freeze:  # Skip animation if frozen
        return
    for point in points:
        # Update position
        point.x += point.direction_x * point.speed 
        point.y += point.direction_y * point.speed

        # Bounce from boundaries
        if point.x <= BOUNDARY_MIN_X or point.x >= BOUNDARY_MAX_X:
            point.direction_x *= -1  # Reverse direction
        if point.y <= BOUNDARY_MIN_Y or point.y >= BOUNDARY_MAX_Y:
            point.direction_y *= -1
    glutPostRedisplay()

def blink_timer(value):
    if freeze:  # Skip blinking if frozen
        return
    any_blinking = any(point.blinking for point in points)  # Check if any point is blinking
    if any_blinking:
        for point in points:
            if point.blinking:
                point.visible = not point.visible  # Toggle visibility
        glutTimerFunc(500, blink_timer, 0)  # Repeat every 500ms
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W_Width // 2, W_Width // 2, -W_Height // 2, W_Height // 2, -1, 1)  # Window projection

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0) 
glutCreateWindow(b"Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()