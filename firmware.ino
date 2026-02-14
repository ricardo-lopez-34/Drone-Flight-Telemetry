#include <MPU6050_tockn.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>

MPU6050 mpu6050(Wire);
Adafruit_BMP280 bmp; 

unsigned long timer = 0;
const int logInterval = 50; 

void setup() {
  Serial.begin(115200);
  
  Wire.setSDA(4); 
  Wire.setSCL(5); 
  Wire.begin();

  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 Sensor Missing!");
  }
  
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true); 
  
  Serial.println("--- PICO FLIGHT SYSTEM ONLINE ---");
}

void loop() {
  mpu6050.update();

  if (millis() - timer > logInterval) {
    float angleX = mpu6050.getAngleX();
    float angleY = mpu6050.getAngleY();
    float angleZ = mpu6050.getAngleZ();

    float temp = bmp.readTemperature();
    float alt  = bmp.readAltitude(1013.25); 

    float accX = mpu6050.getAccX();
    float accY = mpu6050.getAccY();
    float accZ = mpu6050.getAccZ();
    float totalG = sqrt(pow(accX, 2) + pow(accY, 2) + pow(accZ, 2));

    Serial.print("DATA:");
    Serial.print(angleX); Serial.print("|");
    Serial.print(angleY); Serial.print("|");
    Serial.print(totalG); Serial.print("|");
    Serial.println(alt);

    if (abs(angleX) > 45 || abs(angleY) > 45) {
      Serial.println("WARNING: ATTITUDE INSTABILITY");
    }

    timer = millis();
  }
}
