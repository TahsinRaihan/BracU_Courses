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

# New globals (at top of your module)
MAX_POWERUP_LIFETIME = 300    # frames before a power‐up vanishes
MAX_AMMO = 30                 # bullets per wave
current_ammo = MAX_AMMO
shield_active = False
shield_timer = 0
weapon_power_level = 0
weapon_timer = 0


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
    """
    A zombie with type ('normal','runner','tank'), per-type health,
    pulses in size, avoids obstacles, and respawns on a ring.
    Legs are drawn as simple cylinders under the body.
    """
    def __init__(self, enemy_type=None):
        types = ['normal', 'runner', 'tank']
        self.type = enemy_type if enemy_type in types else random.choice(types)
        self.is_dead = False
        self.target = False
        self.respawn(self.type)

    def respawn(self, enemy_type=None):
        global current_wave, weapon_power_level

        # allow type change
        if enemy_type in ('normal','runner','tank'):
            self.type = enemy_type

        # determine base health & speed per type
        if self.type == 'normal':
            base_health, base_speed = 2, 0.10
        elif self.type == 'runner':
            base_health, base_speed = 1, 0.25
        else:  # tank
            base_health, base_speed = 4, 0.05

        # apply weapon‐orb reduction (min 1 HP)
        self.health = max(1, base_health - weapon_power_level)
        self.is_dead = False

        # spawn on random ring so they come from all around
        angle = random.uniform(0, 2 * math.pi)
        dist  = random.uniform(300, 450)
        self.x, self.z = dist * math.sin(angle), dist * math.cos(angle)
        self.y         = 15
        self.fall_y    = 0

        # scale speed +10% per wave (cap wave 10)
        lvl = min(current_wave, 10)
        self.speed = base_speed * (1 + (lvl - 1) * 0.1)

        # pulsing
        self.scale           = 1.0
        self.scale_direction = 0.02

    def update(self):
        """
        Move toward player unless blocked, pulse size.
        """
        if game_paused or game_over:
            return

        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        dist = math.hypot(dx, dz)
        if dist > 0:
            nx = self.x + (dx / dist) * self.speed
            nz = self.z + (dz / dist) * self.speed
            if inside_boundary(nx, nz) and not is_inside_obstacle(nx, nz):
                self.x, self.z = nx, nz

        # falling corpse
        if self.is_dead and self.fall_y > -20:
            self.fall_y -= 0.5

    def draw(self):
        """
        Draw legs, then body/arms/eyes.
        """
        quad = gluNewQuadric()
        fall = getattr(self, 'fall_y', 0)

        # 1) Draw legs as cylinders from ground up to body y
        leg_height = self.y + fall
        glColor3f(0.3, 0.3, 0.3)
        for x_off in (-4, 4):
            glPushMatrix()
            # position at ground
            glTranslatef(self.x + x_off, 0, self.z)
            glRotatef(-90, 1, 0, 0)  # cylinder pointing up
            gluCylinder(quad, 2.5, 2.5, leg_height, 12, 4)
            glPopMatrix()

        # 2) Draw torso + head + arms + eyes
        glPushMatrix()
        glTranslatef(self.x, self.y + fall, self.z)
        glScalef(self.scale, self.scale, self.scale)

        # body color
        if self.is_dead:
            glColor3f(0.2, 0.1, 0.1)
        elif self.type == 'normal':
            glColor3f(0.0, 0.6, 0.0)
        elif self.type == 'runner':
            glColor3f(0.0, 0.0, 0.8)
        else:
            glColor3f(0.8, 0.0, 0.0)

        height = 25 if self.type != 'tank' else 35
        width  = 10 if self.type != 'tank' else 16
        depth  = 10 if self.type != 'tank' else 12

        # body cuboid
        glPushMatrix()
        glTranslatef(0, height/2, 0)
        glScalef(width, height, depth)
        glutSolidCube(1)
        glPopMatrix()

        # head sphere
        glColor3f(0.05, 0.05, 0.05)
        glPushMatrix()
        glTranslatef(0, height + 9, 0)
        glutSolidSphere(7, 16, 16)
        glPopMatrix()

        # eyes
        if not self.is_dead:
            glColor3f(1, 0, 0)
            eye_z = depth/2 + 2
            for ex in (-2.5, 2.5):
                glPushMatrix()
                glTranslatef(ex, height + 11, eye_z)
                glutSolidSphere(1.5, 6, 6)
                glPopMatrix()

        # arms
        arm_h   = height - 10
        arm_th  = 3 if self.type != 'tank' else 5
        arm_len = 16 if self.type != 'tank' else 20
        glColor3f(0.4, 0.3, 0.2)
        for ax in (-13, 13):
            glPushMatrix()
            glTranslatef(ax, arm_h, 0)
            glRotatef(10 if ax < 0 else -10, 1, 0, 0)
            glScalef(arm_th, arm_len, arm_th)
            glutSolidCube(1)
            glPopMatrix()

        glPopMatrix()  # end body

    def check_collision_with_player(self):
        dx = player_pos[0] - self.x
        dz = player_pos[2] - self.z
        return math.hypot(dx, dz) < 20

    def check_collision_with_bullet(self, bullet):
        dx = bullet.x - self.x
        dz = bullet.z - self.z
        return math.hypot(dx, dz) < 15






class Pickup:
    """
    x, z: world position
    color: RGB tuple
    ptype: 'health' | 'shield' | 'upgrade'
    """
    def __init__(self, x, z, color, ptype):
        self.x = x
        self.z = z
        self.y = 10
        self.color = color
        self.ptype = ptype
        self.float_offset = random.uniform(0, 5)
        self.active = True

        # health orbs live forever; shield & upgrade now last 10s @60fps → 600 frames
        if ptype == 'health':
            self.timer = 999999
        else:
            self.timer = 600

    def update(self):
        if self.active and self.timer < 999999:
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
    # If we’re in first-person mode, only draw the arms+gun at head height
    if follow_camera:
        # (you already have this helper defined somewhere)
        draw_first_person_gun_hand_head(
            player_pos[0],
            player_pos[1] + 45,   # your adjusted eye height
            player_pos[2]
        )
        return

    # Otherwise—third-person: draw full body + gun
    glPushMatrix()
    glTranslatef(player_pos[0], 0, player_pos[2])
    glRotatef(player_angle, 0, 1, 0)
    if game_over:
        glRotatef(90, 1, 0, 0)
    # — Legs —
    glColor3f(0.6, 0.0, 1.0)
    quad = gluNewQuadric()
    for x_off in (7, -7):
        glPushMatrix()
        glTranslatef(x_off, 20, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(quad, 6, 3, 25, 12, 6)
        glPopMatrix()

    # — Torso —
    glColor3f(0.2, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(0, 35, 0)
    glScalef(20, 30, 10)
    glutSolidCube(1)
    glPopMatrix()

    # — Head —
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 60, 0)
    glutSolidSphere(10, 16, 16)
    glPopMatrix()

    # — Arms —
    glColor3f(0.8, 0.7, 0.6)
    quad = gluNewQuadric()
    for x_off, pitch in ((-12, 0), (12, 0)):
        glPushMatrix()
        glTranslatef(x_off, 45, 0)
        glRotatef(pitch, 1, 0, 0)
        gluCylinder(quad, 4, 2, 18, 12, 2)
        glPopMatrix()

    # — Gun (third-person) —
    if not game_over:
        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(0, 38, 12)      # position it in hands
        gluCylinder(quad, 3.5, 2, 20, 12, 2)
        glPopMatrix()

    glPopMatrix()


def draw_gun():
    """
    Always shows a simple barrel in first-person (follow_camera=True),
    otherwise your existing third-person gun.
    """
    glPushMatrix()

    if follow_camera:
        # draw in camera-space so it never disappears
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # position barrel low & centered
        glTranslatef(0.0, -0.3, -0.6)

        # draw barrel
        glColor3f(0.2, 0.2, 0.2)
        quad = gluNewQuadric()
        # radius=0.05, length=0.8
        gluCylinder(quad, 0.05, 0.05, 0.8, 12, 3)

        glPopMatrix()
    else:
        # your old TPV gun:
        glColor3f(0.7, 0.7, 0.7)
        glTranslatef(0, 38, 12)
        quad = gluNewQuadric()
        gluCylinder(quad, 3.5, 2, 20, 12, 2)

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

def is_inside_obstacle(x, z):
    for obs in obstacles:
        # shrink the “buffer” from +15 → +8
        if abs(x - obs.x) < obs.size + 8 and abs(z - obs.z) < obs.size + 8:
            return True
    return False

def draw_status():
    """
    Renders the HUD:
      • Health bar + dynamic-colored label
      • Level bar + blue label
      • Score / Weapon Lv / Misses-left (white)
      • Shield timer & “Shield On” (white)
      • CHEAT MODE ON (white, top-right)
      • Big centered notifications
      • PAUSED / GAME OVER
    """
    global notification_timer, notification_text, notification_color
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)

    # — 2D overlay setup —
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    glOrtho(0, w, h, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glDisable(GL_LIGHTING)

    # Base positions
    x0, y0 = 10, 10
    bar_w, bar_h = w * 0.3, 20

    # — Health Bar —
    frac_h = player_health / max_health
    # determine bar color & use same for label
    if frac_h > 0.66:
        hc = (0, 1, 0)
    elif frac_h > 0.33:
        hc = (1, 1, 0)
    else:
        hc = (1, 0, 0)

    # draw bar outline
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x0, y0); glVertex2f(x0 + bar_w, y0)
    glVertex2f(x0 + bar_w, y0 + bar_h); glVertex2f(x0, y0 + bar_h)
    glEnd()
    # draw bar fill
    glColor3f(*hc)
    glBegin(GL_QUADS)
    glVertex2f(x0, y0)
    glVertex2f(x0 + bar_w * frac_h, y0)
    glVertex2f(x0 + bar_w * frac_h, y0 + bar_h)
    glVertex2f(x0, y0 + bar_h)
    glEnd()
    # health label in same color as bar
    label_x = x0 + bar_w + 10
    glColor3f(*hc)
    draw_text(label_x, y0 + bar_h - 5,
              f"Health: {player_health}/{max_health}")

    # — Level Bar —
    level_y0 = y0 + bar_h + 10
    frac_l = current_wave / 10.0
    # outline
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x0, level_y0); glVertex2f(x0 + bar_w, level_y0)
    glVertex2f(x0 + bar_w, level_y0 + bar_h); glVertex2f(x0, level_y0 + bar_h)
    glEnd()
    # fill (blue)
    glColor3f(0.3, 0.3, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(x0, level_y0)
    glVertex2f(x0 + bar_w * frac_l, level_y0)
    glVertex2f(x0 + bar_w * frac_l, level_y0 + bar_h)
    glVertex2f(x0, level_y0 + bar_h)
    glEnd()
    # level label in blue
    glColor3f(0.3, 0.3, 1.0)
    draw_text(label_x, level_y0 + bar_h - 5,
              f"Level: {current_wave}/10")

    # — Score / Weapon Lv / Misses-left (white) —
    stats_y = level_y0 + bar_h + 20
    spacing = 150
    rem = MAX_MISSED_BULLETS - bullets_missed
    glColor3f(1, 1, 1)
    draw_text(x0,               stats_y, f"Score: {game_score}")
    draw_text(x0 + spacing,     stats_y, f"Weapon Lv: {weapon_power_level}")
    draw_text(x0 + 2*spacing,   stats_y, f"Misses left: {rem}/{MAX_MISSED_BULLETS}")

    # — Shield status (white) —
    if shield_active and shield_timer > 0:
        draw_text(x0, stats_y + 20,
                  f"Shield On ({shield_timer//60}s)")

    # — Cheat Mode indicator (white, top-right) —
    if cheat_mode:
        text = "CHEAT MODE ON"
        tw = len(text) * 9
        glColor3f(1, 1, 1)
        draw_text(w - tw - 10, 20, text)

    # — Big centered notifications —
    if notification_timer > 0:
        glColor3f(*notification_color)
        txt = notification_text
        tw = len(txt) * 12
        glRasterPos2f((w - tw) / 2, h * 0.3)
        for ch in txt:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(ch))
        notification_timer -= 1
        glColor3f(1, 1, 1)

    # — PAUSED / GAME OVER —
    if game_paused:
        draw_text((w - len("PAUSED")*9)//2, h//2, "PAUSED")
    if game_over:
        msg = "GAME OVER - Press R to Restart"
        glColor3f(1, 0, 0)
        draw_text((w - len(msg)*9)//2, h//2 + 20, msg)

    # — restore 3D state —
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
    aspect = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)
    gluPerspective(fov, aspect, 1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if follow_camera:
        # --- first-person: camera at eye level (≈head height) ---
        eye_x = player_pos[0]
        eye_y = player_pos[1] + 45    # ← raised from “+ player_height + 10”
        eye_z = player_pos[2]

        # forward vector
        yaw = math.radians(player_angle)
        dx  = math.sin(yaw)
        dz  = math.cos(yaw)

        # look point pitched down by ~15°
        look_x = eye_x + 100 * dx
        look_z = eye_z + 100 * dz
        look_y = eye_y - 20

        gluLookAt(eye_x, eye_y, eye_z,
                  look_x, look_y, look_z,
                  0, 1, 0)
    else:
        # --- third-person: orbit camera as before ---
        radius = 250
        cam_x = player_pos[0] + radius * math.sin(math.radians(camera_angle))
        cam_y = player_pos[1] + camera_height
        cam_z = player_pos[2] + radius * math.cos(math.radians(camera_angle))

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
    """
    A bullet that can optionally home in on a target_enemy if cheat_bullet is True.
    """
    def __init__(self, x, y, z, angle, target_enemy=None, cheat_bullet=False):
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.target_enemy = target_enemy
        self.cheat_bullet = cheat_bullet
        self.hit = False
        self.hit_enemy = False
        self.size = 4
        self.speed = 6

    def update(self):
        if self.hit:
            return

        # If cheat_bullet, home in on target until it dies
        if self.cheat_bullet and self.target_enemy and not self.target_enemy.is_dead:
            dx = self.target_enemy.x - self.x
            dy = (self.target_enemy.y + 15) - self.y
            dz = self.target_enemy.z - self.z
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist > 1:
                self.x += dx/dist * self.speed
                self.y += dy/dist * self.speed
                self.z += dz/dist * self.speed
            else:
                self.hit = True
        else:
            # Straight‐line travel
            rad = math.radians(self.angle)
            new_x = self.x + self.speed * math.sin(rad)
            new_z = self.z + self.speed * math.cos(rad)
            if inside_boundary(new_x, new_z):
                self.x, self.z = new_x, new_z
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
    """
    Shoots infinitely (no ammo cap), still respects cheat_mode targeting.
    """
    global bullets

    if game_paused:
        return

    target = None
    cheat_flag = False
    if cheat_mode:
        # find closest alive enemy
        min_d, closest = float('inf'), None
        for e in enemies:
            if not e.is_dead:
                dx = e.x - player_pos[0]; dz = e.z - player_pos[2]
                d = math.hypot(dx, dz)
                if d < min_d:
                    min_d, closest = d, e
        if closest:
            target = closest
            closest.target = True
            cheat_flag = True

    # spawn at barrel tip
    if follow_camera:
        bx = player_pos[0]
        by = player_pos[1] + player_height + 10
        bz = player_pos[2]
    else:
        off = 25
        bx = player_pos[0] + off * math.sin(math.radians(player_angle))
        by = player_pos[1] + 35
        bz = player_pos[2] + off * math.cos(math.radians(player_angle))

    bullets.append(Bullet(bx, by, bz, player_angle, target, cheat_flag))


class BloodParticle:
    """
    A red cube that flies out briefly (~0.5s) when a zombie is hit.
    """
    def __init__(self, x, y, z):
        self.x = x + random.uniform(-2, 2)
        self.y = y + random.uniform(-2, 2)
        self.z = z + random.uniform(-2, 2)
        self.size = random.uniform(2, 4)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(0.5, 1.5)
        self.dz = random.uniform(-1, 1)
        self.life = 30  # frames (~0.5s at 60fps)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.dy -= 0.06  # gravity‐like
        self.life -= 1

    def draw(self):
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(self.x, self.y, self.z)
        glutSolidCube(self.size)
        glPopMatrix()

    def is_alive(self):
        return self.life > 0


def add_blood_splatter(x, y, z):

    for _ in range(30):
        particles.append(BloodParticle(x, y, z))



def move_player(dx, dz):
    if game_paused or game_over:
        return
    new_x = player_pos[0] + dx
    new_z = player_pos[2] + dz
    if inside_boundary(new_x, new_z) and not is_inside_obstacle(new_x, new_z):
        player_pos[0] = new_x
        player_pos[2] = new_z

def update_game():
    """
    Main game loop update with:
      - per‐type health (normal=2, runner=1, tank=4)
      - infinite bullets; misses counted only when not cheating
      - each bullet deals damage = 1 + weapon_power_level
      - only respawn a zombie when its health drops to ≤0
      - immediate respawn on player collision
      - blood splatter on zombie death
      - wave & power‐up logic unchanged
    """
    global bullets, enemies, health_pickups, power_ups, particles
    global game_score, player_health, bullets_missed, game_over
    global zombies_killed, current_wave, wave_progress_tracker
    global shield_active, shield_timer, weapon_power_level, weapon_timer
    global cheat_mode, game_paused

    if game_over or game_paused:
        return

    # — Bullet update & miss counting —
    new_bullets = []
    for b in bullets:
        b.update()
        if b.is_alive():
            new_bullets.append(b)
        else:
            if not b.hit_enemy and not getattr(b, 'cheat_bullet', False):
                bullets_missed += 1
                if bullets_missed >= MAX_MISSED_BULLETS:
                    game_over = True
                    show_notification("Too many misses! Game Over.", (1,0,0))
    bullets[:] = new_bullets

    # — Spawn / update pickups (unchanged) —
    if random.random() < 0.005 and len(health_pickups) < 3:
        health_pickups.append(Pickup(
            random.uniform(-BOUNDARY_SIZE/2+50, BOUNDARY_SIZE/2-50),
            random.uniform(-BOUNDARY_SIZE/2+50, BOUNDARY_SIZE/2-50),
            (1.0,0.4,0.7), 'health'
        ))
    if random.random() < 0.01 and len(power_ups) < 2:
        color, ptype = ((0.6,0.2,0.8),'shield') if random.random()<0.5 else ((0.0,0.9,0.9),'upgrade')
        power_ups.append(Pickup(
            random.uniform(-BOUNDARY_SIZE/2+50, BOUNDARY_SIZE/2-50),
            random.uniform(-BOUNDARY_SIZE/2+50, BOUNDARY_SIZE/2-50),
            color, ptype
        ))

    for hp in health_pickups[:]:
        hp.update()
        if not hp.active:
            health_pickups.remove(hp)
        elif abs(player_pos[0]-hp.x)<12 and abs(player_pos[2]-hp.z)<12:
            player_health = min(max_health, player_health+1)
            health_pickups.remove(hp)
            show_notification("Health orb taken!", hp.color)

    for pu in power_ups[:]:
        pu.update()
        if not pu.active:
            power_ups.remove(pu)
        elif abs(player_pos[0]-pu.x)<12 and abs(player_pos[2]-pu.z)<12:
            if pu.ptype=='shield':
                shield_active = True
                shield_timer = MAX_POWERUP_LIFETIME
                show_notification("Shield taken!", pu.color)
            else:
                weapon_power_level += 1
                weapon_timer = MAX_POWERUP_LIFETIME
                show_notification("Weapon upgraded!", pu.color)
            power_ups.remove(pu)

    # — Maintain wave enemy count —
    max_en = MAX_ENEMIES_BASE + (current_wave-1)*3
    while len(enemies) < max_en:
        enemies.append(Enemy())

    # — Enemy movement & collision —
    new_enemies = []
    for e in enemies:
        e.update()

        # player collision ⇒ immediate respawn
        if e.check_collision_with_player():
            if shield_active and shield_timer>0:
                shield_active = False
                shield_timer = 0
                show_notification("Shield used!", (0.6,0.2,0.8))
            else:
                player_health -= 1
                show_notification("Hit by zombie!", (1,0,0))
                if player_health <= 0:
                    game_over = True
                    show_notification("You died!", (1,0,0))
            e.respawn()
            new_enemies.append(e)
            continue

        # bullet collision ⇒ apply scaled damage; only respawn if health ≤ 0
        damaged = False
        for b in bullets:
            if not b.hit and e.check_collision_with_bullet(b):
                b.hit = True
                b.hit_enemy = True
                damage = 1 + weapon_power_level
                e.health -= damage
                damaged = True
                if e.health <= 0:
                    game_score += 1
                    zombies_killed += 1
                    add_blood_splatter(e.x, e.y+15, e.z)
                    e.respawn()
                break

        new_enemies.append(e)

    enemies[:] = new_enemies

    # — Wave progression —
    if zombies_killed >= wave_progress_tracker + 5:
        wave_progress_tracker += 5
        if current_wave < 10:
            current_wave += 1
            show_notification("Terror is starting!!!", (1,0,0))
        else:
            show_notification("Final Wave!!!", (1,0,0))

    # — Power-up timers —
    if shield_timer > 0:
        shield_timer -= 1
        if shield_timer == 0:
            shield_active = False
    if weapon_timer > 0:
        weapon_timer -= 1

    # — Particle updates —
    update_particles()





# at top of your module, add:
notification_color = (1,0,0)

def show_notification(text, color=(1,0,0)):
    """
    Queue a centered on-screen message in the given color,
    lasting ~10 seconds at 60 FPS.
    """
    global notification_text, notification_timer, notification_color
    notification_text  = text
    notification_color = color
    notification_timer = 600   # ≈10 s at 60 FPS







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
    # --- set up viewport ---
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    glViewport(0, 0, w, h)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # --- camera ---
    setupCamera()

    # --- 3D world ---
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    draw_floor()
    draw_obstacles()
    draw_all_enemies()
    draw_all_bullets()
    draw_all_pickups()
    draw_all_particles()

    if follow_camera:
        # in FPS mode: draw only arms+gun in view-space
        draw_first_person_gun_hand_head(
            player_pos[0],
            player_pos[1] + player_height + 10,
            player_pos[2]
        )
    else:
        # in 3rd-person: draw full player
        draw_player()

    # --- HUD & notifications ---
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
