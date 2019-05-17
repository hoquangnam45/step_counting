#include <cmath>
#include <iostream>
#include "Libs/Gyro/SFE_LSM9DS0.h"
#include "Libs/OLED/oled/Edison_OLED.h"
#include "Libs/OLED/gpio/gpio.h"

using namespace std;

// Giá trị đo từ thực nghiệm xin đừng thay đổi
#define UPPER_THRESH 1.32208354631175571
#define LOWER_THRESH 1.1277099856081106

LSM9DS0 *imu;
// Define an edOLED object:
edOLED oled;

// Pin definitions:
// All buttons have pull-up resistors on-board, so just declare
// them as regular INPUT's
gpio BUTTON_UP(47, INPUT);
gpio BUTTON_DOWN(44, INPUT);
gpio BUTTON_LEFT(165, INPUT);
gpio BUTTON_RIGHT(45, INPUT);
gpio BUTTON_SELECT(48, INPUT);
gpio BUTTON_A(49, INPUT);
gpio BUTTON_B(46, INPUT);

void init();
void readData();

float gyroX, gyroY, gyroZ, totalGyro,
      accelX, accelY, accelZ, totalAccel;

int main(){
    init();
    bool run = false;
    bool setFlag = 0;
    int stepCount = 0;
    while(true){
        while(!run){
            static bool initFlag = 0;
            stepCount = 0;
            setFlag = 0;
            if (!initFlag){
                oled.clear(PAGE);
                oled.setCursor(0,0);
                oled.print("Nhan A de bat dau");
                oled.display();
                initFlag = 1;
            }
            if (BUTTON_A.pinRead() == LOW){
                initFlag = 0;
                run = true;
                oled.clear(PAGE);
                oled.setCursor(0,0);
                oled.print("Nhan B de dung");
                oled.display();
                usleep(1e6);
            }
        }
        oled.clear(PAGE);
        oled.setCursor(0,0);
        oled.print("Dem: ");
        oled.print(stepCount);
        oled.display();
        readData();
        if (totalAccel < LOWER_THRESH) setFlag = true;
        else if (totalAccel > UPPER_THRESH && setFlag == true){
            setFlag = false;
            stepCount++;
            //cout << stepCount << endl;
        }
        if (BUTTON_B.pinRead() == LOW) run = false;
    }
    return 0;
}

void init(){
    imu = new LSM9DS0(0x6B, 0x1D);
    uint16_t imuResult = imu->begin();
    cout<<hex<<"Chip ID: 0x"<<imuResult<<dec<<" (should be 0x49d4)"<<endl;
    oled.begin();
    oled.clear(PAGE);
    oled.display();
    oled.setFontType(0);
}

void readData(){
    bool newGyroData = false, newAccelData = false;
    while ((newGyroData & newAccelData) != true){
        if (newAccelData != true){
            newAccelData = imu->newXData();
        }
        if (newGyroData != true){
            newGyroData = imu->newGData();
        }
    }
    imu->readAccel();
    imu->readGyro();
    gyroX = imu->calcGyro(imu->gx);
    gyroY = imu->calcGyro(imu->gy);
    gyroZ = imu->calcGyro(imu->gz);
    accelX = imu->calcAccel(imu->ax);
    accelY = imu->calcAccel(imu->ay);
    accelZ = imu->calcAccel(imu->az);
    totalAccel = sqrt(pow(accelX,2) + pow(accelY,2) + pow(accelZ,2));
    totalGyro = sqrt(pow(gyroX,2) + pow(gyroY,2) + pow(gyroZ,2));
}
