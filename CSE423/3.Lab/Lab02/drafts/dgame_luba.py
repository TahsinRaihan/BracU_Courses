from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random


screen_width=800
screen_height=600

catcher_x = screen_width // 2  #center of the screen
catcher_y = 20  #lower wall

diamond_x = random.randint(50, screen_width - 50)   #jekono x theke fall korbe within x= 50 to 750
diamond_y = screen_height

diamond_speed = 5
score = 0
game_over = False
is_paused = False
diamond_color = [random.uniform(0.6, 1.0), random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]  # random generate color
restart_area=(30, screen_height-50)
pause_play_area = (screen_width / 2, screen_height - 50)
cross_area = (screen_width - 50, screen_height - 50)
def draw_points(x, y, color):
    glColor3fv(color)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def zero_zone_conv(x1, y1, x2, y2):  # ZONE determine korbo and return e zone zero te converted x,y and zone return korbo.
    dx = x2 - x1
    dy = y2 - y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)


    if (dx > 0 and dy > 0) and (abs_dx >= abs_dy):
        zone = 0
        return x1, y1, x2, y2, zone
    elif (dx > 0 and dy > 0) and (abs_dx < abs_dy):
        zone = 1
        return y1, x1, y2, x2, zone
    elif (dx < 0 and dy > 0) and (abs_dx < abs_dy):
        zone = 2
        return y1, -x1, y2, -x2, zone
    elif (dx < 0 and dy > 0) and (abs_dx >= abs_dy):
        zone = 3
        return -x1, y1, -x2, y2, zone
    elif (dx < 0 and dy < 0) and (abs_dx >= abs_dy):
        zone = 4
        return -x1, -y1, -x2, -y2, zone
    elif (dx < 0 and dy < 0) and (abs_dx < abs_dy):
        zone = 5
        return -y1, -x1, -y2, -x2, zone
    elif (dx > 0 and dy < 0) and (abs_dx < abs_dy):
        zone = 6
        return -y1, x1, -y2, x2, zone
    else:
        zone = 7
        return x1, -y1, x2, -y2, zone


def zero_to_org_zone(x, y, zone):  # 0 to any zone (x,y axis return korbe)
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        print("Error")
        return x, y


def mpl(x1, y1, x2, y2, color):
    x1, y1, x2, y2, zone = zero_zone_conv(x1, y1, x2, y2)  #get zone zero --x1,y1,x2,y2

    #zone zero formula
    dx = x2 - x1
    dy = y2 - y1

    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    #starting point determine
    x = x1
    y = y1

    while (x <= x2):  # jotokkhon cholbe,,,
        if (d > 0):
            d += NE
            x += 1
            y += 1
        else:
            d += E
            x += 1
            y += 0

        x_org, y_org = zero_to_org_zone(x, y, zone)   #back to main zone

        draw_points(x_org, y_org, color)  #draw===


def draw_diamond(x, y):
    global diamond_color
    mpl(x, y + 20, x - 15, y, diamond_color)
    mpl(x, y + 20, x + 15, y, diamond_color)

    mpl(x, y - 20, x - 15, y, diamond_color)
    mpl(x, y - 20, x + 15, y, diamond_color)


def draw_catcher(x, y):
    global catcher_x, catcher_y, game_over

    if game_over==False:
        color = [1, 1, 1]   #white

    else:
        color = [1, 0, 0]  #RED


    x, y = catcher_x, catcher_y  #x=center of width, y=20=lower wall

    mpl(x - 70, y, x + 70, y, color)  #uporer line
    mpl(x - 70, y, x - 60, y - 20, color) #left connector
    mpl(x + 70, y, x + 60, y - 20, color)  #right connector
    mpl(x - 60, y - 20, x + 60, y - 20, color)  #nicher line

def draw_restart_button(x,y):
    color = (0.0, 0.5, 1.0)  # blue color
    mpl(x, y, x + 40, y, color)
    mpl(x, y, x + 20, y + 20, color)
    mpl(x, y, x + 20, y - 20, color)


def draw_pause_button(x,y):
    if is_paused:

        glColor3f(1.0, 0.69, 0.0)
        glBegin(GL_POLYGON)
        glVertex2f(x - 20, y + 20)
        glVertex2f(x - 20, y - 20)
        glVertex2f(x + 10, y)
        glEnd()

    else:
        glColor3f(1.0, 0.69, 0.0)
        glLineWidth(5)
        glBegin(GL_LINES)

        glVertex2f(x + 10, y + 20)
        glVertex2f(x + 10, y - 20)

        glVertex2f(x - 20, y - 20)
        glVertex2f(x - 20, y + 20)
        glEnd()


def draw_cross(x, y):
        color = (1.0, 0.0, 0.0)
        mpl(x - 10, y + 10, x + 10, y - 8, color)
        mpl(x - 10, y - 10, x + 10, y + 8, color)



def update(value):
    global diamond_x, diamond_y, score, diamond_speed, game_over, diamond_color

    if is_paused==False and game_over==False:
        diamond_y -= diamond_speed

        if diamond_y < 0:
            game_over = True
            print("Game Over. Final Score:", score)

        if catcher_x - 70 <= diamond_x <= catcher_x + 70 and catcher_y <= diamond_y <= catcher_y + 20:
            score += 1
            print("Score:", score)
            diamond_x = random.randint(50, screen_width - 50)
            diamond_y = screen_height
            diamond_speed += 0.1  # Increase speed of falling diamond
            diamond_color = [random.uniform(0.6, 1.0), random.uniform(0.6, 1.0),
                             random.uniform(0.6, 1.0)]

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def mouse_click(button, state, x, y):
    global game_over, score, diamond_speed, diamond_x, diamond_y, is_paused, diamond_color
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = screen_height - y

        if (screen_width - 50 <= x <= screen_width - 10) and (screen_height - 50 <= y <= screen_height - 10):
            print(f"Goodbye. Final Score: {score}")

            glutLeaveMainLoop()


        elif (screen_width // 2 - 20 <= x <= screen_width // 2 + 20) and (
                screen_height - 50 <= y <= screen_height - 10):
            if game_over == False:
                is_paused = not is_paused

        elif (10 <= x <= 60) and (screen_height - 50 <= y <= screen_height - 10):
            print("Starting Over")

            game_over = False
            score = 0
            diamond_speed = 2
            diamond_x = random.randint(50, screen_width - 50)
            diamond_y = screen_height - 50
            is_paused = False
            diamond_color = [random.uniform(0.6, 1.0), random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]

def special_keys(key, x, y):
    global catcher_x
    if not is_paused:
        step = 10
        if not game_over:
            if key == GLUT_KEY_RIGHT:
                catcher_x = min(catcher_x + step, screen_width - 70)
            elif key == GLUT_KEY_LEFT:
                catcher_x = max(catcher_x - step, 70)





# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_restart_button(restart_area[0],restart_area[1])
    draw_pause_button(pause_play_area[0], pause_play_area[1])
    draw_cross(cross_area[0],cross_area[1])
    draw_diamond(diamond_x, diamond_y)
    draw_catcher(catcher_x, catcher_y)
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(screen_width, screen_height)
glutCreateWindow(b"Assignment 2")
glOrtho(0, screen_width, 0, screen_height, -1, 1)
glClearColor(0, 0, 0, 1)

glutDisplayFunc(display)
glutSpecialFunc(special_keys)
glutMouseFunc(mouse_click)
glutIdleFunc(display)
glutDisplayFunc(display)

glutSpecialFunc(special_keys)
glutIdleFunc(display)
glutTimerFunc(16, update, 0)

glutMainLoop()