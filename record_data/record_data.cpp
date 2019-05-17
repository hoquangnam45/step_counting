#include <iostream>
#include <fstream>
#include <cmath>
#include <iomanip>

#include "../Libs/Gyro/SFE_LSM9DS0.h"
#include "../Libs/OLED/oled/Edison_OLED.h"
#include "../Libs/OLED/gpio/gpio.h"

#define PATH_CSV "./data/recorded_data.csv"

using namespace std;

LSM9DS0 *imu;
// Define an edOLED object:
edOLED oled;
ofstream csvwriter;

void init();
void readData();
void writeDataToCsv();

float gyroX, gyroY, gyroZ, totalGyro,
      accelX, accelY, accelZ, totalAccel;

int main(){
    init();
    while (1){
        readData();
        writeDataToCsv();
    }
    return 0;
}

void init(){
    imu = new LSM9DS0(0x6B, 0x1D);
    uint16_t imuResult = imu->begin();
    cout<<hex<<"Chip ID: 0x"<<imuResult<<dec<<" (should be 0x49d4)"<<endl;
    csvwriter.open(PATH_CSV);
    if (!csvwriter.is_open()) cout << "Không mở được file" << endl;
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
}

void writeDataToCsv(){
    static bool initFlag = 0;
    if (!initFlag){
        // Ghi header
        csvwriter \
        << left << setw(12) << "accelX" << " ; " \
        << left << setw(12) << "accelY" << " ; " \
        << left << setw(12) << "accelZ" << " ; " \
        << left << setw(12) << "totalAccel" << " ; " \
        << left << setw(12) << "gyroX" << " ; " \
        << left << setw(12) << "gyroY" << " ; " \
        << left << setw(12) << "gyroZ" << " ; " \
        << left << setw(12) << "totalGyro" << endl;
        initFlag = 1;
    }
    totalAccel = sqrt(pow(accelX, 2) + pow(accelY, 2) + pow(accelZ, 2));
    totalGyro = sqrt(pow(gyroX , 2) + pow(accelY, 2) + pow(gyroZ, 2));
    csvwriter \
    << fixed << setprecision(5) \
    << left << setw(12) << accelX << " ; " \
    << left << setw(12) << accelY << " ; " \
    << left << setw(12) << accelZ << " ; " \
    << left << setw(12) << totalAccel << " ; " \
    << left << setw(12) << gyroX << " ; " \
    << left << setw(12) << gyroY << " ; " \
    << left << setw(12) << gyroZ << " ; " \
    << left << setw(12) << totalGyro << endl;
}