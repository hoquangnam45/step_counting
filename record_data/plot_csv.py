import matplotlib.pyplot as plt
import csv  
import pandas as pd
import numpy as np
import sys 

def main():
    data = pd.read_csv('./data/recorded_data20.csv', sep='\s*;\s*', engine='python')
    #print(data)
    accelX = np.array(data['accelX'])
    accelY = np.array(data['accelY'])
    accelZ = np.array(data['accelZ'])
    totalAccel = np.array(data['totalAccel'])
    gyroX = np.array(data['gyroX'])
    gyroY = np.array(data['gyroY'])
    gyroZ = np.array(data['gyroZ'])
    totalGyro = np.array(data['totalGyro'])

    # fig = plt.figure(figsize=(1,8))
    # plt.plot(accelX)
    plt.plot(accelX, marker='', color='blue', linewidth=0.5, label='accelX')
    plt.plot(accelY, marker='', color='green', linewidth=0.5, label='accelY')
    plt.plot(accelZ, marker='', color='black', linewidth=0.5, label='accelZ')
    plt.plot(totalAccel, marker='', color='red', linewidth=0.5, label='totalAccel')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main();
