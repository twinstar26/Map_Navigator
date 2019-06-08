import pandas as pd
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import geopandas
tree = et.parse('map.osm')
root = tree.getroot()

a = open(file='a.txt',mode='w')
#result = open(file='r.txt',mode='w')
file = open(file='map.osm',mode='r')
fr = file.read()

ref = 0
lat = []
lon = []
latitude = []
latitude.clear()
longitude = []
longitude.clear()
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


df = pd.DataFrame({'lat': latitude, 'lon': longitude})
print(df.head())
df.plot(kind="scatter", x="lon", y="lat", alpha=0.2)
plt.show()





























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