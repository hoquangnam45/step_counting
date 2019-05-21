import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import sys 

THRESH_STEP = 0.01
COUNT_REQUIRED = 30 
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
    data = pd.read_csv('./data/recorded_data30.csv', sep='\s*;\s*', engine='python')
    accelX=np.array(data['accelX'])
    accelY=np.array(data['accelY'])
    accelZ=np.array(data['accelZ'])
    totalAccel=np.array(data['totalAccel'])

    gyroX=np.array(data['gyroX'])
    gyroY=np.array(data['gyroY'])
    gyroZ=np.array(data['gyroZ'])
    totalGyro=np.array(data['totalGyro'])
    
    # countRequired = int(sys.argv[1])
    # print("hihi "+ str(countPeak(0.7340105393786573, totalAccel)))
    threshUpperHigh = findThreshBase(totalAccel.mean() + totalAccel.std() / 2, COUNT_REQUIRED, totalAccel, direction='up', searching='lower')
    threshUpperLow = findThreshBase(totalAccel.mean() + totalAccel.std() / 2, COUNT_REQUIRED, totalAccel, direction='down', searching='higher')
    threshUpper = (threshUpperLow + threshUpperHigh) / 2
    threshLowerHigh = findThreshBase(totalAccel.mean() - totalAccel.std() / 4, COUNT_REQUIRED, totalAccel, direction='up', searching='higher')
    threshLowerLow = findThreshBase(totalAccel.mean() - totalAccel.std() / 4, COUNT_REQUIRED, totalAccel, direction='down', searching='lower')
    threshLower = threshLowerHigh
    # threshUpper = findThresh(28, totalAccel, direction='down', searching='equal'); # 1.6519: 29; 1.63195: 10;
    # threshLower = findThreshBase(threshUpper, 10, totalAccel, direction='down', searching='higher'); # 0.9058: 29; 0.9108: 10; 
    #print(totalAccel.mean() - totalAccel.std());
    #print(totalAccel.mean() + totalAccel.std());
    print(threshUpper);
    print(threshLower);
    # print("totalAccel: " + str(totalAccel.mean()))
    # print(countPeak(totalAccel.mean() + totalAccel.std(), totalAccel))

    # UPPER_THRESH = 1.2153570400735303
    # LOWER_THRESH = 1.136203823714361
    UPPER_THRESH = 1.3375668690185836
    LOWER_THRESH = 1.105345450537175
    # UPPER_THRESH = 53.689616039445696
    #LOWER_THRESH = 34.459430592522054
    plt.plot(totalAccel, marker='', color='red', linewidth=0.5, label='totalAccel')
    plt.axhline(y=threshUpper, color='g', linewidth=1, label='threshUpper')
    plt.axhline(y=threshLower, color='g', linewidth=1, label='threshLower')
    #plt.axhline(y=UPPER_THRESH, color='y', linewidth=1)
    #plt.axhline(y=LOWER_THRESH, color='y', linewidth=1)
    plt.axhline(y=totalAccel.mean(), color='black', linewidth=0.5, linestyle="--", label='mean')
    plt.axhline(y=totalAccel.mean() + totalAccel.std() / 2, color='black', linewidth=0.5, linestyle="--", label='Mean + std/2')
    plt.axhline(y=totalAccel.mean() - totalAccel.std() / 2, color='black', linewidth=0.5, linestyle="-.", label='Mean - std/2')
    plt.legend()
    plt.show()

    count = 0;
    setFlag = 0;
    for accel in totalAccel:
        if (accel < LOWER_THRESH):
            setFlag = 1
        elif (accel > UPPER_THRESH and setFlag == 1):
            setFlag = 0
            count += 1
    print(count)

if __name__ == "__main__":
    main()

# Accel based
#####################
# 30
# 1.4763220364793241 
# 1.136203823714361 

#1.3713220364793242
#1.136203823714361

###################
# 20 
# 1.3236816428270841 
# 1.0931527614741585 

#1.248681642827084
#1.0931527614741585

########################
# 15
# 1.3257048287837687 
# 1.1277099856081156  

#1.2557048287837687
#1.1277099856081156

########################
# 10
# 1.3220835463117557 
# 1.0850492591021863 

#1.2420835463117557
#1.0850492591021863

#########################
# 30b
# 1.2153570400735303
# 1.093841311595888

#1.1803570400735304
#1.093841311595888

##########################
# 20b
# 1.4008835552344938 
# 1.11571787150556 

#1.2558835552344938
#1.11571787150556

###############################
# 10b
# 1.340664144935857 
# 1.0859636833460253 

#1.2656641449358568
#1.0859636833460253




# assemble
# 1.2978613434595392
# 1.1051249079511032

#1.272861343459539
#1.1051249079511032


#avg
# 1.3375668690185836
# 1.105345450537175

#1.2606701174477086
#1.105345450537175

# Gyro based
