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
obstacles = []
particles = []
cheat_mode = False
follow_camera = False
camera_angle = 0
camera_height = 200  # Adjusted for gameplay visibility
game_paused = False
fov = 60
fov_adjust_active = False

# Game state
game_score = 0
player_lives = 5
bullets_missed = 0
game_over = False
current_wave = 1
max_health = 5
player_health = max_health
zombies_killed = 0

# Game constants
MAX_ENEMIES_BASE = 5
MAX_MISSED_BULLETS = 10
BOUNDARY_SIZE = 1000
OBSTACLE_COUNT = 10
OBSTACLE_SIZE = 40

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def to_list(self):
        return [self.x, self.y, self.z]

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

class Particle:
    def __init__(self, x, y, z):
        self.x = x + random.uniform(-5, 5)
        self.y = y + random.uniform(0, 5)
        self.z = z + random.uniform(-5, 5)
        self.size = random.uniform(1, 3)
        self.dx = random.uniform(-0.8, 0.8)
        self.dy = random.uniform(0.5, 1.2)
        self.dz = random.uniform(-0.8, 0.8)
        self.life = 30  # frames

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.dy -= 0.06  # gravity
        self.life -= 1

    def draw(self):
        glPushMatrix()
        glColor3f(1, 0.5, 0.2)
        glTranslatef(self.x, self.y, self.z)
        glutSolidCube(self.size)
        glPopMatrix()

    def is_alive(self):
        return self.life > 0

class Bullet:
    def __init__(self, x, y, z, angle, target_enemy=None):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.hit = False
        self.hit_enemy = False
        self.target_enemy = target_enemy
        self.size = 4  # Increased size
        self.speed = 4  # Slower speed

    def update(self):
        if self.hit:
            return
        if self.target_enemy and not self.target_enemy.hit and not self.target_enemy.is_dead:
            dx = self.target_enemy.x - self.x
            dz = self.target_enemy.z - self.z
            dy = self.target_enemy.y - self.y
            distance = math.sqrt(dx*dx + dz*dz + dy*dy)
            if distance > 0:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                self.z += (dz / distance) * self.speed
        else:
            new_x = self.x + self.speed * math.sin(math.radians(self.angle))
            new_z = self.z + self.speed * math.cos(math.radians(self.angle))
            half = (BOUNDARY_SIZE / 2) - 5
            if abs(new_x) < half and abs(new_z) < half:
                self.x = new_x
                self.z = new_z
            else:
                self.hit = True

    def is_alive(self):
        return not self.hit
    
    def draw(self):
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.angle, 0, 1, 0)
        glScalef(self.size, self.size, self.size * 2)  # Make it longer
        glutSolidCube(1)
        glPopMatrix()

class Enemy:
    def __init__(self, enemy_type='normal'):
        self.respawn(enemy_type)
        self.target = False
        self.hit = False
        self.is_dead = False
        self.fall_y = 0

    def respawn(self, enemy_type):
        while True:
            angle = random.uniform(0, 2*math.pi)
            distance = random.uniform(300, 450)
            x = distance*math.sin(angle)
            z = distance*math.cos(angle)
            if not is_inside_obstacle(x,z):
                break
        self.x = x
        self.z = z
        self.y = 0
        self.speed = 0.1 if enemy_type=='normal' else (0.25 if enemy_type=='runner' else 0.05)
        self.health = 1 if enemy_type=='normal' else (0.4 if enemy_type=='runner' else 2)
        self.type = enemy_type
        self.hit = False
        self.target = False
        self.is_dead = False
        self.fall_y = 0

    def update(self):
        if game_paused or game_over:
            return
        if self.is_dead:
            # Fall down animation
            if self.fall_y > -20:
                self.fall_y -= 0.5
            return
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        dist = math.sqrt(dx*dx + dz*dz)
        if dist > 0:
            vx = (dx / dist) * self.speed
            vz = (dz / dist) * self.speed
            new_x = self.x + vx
            new_z = self.z + vz
            if not is_inside_obstacle(new_x,new_z) and inside_boundary(new_x,new_z):
                self.x = new_x
                self.z = new_z

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y + self.fall_y, self.z)
        # Differentiate zombies by color and shape
        if self.is_dead:
            glColor3f(0.2, 0.1, 0.1)
        elif self.type == 'normal':
            glColor3f(0.0, 0.6, 0.0)  # Green
        elif self.type == 'runner':
            glColor3f(0.0, 0.0, 0.8)  # Blue
        else:
            glColor3f(0.8, 0.0, 0.0)  # Red

        # Body (taller for tank)
        height = 30 if self.type != 'tank' else 40
        width = 12 if self.type != 'tank' else 18
        depth = 12 if self.type != 'tank' else 14
        glPushMatrix()
        glTranslatef(0, height/2, 0)
        glScalef(width, height, depth)
        glutSolidCube(1)
        glPopMatrix()

        # Head with glowing red eyes for scarier look
        glColor3f(0.05, 0.05, 0.05)
        glPushMatrix()
        glTranslatef(0, height + 10, 0)
        glutSolidSphere(8, 16, 16)
        # Eyes
        if not self.is_dead:
            glColor3f(1, 0, 0)
            eye_offset = 3
            glPushMatrix()
            glTranslatef(-eye_offset, height + 12, 6)
            glutSolidSphere(1.8, 6, 6)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(eye_offset, height + 12, 6)
            glutSolidSphere(1.8, 6, 6)
            glPopMatrix()
        glPopMatrix()

        # Arms (thick for tank)
        arm_height = height - 10
        arm_thickness = 4 if self.type != 'tank' else 6
        arm_length = 18 if self.type != 'tank' else 24
        arm_color = (0.4, 0.3, 0.2) if not self.is_dead else (0.2, 0.1, 0.1)
        glColor3f(*arm_color)
        for x_arm in [-15, 15]:
            glPushMatrix()
            glTranslatef(x_arm, arm_height, 0)
            glRotatef(10 if x_arm< 0 else -10, 1, 0, 0)
            glScalef(arm_thickness, arm_length, arm_thickness)
            glutSolidCube(1)
            glPopMatrix()

        glPopMatrix()

    def check_collision_with_player(self):
        if self.is_dead:
            return False
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        distance = math.sqrt(dx*dx + dz*dz)
        return distance < 25

    def check_collision_with_bullet(self, bullet):
        if self.is_dead:
            return False
        dx = bullet.x - self.x
        dz = bullet.z - self.z
        distance = math.sqrt(dx*dx + dz*dz)
        return distance < 15

class HealthPickup:
    def __init__(self):
        while True:
            x = random.uniform(-BOUNDARY_SIZE/2+20, BOUNDARY_SIZE/2-20)
            z = random.uniform(-BOUNDARY_SIZE/2+20, BOUNDARY_SIZE/2-20)
            if not is_inside_obstacle(x,z):
                break
        self.x = x
        self.y = 10
        self.z = z
        self.float_offset = random.uniform(0, 2)

    def draw(self):
        # Floating pinkish cube as health orb
        glPushMatrix()
        glColor3f(1.0, 0.1, 0.5)
        t = glutGet(GLUT_ELAPSED_TIME) / 500.0 + self.float_offset
        bob = math.sin(t) * 3
        glTranslatef(self.x, self.y + bob, self.z)
        glutSolidCube(18)
        glPopMatrix()

class PowerUp:
    def __init__(self, type):
        while True:
            x = random.uniform(-BOUNDARY_SIZE/2+20, BOUNDARY_SIZE/2-20)
            z = random.uniform(-BOUNDARY_SIZE/2+20, BOUNDARY_SIZE/2-20)
            if not is_inside_obstacle(x,z):
                break
        self.type = type
        self.x = x
        self.y = 10
        self.z = z
        self.active = True
        self.timer = 600  # 10 seconds approx
        self.float_offset = random.uniform(0, 2)

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self):
        if not self.active:
            return
        # Floating cyan cube as weapon orb
        glPushMatrix()
        glColor3f(0.0, 0.9, 0.9)
        t = glutGet(GLUT_ELAPSED_TIME) / 500.0 + self.float_offset
        bob = math.sin(t) * 3
        glTranslatef(self.x, self.y + bob, self.z)
        glutSolidCube(18)
        glPopMatrix()

class Obstacle:
    def __init__(self, x, z, size=OBSTACLE_SIZE, color=(1,0,0)):
        self.x = x
        self.z = z
        self.size = size
        self.color = color

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.size/2 - 1, self.z)
        glScalef(self.size*2, self.size, self.size/2)
        # Simplified car shape: cube with a smaller cube as top
        glutSolidCube(1)
        glTranslatef(0, 0.7, 0)
        glScalef(0.8, 0.6, 0.6)
        glutSolidCube(1)
        glPopMatrix()

def inside_boundary(x,z):
    half = BOUNDARY_SIZE/2 - 15
    return -half <= x <= half and -half <= z <= half

def is_inside_obstacle(x,z):
    for obs in obstacles:
        if (abs(x - obs.x) < obs.size + 15) and (abs(z - obs.z) < obs.size + 15):
            return True
    return False

def draw_floor():
    glDisable(GL_LIGHTING)
    size = BOUNDARY_SIZE / 20
    rows = cols = 20
    half = BOUNDARY_SIZE / 2

    for i in range(rows):
        for j in range(cols):
            x1 = i * size - half
            z1 = j * size - half
            x2 = x1 + size
            z2 = z1 + size
            # Mix grass and road with lighter grass
            if (i+j) % 4 == 0:
                # Road
                glColor3f(0.2,0.2,0.2)
            else:
                # Grass lighter
                glColor3f(0.3,0.7,0.3)
            glBegin(GL_QUADS)
            glVertex3f(x1, -1, z1)
            glVertex3f(x2, -1, z1)
            glVertex3f(x2, -1, z2)
            glVertex3f(x1, -1, z2)
            glEnd()

    # Draw boundary walls
    boundary_height = 40
    boundary_thickness = 10
    glColor3f(0.5, 0.3, 0.1)
    for z_wall in [-half, half]:
        glPushMatrix()
        glTranslatef(0, boundary_height/2 - 1, z_wall)
        glScalef(BOUNDARY_SIZE, boundary_height, boundary_thickness)
        glutSolidCube(1)
        glPopMatrix()
    for x_wall in [-half, half]:
        glPushMatrix()
        glTranslatef(x_wall, boundary_height/2 - 1, 0)
        glScalef(boundary_thickness, boundary_height, BOUNDARY_SIZE)
        glutSolidCube(1)
        glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0, player_pos[2])
    glRotatef(player_angle, 0, 1, 0)

    # Legs
    glColor3f(0.4, 0.0, 0.7)
    for x_leg in [7, -7]:
        glPushMatrix()
        glTranslatef(x_leg, 15, 0)
        glRotatef(90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 5, 3, 25, 12, 6)
        glPopMatrix()

    # Torso
    glColor3f(0.1, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(0, 40, 0)
    glScalef(20, 40, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 70, 0)
    glutSolidSphere(10, 16, 16)
    glPopMatrix()

    # Arms
    glColor3f(0.9, 0.8, 0.7)
    for x_arm in [-12, 12]:
        glPushMatrix()
        glTranslatef(x_arm, 50, 0)
        glRotatef(0, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 4, 2, 20, 12, 2)
        glPopMatrix()

    # Gun in hand - cube and barrel like original code
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(10, 45, 8)
    glutSolidCube(7)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(10, 45, 18)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, 2, 2, 15, 12, 2)
    glPopMatrix()

    glPopMatrix()

def draw_obstacles():
    for obs in obstacles:
        obs.draw()

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

def draw_all_particles():
    for p in particles:
        p.draw()

def update_particles():
    global particles
    for p in particles[:]:
        p.update()
        if not p.is_alive():
            particles.remove(p)

def add_explosion(x,y,z):
    for _ in range(20):
        particles.append(Particle(x,y,z))

def draw_status():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    glOrtho(0, w, h, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)

    glColor4f(0,0,0,0.6)
    glBegin(GL_QUADS)
    glVertex2f(5, 5)
    glVertex2f(320, 5)
    glVertex2f(320, 110)
    glVertex2f(5, 110)
    glEnd()

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    bar_width = 150
    bar_height = 25
    spacing = 15
    x = 15
    y = 15

    glColor3f(0.3, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+bar_width, y)
    glVertex2f(x+bar_width, y+bar_height)
    glVertex2f(x, y+bar_height)
    glEnd()

    health_fraction = player_health / max_health
    glColor3f(1.0, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+bar_width*health_fraction, y)
    glVertex2f(x+bar_width*health_fraction, y+bar_height)
    glVertex2f(x, y+bar_height)
    glEnd()

    glColor3f(1,1,1)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x+bar_width, y)
    glVertex2f(x+bar_width, y+bar_height)
    glVertex2f(x, y+bar_height)
    glEnd()

    glColor3f(1,1,1)
    draw_text(x+10, y+18, f"Health: {player_health}/{max_health}")
    draw_text(x, y+bar_height+spacing+18, f"Score: {game_score}")
    draw_text(x, y+2*(bar_height+spacing)+18, f"Wave: {current_wave}")
    draw_text(x, y+3*(bar_height+spacing)+18, f"Kills: {zombies_killed}")

    if game_paused:
        draw_text(w//2 - 40, h//2, "PAUSED")

    if game_over:
        draw_text(w//2 - 110, h//2, "GAME OVER - Press R to Restart")

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect_ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)
    gluPerspective(fov, aspect_ratio, 1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if follow_camera:
        eye_height = player_height + 20
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
        # Draw first person gun, hand, and head
        draw_first_person_gun_hand_head(cam_x, cam_y, cam_z)
    else:
        radius = 250
        cam_x = player_pos[0] + radius * math.sin(math.radians(camera_angle))
        cam_z = player_pos[2] + radius * math.cos(math.radians(camera_angle))
        cam_y = player_pos[1] + camera_height

        gluLookAt(cam_x, cam_y, cam_z,
                  player_pos[0], player_pos[1] + player_height, player_pos[2],
                  0, 1, 0)

def draw_first_person_gun_hand_head(cx, cy, cz):
    glPushMatrix()
    glLoadIdentity()
    # Place view at camera eye
    glTranslatef(cx, cy, cz)
    glRotatef(-player_angle, 0, 1, 0)

    # Translate forward a bit
    glTranslatef(4, -8, -20)

    # Arms - partial cylinders
    glColor3f(0.8, 0.7, 0.6)  # Skin color
    quad = gluNewQuadric()

    # Right Arm
    glPushMatrix()
    glTranslatef(8, 20, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 2.5, 2.0, 25, 12, 2)
    glPopMatrix()

    # Left Arm
    glPushMatrix()
    glTranslatef(-6, 17, -5)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 2.5, 2.0, 25, 12, 2)
    glPopMatrix()

    # Gun body
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 15, 0)
    gluCylinder(quad, 2.0, 1.8, 30, 16, 2)

    # Gun barrel
    glPushMatrix()
    glTranslatef(0, 0, 5)
    gluCylinder(quad, 1.5, 1.3, 25, 16, 2)
    glPopMatrix()

    # Gun handle
    glPushMatrix()
    glTranslatef(0, 1.5, 10)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 1.8, 1.8, 8, 12, 2)
    glPopMatrix()

    glPopMatrix()

    # Head partial sphere (visible)
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 25, -10)
    glutSolidSphere(8, 16, 16)
    glPopMatrix()

    glPopMatrix()

def fire_bullet():
    global bullets, bullets_missed

    if game_paused or game_over:
        return

    target_enemy = None
    if cheat_mode:
        min_distance = float('inf')
        closest_enemy = None

        for enemy in enemies:
            if not enemy.hit and not enemy.target and not enemy.is_dead:
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx*dx + dz*dz)

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
        gun_y = player_pos[1] + 45
        gun_z = player_pos[2] + gun_offset_front * math.cos(math.radians(player_angle))
        bullets.append(Bullet(gun_x, gun_y, gun_z, player_angle, target_enemy))

def move_player(dx, dz):
    global player_pos

    if game_paused or game_over:
        return

    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz

    if inside_boundary(new_x, new_z) and not is_inside_obstacle(new_x, new_z):
        player_pos[0] = new_x
        player_pos[2] = new_z

def update_game():
    global bullets, enemies, health_pickups, power_ups, game_score, player_health, bullets_missed, game_over, game_over_print, zombies_killed, current_wave

    if game_over or game_paused:
        if game_over and not game_over_print:
            print("Player Died. Game Over!! Better Luck Next Time")
            game_over_print = True
        return

    new_bullets = []
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
    bullets[:] = new_bullets

    # Spawn health pickups
    if random.random() < 0.005:
        health_pickups.append(HealthPickup())

    # Update health pickups
    for pickup in health_pickups[:]:
        if player_health < max_health:
            if abs(player_pos[0] - pickup.x) < 12 and abs(player_pos[2] - pickup.z) < 12:
                player_health += 1
                health_pickups.remove(pickup)
                print(f"Health increased! Current Health: {player_health}")

    # Spawn power-ups
    if random.random() < 0.005:
        power_ups.append(PowerUp(random.choice(['shield', 'weapon_upgrade'])))

    # Update power-ups
    for power_up in power_ups[:]:
        power_up.update()
        if not power_up.active:
            power_ups.remove(power_up)

    # Manage enemies with wave difficulty
    max_enemies = MAX_ENEMIES_BASE + current_wave - 1
    while len(enemies) < max_enemies:
        enemy_type = random.choices(['normal', 'runner', 'tank'], weights=[0.6, 0.3, 0.1])[0]
        enemies.append(Enemy(enemy_type))

    new_enemies = []
    for enemy in enemies:
        enemy.update()

        if not enemy.is_dead and enemy.check_collision_with_player():
            player_health -= 1
            print(f"Player Remaining Health: {player_health}")
            if player_health <= 0:
                enemy.is_dead = False
                enemy.hit = False
                game_over = True
            enemy.is_dead = True

        if not enemy.is_dead:
            hit = False
            for bullet in bullets:
                if not bullet.hit and enemy.check_collision_with_bullet(bullet):
                    bullet.hit = True
                    bullet.hit_enemy = True
                    enemy.is_dead = True
                    zombies_killed += 1
                    game_score += 1
                    # Particle explosion
                    add_explosion(enemy.x, enemy.y + 15, enemy.z)
                    hit = True
                    break
            if not hit:
                new_enemies.append(enemy)
        else:
            # If enemy fallen below ground, respawn and increase wave if killed enough
            if enemy.fall_y <= -20:
                enemy.respawn(random.choice(['normal', 'runner', 'tank']))
                new_enemies.append(enemy)
                if zombies_killed >= 5 * current_wave:
                    current_wave += 1
                    print(f"Wave {current_wave} started!")
    enemies[:] = new_enemies

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, follow_camera, game_over, game_over_print, game_paused, fov, fov_adjust_active

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

    step = 10

    if key == b'w':
        move_player(step * math.sin(math.radians(player_angle)),
                    step * math.cos(math.radians(player_angle)))
    elif key == b's':
        move_player(-step * math.sin(math.radians(player_angle)),
                    -step * math.cos(math.radians(player_angle)))
    elif key == b'a':
        player_angle += 5
    elif key == b'd':
        player_angle -= 5
    elif key == b'c':
        cheat_mode = not cheat_mode
    elif key == b'v':
        cheat_mode = not cheat_mode
        fov_adjust_active = not fov_adjust_active

def specialKeyListener(key, x, y):
    global camera_angle, camera_height

    if game_paused:
        return

    if key == GLUT_KEY_LEFT:
        camera_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5
    elif key == GLUT_KEY_UP:
        camera_height = min(camera_height + 10, 800)
    elif key == GLUT_KEY_DOWN:
        camera_height = max(camera_height - 10, 50)

def mouseListener(button, state, x, y):
    global follow_camera, fov_adjust_active

    if game_paused or game_over:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            fov_adjust_active = True
        else:
            fov_adjust_active = False

def mouseMotion(x, y):
    global fov, fov_adjust_active
    if fov_adjust_active:
        height = glutGet(GLUT_WINDOW_HEIGHT)
        ratio = max(min(y / height, 1), 0)
        fov = 25 + 100 * (1 - ratio)
        fov = min(max(fov, 25), 125)

def reset_game():
    global player_pos, player_angle, bullets, enemies, health_pickups, power_ups
    global cheat_mode, follow_camera, game_paused
    global game_score, player_health, bullets_missed, game_over, current_wave, zombies_killed, fov

    player_pos = [0.0, 0.0, 0.0]
    player_angle = 0.0
    bullets.clear()
    enemies.clear()
    health_pickups.clear()
    power_ups.clear()
    cheat_mode = False
    follow_camera = False
    game_paused = False

    game_score = 0
    player_health = max_health
    bullets_missed = 0
    game_over = False
    current_wave = 1
    zombies_killed = 0
    fov = 60

def idle():
    if not game_paused and not game_over:
        update_game()
        if cheat_mode:
            global player_angle
            closest_enemy = None
            min_distance = float('inf')
            for enemy in enemies:
                if enemy.is_dead or enemy.target:
                    continue
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx*dx + dz*dz)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
            if closest_enemy:
                dx = closest_enemy.x - player_pos[0]
                dz = closest_enemy.z - player_pos[2]
                angle_to_enemy = math.degrees(math.atan2(dx, dz))
                angle_to_enemy = (360 - angle_to_enemy) % 360
                diff = (angle_to_enemy - player_angle + 540) % 360 - 180
                player_angle += diff * 0.15
                if abs(diff) < 10 and random.random() < 0.1:
                    fire_bullet()
        glutPostRedisplay()

def init():
    glClearColor(0.05, 0.05, 0.2, 1.0)  # Night sky color
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_pos = [200.0, 300.0, 200.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.15, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    for _ in range(MAX_ENEMIES_BASE):
        enemies.append(Enemy(random.choice(['normal', 'runner', 'tank'])))

    obstacles.clear()
    colors = [(1,0,0), (0,0,1), (1,0.5,0)]
    for i in range(OBSTACLE_COUNT):
        while True:
            x = random.uniform(-BOUNDARY_SIZE/2 + 50, BOUNDARY_SIZE/2 - 50)
            z = random.uniform(-BOUNDARY_SIZE/2 + 50, BOUNDARY_SIZE/2 - 50)
            dist_to_player = math.sqrt(x*x + z*z)
            if dist_to_player > 100 and not is_inside_obstacle(x,z):
                obstacles.append(Obstacle(x, z, OBSTACLE_SIZE, colors[i % len(colors)]))
                break

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    setupCamera()
    draw_floor()
    draw_obstacles()
    draw_all_enemies()
    draw_all_bullets()
    draw_all_health_pickups()
    draw_all_power_ups()
    draw_all_particles()
    draw_player()
    draw_status()

    glutSwapBuffers()

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
    glutMotionFunc(mouseMotion)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()
