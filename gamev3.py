from pygame_functions import *
import RPi.GPIO as GPIO
from time import sleep
import time, math
import random

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

"""
Jump
"""
#jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
#isJumping = FalsejumpCount = 0Falling = False


#def jumping():
        #jumpCount = 0
        #y = 700
        #for v in jumpList:
            #y -= jumpList[v] * 1.3
            #moveSprite(testSprite,100,y,True)
            #jumpCount += 1
            #if (jumpCount > 108):
                #jumpCount = 0
                #isJumping = False
                #runCount = 0
            #self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)

def init_GPIO():					# initialize GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(sensor,GPIO.IN,GPIO.PUD_UP)

def calculate_elapse(channel):				# callback function
	global pulse, start_timer, elapse
	pulse+=1								# increase pulse by 1 whenever interrupt occurred
	elapse = time.time() - start_timer		# elapse for every 1 complete rotation made!
	start_timer = time.time()				# let current time equals to start_timer

def calculate_speed(r_cm):
	global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
	if elapse !=0:							# to avoid DivisionByZero error
		rpm = 1/elapse * 60
		circ_cm = (2*math.pi)*r_cm			# calculate wheel circumference in CM
		dist_km = circ_cm/100000 			# convert cm to km
		km_per_sec = dist_km / elapse		# calculate KM/sec
		km_per_hour = km_per_sec * 3600		# calculate KM/h
		mile_per_hour = km_per_hour * .621
		dist_meas = (dist_km*pulse)*1000	# measure distance traverse in meter
		return int(mile_per_hour)
	else:
            return 0

def init_interrupt():
	GPIO.add_event_detect(sensor, GPIO.FALLING, callback = calculate_elapse, bouncetime = 20)



setBackgroundImage( [  ["images/back1.png", "images/back2.png" , "images/back3.png" , "images/back4.png" ]])


testSprite  = makeSprite("images/links.gif",32)  # links.gif contains 32 separate frames of animation. Sizes are automatically calculated.
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

#obstacle = False
#startpos = 700
#obstacle = True
#obsSprite = makeSprite("images/pothole.png")
#moveSprite(obsSprite,startpos,700,True)

#def obst():
    #num = 0
    #num = random.randint(0,5)
    #if (num <= 3):
        #obstacle = True
        #obsSprite = makeSprite("images/agent1.png")
        #moveSprite(obsSprite,startpos,700,True)
        #showSprite(obsSprite)

def up():
 changeLabel(instructionLabel, "Current Speed: " + str(calculate_speed(40)) + " mph")
 changeLabel(scoreLabel,"Score: " + str(int(score)))

if __name__ == '__main__':
	init_GPIO()
	init_interrupt()
	
while True:
    
    
    #print(calculate_speed(20))	# call this function with wheel radius as parameter
    move = int(calculate_speed(40))
    if clock() > nextFrame:                         # We only animate our character every 80ms.
        frame = (frame+1)%8                         # There are 8 frames of animation in each direction
        nextFrame += 80
        
    if (move > 0):
        score = score + .01*move
        changeSpriteImage(testSprite, 0*8+frame)    # 0*8 because right animations are the 0th set in the sprite sheet
        scrollBackground(-move*4,0)
        #print (obstacle)
        #if (obstacle == True):
            #print("here")
            #moveSprite(obsSprite, startpos - move*2, 700, True)
            #startpos = startpos - move*2
            #if (startpos <= 0):
                #startpos = 700
    if keyPressed("up"):
    #if (GPIO.input(12) == 1):
        #print("press")
        #for ypos in range (800, 550, -1):
            #moveSprite(testSprite, 100, ypos, True)
            #time.sleep(.01)
        if (ypos > 250):
            ypos = ypos - move*3 
            moveSprite(testSprite, 100, ypos, True)
        #for ypos in range (550, 700, 1):
            #moveSprite(testSprite, 100, ypos, True)
    #if (GPIO.input(21) == 1):
    if keyPressed("down"):
        #print("press")
        #for ypos in range (550, 800, 1):
        #moveSprite(testSprite, 100, ypos, True)
        if (ypos < 425):
            ypos = ypos + move*3
            moveSprite(testSprite, 100, ypos, True)

    #if (GPIO.input(12) == False):
    #print("hello")
    #hideLabel(instructionLabel
    #if (obstacle == False):
        #obst()
        #obstacle = True
    #jumping()          
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


