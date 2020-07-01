import folium
import pandas

dataVolcanoes = pandas.read_csv("Volcanoes.txt")
lat = list(dataVolcanoes["LAT"])
lon = list(dataVolcanoes["LON"])
elevation = list(dataVolcanoes["ELEV"])
name = list(dataVolcanoes["NAME"])

dataBars = pandas.read_csv("Bars.txt")
latB = list(dataBars["LAT"])
lonB = list(dataBars["LON"])
barName = list(dataBars["BARNAME"])
barNumber = list(dataBars["NUMBER"])

html = """
<p style = "font-family:verdana">
Volcano name:<br>
<a href = "https://www.google.com/search?q=%%22%s%%22%%20volcano" target="_blank">%s</a><br>
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

featureGroupVolcano = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, el, name in zip(lat, lon, elevation, name):
    iframe = folium.IFrame(html = html % (name, name, el), width = 200, height = 100)

    featureGroupVolcano.add_child(folium.CircleMarker(location = [lt, ln], radius = 6, 
    popup = folium.Popup(iframe), fill = True, fill_color = color_changer(el), color = 'grey', fill_opacity = 0.7))

featureGroupPopulation = folium.FeatureGroup(name = "Population")

featureGroupPopulation.add_child(folium.GeoJson(data = open("world.json", 'r', encoding = 'utf-8-sig').read(), 
style_function = lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x ['properties']['POP2005'] < 25000000 else 'red'}))

htmlBar = """
<p style = "font-family:verdana">
Bar name:<br>
<a href = "https://www.google.com/search?q=%s" target="_blank">%s</a><br>
Ranking: %s </p>
"""

featureGroupBars = folium.FeatureGroup(name = "Bars in Stockholm")

for nr, ltB, lnB, nameB in zip(barNumber, latB, lonB, barName):
    iframeBar = folium.IFrame(html = htmlBar % (nameB, nameB, nr), width = 150, height = 100)

    featureGroupBars.add_child(folium.Marker(location = [ltB, lnB], popup = folium.Popup(iframeBar), color = "yellow"))

map.add_child(featureGroupVolcano)
map.add_child(featureGroupPopulation)
map.add_child(featureGroupBars)
map.add_child(folium.LayerControl())
map.save("Map_html_popups.html")