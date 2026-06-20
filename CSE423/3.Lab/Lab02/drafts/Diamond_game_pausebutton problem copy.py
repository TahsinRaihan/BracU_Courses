from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time

screen_width = 800
screen_height = 600

catcher_x = screen_width // 2
catcher_y = 20

diamond_x = random.randint(50, screen_width - 50)
diamond_y = screen_height
diamond_speed = 150  # initial fall time in milliseconds
score = 0
game_over = False
is_paused = False
diamond_color = [random.uniform(0.6, 1.0), random.uniform(0.6, 1.0), random.uniform(0.6, 1.0)]
last_catch_time = time.time()

restart_area = (30, screen_height - 50)
pause_play_area = (screen_width / 2, screen_height - 50)
cross_area = (screen_width - 50, screen_height - 50)

def draw_points(x, y, color):
    glColor3fv(color)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def zero_zone_conv(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if (dx > 0 and dy > 0) and (abs_dx >= abs_dy):
        return x1, y1, x2, y2, 0
    elif (dx > 0 and dy > 0) and (abs_dx < abs_dy):
        return y1, x1, y2, x2, 1
    elif (dx < 0 and dy > 0) and (abs_dx < abs_dy):
        return y1, -x1, y2, -x2, 2
    elif (dx < 0 and dy > 0) and (abs_dx >= abs_dy):
        return -x1, y1, -x2, y2, 3
    elif (dx < 0 and dy < 0) and (abs_dx >= abs_dy):
        return -x1, -y1, -x2, -y2, 4
    elif (dx < 0 and dy < 0) and (abs_dx < abs_dy):
        return -y1, -x1, -y2, -x2, 5
    elif (dx > 0 and dy < 0) and (abs_dx < abs_dy):
        return -y1, x1, -y2, x2, 6
    else:
        return x1, -y1, x2, -y2, 7

def zero_to_org_zone(x, y, zone):
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
        return x, y

def mpl(x1, y1, x2, y2, color):
    x1, y1, x2, y2, zone = zero_zone_conv(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    x, y = x1, y1
    while x <= x2:
        x_org, y_org = zero_to_org_zone(x, y, zone)
        draw_points(x_org, y_org, color)
        if d > 0:
            d += NE
            y += 1
        else:
            d += E
        x += 1

def draw_diamond(x, y):
    if not game_over:
        mpl(x, y + 20, x - 15, y, diamond_color)
        mpl(x, y + 20, x + 15, y, diamond_color)
        mpl(x, y - 20, x - 15, y, diamond_color)
        mpl(x, y - 20, x + 15, y, diamond_color)

def draw_catcher(x, y):
    color = [1, 1, 1] if not game_over else [1, 0, 0]
    mpl(x - 70, y, x + 70, y, color)
    mpl(x - 70, y, x - 60, y - 20, color)
    mpl(x + 70, y, x + 60, y - 20, color)
    mpl(x - 60, y - 20, x + 60, y - 20, color)

def draw_restart_button(x, y):
    color = (0.0, 1.0, 1.0)
    mpl(x, y, x + 40, y, color)
    mpl(x, y, x + 20, y + 20, color)
    mpl(x, y, x + 20, y - 20, color)

def draw_pause_button(x, y):
    color = (1.0, 0.75, 0.0)
    if not is_paused:
        # Draw pause icon (two vertical bars)
        mpl(x - 10, y + 20, x - 10, y - 20, color)
        mpl(x + 10, y + 20, x + 10, y - 20, color)
    else:
        # Draw play icon (a triangle)
        mpl(x - 10, y + 20, x + 10, y, color)
        mpl(x + 10, y, x - 10, y - 20, color)
        mpl(x - 10, y - 20, x - 10, y + 20, color)  # Optional: Close triangle visually

def draw_cross(x, y):
    color = (1.0, 0.0, 0.0)
    mpl(x - 10, y + 10, x + 10, y - 10, color)
    mpl(x - 10, y - 10, x + 10, y + 10, color)

def update(value):
    global diamond_x, diamond_y, score, diamond_speed, game_over, diamond_color, last_catch_time
    if not is_paused and not game_over:
        current_time = time.time()
        time_passed = current_time - last_catch_time
        diamond_y -= 5
        if diamond_y < 0:
            game_over = True
            print("Game Over. Final Score:", score)
        if catcher_x - 70 <= diamond_x <= catcher_x + 70 and catcher_y <= diamond_y <= catcher_y + 20:
            score += 1
            print("Score:", score)
            diamond_x = random.randint(50, screen_width - 50)
            diamond_y = screen_height
            diamond_speed = max(16, diamond_speed - int(time_passed * 5))
            diamond_color = [random.uniform(0.6, 1.0) for _ in range(3)]
            last_catch_time = current_time
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def mouse_click(button, state, x, y):
    global game_over, score, diamond_speed, diamond_x, diamond_y, is_paused, diamond_color, last_catch_time
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = screen_height - y

        # Quit Button (cross)
        if (screen_width - 50 <= x <= screen_width - 10) and (screen_height - 50 <= y <= screen_height - 10):
            print(f"Goodbye. Final Score: {score}")
            glutLeaveMainLoop()

        # Pause/Play Button (middle)
        elif (pause_play_area[0] - 25 <= x <= pause_play_area[0] + 25) and (pause_play_area[1] - 25 <= y <= pause_play_area[1] + 25):
            if not game_over:
                is_paused = not is_paused
                print("Paused" if is_paused else "Resumed")

        # Restart Button (left)
        elif (10 <= x <= 60) and (screen_height - 50 <= y <= screen_height - 10):
            print("Starting Over")
            game_over = False
            score = 0
            diamond_speed = 150
            diamond_x = random.randint(50, screen_width - 50)
            diamond_y = screen_height
            is_paused = False
            diamond_color = [random.uniform(0.6, 1.0) for _ in range(3)]
            last_catch_time = time.time()

# ... [rest of your original unchanged code: special_keys, display, GLUT setup etc.]


def special_keys(key, x, y):
    global catcher_x
    if not is_paused and not game_over:
        step = 10
        if key == GLUT_KEY_RIGHT:
            catcher_x = min(catcher_x + step, screen_width - 70)
        elif key == GLUT_KEY_LEFT:
            catcher_x = max(catcher_x - step, 70)

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, screen_width, 0, screen_height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_restart_button(restart_area[0], restart_area[1])
    draw_pause_button(pause_play_area[0], pause_play_area[1])
    draw_cross(cross_area[0], cross_area[1])
    draw_diamond(diamond_x, diamond_y)
    draw_catcher(catcher_x, catcher_y)

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(screen_width, screen_height)
glutCreateWindow(b"Assignment 2")
glClearColor(0, 0, 0, 1)

glutDisplayFunc(display)
glutSpecialFunc(special_keys)
glutMouseFunc(mouse_click)
glutIdleFunc(display)
glutTimerFunc(16, update, 0)

glutMainLoop()
