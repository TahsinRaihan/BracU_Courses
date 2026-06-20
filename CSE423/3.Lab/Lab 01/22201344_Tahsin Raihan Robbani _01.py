#Task_1_House in Rain
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 800, 500
rain_speed = 2  # Slower raindrop speed
rain_slope = 0  # Controls the slope of the raindrops

# List to store raindrop positions
raindrops = [(random.randint(0, 500), random.randint(0, 500)) for _ in range(100)]
background_color = [0.0, 0.0, 0.0]

def draw_house():
    glColor3f(0, 0.5, 0.5)  # House color
    glBegin(GL_QUADS)
    glVertex2f(-100, -100)
    glColor3f(1, 0.5, 0.5)
    glVertex2f(100, -100)
    glColor3f(1, 1, 1)
    glVertex2f(100, 50)
    glColor3f(1,0.5, 0)
    glVertex2f(-100, 50)
    glEnd()

    glColor3f(1, 0, 1)  #Roof color
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

def draw_trees():
    for i in range(-475, 500, 45): #Loop because we want multiple trees
        glColor3f(0.4, 0.2, 0.0)  # Brown trunk
        glBegin(GL_QUADS)
        glVertex2f(i - 5, -100)
        glVertex2f(i + 5, -100)
        glVertex2f(i + 5, -50)
        glVertex2f(i - 5, -50)
        glEnd()

        glColor3f(0.0, 0.7, 0.0)  # Green leaves
        glBegin(GL_TRIANGLES)
        glVertex2f(i - 20, -50)
        glColor3f(0.0, 0.7, 0.0)
        glVertex2f(i + 20, -50)
        glColor3f(0.0, 0.8, 0.0)
        glVertex2f(i, 20)
        glEnd()

def draw_ground():
    glColor3f(1, 0.6, 0.0)  # Brown soil
    glBegin(GL_QUADS)
    glVertex2f(-500, -100)
    glColor3f(1, 0.6, 0.0)
    glVertex2f(500, -100)
    glColor3f(0.5, 0, 0.0)
    glVertex2f(500, -500)
    glColor3f(0.5, 0, 0.0)
    glVertex2f(-500, -500)
    glEnd()

def draw_rain():
    glColor3f(0.5, 0.5, 1.0) 
    glLineWidth(2)  # Slightly thicker raindrops
    glBegin(GL_LINES)
    for x, y in raindrops:
        # Apply rain_slope to create a diagonal effect
        glVertex2f(x + rain_slope * (y - 250), y)  # Top of raindrop
        glVertex2f(x + rain_slope * (y - 280), y - 30)  # Bottom of raindrop
    glEnd()

def keyboardListener(key, x, y):
    global background_color, rain_slope
    if key == b'd':  # Day mode
        background_color = [0.9, 1, 1]
    elif key == b'n':  # Night mode
        background_color = [0.0, 0.0, 0.0]
    elif key == b'r':  # Reset rain slope
        rain_slope = 0
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_slope
    if key == GLUT_KEY_LEFT:
        rain_slope += 0.1  # Tilt rain to the left (positive slope)
    elif key == GLUT_KEY_RIGHT:
        rain_slope -= 0.1  # Tilt rain to the right (negative slope)
    glutPostRedisplay()

def animate():
    global raindrops
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        y -= rain_speed
        if y < -500:
            y = random.randint(500, 500)
            x = random.randint(-500, 500)
        raindrops[i] = (x, y)
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*background_color, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0,390, 0, 0, 0, 0, 1, 0)
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




#Task_2_Amazing Box

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random

# glutInit()
# W_Width, W_Height = 800, 700

# freeze = False  # To freeze/unfreeze points
# global_speed = 0.1 

# BOUNDARY_MIN_X, BOUNDARY_MAX_X = -W_Width // 2, W_Width // 2  # This ensures points stay within the window
# BOUNDARY_MIN_Y, BOUNDARY_MAX_Y = -W_Height // 2, W_Height // 2

# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.color = (random.random(), random.random(), random.random())  # Random color
#         self.direction_x = random.choice([-1, 1])  # Random x direction
#         self.direction_y = random.choice([-1, 1])  # Random y direction
#         self.speed = global_speed
#         self.blinking = False  # Blinking state
#         self.visible = True  # Used for blinking

# # To store all points
# points = []

# # Convert screen coordinates to OpenGL coordinates because mouse and opengl are not same
# def convert_coordinate(x, y):
#     cx = x - (W_Width / 2)  # Convert X to OpenGL space
#     cy = (W_Height / 2) - y  # Convert Y to OpenGL space
#     return cx, cy

# def draw_point(point):
#     if point.blinking and not point.visible:
#         return  # Skip drawing if blinking is active
#     glPointSize(10) 
#     glBegin(GL_POINTS)
#     glColor3f(*point.color)
#     glVertex2f(point.x, point.y)
#     glEnd()

# def keyboardListener(key, x, y):
#     global freeze
#     if key == b' ':  # Spacebar to freeze/unfreeze
#         freeze = not freeze
#         print("Freeze:", freeze)
#     glutPostRedisplay()

# def specialKeyListener(key, x, y):
#     global global_speed
#     if key == GLUT_KEY_UP:  # Increase speed
#         global_speed *= 1.1
#     elif key == GLUT_KEY_DOWN:  # Decrease speed
#         global_speed /= 1.1
#     for point in points:
#         point.speed = global_speed  # Update each point's speed
        
#     glutPostRedisplay()

# def mouseListener(button, state, x, y):
#     global points
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:  # Left click to start blinking for each point
#         for point in points:
#             point.blinking = not point.blinking
#         print("Blinking toggled for all points")
#         glutTimerFunc(500, blink_timer, 0)  # For continuous blinking
#     elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:  # Right click to add a point
#         cx, cy = convert_coordinate(x, y) #converted coordinates
#         new_point = Point(cx, cy)
#         points.append(new_point)
#         print(f"New point added at ({cx}, {cy})")
#     glutPostRedisplay()

# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#     for point in points:
#         draw_point(point)

#     glutSwapBuffers()

# def animate():
#     global points, freeze
#     if not freeze:
#         for point in points:
#             # Update position
#             point.x += point.direction_x * point.speed 
#             point.y += point.direction_y * point.speed

#             # Bounce from boundaries
#             if point.x <= BOUNDARY_MIN_X or point.x >= BOUNDARY_MAX_X:
#                 point.direction_x *= -1 #Reverse e ashbe
#             if point.y <= BOUNDARY_MIN_Y or point.y >= BOUNDARY_MAX_Y:
#                 point.direction_y *= -1

#     glutPostRedisplay()

# def blink_timer(value):
#     any_blinking = any(point.blinking for point in points)  # Check if any point is blinking
#     if any_blinking:
#         for point in points:
#             if point.blinking:
#                 point.visible = not point.visible  # Visible to blink and Blink to visible
#         glutTimerFunc(500, blink_timer, 0)  # Repeat every 500ms
#     glutPostRedisplay()

# def init():
#     glClearColor(0, 0, 0, 0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(-W_Width // 2, W_Width // 2, -W_Height // 2, W_Height // 2, -1, 1)  # Window projection (-400,400,-350,350,-1,1)

# glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# glutInitWindowSize(W_Width, W_Height)
# glutInitWindowPosition(0, 0) 
# glutCreateWindow(b"Amazing Box")
# init()
# glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)
# glutMainLoop()