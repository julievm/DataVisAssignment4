import plotly.graph_objects as go
import pandas as pd
from geopy.geocoders import Nominatim
import fontawesome as fa

df_crashData = pd.read_csv('crash_new2.csv')
df_crashData["Route"] = df_crashData["Route"].fillna("")
paths = df_crashData["Route"].copy()
paths2 = paths.str.replace('.', ',')
loc = Nominatim(user_agent="Geopy Library")

lat_start = []
lon_start = []

lat_end = []
lon_end = []
casualties = []


for index, row in df_crashData.iterrows():
    casualties.append(row['Casualty Passenger'] + row['Casuality Crew'] + row['Ground'])


for index, row in paths2.items():
    if " - " in row:
        startLoc = row.split(" - ")[0]
        getLoc = loc.geocode(startLoc)

        lat_start.append(getLoc.latitude)
        lon_start.append(getLoc.longitude)

        endLoc = row.split(" - ")[1]
        getLoc2 = loc.geocode(endLoc)

        lat_end.append(getLoc2.latitude)
        lon_end.append(getLoc2.longitude)

        # print(endLoc)

    else:
        lat_start.append(df_crashData['lat_loc'][index])
        lon_start.append(df_crashData['lon_loc'][index])
        lat_end.append(df_crashData['lat_loc'][index])
        lon_end.append(df_crashData['lon_loc'][index])

df_crashData['lat_start'] = lat_start
df_crashData['lon_start'] = lon_start
df_crashData['lat_end'] = lat_end
df_crashData['lon_end'] = lon_end
df_crashData['casualties'] = casualties

df_crashData.to_csv('crash_new3.csv')
# print(paths)