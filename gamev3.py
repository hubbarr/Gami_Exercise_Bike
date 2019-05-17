from pygame_functions import *
import RPi.GPIO as GPIO
from time import sleep
import time, math
import random

#Hall sensor code based off code from https://www.raspberrypi.org/forums/viewtopic.php?t=148963

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(21, GPIO.IN)
screenSize(800,450)
setAutoUpdate(False)
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 17
pulse = 0
start_timer = time.time()

def init_GPIO():				
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)

def calculate_elapse(channel):				
	global pulse, start_timer, elapse
	pulse+=1								
	elapse = time.time() - start_timer		
	start_timer = time.time()				

def calculate_speed(r_cm):
	global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
	if elapse !=0:							
		rpm = 1/elapse * 60
		circ_cm = (2*math.pi)*r_cm			
		dist_km = circ_cm/100000 			
		km_per_sec = dist_km / elapse		
		km_per_hour = km_per_sec * 3600		
		mile_per_hour = km_per_hour * .621
		dist_meas = (dist_km*pulse)*1000	
		return int(mile_per_hour)
	else:
            return 0

def init_interrupt():
	GPIO.add_event_detect(sensor, GPIO.FALLING, callback = calculate_elapse, bouncetime = 20)



setBackgroundImage( [  ["images/back1.png", "images/back2.png" , "images/back3.png" , "images/back4.png" ]])

testSprite  = makeSprite("images/links.gif",32)  
ypos = 375
moveSprite(testSprite,100,ypos,True)

showSprite(testSprite)

nextFrame = clock()
frame=0
score = 0

instructionLabel = makeLabel("Current Speed: " + str(calculate_speed(20)) + " mph", 40, 10, 10, "white")
showLabel(instructionLabel)
scoreLabel = makeLabel("Score: " + str(int(score)), 40, 10, 50, "white")
showLabel(scoreLabel)

def up():
 changeLabel(instructionLabel, "Current Speed: " + str(calculate_speed(40)) + " mph")
 changeLabel(scoreLabel,"Score: " + str(int(score)))

if __name__ == '__main__':
	init_GPIO()
	init_interrupt()
	
while True:
	
    move = int(calculate_speed(40))
    if clock() > nextFrame:                         
        frame = (frame+1)%8                        
        nextFrame += 80
        
    if (move > 0):
        score = score + .01*move
        changeSpriteImage(testSprite, 0*8+frame)    
        scrollBackground(-move*4,0)
    if keyPressed("up"):
        if (ypos > 250):
            ypos = ypos - move*3 
            moveSprite(testSprite, 100, ypos, True)
    if keyPressed("down"):
        if (ypos < 425):
            ypos = ypos + move*3
            moveSprite(testSprite, 100, ypos, True)       
    up()    
    updateDisplay()
    tick(120)

endWait()

"""        
    if keyPressed("right"):
        changeSpriteImage(testSprite, 0*8+frame)    # 0*8 because right animations are the 0th set in the sprite sheet
        scrollBackground(-5,0)                      # The player is moving right, so we scroll the background left

    elif keyPressed("down"):
        #changeSpriteImage(testSprite, 1*8+frame)    # down facing animations are the 1st set
        #scrollBackground(0, -5)
        z = 0

    elif keyPressed("left"):
        changeSpriteImage(testSprite, 2*8+frame)    # and so on
        scrollBackground(5,0)

    elif keyPressed("up"):
        changeSpriteImage(testSprite,3*8+frame)
        scrollBackground(0,5)

    else:
        changeSpriteImage(testSprite, 1 * 8 + 5)  # the static facing front look

"""


