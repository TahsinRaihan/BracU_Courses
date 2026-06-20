from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Global variables and game state
# Global game state variables clearly defined
game_score = 0
player_health = 5
max_health = 5
zombies_killed = 0
current_wave = 1
bullets_missed = 0
wave_progress_tracker = 0
notification_text = ""
notification_timer = 0
game_paused = False
game_over = False
cheat_mode = False
follow_camera = False

# Player variables
player_pos = [0.0, 0.0, 0.0]
player_angle = 0.0
player_height = 12.0  # Or your desired height
camera_angle = 0
camera_height = 200

# Game objects lists
bullets = []
enemies = []
health_pickups = []
power_ups = []
obstacles = []
particles = []

# Game constants
MAX_ENEMIES_BASE = 5
MAX_MISSED_BULLETS = 10
BOUNDARY_SIZE = 1000
OBSTACLE_COUNT = 10
OBSTACLE_SIZE = 40



cheat_mode = False
follow_camera = False
camera_angle = 0
camera_height = 200
game_paused = False
game_over = False
fov = 60
fov_adjust_active = False



MAX_ENEMIES_BASE = 5
MAX_MISSED_BULLETS = 10
BOUNDARY_SIZE = 1000
OBSTACLE_COUNT = 10
OBSTACLE_SIZE = 40

class Particle:
    def __init__(self, x, y, z):
        self.x = x + random.uniform(-5, 5)
        self.y = y + random.uniform(0, 5)
        self.z = z + random.uniform(-5, 5)
        self.size = random.uniform(1, 3)
        self.dx = random.uniform(-0.8, 0.8)
        self.dy = random.uniform(0.5, 1.2)
        self.dz = random.uniform(-0.8, 0.8)
        self.life = 30

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.dy -= 0.06
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
    def __init__(self, x, y, z, angle, target_enemy=None, cheat_bullet=False):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.target_enemy = target_enemy
        self.hit = False
        self.hit_enemy = False
        self.size = 4
        self.speed = 6
        self.cheat_bullet = cheat_bullet  # Indicates cheat mode bullet clearly

    def update(self):
        if self.hit:
            return
        if self.target_enemy and not self.target_enemy.is_dead:
            dx = self.target_enemy.x - self.x
            dz = self.target_enemy.z - self.z
            dy = (self.target_enemy.y + 15) - self.y
            dist = math.sqrt(dx ** 2 + dz ** 2 + dy ** 2)
            if dist > 1:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
                self.z += dz / dist * self.speed
            else:
                self.hit = True
        else:
            rad = math.radians(self.angle)
            new_x = self.x + self.speed * math.sin(rad)
            new_z = self.z + self.speed * math.cos(rad)
            if inside_boundary(new_x, new_z):
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
        glScalef(self.size, self.size, self.size * 2)
        glutSolidCube(1)
        glPopMatrix()






class Enemy:
    def __init__(self, enemy_type='normal'):
        self.type = enemy_type
        self.is_dead = False
        self.fall_y = 0
        self.speed = 0.1 if enemy_type == 'normal' else (0.25 if enemy_type == 'runner' else 0.05)
        self.respawn(enemy_type)
        self.target = False


    def respawn(self, enemy_type):
        while True:
            angle = random.uniform(0, 2*math.pi)
            dist = random.uniform(300, 450)
            x = dist * math.sin(angle)
            z = dist * math.cos(angle)
            if not is_inside_obstacle(x,z):
                break
        self.x = x
        self.z = z
        self.y = 0
        self.is_dead = False
        self.fall_y = 0
        self.type = enemy_type
        self.speed = 0.1 if enemy_type == 'normal' else (0.25 if enemy_type == 'runner' else 0.05)

    def update(self):
        global game_over
        if game_paused or game_over:
            return
        if self.is_dead:
            if self.fall_y > -20:
                self.fall_y -= 0.5
            return
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        dist = math.sqrt(dx*dx + dz*dz)
        if dist > 0:
            vx = (dx/dist) * self.speed
            vz = (dz/dist) * self.speed
            new_x = self.x + vx
            new_z = self.z + vz
            if not is_inside_obstacle(new_x,new_z) and inside_boundary(new_x,new_z):
                self.x = new_x
                self.z = new_z

    def check_collision_with_player(self):
        if self.is_dead:
            return False
        dx = player_pos[0]-self.x
        dz = player_pos[2]-self.z
        dist = math.sqrt(dx*dx + dz*dz)
        return dist < 20

    def check_collision_with_bullet(self, bullet):
        if self.is_dead:
            return False
        dx = bullet.x - self.x
        dz = bullet.z - self.z
        dist = math.sqrt(dx*dx + dz*dz)
        return dist < 15

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y + self.fall_y, self.z)
        if self.is_dead:
            glColor3f(0.2, 0.1, 0.1)
        elif self.type == 'normal':
            glColor3f(0.0, 0.6, 0.0)
        elif self.type == 'runner':
            glColor3f(0.0, 0.0, 0.8)
        else:
            glColor3f(0.8, 0.0, 0.0)
        height = 25 if self.type != 'tank' else 35
        width = 10 if self.type != 'tank' else 16
        depth = 10 if self.type != 'tank' else 12
        glPushMatrix()
        glTranslatef(0, height/2, 0)
        glScalef(width, height, depth)
        glutSolidCube(1)
        glPopMatrix()
        glColor3f(0.05, 0.05, 0.05)
        glPushMatrix()
        glTranslatef(0, height+9, 0)
        glutSolidSphere(7,16,16)
        if not self.is_dead:
            glColor3f(1,0,0)
            eye_offset = 2.5
            glPushMatrix()
            glTranslatef(-eye_offset, height+11, 5)
            glutSolidSphere(1.5,6,6)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(eye_offset, height+11, 5)
            glutSolidSphere(1.5,6,6)
            glPopMatrix()
        glPopMatrix()
        arm_height = height - 10
        arm_thickness = 3 if self.type != 'tank' else 5
        arm_length = 16 if self.type != 'tank' else 20
        arm_color = (0.4, 0.3, 0.2) if not self.is_dead else (0.2, 0.1, 0.1)
        glColor3f(*arm_color)
        for x_arm in [-13,13]:
            glPushMatrix()
            glTranslatef(x_arm, arm_height, 0)
            glRotatef(10 if x_arm<0 else -10,1,0,0)
            glScalef(arm_thickness, arm_length, arm_thickness)
            glutSolidCube(1)
            glPopMatrix()
        glPopMatrix()

class Pickup:
    def __init__(self, x, z, color):
        self.x = x
        self.z = z
        self.y = 10
        self.color = color
        self.float_offset = random.uniform(0, 5)
        self.active = True
        self.timer = 900  # clearly defined lifespan

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self):
        if not self.active:
            return
        t = glutGet(GLUT_ELAPSED_TIME) / 500.0 + self.float_offset
        bob = math.sin(t) * 3
        glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(self.x, self.y + bob, self.z)
        glutSolidSphere(9, 20, 20)
        glPopMatrix()


class Obstacle:
    def __init__(self, x, z, size=OBSTACLE_SIZE, color=(1, 0, 0)):
        self.x = x
        self.z = z
        self.size = size
        self.color = color

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.size / 2 - 1, self.z)
        glScalef(self.size * 2, self.size, self.size / 2)
        glutSolidCube(1)
        glTranslatef(0, 0.7, 0)
        glScalef(0.8, 0.6, 0.6)
        glutSolidCube(1)
        glPopMatrix()

def inside_boundary(x, z):
    half = BOUNDARY_SIZE / 2 - 15
    return -half <= x <= half and -half <= z <= half

def is_inside_obstacle(x, z):
    for obs in obstacles:
        if abs(x - obs.x) < obs.size + 15 and abs(z - obs.z) < obs.size + 15:
            return True
    return False

def draw_floor():
    glDisable(GL_LIGHTING)
    size = BOUNDARY_SIZE / 20
    half = BOUNDARY_SIZE / 2

    for i in range(20):
        for j in range(20):
            x1 = i * size - half
            z1 = j * size - half
            x2 = x1 + size
            z2 = z1 + size
            if (i + j) % 4 == 0:
                glColor3f(0.2, 0.2, 0.2)
            else:
                glColor3f(0.4, 0.8, 0.4)
            glBegin(GL_QUADS)
            glVertex3f(x1, -1, z1)
            glVertex3f(x2, -1, z1)
            glVertex3f(x2, -1, z2)
            glVertex3f(x1, -1, z2)
            glEnd()

    boundary_height = 40
    boundary_thickness = 10
    glColor3f(0.5, 0.3, 0.1)
    for z_wall in [-half, half]:
        glPushMatrix()
        glTranslatef(0, boundary_height / 2 - 1, z_wall)
        glScalef(BOUNDARY_SIZE, boundary_height, boundary_thickness)
        glutSolidCube(1)
        glPopMatrix()
    for x_wall in [-half, half]:
        glPushMatrix()
        glTranslatef(x_wall, boundary_height / 2 - 1, 0)
        glScalef(boundary_thickness, boundary_height, BOUNDARY_SIZE)
        glutSolidCube(1)
        glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], 0, player_pos[2])
    glRotatef(player_angle, 0, 1, 0)
    glColor3f(0.4, 0.0, 0.7)
    for x_leg in [5, -5]:
        glPushMatrix()
        glTranslatef(x_leg, 15, 0)
        glRotatef(90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 4, 2, 20, 12, 6)
        glPopMatrix()
    glColor3f(0.1, 0.7, 0.1)
    glPushMatrix()
    glTranslatef(0, 35, 0)
    glScalef(15, 30, 7)
    glutSolidCube(1)
    glPopMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 60, 0)
    glutSolidSphere(8, 16, 16)
    glPopMatrix()
    glColor3f(0.9, 0.8, 0.7)
    for x_arm in [-8, 8]:
        glPushMatrix()
        glTranslatef(x_arm, 45, 0)
        glRotatef(0, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 3, 1.8, 18, 12, 2)
        glPopMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(8, 43, 12)
    glutSolidCube(5)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(8, 43, 20)
    glRotatef(-90, 1, 0, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, 1.5, 1.5, 15, 12, 2)
    glPopMatrix()
    glPopMatrix()

def draw_all_bullets():
    for b in bullets:
        b.draw()

def draw_all_enemies():
    for e in enemies:
        e.draw()

def draw_all_pickups():
    for hp in health_pickups:
        hp.draw()
    for pw in power_ups:
        pw.draw()

def draw_all_particles():
    for p in particles:
        p.draw()

def update_particles():
    for p in particles[:]:
        p.update()
        if not p.is_alive():
            particles.remove(p)

def add_explosion(x, y, z):
    for _ in range(20):
        particles.append(Particle(x, y, z))

def draw_obstacles():
    for obs in obstacles:
        obs.draw()

def draw_status():
    global notification_timer, notification_text
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
    glColor3f(1, 1, 1)
    draw_text(10, 20, f"Health: {player_health}/{max_health}")
    draw_text(10, 40, f"Score: {game_score}")
    draw_text(10, 60, f"Wave: {current_wave}")
    draw_text(10, 80, f"Kills: {zombies_killed}")
    if notification_timer > 0:
        draw_text(w//2 - 70, h//3, notification_text)
        notification_timer -= 1
    if game_paused:
        draw_text(w//2 - 40, h//2, "PAUSED")
    if game_over:
        draw_text(w//2 - 110, h//2, "GAME OVER - Press R to Restart")
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
        eye_height = player_height + 25
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
    glTranslatef(cx, cy, cz)
    glRotatef(-player_angle, 0, 1, 0)
    glTranslatef(6, -8, -18)

    glColor3f(0.8, 0.7, 0.6)
    quad = gluNewQuadric()

    # Right arm
    glPushMatrix()
    glTranslatef(7, 18, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 2.8, 2.3, 25, 12, 2)
    glPopMatrix()

    # Left arm
    glPushMatrix()
    glTranslatef(-7, 17, -7)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 2.8, 2.3, 25, 12, 2)
    glPopMatrix()

    # Gun body
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 15, 0)
    gluCylinder(quad, 2.5, 2.3, 35, 16, 2)

    # Gun barrel (horizontal fix)
    glPushMatrix()
    glTranslatef(15, 5, 10)
    glRotatef(90, 0, 1, 0)
    gluCylinder(quad, 1.8, 1.5, 30, 16, 2)
    glPopMatrix()

    # Gun handle
    glPushMatrix()
    glTranslatef(0, 2, 15)
    glRotatef(90, 1, 0, 0)
    gluCylinder(quad, 2.0, 2.0, 10, 12, 2)
    glPopMatrix()

    glPopMatrix()

    # Partial head
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 27, -10)
    glutSolidSphere(9, 16, 16)
    glPopMatrix()

    glPopMatrix()

class Bullet:
    def __init__(self, x, y, z, angle, target_enemy=None, cheat_bullet=False):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.target_enemy = target_enemy
        self.hit = False
        self.hit_enemy = False
        self.size = 4
        self.speed = 6
        self.cheat_bullet = cheat_bullet  # Indicates cheat mode bullet clearly

    def update(self):
        if self.hit:
            return
        if self.target_enemy and not self.target_enemy.is_dead:
            dx = self.target_enemy.x - self.x
            dz = self.target_enemy.z - self.z
            dy = (self.target_enemy.y + 15) - self.y
            dist = math.sqrt(dx ** 2 + dz ** 2 + dy ** 2)
            if dist > 1:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed
                self.z += dz / dist * self.speed
            else:
                self.hit = True
        else:
            rad = math.radians(self.angle)
            new_x = self.x + self.speed * math.sin(rad)
            new_z = self.z + self.speed * math.cos(rad)
            if inside_boundary(new_x, new_z):
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
        glScalef(self.size, self.size, self.size * 2)
        glutSolidCube(1)
        glPopMatrix()



def fire_bullet():
    global bullets
    if game_paused or game_over:
        return

    target_enemy = None
    cheat_bullet = False

    if cheat_mode:
        closest_enemy = None
        min_dist = float('inf')
        for enemy in enemies:
            if enemy.is_dead:
                continue
            dx = enemy.x - player_pos[0]
            dz = enemy.z - player_pos[2]
            dist = math.sqrt(dx ** 2 + dz ** 2)
            if dist < min_dist:
                min_dist = dist
                closest_enemy = enemy
        target_enemy = closest_enemy
        cheat_bullet = True  # Explicitly indicate cheat bullet

    offset = 25
    gun_x = player_pos[0] + offset * math.sin(math.radians(player_angle))
    gun_y = player_pos[1] + 45
    gun_z = player_pos[2] + offset * math.cos(math.radians(player_angle))

    bullets.append(Bullet(gun_x, gun_y, gun_z, player_angle, target_enemy, cheat_bullet))




def move_player(dx, dz):
    if game_paused or game_over:
        return
    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz
    if inside_boundary(new_x, new_z) and not is_inside_obstacle(new_x, new_z):
        player_pos[0] = new_x
        player_pos[2] = new_z

def update_game():
    global bullets, enemies, health_pickups, power_ups
    global game_score, player_health, bullets_missed, game_over
    global zombies_killed, current_wave, notification_text, notification_timer
    global game_paused, wave_progress_tracker

    if game_over or game_paused:
        return

    # --- Bullet logic ---
    new_bullets = []
    for bullet in bullets:
        bullet.update()
        if bullet.is_alive():
            new_bullets.append(bullet)
        else:
            if not bullet.hit_enemy and not bullet.cheat_bullet:  # <- skip cheat-mode misses
                bullets_missed += 1
                if bullets_missed >= MAX_MISSED_BULLETS:
                    game_over = True
                    show_notification("Too many misses! Game Over.")
    bullets = new_bullets

    # --- Health pickups spawn ---
    if random.random() < 0.005 and len(health_pickups) < 3:
        hp = Pickup(
            random.uniform(-BOUNDARY_SIZE / 2 + 50, BOUNDARY_SIZE / 2 - 50),
            random.uniform(-BOUNDARY_SIZE / 2 + 50, BOUNDARY_SIZE / 2 - 50),
            (0, 1, 0)
        )
        health_pickups.append(hp)

    # --- Power-ups spawn ---
    if random.random() < 0.01 and len(power_ups) < 2:
        pw = Pickup(
            random.uniform(-BOUNDARY_SIZE / 2 + 50, BOUNDARY_SIZE / 2 - 50),
            random.uniform(-BOUNDARY_SIZE / 2 + 50, BOUNDARY_SIZE / 2 - 50),
            (0.0, 0.9, 0.9)
        )
        power_ups.append(pw)

    # --- Update pickups ---
    for hp in health_pickups[:]:
        hp.update()
        if not hp.active:
            health_pickups.remove(hp)
        elif player_health < max_health:
            if abs(player_pos[0] - hp.x) < 12 and abs(player_pos[2] - hp.z) < 12:
                player_health += 1
                health_pickups.remove(hp)
                show_notification("Health orb taken!")

    for pw in power_ups[:]:
        pw.update()
        if not pw.active:
            power_ups.remove(pw)
        elif abs(player_pos[0] - pw.x) < 12 and abs(player_pos[2] - pw.z) < 12:
            power_ups.remove(pw)
            show_notification("Weapon orb taken!")

    # --- Increase enemy count per wave ---
    max_enemies = MAX_ENEMIES_BASE + (current_wave - 1) * 2
    while len(enemies) < max_enemies:
        enemy_type = random.choices(['normal', 'runner', 'tank'], weights=[0.6, 0.3, 0.1])[0]
        enemies.append(Enemy(enemy_type))

    # --- Enemy movement + collision ---
    new_enemies = []
    for enemy in enemies:
        enemy.update()

        if not enemy.is_dead and enemy.check_collision_with_player():
            player_health -= 1
            if player_health <= 0:
                game_over = True
                show_notification("You died!")
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
                    add_explosion(enemy.x, enemy.y + 15, enemy.z)
                    hit = True
                    break
            if not hit:
                new_enemies.append(enemy)
        else:
            if enemy.fall_y <= -20:
                enemy.respawn(random.choice(['normal', 'runner', 'tank']))
            new_enemies.append(enemy)

    enemies = new_enemies

    # --- Wave progression ---
    if zombies_killed >= wave_progress_tracker + 5:
        wave_progress_tracker += 5
        current_wave += 1
        notification_text = f"TERROR IS STARTING... WAVE {current_wave}"
        notification_timer = 150
        show_notification(notification_text)

    update_particles()




def show_notification(text):
    global notification_text, notification_timer
    notification_text = text
    notification_timer = 150  # visible for a slightly longer time


def keyboardListener(key, x, y):
    global player_angle, cheat_mode, follow_camera, game_over, game_paused
    if game_over and key == b'r':
        reset_game()
        return
    if key == b'p':
        game_paused = not game_paused
        return
    if game_paused:
        return
    step = 10
    if key == b'w':
        move_player(step * math.sin(math.radians(player_angle)), step * math.cos(math.radians(player_angle)))
    elif key == b's':
        move_player(-step * math.sin(math.radians(player_angle)), -step * math.cos(math.radians(player_angle)))
    elif key == b'a':
        player_angle += 5
    elif key == b'd':
        player_angle -= 5
    elif key == b'c':
        cheat_mode = not cheat_mode
        print("Cheat Mode:", "ON" if cheat_mode else "OFF")
    elif key == b'v':
        follow_camera = not follow_camera
        print("Camera Mode:", "First-Person" if follow_camera else "Third-Person")



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
    global fov_adjust_active, follow_camera
    if game_paused or game_over:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        follow_camera = not follow_camera
        print("Camera Mode:", "First-Person" if follow_camera else "Third-Person")



def mouseMotion(x, y):
    global fov, fov_adjust_active
    if fov_adjust_active:
        height = glutGet(GLUT_WINDOW_HEIGHT)
        ratio = max(min(y / height, 1), 0)
        fov = 25 + 100 * (1 - ratio)
        fov = min(max(fov, 25), 125)

def reset_game():
    global player_pos, player_angle, bullets, enemies, health_pickups, power_ups, cheat_mode, follow_camera, game_paused, game_score, player_health, bullets_missed, game_over, current_wave, zombies_killed, fov, notification_text, notification_timer
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
    notification_text = ""
    notification_timer = 0

def idle():
    global player_angle, bullets_missed, game_over

    if not game_paused and not game_over:
        update_game()

        if cheat_mode:
            closest_enemy = None
            min_distance = float('inf')
            for enemy in enemies:
                if enemy.is_dead:
                    continue
                dx = enemy.x - player_pos[0]
                dz = enemy.z - player_pos[2]
                distance = math.sqrt(dx**2 + dz**2)
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy

            if closest_enemy:
                dx = closest_enemy.x - player_pos[0]
                dz = closest_enemy.z - player_pos[2]
                target_angle = math.degrees(math.atan2(dx, dz))
                angle_diff = (target_angle - player_angle + 360) % 360
                if angle_diff > 180:
                    angle_diff -= 360

                player_angle += angle_diff * 0.15  # smooth rotation

                # Fire less frequently to avoid excessive misses
                if abs(angle_diff) < 5 and random.random() < 0.05:
                    fire_bullet()

    glutPostRedisplay()




def init():
    glClearColor(0.05, 0.05, 0.2, 1.0)
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
    colors = [(1, 0, 0), (0, 0, 1), (1, 0.5, 0)]
    for i in range(OBSTACLE_COUNT):
        while True:
            x = random.uniform(-BOUNDARY_SIZE / 2 + 50, BOUNDARY_SIZE / 2 - 50)
            z = random.uniform(-BOUNDARY_SIZE / 2 + 50, BOUNDARY_SIZE / 2 - 50)
            dist = math.sqrt(x * x + z * z)
            if dist > 100 and not is_inside_obstacle(x, z):
                obstacles.append(Obstacle(x, z, OBSTACLE_SIZE, colors[i % len(colors)]))
                break

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1, 1, 1)  # explicit color reset

    setupCamera()

    # ensure depth buffer and colors are correct
    glEnable(GL_DEPTH_TEST)

    draw_floor()
    draw_obstacles()
    draw_all_enemies()
    draw_all_bullets()
    draw_all_pickups()
    draw_all_particles()
    draw_player()
    draw_status()

    glutSwapBuffers()



def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Zombie Survival")
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
