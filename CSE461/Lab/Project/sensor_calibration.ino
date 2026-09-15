/* =====================================================================
   STEP 0 - RUN THIS FIRST, BEFORE THE MAIN LAWNMOWER CODE
   =====================================================================
   Purpose: confirm (a) each wheel spins the correct direction, and
   (b) whether your IR sensors report LOW or HIGH when they see an object.
   Open Serial Monitor at 9600 baud after uploading.

   Wiring assumed exactly as in wiring_diagram.txt.
   ===================================================================== */

#define ENA 5
#define IN1 8
#define IN2 7
#define ENB 6
#define IN3 4
#define IN4 2

#define IR_LEFT  A0
#define IR_RIGHT A1

void setup() {
  Serial.begin(9600);
  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT); pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(IR_LEFT, INPUT);
  pinMode(IR_RIGHT, INPUT);

  Serial.println(F("=== MOTOR TEST ==="));
  Serial.println(F("LEFT side motors should now spin FORWARD for 2s..."));
  leftMotor(200, true);   rightMotor(0, true); delay(2000); stopAll();
  Serial.println(F("Did LEFT wheel(s) spin FORWARD (pushing robot ahead)?"));
  Serial.println(F("If it spun BACKWARD, swap that channel's OUT wires on the L298N, or flip IN1/IN2 logic in the main code."));
  delay(1500);

  Serial.println(F("RIGHT side motors should now spin FORWARD for 2s..."));
  leftMotor(0, true);     rightMotor(200, true); delay(2000); stopAll();
  Serial.println(F("Did RIGHT wheel(s) spin FORWARD? If backward, swap OUT3/OUT4 or flip IN3/IN4 logic."));
  delay(1500);

  Serial.println(F("=== TEST COMPLETE - now watch the IR readings below ==="));
  Serial.println(F("Wave your hand under each IR sensor (3-5cm away) and read Serial Monitor."));
}

void loop() {
  int l = digitalRead(IR_LEFT);
  int r = digitalRead(IR_RIGHT);
  Serial.print(F("IR_LEFT raw = "));
  Serial.print(l);
  Serial.print(F("   IR_RIGHT raw = "));
  Serial.println(r);
  Serial.println(F("-> Note the value with NOTHING under the sensor, then the value WITH your hand under it."));
  Serial.println(F("-> Whichever value appears when an object IS present = your 'detected' value. Write it down."));
  delay(500);
}

// ---- helper functions ----
void leftMotor(int speed, bool forward) {
  digitalWrite(IN1, forward ? HIGH : LOW);
  digitalWrite(IN2, forward ? LOW  : HIGH);
  analogWrite(ENA, speed);
}
void rightMotor(int speed, bool forward) {
  digitalWrite(IN3, forward ? HIGH : LOW);
  digitalWrite(IN4, forward ? LOW  : HIGH);
  analogWrite(ENB, speed);
}
void stopAll() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}
