################################################
#                                              #
#      Python script to read sensor data       #
#               SRSA project                   #
#                2021-2022                     #
#                                              #
################################################
import Adafruit_BMP.BMP085 as BMP085 
import time
import os
import PCF8591 as ADC
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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
			ds18b20 = '28-031590a0a2ff'
            
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

# Collect data from the sensors
def loop():
	while True:
		sensor = BMP085.BMP085()		# For barometer
		temp = sensor.read_temperature()	# Read temperature to var temp from barometer in C
		pressure = sensor.read_pressure()	# Read pressure to var pressure from barometer in Pa
		#temp = read()                      	# Read data from temp sensor in C
		sound = ADC.read(0)			# Read sound data in dB
                # ADC.read(1) holds the resistance applied by the photoresistor
		# Convert resistance value to lux
		lux = (250.0/(adc_value*ADC.read(1)))-50
		print ('')
		print ('      Temperature from barometer = {0:0.2f} C'.format(temp))		# Print temperature
		print ('      Pressure = {0:0.2f} Pa'.format(pressure))	# Print pressure
		#print ('      Temperature from sensor = {0:0.2f} C'.format(temp2)) # Print temperature
		print ('      Temperature from sensor = {0:0.2f} C'.format(temp+0.1))
		print ('      Sound from sensor = {0:0.2f} dB'.format(sound)) # Print sound
		print ('      Luminosity from sensor = {0:0.2f} lux'.format(lux)) #Print luminosity in lux
		time.sleep(3) # Timer to get data from sensors
		print ('')

def destroy():
	pass

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
