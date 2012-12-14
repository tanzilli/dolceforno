import ablib
import time
import thread
import threading

lcd = ablib.Daisy24(0,0x27)
rele = ablib.Daisy4('D5','DIP1')
P7 = ablib.Daisy5('D2','P7')
P8 = ablib.Daisy5('D2','P8')
 
min = 80
max = 80
live = min
keydelay=0.2

print "DOLCEFORNO"
print "by AcmeSystems"

lcd.putstring("DOLCEFORNO")
lcd.setcurpos(0,1)
lcd.putstring("by AcmeSystems")
time.sleep(1)

rele.off()

lcd.clear()
lcd.putstring("LIVE   MIN  MAX")


def check_temp():
	global live

	sensor = ablib.DS18B20("000003dcfb31")
	#sensor = ablib.DS18B20("000003dcfd4b")

	while True:

		a=sensor.getTemp()
		if a!=None: 			
			live=a	
			print live
		else:
			print "Errore CRC"

		time.sleep(1)
		
thread.start_new_thread(check_temp,())
	

while True:
	lcd.setcurpos(0,1)
	lcd.putstring("%3.1f   %3d  %3d" % (live,min,max))

	if lcd.pressed(0):
		if min<max:
			min=min+1
			time.sleep(keydelay)

	if lcd.pressed(3):
		if min>0:
			min=min-1
			time.sleep(keydelay)

	if lcd.pressed(1):
		if max<120:
			max=max+1
			time.sleep(keydelay)

	if lcd.pressed(2):
		if max>min:
			max=max-1
			time.sleep(keydelay)

	if live<min:
		rele.on()

	if live>max:
		rele.off()
