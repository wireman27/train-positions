import pandas as pd
import json
df = pd.read_csv('C:/Coursera/mumbai_wr/ready_for_plot_all.csv')
geojson = {
    'type': 'FeatureCollection',
    'features': []
    }
for row in range(0,len(df.index.tolist())):
    geojson['features'].append({
        'type': 'Feature',
	'geometry': {
            'type': 'Point',
	    'coordinates': [float(df.iloc[row,5]), float(df.iloc[row,6])]
            },
	'properties':{
            'service':df.iloc[row,3],
            'time': float(df.iloc[row,1]),
            'speed': str(df.iloc[row,7])
            }
        })
    
with open('C:/Coursera/mumbai_wr/all.geojson', 'w') as f:
    f.write(json.dumps(geojson))

ls = pd.read_csv('C:/Coursera/mumbai_wr/station_metadata.csv')


geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "geometry": {
            "type": "LineString"
        },
        "properties":{}
    }]
}


coordinates = list()

for row in range(0,len(ls.index.tolist())):
    coordinates.append([float(ls.iloc[row,3]),float(ls.iloc[row,2])])
    geojson['features'].append({
        "type":"Feature",
        "geometry":{
            "type":"Point",
            "coordinates":[float(ls.iloc[row,3]),float(ls.iloc[row,2])]
            },
        "properties":{
            "station":ls.iloc[row,0]
            }
        }
    )

geojson['features'][0]['geometry']['coordinates']=coordinates


with open('C:/Coursera/mumbai_wr/linestring_all.geojson', 'w') as f:
    f.write(json.dumps(geojson))







