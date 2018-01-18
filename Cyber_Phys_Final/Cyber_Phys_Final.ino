#include <EventTimer.h>
#include <Adafruit_CC3000.h>
#include <ccspi.h>
#include <SPI.h>
#include <string.h>
#include "utility/debug.h"


//Pins
#define REFLECT_LEFT_PIN      7
#define REFLECT_RIGHT_PIN     9
#define RIGHT_WHEEL_A1        2
#define RIGHT_WHEEL_A2        4
#define RIGHT_WHEEL_PWM       6
#define LEFT_WHEEL_B1         A0
#define LEFT_WHEEL_B2         A1
#define LEFT_WHEEL_PWM        5
#define ADAFRUIT_CC3000_IRQ   3
#define ADAFRUIT_CC3000_VBAT  8
#define ADAFRUIT_CC3000_CS    10

Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
                                         SPI_CLOCK_DIVIDER);

#define WLAN_SSID       "wahoo"
#define WLAN_PASS       ""
#define WLAN_SECURITY   WLAN_SEC_UNSEC
#define IDLE_TIMEOUT_MS  3000
#define WEBSITE         "172.28.39.32"
#define WEBPAGE_PATH "/tlp2019/ak2hr/find_path.php?"
#define WEBPAGE_DEST "/tlp2019/ak2hr/get_dest.php?"
#define NODEA   "A"
#define NODEB   "B"
#define NODEC   "C"
#define NODED   "D"
#define NODEE   "E"
#define NODEF   "F"
#define NODEG   "G"
#define NODEH   "H"
#define NODEI   "I"
#define NODEJ   "J"
#define NODEK   "K"
#define NODEL   "L"
#define NODEM   "M"    
#define NODEN   "N"
#define NODEO   "O"
#define NODEZ   "Z"



//Global Variables/Objects
EventTimer calibrateTimer;
int reflectMidpoint;
int reflectMax = 0;
int reflectMin = 10000;
float left_pwm = 50.0;
float right_pwm = 50.0;
int regSpeed = 50;
int curInstruct = 0;
String directions;
String instructions;
String destination;
uint32_t ip = cc3000.IP2U32(172,28,39,32);
char prevNode = 'Z';
char startNode = 'A';
char destNode;
int destID = 1;



//States
typedef enum State{
  calibrating,
  following,
  instructing,
  stopped
};

State curState = stopped;


void setup() {
  Serial.begin(115200);    
  pinMode(RIGHT_WHEEL_A1, OUTPUT);  
  pinMode(RIGHT_WHEEL_A2, OUTPUT);
  pinMode(RIGHT_WHEEL_PWM, OUTPUT);  
  pinMode(LEFT_WHEEL_B1, OUTPUT);  
  pinMode(LEFT_WHEEL_B2, OUTPUT);
  pinMode(LEFT_WHEEL_PWM, OUTPUT);
  digitalWrite(RIGHT_WHEEL_A1, LOW); 
  digitalWrite(RIGHT_WHEEL_A2, HIGH);
  digitalWrite(LEFT_WHEEL_B1, LOW); 
  digitalWrite(LEFT_WHEEL_B2, HIGH);
  delay(1000);
  calibrate();
  Serial.println("connecting to internet");
  if (!cc3000.begin())
  {
    Serial.println(F("Couldn't begin()! Check your wiring?"));
    while(1);
  }
  if (!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) {
    Serial.println(F("Failed!"));
    while(1);
  }
  while (!cc3000.checkDHCP())
  {
    delay(100); // ToDo: Insert a DHCP timeout!
  }          
  Serial.println("connected");
  delay(1000);  
}

//Read Reflectance Sensor------------------------------------------------------------------
long readReflectanceSensor(const int pin) {
   pinMode(pin, OUTPUT);
   digitalWrite(pin, HIGH);
   delay(1);
   long startValue = micros();
   pinMode(pin, INPUT);
   while(digitalRead(pin) == HIGH) {
   }
   return micros() - startValue;
}

//Calibrate--------------------------------------------------------------------------------
void calibrate() {
  Serial.println("calibrating");
  calibrateTimer.start(5000);
  while(!calibrateTimer.checkExpired()) {
    int val = readReflectanceSensor(REFLECT_LEFT_PIN);
    if(val > reflectMax) reflectMax = val;
    if(val < reflectMin) reflectMin = val;
    val = readReflectanceSensor(REFLECT_RIGHT_PIN);
    if(val > reflectMax) reflectMax = val;
    if(val < reflectMin) reflectMin = val;
  }
  reflectMidpoint = ((reflectMax - reflectMin)/2) + reflectMin;
}

//Follow Line------------------------------------------------------------------------------
void followLine() {
  long left = readReflectanceSensor(REFLECT_LEFT_PIN);
  long right = readReflectanceSensor(REFLECT_RIGHT_PIN);
  if((right < reflectMidpoint)  && (left > reflectMidpoint)) {
    right_pwm += 0.7;
    left_pwm -= 0.7;
  }
  else if((right > reflectMidpoint) && (left < reflectMidpoint)) {
    right_pwm -= 0.7;
    left_pwm += 0.7;
  }
  else if((right > reflectMidpoint) && (left > reflectMidpoint)) {  
    handleIntersection();
  }
  else if((right < reflectMidpoint) && (left < reflectMidpoint)) {  
    right_pwm = regSpeed;
    left_pwm = regSpeed;
  }
  analogWrite(RIGHT_WHEEL_PWM, right_pwm);
  analogWrite(LEFT_WHEEL_PWM, left_pwm);  
}

//Turn Right--------------------------------------------------------------------------------
void turnRight() {
  delay(500);
  analogWrite(RIGHT_WHEEL_PWM, 0);
  analogWrite(LEFT_WHEEL_PWM, 0);
  delay(1000);
  right_pwm = regSpeed;
  left_pwm = regSpeed;
  digitalWrite(RIGHT_WHEEL_A1, HIGH); 
  digitalWrite(RIGHT_WHEEL_A2, LOW);
  analogWrite(RIGHT_WHEEL_PWM, right_pwm);
  analogWrite(LEFT_WHEEL_PWM, left_pwm);  
  delay(800);
  analogWrite(RIGHT_WHEEL_PWM, 0);
  analogWrite(LEFT_WHEEL_PWM, 0);
  digitalWrite(RIGHT_WHEEL_A1, LOW); 
  digitalWrite(RIGHT_WHEEL_A2, HIGH);
  delay(1000);
}

//Turn Left-------------------------------------------------------------------------------
void turnLeft() {
  delay(500);
  analogWrite(RIGHT_WHEEL_PWM, 0);
  analogWrite(LEFT_WHEEL_PWM, 0);
  delay(1000);
  right_pwm = regSpeed;
  left_pwm = regSpeed;
  digitalWrite(RIGHT_WHEEL_A1, HIGH); 
  digitalWrite(RIGHT_WHEEL_A2, LOW);
  analogWrite(RIGHT_WHEEL_PWM, right_pwm);
  analogWrite(LEFT_WHEEL_PWM, left_pwm);  
  delay(2550);
  analogWrite(RIGHT_WHEEL_PWM, 0);
  analogWrite(LEFT_WHEEL_PWM, 0);
  digitalWrite(RIGHT_WHEEL_A1, LOW); 
  digitalWrite(RIGHT_WHEEL_A2, HIGH);
  delay(1000);
}

//Uturn-----------------------------------------------------------------------------------
void uTurn() {
  delay(500);
  analogWrite(RIGHT_WHEEL_PWM, 0);
  analogWrite(LEFT_WHEEL_PWM, 0);
  delay(1000);
  right_pwm = regSpeed;
  left_pwm = regSpeed;
  digitalWrite(RIGHT_WHEEL_A1, HIGH); 
  digitalWrite(RIGHT_WHEEL_A2, LOW);
  analogWrite(RIGHT_WHEEL_PWM, right_pwm);
  analogWrite(LEFT_WHEEL_PWM, left_pwm);  
  delay(1800);
  analogWrite(RIGHT_WHEEL_PWM, 0);
  analogWrite(LEFT_WHEEL_PWM, 0);
  digitalWrite(RIGHT_WHEEL_A1, LOW); 
  digitalWrite(RIGHT_WHEEL_A2, HIGH);
  delay(1000);
}

//getInstructions
void getInstructions() {  
  String ret = ""; 
  instructions = "";      
  directions = "";  
  Adafruit_CC3000_Client www = cc3000.connectTCP(ip, 80);
  if (www.connected()) {    
    www.fastrprint(F("GET "));
    www.fastrprint(WEBPAGE_PATH);    
    www.fastrprint(F("prev="));
    www.print(prevNode);
    www.fastrprint(F("&start="));
    www.print(startNode);
    www.fastrprint(F("&dest=")); 
    www.print(destNode);   
    www.fastrprint(F(" HTTP/1.1\r\n"));
    www.fastrprint(F("Host: ")); www.fastrprint(WEBSITE); www.fastrprint(F("\r\n"));
    www.fastrprint(F("\r\n"));
    www.println();    
  }
  else Serial.println(F("Failed to connect. No biscuit!"));

  unsigned long lastRead = millis();
  while (www.connected() && (millis() - lastRead < IDLE_TIMEOUT_MS)) {
    while (www.available()) {      
      char c = www.read();
      if(c != '\n' && c != '\r')
        ret += c;
      if(c == '\n') {
        if(ret.startsWith("<pre>")) {
          instructions = ret.substring(5);
        }
        ret = "";
      }      
      lastRead = millis();
    }
  }
    
  www.close();  

  startNode = destNode;
  prevNode = instructions.charAt(0);
  directions = instructions.substring(1);
}


//Handle Intersection------------------------------------------------------------------------------
void handleIntersection() {
  if(directions.charAt(curInstruct) == 'R') {
    Serial.println("right");
    turnRight();
  }
  else if(directions.charAt(curInstruct) == 'L') {
    Serial.println("left");
    turnLeft();
  }
  else if(directions.charAt(curInstruct) == 'U') {
    Serial.println("uturn");
    uTurn();
  }
  else if(directions.charAt(curInstruct) == 'F') {
    Serial.println("forward");
    delay(500);
  }
  else if(directions.charAt(curInstruct) == 'D') {
    Serial.println("stop");
    delay(500);    
    analogWrite(RIGHT_WHEEL_PWM, 0);
    analogWrite(LEFT_WHEEL_PWM, 0);
    curState = stopped;
  }
  curInstruct++;
}

//Get Dest-----------------------------------------------------------------------------------------
void getDest() {
  String ret = "";  
  Adafruit_CC3000_Client www = cc3000.connectTCP(ip, 80);
  if (www.connected()) {
    www.fastrprint(F("GET "));
    www.fastrprint(WEBPAGE_DEST);
    www.fastrprint(F("id="));
    www.print(destID);
    www.fastrprint(F(" HTTP/1.1\r\n"));
    www.fastrprint(F("Host: ")); www.fastrprint(WEBSITE); www.fastrprint(F("\r\n"));
    www.fastrprint(F("\r\n"));
    www.println();
  }
  unsigned long lastRead = millis();
  while (www.connected() && (millis() - lastRead < IDLE_TIMEOUT_MS)) {
    while (www.available()) {      
      char c = www.read();
      if(c != '\n' && c != '\r')
        ret += c;
      if(c == '\n') {
        if(ret.startsWith("id:")) {
          destID++;
          destNode = ret.charAt(ret.indexOf(";") + 8);
          curState = instructing;
        }
        ret = "";
      }                
      lastRead = millis();
    }
  }  
  www.close();
}

void loop() {       
  if(curState == stopped) {
    Serial.println("getting destination");
    analogWrite(RIGHT_WHEEL_PWM, 0);
    analogWrite(LEFT_WHEEL_PWM, 0);
    getDest();
    delay(5000);    
  }
  else if(curState == instructing) {
    Serial.println("getting instructions");
    curInstruct = 0;
    getInstructions();
    handleIntersection();
    curState = following;
  }
  else if(curState == following) {
    followLine();
  }
}
