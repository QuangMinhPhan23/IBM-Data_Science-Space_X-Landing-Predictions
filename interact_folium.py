import folium
import pandas as pd
# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon
import requests

## Task 1: Mark all launch sites on a map

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
spacex_df=pd.read_csv(URL)

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# Create and add folium.Circle and folium.Marker for each launch site on the site map
# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
for index, row in launch_sites_df.iterrows():
    
    folium.Circle([row['Lat'], row['Long']], radius=1000, color='#d35400', fill=True
                  ).add_child(folium.Popup(row['Launch Site'])).add_to(site_map)
    
    folium.Marker([row['Lat'], row['Long']], icon=DivIcon(icon_size=(20,20),icon_anchor=(0,0)
    ,html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % row['Launch Site'])
                  ).add_to(site_map)
site_map

# # Task 2: Mark the success/failed launches for each site on the map
marker_cluster = MarkerCluster()
# Apply a function to check the value of `class` column
# If class=1, marker_color value will be green
# If class=0, marker_color value will be red
def get_color(row):
    if row['class'] == 1:
        return 'green'
    else:
        return 'red'
# Add a new column `marker_color` to the `launch_sites` dataframe
spacex_df['marker_color'] = spacex_df.apply(lambda row: get_color(row), axis=1)

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
for index, record in spacex_df.iterrows():
    # TODO: Create and add a Marker cluster to the site map
    marker = folium.Marker([record['Lat'], record['Long']], icon=folium.Icon(color='white', icon_color=record['marker_color']))
    marker_cluster.add_child(marker)

site_map

# TASK 3: Calculate the distances between a launch site to its proximities
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Mark down a point on the closest coastline using MousePosition and calculate the distance between
# the coastline point and the launch site.
# find coordinate of the closet coastline
coastline_lat = 28.56342
coastline_lon = -80.57155
# find coordinate of the launch site
launch_site_lat = 28.56342
launch_site_lon = -80.577356
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example
distance_marker = folium.Marker(
    location=[coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
        )
    )

# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
lines = folium.PolyLine(locations = [(launch_site_lat, launch_site_lon), (coastline_lat, coastline_lon)], color = 'blue')
site_map.add_child(lines)

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site
marker = folium.map.Marker(
    location=[coastline_lat, coastline_lon],
    icon=folium.Icon(color='red'),
    )
line = folium.PolyLine(
    locations = [(launch_site_lat, launch_site_lon), (coastline_lat, coastline_lon
    )],
    color = 'red'
    )

site_map.add_child(marker)
site_map.add_child(line)
site_map.add_child(distance_marker)
site_map

