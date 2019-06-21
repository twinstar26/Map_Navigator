import pandas as pd
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import math
tree = et.parse('map.osm')
root = tree.getroot()
import sklearn.neighbors as N
####################################################################

def euclidian_distance_heuristic(xf,yf,xi,yi):
        return(math.sqrt(math.pow((yf-yi),2)+math.pow((xf-xi),2)))

def Astar(xf,yf,xi,yi,latitude,longitude,data):
        iteration = 0
        flag = True
        visited = pd.DataFrame(columns=['node','lat','lon', 'euc_dist'])
        visited_lat = list()
        visited_lon = list()
        for i in range(1000):
                priority_queue = {}
                if(flag):
                        next5node = nearest_neighbours(data,xi,yi)
                        next5node = next5node[0]
                        for node in next5node:
                                priority_queue.clear()
                                #info = []
                                visited_lat.append(latitude[node])
                                visited_lon.append(longitude[node])
                                #info.append(float(latitude[node]))
                                #info.append(float(longitude[node]))
                                #info.append(float(euclidian_distance_heuristic(xf,yf,latitude[node],longitude[node])))
                                latitude.pop(node)
                                longitude.pop(node)
                                data.pop(node)
                                priority_queue.update({'node': node, 'lat': latitude[node], 'lon': longitude[node], 'euc_dist': euclidian_distance_heuristic(xf,yf,latitude[node],longitude[node])})#({float(euclidian_distance_heuristic(xf,yf,latitude[node],longitude[node])): info})
                                visited = visited.append(priority_queue,ignore_index=True)
                        flag = False
                else:
                        visited.sort_values('euc_dist', inplace=True)
                        node = int(visited['node'][0])
                        visited = visited.drop(0)
                        visited.reset_index(drop=True, inplace=True)
                        #node = int(list(node['node']))
                        #print('index0 is  :' + str(index[0]))
                        #print('node:')
                        #print(node)
                        #print(latitude[node])
                        #print(longitude[node])
                        print('req for '+str(node) + ' avail ' + str(len(latitude)))
                        next5node = nearest_neighbours(data,data[node][0],data[node][1])#(data,float(visited['lat'][node]),float(visited['lon'][node]))#(data,latitude[node],longitude[node])
                        next5node = next5node[0]
                        #print('net5 is: '+  str(next5node))
                        
                        for node in next5node:
                                priority_queue.clear()
                                #info = []
                                visited_lat.append(latitude[node])
                                visited_lon.append(longitude[node])                               
                                #info.append(float(latitude[node]))
                                #info.append(float(longitude[node]))
                                #info.append(float(euclidian_distance_heuristic(xf,yf,latitude[node],longitude[node])))
                                latitude.pop(node)
                                longitude.pop(node)
                                data.pop(node)
                                #print('info is : ' + str(info))
                                priority_queue.update({'node': node, 'lat': latitude[node], 'lon': longitude[node], 'euc_dist': euclidian_distance_heuristic(xf,yf,latitude[node],longitude[node])})#({float(euclidian_distance_heuristic(xf,yf,latitude[node],longitude[node])): info})
                                visited = visited.append(priority_queue,ignore_index=True)
                                iteration+=1
                                print(iteration)
        visited.plot(kind="scatter", x="lon", y="lat", alpha=0.2)
        plt.show()

def nearest_neighbours(data,x,y,n_neighbors=5):
        model = N.NearestNeighbors(n_neighbors, n_jobs=-1, p=2)
        model.fit(data)
        return(model.kneighbors([[x,y]], n_neighbors, return_distance=False))

########################################################################

a = open(file='a.txt',mode='r')

#xi,yi = input('ENTER STARTING CO-ORDINATES: ')
#xf,yf = input('ENTER FINAL CO-ORDINATES: ')
str1 = a.read()
l =  str1.split('\n')
xi = float(l[0])
yi = float(l[1])
xf = float(l[2])
yf = float(l[3])
file = open(file='map.osm',mode='r')
fr = file.read()

ref = 0
lat = []
lon = []
latitude = []
latitude.clear()
longitude = []
longitude.clear()
data = []
data.clear()
for child in root:
    if(child.tag == 'way'):
        child_dict = child.iter()
        l = []
        l.clear()
        for ref in child_dict:
                dict = ref.attrib
                for key in dict:
                        if(key == 'ref'):
                                l.append(dict['ref'])
                        if(key == 'k' ):
                                if(dict['k']=='highway'):
                                        for ll in l:
                                                search = fr.find(ll)
                                                lat = fr.find(r'lat="',search)
                                                lon = fr.find(r'lon="',search)
                                                latitude.append(float(fr[lat+5:lat+14]))
                                                longitude.append(float(fr[lon+5:lon+14]))
                                                data.append([latitude[-1], longitude[-1]])

df = pd.DataFrame({'lat': latitude, 'lon': longitude})

# need to sort values so as tpo obtain increasing curve
#df.sort_values('edorigin',ascending=True,inplace=True)
#ans = nearest_neighbours(data,0.0450000, 51.513000)
#print(ans)
#for a in ans:
#        for aa in a:
#                print(latitude[aa], longitude[aa])
#                print(euclidian_distance_heuristic(latitude[aa], longitude[aa], 51.535, 0.0))
#df.plot(kind="scatter", x="lon", y="lat", alpha=0.2)
#df.hist(bins=100)
#plt.plot(df['lat'],df['lon'])
#plt.show()


Astar(xf,yf,xi,yi,latitude,longitude,data)















'''
  lat.append(float(child_dict['lat']))
                lon.append(float(child_dict['lon']))

#lat.sort()
#lon.sort()

for tag in (child.iter('tag')):
    file.write(str(tag.attrib) + '  ')


df = pd.DataFrame({'lat': lat, 'lon': lon})
print(df.head())

#df.plot.scatter(x='lat',y='lon')
#plt.show()

#plt.scatter(lat[:1000], lon[:1000])
#plt.plot(lat[:5000], lon[:5000])
df.plot(kind="scatter", x="lon", y="lat", alpha=0.2)
plt.show()
'''