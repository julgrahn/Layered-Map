import folium
import pandas

dataVolcanoes = pandas.read_csv("Volcanoes.txt")
lat = list(dataVolcanoes["LAT"])
lon = list(dataVolcanoes["LON"])
elevation = list(dataVolcanoes["ELEV"])
name = list(dataVolcanoes["NAME"])

html = """
<p style = "font-family:verdana">
Volcano name:<br>
<a href = "https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m</p>
"""

def color_changer(volElevation):
    if volElevation < 1500:
        return 'green'
    elif 1500 <= volElevation <= 2500:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location = [59.19124, 18.03528], zoom_start = 10, tiles = "Stamen Terrain")

featureGroup = folium.FeatureGroup(name = "My Map")

for lt, ln, el, name in zip(lat, lon, elevation, name):
    iframe = folium.IFrame(html = html % (name, name, el), width = 200, height = 100)
    featureGroup.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(iframe), icon = folium.Icon(color = color_changer(el))))


map.add_child(featureGroup)
map.save("Map_html_popups.html")