import matplotlib.pyplot as plt
import csv  
import pandas as pd
import numpy as np
import sys 

def main():
    data = pd.read_csv('./data/recorded_data20b.csv', sep='\s*;\s*', engine='python')
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
    # plt.plot(gyroX)
    # plt.plot(accelX, marker='', color='blue', linewidth=0.5, label='x')
    # plt.plot(accelY, marker='', color='green', linewidth=0.5, label='y')
    # plt.plot(accelZ, marker='', color='black', linewidth=0.5, label='z')
    plt.plot(totalAccel, marker='', color='red', linewidth=0.5, label='total')
    plt.show()

if __name__ == "__main__":
    main();
