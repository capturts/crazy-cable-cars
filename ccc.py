#!/usr/bin/env python

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>

	This is version 0.0.4
	See bottom of source for changelog
"""

import pygame, sys

from cablecar import *

from pygame.locals import *

"""
Each cable car follows a route defined by their list of nodes. The nodes are the (x, y)
coordinates of the track 'joints'. The longer the section of track the faster the cable
car will go on that section. For example if the nodes were ((100, 100), (200, 200)) the car
will go at a medium speed left and downwards. If the nodes were ((300, 300), (800, 200)) then
the car will travel quite fast to the left and slightly upwards.

The tracks can overlap, but do not add the same coordinates twice for your car as you will
end up in a inescapable loop. The baddies, however, can have their first and last coordinates 
the same and it makes an interesting circuit path.
"""

## levels is a list of levels. The game will cycle through them until you win the last one.
levels=[]

## Each level has "your" nodes.
me=Car(((100, 300), (200, 300), (300, 300), (400, 300), (500, 300), (600, 300), (700, 300)))
## And the baddies nodes. 
baddies=[]
baddie=Car(((350, 100), (350, 200), (350, 300), (350, 400), (350, 500)), False, True)
baddies.append(baddie)
baddie=Car(((450, 100), (500, 200), (550, 300), (600, 400), (650, 500)), False, True)
baddies.append(baddie)
## The node tuples are added as a tuple !in the right order!
levels.append((me, baddies))

## Each level has "your" nodes.
me=Car(((100, 300), (200, 300), (300, 300), (400, 300), (500, 300), (600, 300), (700, 300)))
## And the baddies nodes. 
baddies=[]
baddie=Car(((200, 100), (250, 200), (300, 300), (350, 200), (400, 100)), False, True)
baddies.append(baddie)
baddie=Car(((400, 290), (500, 290), (600, 290), (600, 400), (500, 400), (400, 400), (400, 290)), False, True)
baddies.append(baddie)
## The node tuples are added as a tuple !in the right order!
levels.append((me, baddies))

## Each level has "your" nodes.
me=Car(((100, 300), (200, 300), (300, 300), (400, 400), (500, 400), (600, 300), (700, 300)))
## And the baddies nodes. 
baddies=[]
baddie=Car(((200, 200), (200, 300), (200, 400), (300, 400), (400, 400), (400, 300), (400, 200), (300, 200), (200, 200)), False, True)
baddies.append(baddie)
baddie=Car(((450, 320), (550, 320), (650, 420), (650, 520)), False, True)
baddies.append(baddie)
## The node tuples are added as a tuple !in the right order!
levels.append((me, baddies))

## Each level has "your" nodes.
me=Car(((100, 300), (200, 400), (100, 400), (200, 300), (300, 300), (300, 400), (400, 400), (600, 400), (600, 300)))
## And the baddies nodes. 
baddies=[]
baddie=Car(((170, 400), (270, 400), (220, 450), (170, 400)), False, True)
baddies.append(baddie)
baddie=Car(((600, 420), (400, 420), (400, 520), (500, 520), (600, 520), (600, 420)), False, True)
baddies.append(baddie)
## The node tuples are added as a tuple !in the right order!
levels.append((me, baddies))

##### END OF LEVEL DEFINING #####

FPS = 24 # frames per second, the general speed of the program
WINDOWWIDTH = 250 # size of window's width in pixels
WINDOWHEIGHT = 250 # size of windows' height in pixels
#WINDOWWIDTH = 800 # size of window's width in pixels
#WINDOWHEIGHT = 600 # size of windows' height in pixels

pygame.init()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
FPSCLOCK = pygame.time.Clock()
BACKGROUND=pygame.image.load('backtile.png')
BGH=64
BGW=64
CAR=pygame.image.load('car.png')
BAD=pygame.image.load('bad.png')
CAR_W=25
CAR_H=50
fontObj = pygame.font.Font('freesansbold.ttf', 16)
CRASH=pygame.mixer.Sound('crash.ogg')
pygame.mixer.music.load('music.ogg')

TRACKWIDTH=3

RED=(255, 0, 0)
BLUE=(0, 0, 255)
BLACK=(0, 0, 0)
GREEN=(0, 255, 0)

def crash(me, you):
	my_left=me.x-(CAR_W/2)
	my_right=me.x+(CAR_W/2)
	my_top=me.y
	my_bottom=me.y+CAR_H

	your_left=you.x-(CAR_W/2)
	your_right=you.x+(CAR_W/2)
	your_top=you.y
	your_bottom=you.y+CAR_H
	
	if my_left<your_right:
		if my_right>your_left:
			if my_top<your_bottom:
				if my_bottom>your_top:
					return True
					
	return False

def translate(nodes, pov):
	#pov is where I am
	out=[]
	ox=pov[0]-WINDOWWIDTH/2
	oy=pov[1]-WINDOWHEIGHT/2+CAR_H/2
	for c in nodes:
		x=c[0]-ox
		y=c[1]-oy
		out.append((x, y))
	return out

pygame.display.set_caption ("Crazy Cable Cars")
pygame.mixer.music.play(-1, 0.0)

lives=5
lev=0
def main():
	global lives, lev
	for level in levels:
		if lives>0:
			lev=lev+1
			me=level[0]
			baddies=level[1]
			exit=False
			while exit==False: #main game loop
				
				for event in pygame.event.get(): # event handling loop
					if event.type == QUIT:
						exit=True
						lives=0
					elif event.type==KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							exit=True
							lives=0
						elif event.key==112:
							me.dir=1
						elif event.key==111:
							me.dir=-1
						else:
							print event.key
					elif event.type==KEYUP:
						me.dir=0
			
				me.move()
				for baddie in baddies:
					baddie.move()
			
				if me.win==True:
					exit=True
			
				for iy in xrange(0, (WINDOWHEIGHT/BGH)+2):
					for ix in xrange(0, (WINDOWWIDTH/BGW)+2):
						DISPLAYSURF.blit(BACKGROUND, (ix*BGW-(me.x % BGW), iy*BGH-(me.y % BGH)))
		
				pygame.draw.lines(DISPLAYSURF, RED, False, translate(me.path, (me.x, me.y)), TRACKWIDTH)
				for baddie in baddies:
					pygame.draw.lines(DISPLAYSURF, BLUE, baddie.loop, translate(baddie.path, (me.x, me.y)), TRACKWIDTH)
				for baddie in baddies:
					DISPLAYSURF.blit(BAD, (baddie.x-(me.x-WINDOWWIDTH/2)-CAR_W/2, baddie.y-(me.y-WINDOWHEIGHT/2+CAR_H/2)))
				DISPLAYSURF.blit(CAR, (WINDOWWIDTH/2-CAR_W/2, WINDOWHEIGHT/2-CAR_H/2))
				
				"""pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, 250, 20), 0)
				textSurfaceObj = fontObj.render('FPS:'+str(round(FPSCLOCK.get_fps(), 2)), True, GREEN, BLUE)
				textRectObj = textSurfaceObj.get_rect()
				textRectObj.topleft=(0,0)
				DISPLAYSURF.blit(textSurfaceObj, textRectObj)"""
	
				pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, 250, 20), 0)
				textSurfaceObj = fontObj.render('Level: '+str(lev)+' Lives: '+str(lives), True, GREEN, BLUE)
				textRectObj = textSurfaceObj.get_rect()
				textRectObj.topleft=(0,0)
				DISPLAYSURF.blit(textSurfaceObj, textRectObj)
	
				for baddie in baddies:
					if crash(me, baddie)==True:
						CRASH.play()
						lives=lives-1
						if (lives>0):
							me.x=me.path[0][0]
							me.y=me.path[0][1]
							me.getVectors()
						else:
							exit=True
			
				pygame.display.update()
				FPSCLOCK.tick(FPS)

#import cProfile as profile
#profile.run('main()')
main()

pygame.mixer.music.stop()

exit=True
while exit==False:
	#closing bit loop
	for event in pygame.event.get(): # event handling loop
		if event.type == QUIT:
			exit=True
		elif event.type==KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				exit=True
	pygame.display.update()
	FPSCLOCK.tick(1)

print "End of game"
if lives==0:
	print "You lost"
else:
	print "You won"

pygame.quit()
sys.exit()

"""
	Changelog

	2012-08-09
	version 0.0.4
	Added sound and music
	OK, enough for one day

	2012-08-08
	version 0.0.3
	Made some proper levels
	Made an explanation of how to make your own levels
	Improved the background. It now uses a tiled background
	Made baddies a different colour
	Set the window title :p
	Added the concept of 'lives'

	2012-08-08
	version 0.0.2
	Changed the view so it is more like looking through a window, allowing much bigger levels

	2012-08-07
	version 0.0.1
	Initial Release

"""
