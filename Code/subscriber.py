from pydoc import cli
import paho.mqtt.client as mqtt #import library
import time

def updatefile(array):
    with open("./sensor_data.txt", "w")as file:

        for i in array:
            file.write(" ".join(i) + " \n")
        
 
MQTT_SERVER = "10.6.1.9" #specify the broker address, it can be IP of raspberry pi or simply localhost
MQTT_PATH = "group13_temp01"
MQTT_PATH2 = "group13_pressure"
MQTT_PATH3 = "group13_sound"
MQTT_PATH4 = "group13_lux"  #this is the name of topic, like temp
MQTT_PATH5 = "group13_temp02"

sensors = [["-1", "-1", "-1", "-1", "-1"], ["-1", "-1", "-1", "-1", "-1"], ["-1", "-1", "-1", "-1", "-1"], ["-1", "-1", "-1", "-1", "-1"], ["-1", "-1", "-1", "-1", "-1"]]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)
    client.subscribe(MQTT_PATH2)
    client.subscribe(MQTT_PATH3)
    client.subscribe(MQTT_PATH4)
    client.subscribe(MQTT_PATH5)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "group13_temp01":
        sensors[0].insert(0, str(msg.payload.decode("UTF-8")))
    elif msg.topic == "group13_pressure":
        sensors[3].insert(0, str(msg.payload.decode("UTF-8")))
    elif msg.topic == "group13_sound":
        sensors[1].insert(0, str(msg.payload.decode("UTF-8")))
    elif msg.topic == "group13_lux":
        sensors[2].insert(0, str(msg.payload.decode("UTF-8")))
    elif msg.topic == "group13_temp02":
        sensors[4].insert(0, str(msg.payload.decode("UTF-8")))
    
    for i in sensors:
        if len(i) == 6:
            i.pop(5)
    
    # more callbacks, etc
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)


#client.loop_forever()# use this line if you don't want to write any further code. It blocks the code forever to check for data

while True:
    client.loop_start() #use this line if you want to write any more code here
    updatefile(sensors)
    time.sleep(5)