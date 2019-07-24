//CONTROLADOR MANUAL
#include <Wire.h>
#include <ros.h>
#include <geometry_msgs/Pose2D.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Bool.h>
#include <sensor_msgs/Range.h>
//PROTOTIPOS
void ordenar(void); //ordena leitura recebida para casos de problema na comunicação
//MOTORES VIBRACAO (L293D)
const int enable1 = 8;
const int enable2 = 9;
const int motor1pin = 3;
const int motor2pin = 5;
const int motor3pin = 6;
const int pwm_forte = 180;
const int pwm_fraco = 100;
//ACELEROMETRO
const int MPU_addr = 0x68;
int16_t AcX, AcY;
int x, y, z, aux,X,Y,Z;

ros::NodeHandle  nh;
geometry_msgs::Pose2D imu_msg;
ros::Publisher imu("imu", &imu_msg);
void messageCb(const sensor_msgs::Range& Leitura1){
  X = Leitura1.range;
}

void messageCb2(const std_msgs::Float64& Leitura2){
  Y = Leitura2.data;  
}
void messageCb3(const std_msgs::Float64& Leitura3){
  Z = Leitura3.data;
}

ros::Subscriber<sensor_msgs::Range> local("local",&messageCb);
ros::Subscriber<std_msgs::Float64> local2("local2",&messageCb2);
ros::Subscriber<std_msgs::Float64> local3("local3",&messageCb3);

/*void motor_msg(const std_msgs::Bool& aux1){
  if(aux1.data==true){
      if (x == '1') analogWrite(motor2pin, 0);
      if (x == '2') analogWrite(motor2pin, pwm_fraco);
      if (x == '3') analogWrite(motor2pin, pwm_forte);
      if (y == '4') analogWrite(motor1pin, 0);
      if (y == '5') analogWrite(motor1pin, pwm_fraco);
      if (y == '6') analogWrite(motor1pin, pwm_forte);
      if (z == '7') analogWrite(motor3pin, 0);
      if (z == '8') analogWrite(motor3pin, pwm_fraco);
      if (z == '9') analogWrite(motor3pin, pwm_forte);
      } 
  }
*/
//ros::Subscriber<std_msgs::Bool> motor("motor", &motor_msg); 

void setup() {
//SETUP MOTORES VIBRACAO
pinMode(enable1, OUTPUT);
pinMode(enable2, OUTPUT);
pinMode(motor1pin, OUTPUT);
pinMode(motor2pin, OUTPUT);
pinMode(motor3pin, OUTPUT);
analogWrite(motor1pin, 0);
analogWrite(motor2pin, 0);
analogWrite(motor3pin, 0);
//SETUP ACELEROMETRO
  nh.initNode();
  nh.advertise(imu);
  nh.subscribe(local);
  nh.subscribe(local2);
  nh.subscribe(local3);

Wire.begin();
Wire.beginTransmission(MPU_addr);
Wire.write(0x6B); //registrador PWR_MGMT_1
Wire.write(0); //inicia o MPU-6050
Wire.endTransmission(true);
//Serial.begin(9600);
//tempo de espera para os módulos Bluetooth se conectarem
delay(5000); 
 //nh.initNode();
 //nh.subscribe(motor);
}

long publisher_timer;

void loop() {
//LEITURA ACELEROMETRO
Wire.beginTransmission(MPU_addr);
Wire.write(0x3B); //ACCEL_XOUT_H
Wire.endTransmission(false);
Wire.requestFrom(MPU_addr, 4, true);
AcX = Wire.read() << 8 | Wire.read(); //0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
AcY = Wire.read() << 8 | Wire.read(); //0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)

  imu_msg.x = AcX;
//Serial.print(x);
delay(2);
  imu_msg.y = AcY;
delay(2);

//ENVIAR DADOS DO ACELEROMETRO
if (AcX >= 6000) x = 2;
if (AcX < 6000 && AcX > -6000) x = 1;
if (AcX <= -6000) x = 0;
if (AcY >= 6000) y = 5;
if (AcY < 6000 && AcY > -6000) y = 4;
if (AcY <= -6000) y = 3;

  imu_msg.x = x;
//Serial.print(x);
delay(2);
  imu_msg.y = y;
delay(2);

//RECEBER DADOS DOS SENSORES
/*while (!Serial.available()); //123
x = Serial.read();
while (!Serial.available()); //456
y = Serial.read();
while (!Serial.available()); //789
z = Serial.read();*/
x = X;
y = Y;
z = Z;
delay(2);

ordenar();
//ACIONAMENTO DA VIBRAÇAO
if (x == '1') analogWrite(motor2pin, 0);
if (x == '2') analogWrite(motor2pin, pwm_fraco);
if (x == '3') analogWrite(motor2pin, pwm_forte);
if (y == '4') analogWrite(motor1pin, 0);
if (y == '5') analogWrite(motor1pin, pwm_fraco);
if (y == '6') analogWrite(motor1pin, pwm_forte);
if (z == '7') analogWrite(motor3pin, 0);
if (z == '8') analogWrite(motor3pin, pwm_fraco);
if (z == '9') analogWrite(motor3pin, pwm_forte);

  if (millis() > publisher_timer) {
    // step 1: request reading from sensor
    imu.publish(&imu_msg);
    publisher_timer = millis() + 100; //publish ten times a second
    nh.spinOnce();
  }

  delay(40);
}
//ACIONAMENTO DA VIBRAÇAO

void ordenar() {
if (x > y) {
aux = x; x = y; y = aux; }
if (x > z) {
aux = x; x = z; z = aux; }
if (y > z) {
aux = y; y = z; z = aux; }
if (x > y) {
aux = x; x = y; y = aux; }
if (x > z) {
aux = x; x = z; z = aux; }
if (y > z) {
aux = y; y = z; z = aux; }
}
