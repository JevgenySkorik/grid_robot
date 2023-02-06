char x;

int motor1pin1 = 2;
int motor1pin2 = 3;

int motor2pin1 = 4;
int motor2pin2 = 5;

int led = 13;

void setup() {
  Serial.begin(9600);
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);

  pinMode(led, OUTPUT);
}

void go_forward(int time) {
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
  
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
    
  delay(time);
}

void turn_right(int time) {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);

  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);

  delay(time);
}

void turn_left(int time) {
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);

  delay(time);
}

void turn_motors_off() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);

  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void calibrate() {
  // TODO: change pins to real values
  int left_sensor = analogRead(A0);
  int right_sensor = analogRead(A1);

  Serial.print("Left sensor: ");
  Serial.print(left_sensor);
  Serial.print("Right sensor: ");
  Serial.print(right_sensor);

  // If robot too far to the left(left sensor is sensing a lot of light),
  // turn robot right until light is dim
  // TODO: replace 500 with value of the sensor when robot is over black dot,
  //       change time of turn if necessary
  while (left_sensor > 500) {
    Serial.print("Left sensor not aligned, aligning...");
    Serial.print("Left sensor: ");
    Serial.print(left_sensor);
  	turn_right(100);
  }
  turn_motors_off();
  Serial.print("Left sensor aligned");
  
  // Do the same with right sensor
  while (right_sensor > 500) {
    Serial.print("Right sensor not aligned, aligning...");
    Serial.print("Right sensor: ");
    Serial.print(right_sensor);
    turn_left(100);
  }
  turn_motors_off();
  Serial.print("Right sensor aligned");
}

void loop() {
  // Read received commands and execute them
  if (Serial.available() > 0) {
    x = Serial.read();
    switch (x) {
      case 'F':
        go_forward(550);
      	turn_motors_off();
        break;
      case 'R':
        turn_right(460);
      	turn_motors_off();
        break;
      case 'L':
      	turn_left(460);
      	turn_motors_off();
        break;
      case 'C':
      	calibrate();
        break;
    }
    // Default delay after every action
    delay(500);
  }
}