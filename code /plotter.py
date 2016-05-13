import numpy as np
import pandas as pd
from collections import defaultdict,Counter
import gmplot
from datetime import  datetime,timedelta
import datetime
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from scipy.interpolate import interp1d



############################

col = ['pick_ID','drop_ID','year','month','day','hour',
       'passenger_count', 'trip_distance', 'fare_amount', 'surcharge',
       'tip_amount', 'tolls_amount', 'total_amount','tip_rate',
       'surcharge_rate', 'mile_per_dollar', 'current_trip_count','date']

manhattan = [13 ,15,  23,  29,  33,  34,
             35,  44,  45,  61,  67,  81,
             82, 101, 144, 149, 150, 158,
             163, 164, 165, 176, 179, 180,
             190, 191, 192, 193, 194]
brooklyn = [1,  24,  26,  28,  50,
            53 , 57,  58,  59,  60,
            62,  66,  70,  71,  72,
            75,  86,  87,  88,  93,
            94,  95, 112, 113, 121,
            124, 125, 126, 127,128,
            137, 138, 139, 143, 145,
            147, 148, 151, 153, 154,
            155, 156, 157, 159, 160,
            162, 166, 168, 169, 183,
            184]
queens = [2,   3,   4,   5,   8,
          10,  12,  14,  17,  18,
          19,  20,  27,  30,  32,
          38,  39,  40 , 42,  48,
          49,  55,  56,  68,  69,
          74,  76,  77,  78,  79,
          83,  84,  85,  89,  91,
          92,  96,  97,  98, 102,
          103, 108, 109, 110, 114,
          115, 116, 118, 119, 120,
          133, 134, 146, 152, 167,
          181, 182, 188]


data = np.load('data_combined.npy')
data = pd.DataFrame(data,columns = col)
weather = pd.read_csv('q1/weather_mod.csv')
weather['YEARMODA'] = pd.to_datetime(weather['YEARMODA'] )
weather[:,0] = pd.to_datetime(weather[:,0])
weather = weather.values

date_normal =  weather[(weather[:,0] >= datetime(2014,1,1) )*  (np.sum(weather[:,-3:] ,1) ==0)][:,0]
date_rain = weather[(weather[:,0] >= datetime(2014,1,1) )*  (weather[:,3] >=1)][:,0]
date_snow = weather[(weather[:,0] >= datetime(2014,1,1) )*  (weather[:,4] >=10)][:,0]


index = []
for j,i in enumerate(data.values):
    if i[-1] in date_snow:
        index.append('s')
    elif i[-1] in date_rain:
        index.append('r')
    else:
        index.append('n')
    if j%200000 == 0:
        print(j)

date_normal = data.iloc[index =='n']
date_rain = data.iloc[index == 'r']
date_snow = data.iloc[index =='s']

C_man = Counter()
C_Brok = Counter()
C_que = Counter()
for j,i in enumerate(data.values):
    if i[0] in manhattan:
        C_man[int(i[0])] += i[-2]
    elif i[0] in brooklyn:
        C_Brok[int(i[0])] += i[-2]
    else:
        C_que[int(i[0])] +=i[-2]
    if j%1000000 ==0:
        print(j)

dist_man_normal = np.array(map(lambda  x:[x[0],x[1]],C_man.items()))
dist_man_normal[:,1] = dist_man_normal[:,1]/np.sum(dist_man_normal[:,1])
dist_brok_normal = np.array(map(lambda  x:[x[0],x[1]],C_Brok.items()))
dist_brok_normal[:,1] = dist_brok_normal[:,1]/np.sum(dist_brok_normal[:,1])
dist_que_normal = np.array(map(lambda  x:[x[0],x[1]],C_que.items()))
dist_que_normal[:,1] = dist_que_normal[:,1]/np.sum(dist_que_normal[:,1])

pd.DataFrame( dist_que_normal).to_csv(' dist_que_snow.csv',index = False)


top_20_man = Counter()
top_20_brok = Counter()
top_20_que = Counter()
for j,i in enumerate(data.values):
    if i[0] in manhattan:
        top_20_man[str(i[0])+','+str(i[1])] += i[-2]
    elif i[0] in brooklyn:
        top_20_brok[str(i[0])+','+str(i[1])] += i[-2]
    else:
        top_20_que[str(i[0])+','+str(i[1])] += i[-2]
    if j%1000000 ==0:
        print(j)

myList = range(50)
evensList = [x%2 == 0 for x in myList ]


dist_brok_normal = np.array(map(lambda  x:[x[0].split(',')[0],x[0].split(',')[1],
                                           x[1]],np.array(top_20_man.most_common(50))[np.array(evensList)]),dtype=object )
dist_brok_normal = dist_brok_normal[10:,]
dist_brok_normal[:,2] = dist_brok_normal[:,2].astype(float)/np.sum(dist_brok_normal[:,2].astype(float))

pd.DataFrame( dist_brok_normal).to_csv('pointer_man_normal.csv',index = False)

#####
date = data['date'].unique()


col2=['passenger_count', 'trip_distance', 'fare_amount', 'surcharge',
       'tip_amount', 'tolls_amount', 'total_amount', 'current_trip_count','date']

summary_by_day = pd.DataFrame(columns= col2)
summary_by_day['date'] = date
summary_by_day[col2[:-1]] = 0


for i in data.values:
    summary_by_day.loc[summary_by_day['date']==i[-1]][col2[:-1]] +=  list(i[6:-5])+[i[-2]]
    if i % 1000000 == 0:
        print(i)

res = []
for j,i in enumerate(date):
    index = (data['date'] == i)
    temp = data.loc[index].values[:,:-1]
    temp[:,6:-4] = temp[:,6:-4] *temp[:,-1:]
    temp_2 = np.sum(temp,0)
    res.append(list(temp_2[6:-4]) + [temp_2[-1]] + [i])
    if j%10 == 0:
        print(j)
pd.DataFrame(res,columns=col2).to_csv('summary_by_day.csv',index = False)

#########################################################################################

def smooth(x,window_len=11,window='hanning'):

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=numpy.ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=numpy.convolve(w/w.sum(),s,mode='valid')
    return y


data = pd.read_csv('summary_by_day.csv')
data['date'] =pd.to_datetime(data['date'])
weather = pd.read_csv('q1/weather_mod.csv')
weather = weather.iloc[-730:]
data['weather'] = (np.sum(weather[['Snow','Rain','Fog']],1) ==1).values.astype(int)


Mon = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 1,data.values)),columns =col2)
Tue = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 2,data.values)),columns =col2)
Wed = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 3,data.values)),columns =col2)
Thu = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 4,data.values)),columns =col2)
Fri = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 5,data.values)),columns =col2)
Sat = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 6,data.values)),columns =col2)
Sun = pd.DataFrame(np.array(filter(lambda x:x[-1].isoweekday() == 7,data.values)),columns =col2)

index_rain =  ((weather['Rain'] ==1)  ).values
index_snow = ((weather['Snow'] ==1)  ).values
index_fog = ((weather['Fog'] ==1)  ).values
index_normal = ((weather['Rain'] ==0)).values
data_rain= data.loc[index_rain]
data_normal= data.loc[index_normal]

summary = pd.DataFrame()
summary['Mon'] =np.mean((Mon.values[:,:-2]/ Mon.values[:,-2:-1]),0)
summary['Tue'] =np.mean((Tue.values[:,:-2]/ Tue.values[:,-2:-1]),0)
summary['Wed'] =np.mean((Wed.values[:,:-2]/ Wed.values[:,-2:-1]),0)
summary['Thu'] =np.mean((Thu.values[:,:-2]/ Thu.values[:,-2:-1]),0)
summary['Fri'] =np.mean((Fri.values[:,:-2]/ Fri.values[:,-2:-1]),0)
summary['Sat'] =np.mean((Sat.values[:,:-2]/ Sat.values[:,-2:-1]),0)
summary['Sun'] =np.mean((Sun.values[:,:-2]/ Sun.values[:,-2:-1]),0)
summary.loc[7] = np.array([np.mean(Mon['current_trip_count']),np.mean(Tue['current_trip_count']),
                          np.mean(Wed['current_trip_count']),np.mean(Thu['current_trip_count']),
                          np.mean(Fri['current_trip_count']),np.mean(Sat['current_trip_count']),
                          np.mean(Sun['current_trip_count'])])

plt.bar((np.linspace(1,9,9)*7)[1:-1],summary["Mon"][:7])
plt.bar((np.linspace(1,9,9)*7+1)[1:-1],summary["Tue"][:7])
plt.bar((np.linspace(1,9,9)*7+2)[1:-1],summary["Wed"][:7])
plt.bar((np.linspace(1,9,9)*7+3)[1:-1],summary['Thu'][:7])
plt.bar((np.linspace(1,9,9)*7+4)[1:-1],summary['Fri'][:7])
plt.bar((np.linspace(1,9,9)*7+5)[1:-1],summary['Sat'][:7])
plt.bar((np.linspace(1,9,9)*7+6)[1:-1],summary['Sun'][:7])



np.mean(Mon['current_trip_count'])
np.mean(Tue['current_trip_count'])
np.mean(Wed['current_trip_count'])
np.mean(Thu['current_trip_count'])
np.mean(Fri['current_trip_count'])
np.mean(Sat['current_trip_count'])
np.mean(Sun['current_trip_count'])



s1_rain =  data_rain['passenger_count']/data_rain['current_trip_count']
s1_normal =  data_normal['passenger_count']/data_normal['current_trip_count']


import matplotlib.patches as mpatches

layer1 = smooth(data['fare_amount'],10) *np.linspace(1,0.85,739)
layer2 = smooth( data['fare_amount']+data['tip_amount'],10)*np.linspace(1,0.85,739)
layer3 = smooth(data['fare_amount']+data['tip_amount']+data['surcharge']+data['tolls_amount'],10)*np.linspace(1,0.85,739)

fig, ax1 =plt.subplots()
ax1.fill_between(range(len(layer3)), layer2, layer3,color='grey')
ax1.fill_between(range(len(layer3)), layer1, layer2,color='lightskyblue')
ax1.fill_between(range(len(layer3)), layer1, 0,color='linen')
ax1.set_ylim([3000000, 8000000])
ax1.set_ylabel('Total revenue')
patch_1 = mpatches.Patch(color='grey', label='The surcharge + tolls')
patch_2 = mpatches.Patch(color='lightskyblue', label='The tips')
patch_3 = mpatches.Patch(color='linen', label='The fare')
plt.legend(handles=[patch_1,patch_2,patch_3],loc =1)
plt.title('Total Revenue by Day')
plt.savefig('total_revenue.png')

import seaborn as sns
data['weekday'] = map(lambda x:x.isoweekday(),data['date'])

temp = np.max(data['trip_distance'])
mean = np.mean(data['trip_distance'])
std = np.std(data['trip_distance'])
for i,j in enumerate(data['trip_distance']):
    if j> mean +2*std:
        data['trip_distance'].loc[i] = mean




sns.violinplot(x="weekday", y=data["trip_distance"]/data["current_trip_count"], hue="weather",
               data=data,inner="box")


ax = sns.violinplot(x="weekday", y=data["trip_distance"], hue="weather",
               data=data, palette="Set2",inner="quartile")
ax = sns.violinplot(x="weekday", y="passenger_count", data=data)

###########################
data = pd.read_csv("yellow_tripdata_2015-01.csv")
data['tpep_pickup_datetime'] = pd.to_datetime(data['tpep_pickup_datetime'])

temp_fri = filter(lambda x:x[1].day == 10,data)
temp_sat = filter(lambda x:x[1].day == 11,data)
temp_sun= filter(lambda x:x[1].day == 12,data)

temp_27 = filter(lambda x:x[1].day == 27,data)


s1 = np.array(filter(lambda x: (x[1].hour ==23) and (x[5] != x[9]),temp_sat))[:,[5,6,9,10]]
s2 = np.array(filter(lambda x: (x[1].hour in [5,6,7,8,9,10]) and (x[5] != x[9]),temp_27))[:,[5,6,9,10]]

s = np.vstack((s1,s2))

sample = pd.DataFrame(s2,columns= ['x1','x2','y1','y2'] )
sample.to_csv('sample_day.csv',index = False)


