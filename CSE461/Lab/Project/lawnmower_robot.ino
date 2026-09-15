/* =====================================================================
   AUTONOMOUS GARBAGE-COLLECTING ROBOT - PHASE 1 (CAR ONLY)
   Lawnmower (boustrophedon) coverage pattern + obstacle avoidance
   + garbage DETECTION (claw action added in Phase 2)

   BEFORE USING THIS FILE:
   1. Run sensor_calibration.ino first and confirm motor directions.
   2. Note what value (HIGH or LOW) your IR sensors give when they
      DETECT an object, and set IR_TRIGGER_STATE below to match.
   3. Measure your actual row length / turn timing on your real floor
      and adjust the CALIBRATION SECTION below. The numbers here are
      starting guesses, not guaranteed for your motors/battery/floor.
   ===================================================================== */

// ---------------- PIN DEFINITIONS (see wiring_diagram.txt) ----------------
#define ENA 5      // Left side speed  (PWM)
#define IN1 8      // Left side direction bit A
#define IN2 7      // Left side direction bit B
#define ENB 6      // Right side speed (PWM)
#define IN3 4      // Right side direction bit A
#define IN4 2      // Right side direction bit B

#define TRIG_PIN 9
#define ECHO_PIN 10

#define IR_LEFT   A0
#define IR_RIGHT  A1

#define BUZZER_PIN 11

// ---------------- CALIBRATION SECTION - TUNE THESE ----------------
int DRIVE_SPEED        = 180;   // 0-255 PWM speed for straight driving
int TURN_SPEED          = 170;   // 0-255 PWM speed while turning

unsigned long ROW_FORWARD_TIME   = 6000;  // ms to drive down one full row - MEASURE THIS
unsigned long TURN_90_TIME       = 420;   // ms to rotate ~90 degrees - MEASURE THIS with a protractor
unsigned long ROW_SPACING_TIME   = 700;   // ms forward move between the two 90-deg turns
                                           // (this sets the gap between rows - roughly
                                           // your robot's width; measure and tune)
int NUM_ROWS               = 6;      // how many rows before the pattern stops

float OBSTACLE_DISTANCE_CM = 25.0;  // ultrasonic trigger distance
int   IR_TRIGGER_STATE     = LOW;   // <-- SET based on sensor_calibration.ino results!
                                     //     (many IR modules go LOW when object detected)

unsigned long GARBAGE_PAUSE_TIME = 1500; // how long to pause/buzz when garbage is spotted
// ---------------------------------------------------------------------

int rowsCompleted = 0;
bool turnRightNext = true;  // alternates so the pattern zig-zags correctly

void setup() {
  Serial.begin(9600);
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(IR_LEFT, INPUT);
  pinMode(IR_RIGHT, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  stopMotors();
  delay(2000); // give you time to put the robot down and step back
  Serial.println(F("Starting lawnmower pattern..."));
}

void loop() {
  if (rowsCompleted >= NUM_ROWS) {
    stopMotors();
    Serial.println(F("Pattern complete. Halting."));
    while (true) { delay(1000); } // stop forever
  }

  // ---- Drive down one full row, checking sensors continuously ----
  driveRowWithMonitoring(ROW_FORWARD_TIME);
  rowsCompleted++;
  Serial.print(F("Row complete: "));
  Serial.println(rowsCompleted);

  if (rowsCompleted >= NUM_ROWS) {
    stopMotors();
    Serial.println(F("Pattern complete. Halting."));
    while (true) { delay(1000); }
  }

  // ---- Execute the U-turn into the next row (deterministic, not random) ----
  if (turnRightNext) {
    turn(true, TURN_90_TIME);
    driveStraight(ROW_SPACING_TIME);
    turn(true, TURN_90_TIME);
  } else {
    turn(false, TURN_90_TIME);
    driveStraight(ROW_SPACING_TIME);
    turn(false, TURN_90_TIME);
  }
  turnRightNext = !turnRightNext; // alternate direction so rows zig-zag
  stopMotors();
  delay(300);
}

// =====================================================================
// Drives forward for `duration` ms in small monitored chunks, so
// obstacle avoidance and garbage detection can interrupt mid-row.
// =====================================================================
void driveRowWithMonitoring(unsigned long duration) {
  unsigned long elapsed = 0;
  const unsigned long CHUNK = 100; // check sensors every 100ms

  while (elapsed < duration) {
    // --- garbage check first (low sensors) ---
    if (checkGarbage()) {
      stopMotors();
      handleGarbageDetected();
      // resume driving after handling; don't count this pause in elapsed time
      continue;
    }

    // --- obstacle check (front ultrasonic) ---
    float dist = getDistanceCM();
    if (dist > 0 && dist < OBSTACLE_DISTANCE_CM) {
      stopMotors();
      handleObstacleAvoidance();
      continue; // resume the row after the side-step maneuver
    }

    driveStraight(CHUNK);
    elapsed += CHUNK;
  }
  stopMotors();
}

// =====================================================================
// Obstacle avoidance: deterministic side-step, NOT random.
// Backs up a little, steps right around it, then returns to original
// heading so the lawnmower pattern is preserved.
// =====================================================================
void handleObstacleAvoidance() {
  Serial.println(F("Obstacle detected - side-stepping."));
  driveBackward(400);
  turn(true, TURN_90_TIME);     // face right
  driveStraight(500);           // move past the obstacle's width
  turn(false, TURN_90_TIME);    // face original heading again
  driveStraight(200);           // re-enter the row line
  turn(false, 0);               // no-op placeholder for symmetry (kept for clarity)
}

// =====================================================================
// Garbage detected: stop, alert with buzzer.
// Claw pickup sequence goes here in Phase 2 - currently just pauses.
// =====================================================================
void handleGarbageDetected() {
  Serial.println(F("Garbage detected - pausing (claw not yet installed)."));
  tone(BUZZER_PIN, 1000);
  delay(GARBAGE_PAUSE_TIME);
  noTone(BUZZER_PIN);
  // TODO Phase 2: call clawPickupSequence() here, then resume.
  driveBackward(150); // small nudge back so we don't re-trigger the same item instantly
}

bool checkGarbage() {
  int l = digitalRead(IR_LEFT);
  int r = digitalRead(IR_RIGHT);
  return (l == IR_TRIGGER_STATE) || (r == IR_TRIGGER_STATE);
}

// =====================================================================
// Ultrasonic distance read (HC-SR04), returns cm, -1 if no echo
// =====================================================================
float getDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout (~5m max)
  if (duration == 0) return -1;
  return duration * 0.0343 / 2.0;
}

// =====================================================================
// Low-level motor control
// =====================================================================
void driveStraight(unsigned long ms) {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);   // left forward
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);   // right forward
  analogWrite(ENA, DRIVE_SPEED);
  analogWrite(ENB, DRIVE_SPEED);
  delay(ms);
  stopMotors();
}

void driveBackward(unsigned long ms) {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);   // left backward
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);   // right backward
  analogWrite(ENA, DRIVE_SPEED);
  analogWrite(ENB, DRIVE_SPEED);
  delay(ms);
  stopMotors();
}

// clockwise = true turns right (left wheels forward, right wheels backward)
void turn(bool clockwise, unsigned long ms) {
  if (ms == 0) return;
  if (clockwise) {
    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);   // left forward
    digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);  // right backward
  } else {
    digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);  // left backward
    digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);   // right forward
  }
  analogWrite(ENA, TURN_SPEED);
  analogWrite(ENB, TURN_SPEED);
  delay(ms);
  stopMotors();
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
}
