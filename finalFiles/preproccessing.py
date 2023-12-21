import plotly.graph_objects as go
import pandas as pd
from geopy.geocoders import Nominatim
import fontawesome as fa

df_crashData = pd.read_csv('airplaneData.csv')
locations = df_crashData["Location"].copy()
summaries = df_crashData["Summary"].copy()

# replace the '.' back to ',' (was previously done for formatting csv)
locations2 = locations.str.replace('.', ',')
loc = Nominatim(user_agent="Geopy Library")

# add icon based on whether a plane, helicopter or military plane crashed
# icon will be used as marker
icon = []
for index, row in summaries.items():
    if("copter" in row):
        # icon.append(fa.icons['helicopter'])
        icon.append('🚁')
    elif ("military" in row):
        # icon.append(fa.icons['fighter-jet'])
        icon.append('🛦')
    else:
        # icon.append(fa.icons['plane'])
        icon.append('✈')

lat = []
lon = []

for index, row in locations2.items():
    # entering the location name
    getLoc = loc.geocode(row)
    print(row)
    # print(getLoc.address)
    lat.append(getLoc.latitude)
    lon.append(getLoc.longitude)
    print("Latitude = ", getLoc.latitude, "\n")
    print("Longitude = ", getLoc.longitude)



df_crashData["lat_loc"] = lat
df_crashData["lon_loc"] = lon
df_crashData["icon"] = icon

df_crashData.to_csv('crash_new2.csv')
# print(locations2)
print(lat)