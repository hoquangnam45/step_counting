import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import sys 

THRESH_STEP = 0.01

def countPeak(thresh, array):
    flag = 0
    count = 0
    for i in array:
        if (i < thresh):
            flag = 1
        elif (i >= thresh and flag == 1):
            flag = 0
            count += 1
    return count


def findThresh(countRequired, array, direction='up', searching='equal'):
    if (direction == 'up'): 
        thresh_start = array.min()
    elif (direction == 'down'): 
        thresh_start = array.max()
    return findThreshBase(thresh_start, countRequired, array, direction, searching)

def findThreshBase(threshStart, countRequired, array, direction='up', searching='equal'):
    if (direction == 'up'): 
        thresh_limit = array.max()
        sign = 1
    elif (direction == 'down'): 
        thresh_limit = array.min()
        sign = -1
    thresh = threshStart
    count = countPeak(thresh, array)

    if searching == 'equal':
        while (count != countRequired):
            if ((direction == 'up' and thresh > thresh_limit) or (direction == 'down' and thresh < thresh_limit)):
                return -1
            thresh += sign * THRESH_STEP
            count = countPeak(thresh, array)
        print("exact:" + str(count))
        return thresh
    elif searching == 'lower':
        while (count >= countRequired):
            if ((direction == 'up' and thresh > thresh_limit) or (direction == 'down' and thresh < thresh_limit)):
                return -1
            thresh += sign * THRESH_STEP
            count = countPeak(thresh, array)
        print("lower:" + str(count))
        return thresh
    elif searching == 'higher':
        while (count <= countRequired):
            if ((direction == 'up' and thresh > thresh_limit) or (direction == 'down' and thresh < thresh_limit)):
                return -1
            thresh += sign * THRESH_STEP
            count = countPeak(thresh, array)
        print("higher:" + str(count))
        return thresh

def main():
    data = pd.read_csv('./data/recorded_data15.csv', sep='\s*;\s*', engine='python')
    accelX=np.array(data['accelX'])
    accelY=np.array(data['accelY'])
    accelZ=np.array(data['accelZ'])
    totalAccel=np.array(data['totalAccel'])

    gyroX=np.array(data['gyroX'])
    gyroY=np.array(data['gyroY'])
    gyroZ=np.array(data['gyroZ'])
    totalGyro=np.array(data['totalGyro'])
    
    # countRequired = int(sys.argv[1])
    #print("hihi "+ str(countPeak(0.7340105393786573, totalAccel)))
    threshUpperHigh = findThreshBase(totalAccel.mean() + totalAccel.std() / 2, 10, totalAccel, direction='up', searching='lower')
    threshUpperLow = findThreshBase(totalAccel.mean() + totalAccel.std() / 2, 10, totalAccel, direction='down', searching='higher')
    threshUpper = (threshUpperHigh + threshUpperLow) / 2
    threshLowerHigh = findThreshBase(totalAccel.mean() - totalAccel.std() / 4, 10, totalAccel, direction='up', searching='higher')
    threshLowerLow = findThreshBase(totalAccel.mean() - totalAccel.std() / 4, 10, totalAccel, direction='down', searching='lower')
    threshLower = threshLowerHigh
    # threshUpper = findThresh(28, totalAccel, direction='down', searching='equal'); # 1.6519: 29; 1.63195: 10;
    # threshLower = findThreshBase(threshUpper, 10, totalAccel, direction='down', searching='higher'); # 0.9058: 29; 0.9108: 10; 
    print(totalAccel.mean() - totalAccel.std());
    print(totalAccel.mean() + totalAccel.std());
    print(threshUpper);
    print(threshLower);
    # print("totalAccel: " + str(totalAccel.mean()))
    #print(countPeak(totalAccel.mean() + totalAccel.std(), totalAccel))
    plt.plot(totalAccel, marker='', color='red', linewidth=0.5, label='total')
    plt.axhline(y=threshUpper, color='g', linewidth=1)
    plt.axhline(y=threshLower, color='g', linewidth=1)
    plt.axhline(y=totalAccel.mean(), color='black', linewidth=0.5, linestyle="--")
    plt.axhline(y=totalAccel.mean() + totalAccel.std(), color='black', linewidth=0.5, linestyle="--")
    plt.axhline(y=totalAccel.mean() - totalAccel.std(), color='black', linewidth=0.5, linestyle="-.")
    plt.show()

    count = 0;
    setFlag = 0;
    for accel in totalAccel:
        if (accel < 1.1277099856081106):
            setFlag = 1
        elif (accel > 1.3220835463117557 and setFlag == 1):
            setFlag = 0
            count += 1
    print(count)
if __name__ == "__main__":
    main()

# 30
# 1.4763210364793241
# 1.136103823714361

# 20
# 1.3236816428270841
# 1.0931027614741085

# 15
# 1.3257048287837687
# 1.1277099856081106

# 10
# 1.3220835463117557
# 1.0850492591021863