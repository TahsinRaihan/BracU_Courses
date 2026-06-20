from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Game state variables
game_over_print = False
player_pos = [0.0, 0.0, 0.0]
player_angle = 0.0
player_height = 15.0  # Player's eye height
bullets = []
enemies = []
health_pickups = []
power_ups = []
cheat_mode = False
follow_camera = False
camera_angle = 0
camera_height = 900  # Default camera height for intended gameplay
game_paused = False

# Game state
game_score = 0
player_lives = 5
bullets_missed = 0
game_over = False
current_wave = 0
max_health = 5
player_health = max_health
zombies_killed = 0

# Game constants
MAX_ENEMIES = 5
MAX_MISSED_BULLETS = 10
BOUNDARY_SIZE = 1000

class Vector3:  # Vector movement
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def to_list(self):
        return [self.x, self.y, self.z]

    def distance(self, other):  # Calculates distance between two vectors
        return math.sqrt((self.x - other.x) ** 2 +
                         (self.y - other.y) ** 2 +
                         (self.z - other.z) ** 2)

    def move(self, dx, dy, dz):  # Movement in vector space
        self.y += dy
        self.z += dz

class Bullet:
    def __init__(self, x, y, z, angle, target_enemy=None):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.hit = False
        self.hit_enemy = False
        self.target_enemy = target_enemy

    def update(self):
        if self.hit:  # if the bullet hit something then no update
            return

        speed = 1

        if self.target_enemy and not self.target_enemy.hit:  # Cheat Mode distance calculation
            dx = self.target_enemy.x - self.x
            dz = self.target_enemy.z - self.z
            dy = self.target_enemy.y - self.y

            distance = math.sqrt(dx * dx + dz * dz + dy * dy)

            if distance > 0:
                self.x += (dx / distance) * speed
                self.y += (dy / distance) * speed
                self.z += (dz / distance) * speed
        else:  # Normal Mode bullet direction in XZ plane
            new_x = self.x + speed * math.sin(math.radians(self.angle))
            new_z = self.z + speed * math.cos(math.radians(self.angle))

            half_size = (BOUNDARY_SIZE / 2) - 5

            if abs(new_x) < half_size and abs(new_z) < half_size:  # Bullet to keep in boundary
                self.x = new_x
                self.z = new_z
            else:
                self.hit = True

    def is_alive(self):
        return not self.hit

    def draw(self):
        glPushMatrix()
        glColor3f(1, 0, 0)  # Red bullets
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 1, 0)  # Orient the cube in firing direction
        glScalef(3, 3, 6)  # Make it longer in the direction of travel
        glutSolidCube(1)  # Cube Bullets
        glPopMatrix()

class Enemy:
    def __init__(self, enemy_type='normal'):
        self.respawn(enemy_type)  # To respawn at random location
        self.target = False
        self.hit = False

    def respawn(self, enemy_type):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(300, 450)
        self.x = distance * math.sin(angle)
        self.z = distance * math.cos(angle)
        self.y = 15
        self.speed = 0.1 if enemy_type == 'normal' else (0.2 if enemy_type == 'runner' else 0.05)
        self.health = 1 if enemy_type == 'normal' else (0.5 if enemy_type == 'runner' else 2)
        self.type = enemy_type
        self.hit = False
        self.target = False

    def update(self):
        if game_paused:
            return

        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx * dx + dz * dz)  # Distance in XZ plane from player

        if distance > 0:  # Move along the distance
            self.x += (dx / distance) * self.speed
            self.z += (dz / distance) * self.speed

    def draw(self):
        if self.hit:
            return

        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(0, 1, 0) if self.type == 'normal' else (0, 0, 1) if self.type == 'runner' else (1, 0, 0)
        glutSolidSphere(15, 20, 20)
        glPopMatrix()

    def check_collision_with_player(self):  # if enemy is within range of player
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx * dx + dz * dz)
        return distance < 30

    def check_collision_with_bullet(self, bullet):  # if bullets within range of enemy
        dx = bullet.x - self.x
        dz = bullet.z - self.z
        distance = math.sqrt(dx * dx + dz * dz)
        return distance < 15

class HealthPickup:
    def __init__(self):
        self.x = random.uniform(-BOUNDARY_SIZE / 2, BOUNDARY_SIZE / 2)
        self.y = 0
        self.z = random.uniform(-BOUNDARY_SIZE / 2, BOUNDARY_SIZE / 2)

    def draw(self):
        glPushMatrix()
        glColor3f(0, 1, 0)  # Green color for health pickup
        glTranslatef(self.x, self.y, self.z)
        glutSolidCube(5)  # Size of the health pickup
        glPopMatrix()

class PowerUp:
    def __init__(self, type):
        self.type = type
        self.x = random.uniform(-BOUNDARY_SIZE / 2, BOUNDARY_SIZE / 2)
        self.y = 0
        self.z = random.uniform(-BOUNDARY_SIZE / 2, BOUNDARY_SIZE / 2)
        self.active = True
        self.timer = 10  # Active for 10 seconds

    def update(self):
        if self.active:
            self.timer -= 1  # Decrease timer
            if self.timer <= 0:
                self.active = False  # Power-up expires

    def draw(self):
        if self.active:
            glPushMatrix()
            glColor3f(1, 1, 0)  # Yellow color for power-up
            glTranslatef(self.x, self.y, self.z)
            glutSolidSphere(5, 20, 20)  # Size of the power-up
            glPopMatrix()

def draw_cube(x, y, z, size=1, color=(1, 0, 0)):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    glutSolidCube(size)
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0, player_pos[2])
    glRotatef(player_angle, 0, 1, 0)

    # Legs
    glColor3f(0.6, 0.0, 1.0)
    for x in [7, -7]:
        glPushMatrix()
        glTranslatef(x, 20, 0)
        glRotatef(90, 1, 0, 0)
        quad = gluNewQuadric()
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

    # Arms
    glColor3f(0.8, 0.7, 0.6)
    for x in [-12, 12]:
        glPushMatrix()
        glTranslatef(x, 45, 0)
        glRotatef(0, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 4, 2, 18, 12, 2)
        glPopMatrix()

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

    # Red text
    glColor3f(1, 0, 0)

    draw_text(10, 20, f"Player Health: {player_health}/{max_health}")
    draw_text(10, 40, f"Wave: {current_wave}")
    draw_text(10, 60, f"Zombies Killed: {zombies_killed}")

    if game_over:
        draw_text(glutGet(GLUT_WINDOW_WIDTH) // 2 - 100,
                  glutGet(GLUT_WINDOW_HEIGHT) // 2, "GAME OVER - Press R to restart")

    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))  # Font & Size of the text

def draw_floor():
    glDisable(GL_LIGHTING)

    size = 50
    rows, cols = 20, 20

    for i in range(-rows // 2, rows // 2):
        for j in range(-cols // 2, cols // 2):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.6, 0.4, 0.8)

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

    glEnable(GL_LIGHTING)

def update_game():
    global bullets, enemies, health_pickups, power_ups, game_score, player_health, bullets_missed, game_over, game_over_print, zombies_killed

    if game_over or game_paused:
        if game_over and not game_over_print:
            print("Player Died. Game Over!! Better Luck Next Time")
            game_over_print = True
        return

    new_bullets = []  # Bullet count
    for bullet in bullets:
        bullet.update()
        if bullet.is_alive():
            new_bullets.append(bullet)
        else:
            if not bullet.hit_enemy:
                bullets_missed += 1
                print(f"Player missed bullet: {bullets_missed}")
                if bullets_missed >= MAX_MISSED_BULLETS:
                    game_over = True
    bullets = new_bullets

    # Spawn health pickups
    if random.random() < 0.01:  # 1% chance to spawn health pickup
        health_pickups.append(HealthPickup())

    # Update health pickups
    for pickup in health_pickups:
        if player_health < max_health and pickup.x is not None:
            if abs(player_pos[0] - pickup.x) < 5 and abs(player_pos[2] - pickup.z) < 5:
                player_health += 1
                health_pickups.remove(pickup)
                print(f"Health increased! Current Health: {player_health}")

    # Spawn power-ups
    if random.random() < 0.01:  # 1% chance to spawn power-up
        power_ups.append(PowerUp(random.choice(['shield', 'weapon_upgrade'])))

    # Update power-ups
    for power_up in power_ups:
        power_up.update()
        if not power_up.active:
            power_ups.remove(power_up)

    # Manage enemies
    while len(enemies) < MAX_ENEMIES + current_wave:  # Increase number of enemies with each wave
        enemy_type = random.choice(['normal', 'runner', 'tank'])
        enemies.append(Enemy(enemy_type))

    new_enemies = []
    for enemy in enemies:
        enemy.update()

        if enemy.check_collision_with_player():
            player_health -= 1
            print(f"Player Remaining Health: {player_health}")
            if player_health <= 0:
                game_over = True
            enemy.respawn(random.choice(['normal', 'runner', 'tank']))

        hit = False
        for bullet in bullets:  # If bullet hits then enemy respawn
            if not bullet.hit and enemy.check_collision_with_bullet(bullet):
                bullet.hit = True
                bullet.hit_enemy = True
                enemy.hit = True
                zombies_killed += 1
                game_score += 1
                enemy.respawn(random.choice(['normal', 'runner', 'tank']))
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

def draw_all_health_pickups():
    for pickup in health_pickups:
        pickup.draw()

def draw_all_power_ups():
    for power_up in power_ups:
        power_up.draw()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if follow_camera:
        # First person view - from player's perspective
        eye_height = player_height + 23
        cam_x = player_pos[0]
        cam_y = player_pos[1] + eye_height
        cam_z = player_pos[2]

        look_dist = 100
        look_x = cam_x + look_dist * math.sin(math.radians(player_angle))
        look_y = cam_y
        look_z = cam_z + look_dist * math.cos(math.radians(player_angle))

        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 1, 0)
    else:
        # Third person view - orbiting camera
        radius = 200
        cam_x = player_pos[0] + radius * math.sin(math.radians(camera_angle))
        cam_z = player_pos[2] + radius * math.cos(math.radians(camera_angle))
        cam_y = player_pos[1] + camera_height  # Use the adjustable camera height

        gluLookAt(cam_x, cam_y, cam_z,
                  player_pos[0], player_pos[1], player_pos[2],
                  0, 1, 0)

def fire_bullet():
    global bullets, bullets_missed

    if game_paused:
        return

    target_enemy = None
    if cheat_mode:
        min_distance = float('inf')
        closest_enemy = None

        for enemy in enemies:
            if not enemy.hit and not enemy.target:  # Calculate distance between enemy & player
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx * dx + dz * dz)

                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy

        if closest_enemy:
            target_enemy = closest_enemy
            target_enemy.target = True

    if follow_camera:
        gun_x = player_pos[0]
        gun_y = player_pos[1] + player_height + 10
        gun_z = player_pos[2]
        bullets.append(Bullet(gun_x, gun_y, gun_z, player_angle, target_enemy))
    else:
        gun_offset_front = 25
        gun_x = player_pos[0] + gun_offset_front * math.sin(math.radians(player_angle))
        gun_y = player_pos[1] + 35
        gun_z = player_pos[2] + gun_offset_front * math.cos(math.radians(player_angle))

        bullets.append(Bullet(gun_x, gun_y, gun_z, player_angle, target_enemy))
    print("Player fired bullet")

def move_player(dx, dz):  # player movement
    global player_pos

    if game_paused:
        return

    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz

    half_size = (BOUNDARY_SIZE / 2) - 30

    if abs(new_x) < half_size and abs(new_z) < half_size:  # to ensure player does not go out of boundary
        player_pos[0] = new_x
        player_pos[2] = new_z

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    setupCamera()
    draw_floor()

    draw_all_enemies()
    draw_all_bullets()
    draw_all_health_pickups()
    draw_all_power_ups()
    draw_player()
    draw_status()

    glutSwapBuffers()

def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(-500, 0, 0)  # X axis
    glVertex3f(500, 0, 0)
    glColor3f(0, 1, 0)
    glVertex3f(0, -500, 0)  # Y axis
    glVertex3f(0, 500, 0)
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -500)
    glVertex3f(0, 0, 500)  # Z axis
    glEnd()

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, follow_camera, game_over, game_over_print, game_paused

    if game_over:
        if key == b'r':
            reset_game()
            if game_over_print:
                game_over_print = False
        return

    if key == b'p':
        game_paused = not game_paused
        print("Game", "paused" if game_paused else "resumed")
        return

    if game_paused:
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
    elif key == b'v' and cheat_mode:
        follow_camera = not follow_camera

def specialKeyListener(key, x, y):
    global camera_angle, camera_height

    if game_paused:
        return

    # Left/Right arrows now rotate camera around player
    if key == GLUT_KEY_LEFT:
        camera_angle -= 5  # rotation speed
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5
    elif key == GLUT_KEY_UP:
        camera_height += 10  # movement speed
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10
        camera_height = max(50, camera_height)  # Cannot go below ground level

def mouseListener(button, state, x, y):
    global follow_camera

    if game_paused:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        follow_camera = not follow_camera

def reset_game():  # Resets everything when restart
    global player_pos, player_angle, bullets, enemies, health_pickups, power_ups
    global cheat_mode, follow_camera, game_paused
    global game_score, player_health, bullets_missed, game_over, current_wave, zombies_killed

    player_pos = [0.0, 0.0, 0.0]
    player_angle = 0.0
    bullets = []
    enemies = []
    health_pickups = []
    power_ups = []
    cheat_mode = False
    follow_camera = False
    game_paused = False

    game_score = 0
    player_health = max_health
    bullets_missed = 0
    game_over = False
    current_wave = 0
    zombies_killed = 0

def idle():  # the main background function closest enemy calculation and fire bullet
    if not game_paused:
        update_game()

        if cheat_mode and not game_over:  # if cheat mode find closest enemy and hit
            global player_angle

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

            if closest_enemy:  # rotate towards enemy
                dx = closest_enemy.x - player_pos[0]
                dz = closest_enemy.z - player_pos[2]
                angle_to_enemy = math.degrees(math.atan2(dx, dz))

                while angle_to_enemy < 0:
                    angle_to_enemy += 360

                target_angle = 360 - angle_to_enemy
                while target_angle >= 360:
                    target_angle -= 360

                angle_diff = target_angle - player_angle
                while angle_diff > 180:
                    angle_diff -= 360
                while angle_diff < -180:
                    angle_diff += 360

                player_angle += angle_diff * 0.1

                if abs(angle_diff) < 10 and random.random() < 0.2:
                    fire_bullet()

        for enemy in enemies:
            if enemy.hit:
                enemy.target = False

            if enemy.target:
                bullet_still_tracking = False
                for bullet in bullets:
                    if bullet.target_enemy == enemy and bullet.is_alive():
                        bullet_still_tracking = True
                        break

                if not bullet_still_tracking:
                    enemy.target = False

    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_pos = [200.0, 300.0, 200.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    for _ in range(MAX_ENEMIES):  # When it reset add max=5 enemies in enemy list
        enemies.append(Enemy(random.choice(['normal', 'runner', 'tank'])))

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL Zombie Survival Game")

    init()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
