from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import random
game_over_print = False

player_pos = [0.0, 0.0, 0.0]
player_angle = 0.0
player_height = 15.0  # Player's eye height
bullets = []
enemies = []
particles = []
cheat_mode = False
follow_camera = False
camera_angle = 0  # Changed to show more of the boundary
camera_height = 200  # Reduced from 800 to make camera movement more noticeable
camera_distance = 200  # Added camera distance for better control

# Game state
game_score = 0
player_lives = 5
bullets_missed = 0
game_over = False

# Game constants
MAX_ENEMIES = 5
MAX_MISSED_BULLETS = 10
BOUNDARY_SIZE = 1000  # Define boundary size

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def to_list(self):
        return [self.x, self.y, self.z]

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2 +
                         (self.z - other.z) ** 2)  ##3d euclid 2ta vector er majer dis

    def move(self, dx, dy, dz): #vector movement
        self.y += dy
        self.z += dz

class Bullet:
    def __init__(self, x, y, z, angle, target_enemy=None):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.hit = False  # True if hit enemy or boundary
        self.hit_enemy = False  # Specifically hit an enemy
        self.target_enemy = target_enemy  # For guided bullets in cheat mode

    def update(self):
        if self.hit:
            return

        speed = 1

        # If in cheat/auto mode with a target, guide the bullet to the enemy
        if self.target_enemy and not self.target_enemy.hit:
            # Calculate direction to target
            dx = self.target_enemy.x - self.x
            dz = self.target_enemy.z - self.z
            dy = self.target_enemy.y - self.y

            distance = math.sqrt(dx * dx + dz * dz + dy * dy)

            if distance > 0:
                self.x += (dx / distance) * speed
                self.y += (dy / distance) * speed
                self.z += (dz / distance) * speed
        else:
            new_x = self.x + speed * math.sin(math.radians(self.angle)) # x dane bamme, y upre niche
            new_z = self.z + speed * math.cos(math.radians(self.angle))# front behind

            # Check if new position is within boundary
            half_size = (BOUNDARY_SIZE / 2) - 5  # Buffer from wall

            if abs(new_x) < half_size and abs(new_z) < half_size:
                self.x = new_x
                self.z = new_z
            else:
                # Hit boundary wall, mark as hit to be removed
                self.hit = True
                # Create impact particles

    def is_alive(self):
        return not self.hit  #

    def draw(self):
        glPushMatrix()
        glColor3f(1, 0, 0)  # Red bullets
        glTranslatef(self.x, self.y, self.z)
        # Changed from sphere to cube
        glutSolidCube(5)  # Cube bullets instead of spheres
        glPopMatrix()

class Enemy:
    def __init__(self):
        self.respawn() #nnew enemy
        self.target = False  # Track if this enemy is currently targeted
        self.hit = False

    def respawn(self, value=None):
        angle = random.uniform(0, 2 * math.pi) #j kono dik theke enemy
        distance = random.uniform(300, 450)  # Keep inside boundary
        self.x = distance * math.sin(angle)
        self.z = distance * math.cos(angle)
        self.y = 15 #vumir upre
        self.speed = random.uniform(0.02, 0.2)  # Reduced speed range
        self.scale = 1.0
        self.scale_direction = 0.02
        self.hit = False
        self.target = False  # Reset target status when respawning

    def update(self): #enemy movement and body pulsing
        # Move towards player
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx * dx + dz * dz)

        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.z += (dz / distance) * self.speed

        # Pulsate size # pulsing
        self.scale += self.scale_direction
        if self.scale > 1.2 or self.scale < 0.8:
            self.scale_direction *= -1

    def draw(self):
        if self.hit:
            return

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScalef(self.scale, self.scale, self.scale)

        # Red body sphere (larger)
        glColor3f(1, 0, 0)  # Red enemy body
        glutSolidSphere(15, 20, 20)

        # Black head sphere (smaller)
        glColor3f(0, 0, 0)  # Black enemy head
        glTranslatef(0, 15, 0)
        glutSolidSphere(10, 16, 16)

        glPopMatrix()

    def check_collision_with_player(self):
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx * dx + dz * dz)
        return distance < 30

    def check_collision_with_bullet(self, bullet):
        dx = bullet.x - self.x
        dz = bullet.z - self.z
        distance = math.sqrt(dx * dx + dz * dz)
        return distance < 15

def draw_cube(x, y, z, size=1, color=(1, 0, 0)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    glutSolidCube(size)
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0, player_pos[2])  # Position the player
    glRotatef(player_angle, 0, 1, 0)  # Rotate player based on angle

    if game_over:
        glRotatef(90, 1, 0, 0)  # Rotate player to lie flat when dead

    # Legs - Upper part thick, lower part thin, remains same after death
    glColor3f(0.6, 0.0, 1.0)  # Leg color
    for x in [7, -7]:  # Two legs, spaced apart
        glPushMatrix()
        glTranslatef(x, 20, 0)  # Lower the legs when laying flat
        glRotatef(90, 1, 0, 0)  # No rotation needed while lying down
        quad = gluNewQuadric()
        # Thick upper leg (6), gradually thin lower leg (2)
        gluCylinder(quad, 6, 3, 25, 12, 6)
        glPopMatrix()

    # Torso
    glColor3f(0.2, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(0, 35, 0)
    glScalef(20, 30, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 60, 0)
    glutSolidSphere(10, 16, 16)
    glPopMatrix()

    # Arms - Adjusted to connect naturally with shoulders
    glColor3f(0.8, 0.7, 0.6)
    for x in [-12, 12]:
        glPushMatrix()
        glTranslatef(x, 45, 0)  # Arms now correctly positioned at shoulder level
        glRotatef(0, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 4, 2, 18, 12, 2)  # Slightly thicker near shoulders, thinner at hands
        glPopMatrix()

    # Gun - Only draw if player is alive
    if not game_over:
        draw_gun()

    glPopMatrix()

def draw_gun():
    glPushMatrix()
    
    if follow_camera:
        # First-person view - draw gun in front of camera
        glColor3f(0.7, 0.7, 0.7)
        glTranslatef(0, -10, -20)  # Position gun in first-person view
        glRotatef(90, 1, 0, 0)  # Rotate gun to point forward
        
        # Gun barrel
        quad = gluNewQuadric()
        gluCylinder(quad, 2, 2, 40, 12, 2)  # Longer barrel for first-person view
        
        # Gun handle
        glPushMatrix()
        glTranslatef(0, 0, 10)
        glRotatef(90, 0, 1, 0)
        gluCylinder(quad, 3, 2, 15, 12, 2)
        glPopMatrix()
    else:
        # Third-person view - original gun
        glColor3f(0.7, 0.7, 0.7)
        glTranslatef(0, 38, 12)  # Better chest alignment
        quad = gluNewQuadric()
        gluCylinder(quad, 3.5, 2, 20, 12, 2)
    
    glPopMatrix()

def draw_status():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT), 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)

    # Draw status text
    glColor3f(1, 0, 0)

    # Player Lives
    draw_text(10, 20, f"Player Life Remaining: {player_lives}")

    # Game Score
    draw_text(10, 40, f"Game Score: {game_score}")

    # Bullets Missed
    draw_text(10, 60, f"Player Bullet Missed: {bullets_missed}")
    draw_text(10, 80, f"Camera Mode: {'First Person' if follow_camera else 'Third Person'}")
    draw_text(10, 100, f"Cheat Mode: {'ON' if cheat_mode else 'OFF'}")

    # Game Over message
    if game_over:
        draw_text(glutGet(GLUT_WINDOW_WIDTH) // 2 - 10,
                  glutGet(GLUT_WINDOW_HEIGHT) // 2,
                  "GAME OVER - Press R to restart")

    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text(x, y, text ):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def draw_floor():
    glDisable(GL_LIGHTING)

    # Draw checkered floor
    size = 50 #per squre
    rows, cols = 20, 20 #row collum

    for i in range(-rows // 2, rows // 2):
        for j in range(-cols // 2, cols // 2):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)  # White
            else:
                glColor3f(0.6, 0.4, 0.8)  # Purple

            x1 = i * size
            z1 = j * size
            x2 = (i + 1) * size
            z2 = (j + 1) * size

            glBegin(GL_QUADS)
            glVertex3f(x1, -1, z1)
            glVertex3f(x2, -1, z1)
            glVertex3f(x2, -1, z2)
            glVertex3f(x1, -1, z2)
            glEnd()

    # Draw boundary walls
    half_size = BOUNDARY_SIZE / 2
    wall_height = 50  # Increased wall height for visibility

    glBegin(GL_QUADS)
    # North wall (blue)
    glColor3f(1, 1, 1)
    glVertex3f(-half_size, -1, -half_size)
    glVertex3f(half_size, -1, -half_size)
    glVertex3f(half_size, wall_height, -half_size)
    glVertex3f(-half_size, wall_height, -half_size)

    # East wall (green)
    glColor3f(0, 1, 0)
    glVertex3f(half_size, -1, -half_size)
    glVertex3f(half_size, -1, half_size)
    glVertex3f(half_size, wall_height, half_size)
    glVertex3f(half_size, wall_height, -half_size)

    # South wall (cyan)
    glColor3f(0, 1, 1)
    glVertex3f(half_size, -1, half_size)
    glVertex3f(-half_size, -1, half_size)
    glVertex3f(-half_size, wall_height, half_size)
    glVertex3f(half_size, wall_height, half_size)

    # West wall (blue)
    glColor3f(0, 0, 1)
    glVertex3f(-half_size, -1, half_size)
    glVertex3f(-half_size, -1, -half_size)
    glVertex3f(-half_size, wall_height, -half_size)
    glVertex3f(-half_size, wall_height, half_size)
    glEnd()

    glEnable(GL_LIGHTING)

def update_game():
    global bullets, enemies, particles, game_score, player_lives, bullets_missed, game_over,game_over_print

    if game_over:
        if not game_over_print:
            print("Player Died. Game Over!! Better Luck Next Time")
            game_over_print=True
        return

    # Update bullets
    new_bullets = []
    for bullet in bullets:
        bullet.update()
        if bullet.is_alive():
            new_bullets.append(bullet)
        else:
            if not bullet.hit_enemy:
                bullets_missed += 1
                print(f"Player missed bullet:{bullets_missed}")
                if bullets_missed >= MAX_MISSED_BULLETS:
                    game_over = True
    bullets = new_bullets

    # Ensure we have enough enemies
    while len(enemies) < MAX_ENEMIES:
        enemies.append(Enemy())

    # Update enemies
    new_enemies = []
    for enemy in enemies:
        enemy.update()

        # Check enemy collision with player
        if enemy.check_collision_with_player():
            player_lives -= 1
            print(f"Player Remaining Life:{player_lives}")
            if player_lives <= 0:
                game_over = True
            enemy.respawn()

        # Check enemy collision with bullets
        hit = False
        for bullet in bullets:
            if not bullet.hit and enemy.check_collision_with_bullet(bullet):
                bullet.hit = True
                bullet.hit_enemy = True  # Mark that this bullet hit an enemy
                enemy.hit = True
                game_score += 1
                enemy.respawn()
                hit = True
                break

        if not hit:
            new_enemies.append(enemy)
    enemies = new_enemies

def draw_all_bullets():
    for bullet in bullets:
        bullet.draw()

def draw_all_enemies():
    for enemy in enemies:
        enemy.draw()

def setupCamera():
    glMatrixMode(GL_PROJECTION)# duruer jinish choto kacher boro
    glLoadIdentity()
    gluPerspective(60, 1.25, 1,1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if follow_camera:
        # First person view
        eye_height = player_height + 30  # Eye height is above player position
        cam_x = player_pos[0]
        cam_y = player_pos[1] + eye_height
        cam_z = player_pos[2]

        # Look point is in front of player
        look_dist = 100
        look_x = cam_x + look_dist * math.sin(math.radians(player_angle))
        look_y = cam_y
        look_z = cam_z + look_dist * math.cos(math.radians(player_angle))

        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 1, 0)
    else:
        # Third person view - adjusted to see all boundaries
        cam_x = player_pos[0] + camera_distance * math.sin(math.radians(camera_angle))
        cam_z = player_pos[2] + camera_distance * math.cos(math.radians(camera_angle))
        cam_y = player_pos[1] + camera_height

        gluLookAt(cam_x, cam_y, cam_z,
                  player_pos[0], player_pos[1], player_pos[2],
                  0, 1, 0)

def fire_bullet():
    global bullets, bullets_missed

    # In cheat mode or auto fire, find a target enemy
    target_enemy = None
    if cheat_mode:
        # Find closest live enemy that's not already targeted
        min_distance = float('inf')
        closest_enemy = None

        for enemy in enemies:
            if not enemy.hit and not enemy.target:
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx * dx + dz * dz)

                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy

        if closest_enemy:
            target_enemy = closest_enemy
            target_enemy.target = True  # Mark this enemy as targeted

    if follow_camera:
        # First person mode - fire from camera position
        gun_x = player_pos[0]
        gun_y = player_pos[1] + player_height + 10
        gun_z = player_pos[2]
        bullets.append(Bullet(gun_x, gun_y, gun_z, player_angle, target_enemy))
    else:
        # Third person mode - fire from player's gun at chest level
        gun_offset_front = 25  # Distance in front of player
        gun_x = player_pos[0] + gun_offset_front * math.sin(math.radians(player_angle))
        gun_y = player_pos[1] + 35  # Height of gun at chest level
        gun_z = player_pos[2] + gun_offset_front * math.cos(math.radians(player_angle))

        bullets.append(Bullet(gun_x, gun_y, gun_z, player_angle, target_enemy))
    print("Player fired bullet")

def move_player(dx, dz):
    global player_pos

    # Calculate new position
    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz

    # Check boundary
    half_size = (BOUNDARY_SIZE / 2) - 30  # Buffer from wall

    if abs(new_x) < half_size and abs(new_z) < half_size:
        player_pos[0] = new_x
        player_pos[2] = new_z

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    setupCamera()
    draw_floor()
    draw_axes()

    # Only draw player if not in first person mode
    if not follow_camera or game_over:
        draw_player()

    draw_all_bullets()
    draw_all_enemies()
    draw_status()

    glutSwapBuffers()

def draw_axes():
        glBegin(GL_LINES)
        # X - Red
        glColor3f(1, 0, 0)
        glVertex3f(-500, 0, 0)
        glVertex3f(500, 0, 0)
        # Y - Green
        glColor3f(0, 1, 0)
        glVertex3f(0, -500, 0)
        glVertex3f(0, 500, 0)
        # Z - Blue
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, -500)
        glVertex3f(0, 0, 500)
        glEnd()

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, follow_camera, game_over,game_over_print

    if game_over:
        if key == b'r':
            reset_game()
            if game_over_print==True:
                game_over_print=False
        return

    if key == b's':
        move_player(-5 * math.sin(math.radians(player_angle)),
                    -5 * math.cos(math.radians(player_angle)))
    elif key == b'w':
        move_player(5 * math.sin(math.radians(player_angle)),
                    5 * math.cos(math.radians(player_angle)))
    elif key == b'a':
        player_angle += 5
    elif key == b'd':
        player_angle -= 5
    elif key == b'c':
        cheat_mode = not cheat_mode
    if cheat_mode==True:
        if key == b'v':
            follow_camera = not follow_camera

def specialKeyListener(key, x, y):
    global camera_angle, camera_height, camera_distance

    # Camera rotation (left/right)
    if key == GLUT_KEY_LEFT:
        camera_angle -= 5  # Increased rotation speed
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5  # Increased rotation speed
    # Camera movement (up/down)
    elif key == GLUT_KEY_UP:
        camera_distance -= 5  # Move camera closer
        if camera_distance < 50:  # Minimum distance
            camera_distance = 50
    elif key == GLUT_KEY_DOWN:
        camera_distance += 5  # Move camera farther
        if camera_distance > 400:  # Maximum distance
            camera_distance = 400

def mouseListener(button, state, x, y):
    global follow_camera
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        follow_camera = not follow_camera

def reset_game():
    global player_pos, player_angle, bullets, enemies, particles
    global cheat_mode, follow_camera
    global game_score, player_lives, bullets_missed, game_over

    player_pos = [0.0, 0.0, 0.0]
    player_angle = 0.0
    bullets = []
    enemies = []
    particles = []
    cheat_mode = False
    follow_camera = False

    game_score = 0
    player_lives = 5
    bullets_missed = 0
    game_over = False

def idle():
    update_game()

    # Cheat mode (auto aim and fire)
    if cheat_mode and not game_over:
        global player_angle

        # Find closest untargeted enemy
        closest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            if enemy.hit or enemy.target:
                continue

            dx = enemy.x - player_pos[0]
            dz = enemy.z - player_pos[2]
            distance = math.sqrt(dx * dx + dz * dz)

            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy

        # If enemy found, turn player to face it
        if closest_enemy:
            # Calculate angle to enemy
            dx = closest_enemy.x - player_pos[0]
            dz = closest_enemy.z - player_pos[2]
            angle_to_enemy = math.degrees(math.atan2(dx, dz))

            # Normalize to 0-360
            while angle_to_enemy < 0:
                angle_to_enemy += 360

            # Set player angle to face enemy
            target_angle = 360 - angle_to_enemy
            while target_angle >= 360:
                target_angle -= 360

            # Gradually turn toward target
            angle_diff = target_angle - player_angle
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360

            player_angle += angle_diff * 0.1  # Smooth turning

            # Fire when approximately facing the enemy
            if abs(angle_diff) < 10 and random.random() < 0.2:
                fire_bullet()

    # Reset targeting for enemies that have been hit or are no longer associated with bullets
    for enemy in enemies:
        if enemy.hit:
            enemy.target = False

        # Check if any bullet is still tracking this enemy
        if enemy.target:
            bullet_still_tracking = False
            for bullet in bullets:
                if bullet.target_enemy == enemy and bullet.is_alive():
                    bullet_still_tracking = True
                    break

            # If no bullet is tracking this enemy anymore, reset target flag
            if not bullet_still_tracking:
                enemy.target = False

    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    # LIGHTING
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_pos = [200.0, 300.0, 200.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    # Initialize enemies
    for _ in range(MAX_ENEMIES):
        enemies.append(Enemy())

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Gun Game")

    init()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()