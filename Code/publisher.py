import paho.mqtt.publish as publish
import BMP085 as BMP085
import time
import os
import PCF8591 as ADC
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)
MQTT_SERVER = "localhost"

ds18b20 = ''
DO = 17
adc_value = 0.0048828125

def setup():
        ADC.setup(0x48) # For photoresistor+sound
        GPIO.setup(DO, GPIO.IN) #For photoresistor
        global ds18b20 # For temp sensor
        for i in os.listdir('/sys/bus/w1/devices'):
                if i != 'w1_bus_master1':
                        # Updated to match Raspberry value
                        ds18b20 = '28-031550d37fff'


def read():
        # Read temperature data from file updated by temp sensor
        location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
        tfile = open(location)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature



if __name__ == "__main__":
    setup()
    while True:
        sensor = BMP085.BMP085()                # For barometer
        temp = sensor.read_temperature()
        pressure = sensor.read_pressure()
        temp2 = read()
        sound = ADC.read(0)
        ADC.read(1)
        lux = (250.0/(adc_value*ADC.read(1)))-50
        publish.single("group13_temp01", temp, hostname=MQTT_SERVER)
        publish.single("group13_pressure", pressure, hostname=MQTT_SERVER)
        publish.single("group13_sound", sound, hostname=MQTT_SERVER)
        publish.single("group13_lux", lux, hostname=MQTT_SERVER)
        publish.single("group13_temp02", temp2, hostname=MQTT_SERVER)
        time.sleep(3)