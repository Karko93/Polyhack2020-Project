import json
import folium
import os
def create_map():
    # Reading the initialisation files
    filename_sensors = os.path.join(os.path.split(__file__)[0], 'initialisation_sensor.json')
    filename_actuators = os.path.join(os.path.split(__file__)[0], 'initialisation_actuator.json')

    with open(filename_sensors) as initialisation_file:
        list_of_sensors = json.load(initialisation_file)
    with open(filename_actuators) as initialisation_file:
        list_of_actuators = json.load(initialisation_file)

    m = folium.Map(location=[47.40667, 8.55], zoom_start=13)

    for sensor in list_of_sensors[:20]:
        posx, posy = sensor['position']['x'], sensor['position']['y']
        # print(posx, posy)

        folium.Marker(location=[posx, posy], popup=sensor['serial'], icon=folium.Icon(color='blue', icon='')).add_to(m)

    for actuator in list_of_actuators[:20]:
        posx, posy = actuator['position']['x'], actuator['position']['y']
        # print(posx, posy)

        folium.Marker(location=[posx, posy], popup=actuator['serial'], icon=folium.Icon(color='red', icon='')).add_to(m)

    m.save(os.path.join(os.path.split(__file__)[0], '../websocket/html/map.html'))
