import numpy as np
import pandas as pd
from collections import defaultdict


def to_weather(data):
    if data == '0':
        return np.zeros(6,dtype=int)
    data = str(data)
    if len(data) <6:
        diff = 6-len(data)
        data = '0'*diff +data
    res = np.zeros(6,dtype=int)
    for i in range(6):
        res[i] = (data[i] == '1')
    return res





####################
## Modify weather ##
####################

data_weather = pd.read_csv('weather.csv')
features = ['YEARMODA','TEMP','VISIB','PRCP','SNDP','FRSHTT']
data_weather = data_weather[features]
data_weather['YEARMODA'] = pd.to_datetime(data_weather['YEARMODA'],format='%Y%m%d')
data_weather['PRCP'] = map(lambda x:float(x[:4]),data_weather['PRCP'].values)

temp = data_weather['VISIB'].values.copy()
np.place(temp,temp == 999.9,0)
np.place(temp,temp==0,np.mean(temp))
data_weather['VISIB'] = temp

temp = data_weather['SNDP'].values.copy()
np.place(temp,temp == 999.9,0)
data_weather['SNDP'] = temp

data_weather = data_weather.join(pd.DataFrame(np.array(map(lambda x:to_weather(x),data_weather['FRSHTT'].values))
                                                                            ,columns = ['Fog','Rain','Snow','Hail','Thunder','Tornado'])).drop('FRSHTT',1)


##############################
## Modify uber 4-9          ##
##############################


#data_uber = pd.read_csv('uber-apr-sep.csv',dtype = {'Date/Time':pd.Timestamp,'Lat':np.float,'Lon':np.float},skiprows = [564517,1393793,2189915,2853760,3506196])
data_plot = (data_uber['Lat'].values,data_uber['Lon'].values)
res = pd.Timestamp(data_uber['Date/Time'])
data_uber['Date/Time'] = res
#data_uber.to_csv('uber_mod.csv')

d1 = pd.read_csv('uber-raw-data-apr14.csv')
print(1)
d2 = pd.read_csv('uber-raw-data-may14.csv')
print(2)
d3 = pd.read_csv('uber-raw-data-jun14.csv')
print(3)
d4 = pd.read_csv('uber-raw-data-jul14.csv')
print(4)
d5 = pd.read_csv('uber-raw-data-aug14.csv')
print(5)
d6  =pd.read_csv('uber-raw-data-sep14.csv')
print(6)

#############
#join uber with weather

new = np.zeros((data_uber.shape[0],data_weather.shape[1]))
data_uber = np.hstack((data_uber,new))


pointer_1 = data_uber[0,0]
pointer_2 = data_weather[0,0]
j = 0
i = 0
start_time = time.time()



while 1:
    if i >= data_uber.shape[0]:
        break
    if pointer_1.date() != pointer_2.date():
        pointer_2 = data_weather[j,0]
        j+=1
    else:
        data_uber[i,4:] = data_weather[j-1]
        pointer_1 = data_uber[i,0]
        i+=1
    if (i%10000) == 0:
        print(i%10000)

time.time() - start_time

#######################

data = pd.read_csv('uber-raw-data-janjune-15.csv')
zone = pd.read_csv('Zone_location.csv')

data['Pickup_date'] = pd.to_datetime(data['Pickup_date'])
data = data.values
data = data[data[:, 1].argsort()]
data = data[:,1:]
new = np.zeros((data.shape[0],data_weather.shape[1]))
data = np.hstack((data,new))


pointer_1 = data_uber[0,0]
pointer_2 = data_weather[0,0]
j = 0
i = 0
start_time = time.time()



while 1:
    data_uber[i][3:5] = zone.loc[data_uber[i][2] -1][5:7].values
    if i >= data_uber.shape[0]:
        break
    if pointer_1.date() != pointer_2.date():
        pointer_2 = data_weather[j,0]
        j+=1
    else:
        data_uber[i,5:] = data_weather[j-1]
        pointer_1 = data_uber[i,0]
        i+=1
    if (i%10000) == 0:
        print(i)

time.time() - start_time


for i in range(data_uber.shape[0]):
    data_uber[i,3] = zone.loc[data_uber[i][2] -1][4]
    if (i%100000) == 0:
        print(i)


label = np.array(['Time','Latitude','longitude','Base','Temp','VISIB','PRCP','SNDP','Fog','Rain','Snow'])



######################
mymap = gmplot.GoogleMapPlotter(40.715,-73.9549, 12)
mymap.heatmap(data_uber[:,1][200000:500000], data_uber[:,2][200000:5000000],radius=20)
mymap.draw('mymap.html')


#
mymap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
    # mymap = GoogleMapPlotter.from_geocode("Stanford University")

#mymap.grid(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)
#mymap.marker(37.427, -122.145, "yellow")
#mymap.marker(37.428, -122.146, "cornflowerblue")
#mymap.marker(37.429, -122.144, "k")
lat, lng = mymap.geocode("Stanford University")
#mymap.marker(lat, lng, "red")
#mymap.circle(37.429, -122.146, 100, "red", ew=10,radius = 1)
path = [(37.429, 37.428, 37.427, 37.427, 37.427),
         (-122.145, -122.145, -122.145, -122.146, -122.146)]
path2 = [[i+.01 for i in path[0]], [i+.02 for i in path[1]]]
path3 = [(37.433302 , 37.431257 , 37.427644 , 37.430303), (-122.14488, -122.133121, -122.137799, -122.148743)]
path4 = [(37.423074, 37.422700, 37.422410, 37.422188, 37.422274, 37.422495, 37.422962, 37.423552, 37.424387, 37.425920, 37.425937),
     (-122.150288, -122.149794, -122.148936, -122.148142, -122.146747, -122.14561, -122.144773, -122.143936, -122.142992, -122.147863, -122.145953)]
mymap.plot(path[0], path[1], "black", edge_width=1)
mymap.plot(path2[0], path2[1], "red")
#mymap.polygon(path3[0], path3[1], edge_color="cyan", edge_width=5, face_color="blue", face_alpha=0.1)
mymap.heatmap(path4[0][:2], path4[1][:2], threshold=2, radius=40)
mymap.heatmap(path3[0], path3[1], threshold=10, radius=40, dissipating=False)
mymap.scatter(path4[0], path4[1], c='r', marker=True)
mymap.scatter(path4[0], path4[1], s=90, marker=False, alpha=0.1)

scatter_path = ([37.424435, 37.424417, 37.424417, 37.424554, 37.424775, 37.425099, 37.425235, 37.425082, 37.424656, 37.423957, 37.422952, 37.421759, 37.420447, 37.419135, 37.417822, 37.417209],
                [-122.142048, -122.141275, -122.140503, -122.139688, -122.138872, -122.138078, -122.137241, -122.136405, -122.135568, -122.134731, -122.133894, -122.133057, -122.13222, -122.131383, -122.130557, -122.129999])
mymap.scatter(scatter_path[0], scatter_path[1], c='r', marker=True)

mymap.draw('mymap.html')