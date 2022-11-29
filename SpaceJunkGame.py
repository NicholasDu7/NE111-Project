'''
Original game by Faisal Shahbaz
Date: 2022/11/01

Group Members:
Faisal Shahbaz (FS) @Faisal-Shahbaz (Github)
Nicholas Du (ND)
Jeniton Augustinpillai (JA)

'''
import random #import needed modules
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20) #positions the window on the screen. If run nativley, that 20x20 position refers to offset down and right from the top-left of your monitor
from pygame import * #import everything from pygame
init() #initializes pygame
SIZE = width, height = 1000, 700 #set the size of the screen
screen = display.set_mode(SIZE) #defines the screen
BLACK = (0, 0, 0) #defines basic colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
myClock = time.Clock() #defines clock
running = True #simple game state variable

keyA = False #FS key-related variables
keyW = False
keyS = False
keyD = False
keySpace = False
keyEscape = False
keyH = False

isAlive = True #FS game states
cutscene = True
currentScore = 0
prevShoot = 0
frenzy = False

ship = Rect(300, 100, 20, 20) #defines the ship as type rect
points = [] #include 4 rectangles
listJunk = [] #init empty list of soon-to-be junk
listBullets = []
scoreFont = font.SysFont("calibri",30) #fonts
mainTitleFont = font.SysFont('calibri', 60)
secondTitleFont = font.SysFont('calibri', 45)
framerate = 60

def drawCutscene(): #FS used in the first five seconds to generate the cutscene
    screen.blit(mainTitleFont.render('SPACE JUNK', 1, WHITE), Rect(350, 150, 50, 50)) #Title
    screen.blit(scoreFont.render('Navigate the drone through the space junk debris field, and collect green', 1, WHITE), Rect(175, 250, 50, 50)) #FS Instructions
    screen.blit(scoreFont.render('Use WASD to navigate', 1, WHITE), Rect(350, 300, 50, 50)) #FS Instructions
    screen.blit(scoreFont.render('Press SPACE to begin, press H for hard mode', 1, WHITE), Rect(200, 350, 50, 50)) #FS Instructions
    display.flip() #FS prints to display

def drawScene(shipRect, junk, life, finalScore, points, lbullets, cooldown): #FS used to draw the screen. Given all elements that must be drawn
    draw.rect(screen, BLACK, (0, 0, width, height)) #FS draws background
    if cooldown==False:
        draw.rect(screen, ORANGE, shipRect) #FS draws our ship
    else:
        draw.rect(screen, RED, shipRect) 
    for x in junk: #FS iterates through junk array to print each piece of junk
        draw.rect(screen, BLUE, x)
    for x in lbullets:
        draw.rect(screen, WHITE, x)
    draw.rect(screen, GREEN, points[0])
    if life == True: #FS prints score at top right
        screen.blit(scoreFont.render("%20s" %(finalScore), 1, WHITE), Rect(800, 20, 50, 50))
    if life == False: #FS prints death message
        screen.blit(scoreFont.render("%20s" %(finalScore), 1, WHITE), Rect(800, 20, 50, 50))
        screen.blit(mainTitleFont.render('YOU DIED', 1, WHITE), Rect(400, 200, 200, 100))
        screen.blit(secondTitleFont.render('Final Score: %20s' %finalScore, 1, WHITE), Rect(270, 300, 50, 50))
        screen.blit(secondTitleFont.render('Press [ESC] to exit', 1, WHITE), Rect(320, 400, 50, 50))
    display.flip() #FS print to display
    
def createJunk(junk): #FS generates the space junk
    num = random.random() #FS creates a random number
    if num < 0.09: #FS this is the weight to generate new junk
        junkSize = int(random.choices([10, 10, 10, 20, 20, 20, 30, 30, 30, 45, 45])[0]) #FS dice roll to determine the odds of each size of junk
        junk += [Rect(1000, random.randint(0, 700), junkSize, junkSize)] #FS appends new junk to array. Should be dependent on the variable 'width'
        return junk
    else: return junk #FS if no junk is created this frame, this module simple returns the original array
    
def manipulateJunk(junk): #FS moves generated space junk
    newJunk = [] #FS initializes new array to contain the moved junk
    while junk != []: #FS runs until the original array is empty
        junkItem = junk.pop() #FS new temporary variable containing the last item in the original array
        if junkItem[3] == 10: junkItem[0] -= 5 #FS find the size of the asteriod, and then change the position of that asteriod depending on the size. Has the effect of larger asteriods moving slower
        if junkItem[3] == 20: junkItem[0] -= 3
        if junkItem[3] == 30: junkItem[0] -= 2
        if junkItem[3] == 45: junkItem[0] -= 1
        if junkItem[0] > -20: newJunk += [junkItem] #FS if the junk is off the screen, it isn't added to the new list
    return newJunk

def checkPointsCollision(ship, points, frenzy):
    if len(points) < 1: return(points, 0)
    if frenzy==False:
        if ship.colliderect(points[0]):
            points.pop(0)
            return (points, 1)
        else: return (points, 0)
    else: pass

def genPoints(ship):
    while True:
        numx = random.randint(50,850)
        numy = random.randint(50,650)
        return [Rect(numx, numy, 20, 20)]

def iterPoints(ship, points, frenzy, score):
    (points, s)=checkPointsCollision(ship, points, frenzy)
    score += s
    while len(points) < 4:
            points+=genPoints(ship)
    return(points, score)

def genBullet(ship):
    return [Rect(ship[0]+20, ship[1]+5, 10, 10)]

def iterBullets(ljunk, lbullets):
    for x in range(len(ljunk)):
        for y in range(len(lbullets)):
            if y >= len(lbullets): break
            if lbullets[y].colliderect(ljunk[x]):
                lbullets.pop(y)
                ljunk[x][1] += ljunk[x][2]//2
                ljunk[x][2] = 10
                ljunk[x][3] = 10
    for x in range(len(lbullets)):
        if x < len(lbullets):
            lbullets[x][0] += 5
            if lbullets[x][0] > 1100: lbullets.pop(x)
    return(ljunk, lbullets)

def checkShipCollision(ship, listOfJunk): #FS checks to see if the ship has collided with space junk
    if ship.collidelist(listOfJunk) != -1: #FS uses pygame's built in collidelist() function. 
        return False
    return True #FS the else was omitted, it makes no difference

#JA This function prevents the ship from going off screen, which would break the game 
def checkShipOnScreen(ship): #FS prevents the ship from moving off the screen
    if ship[0] < 0:#FS these just reset the x and y values of the ship if it were to be off the screen
        ship[0] = 0
    if ship[0] > 980: #FS This should be dependent on (width, height) that was created at the beginning. This will be changed
        ship[0] = 980
    if ship[1] < 0:
        ship[1] = 0
    if ship[1] > 680:
        ship[1] = 680
    return ship

#JA Main game loop 
while running:
    for evnt in event.get(): #JA Checks if the game is closed
        if evnt.type == QUIT: 
            running = False
          
        #JA If the key is pressed(JA), it will associate which key is pressed down to True
        if evnt.type == KEYDOWN: #FS checks if keys are pressed
            if evnt.key == K_w: keyW = True
            if evnt.key == K_a: keyA = True
            if evnt.key == K_s: keyS = True
            if evnt.key == K_d: keyD = True
            if evnt.key == K_h: keyH = True
            if evnt.key == K_SPACE: keySpace = True
            if evnt.key == K_ESCAPE: keyEscape = True
        #JA If the key is not pressed, then it will associate the specific key to False 
        if evnt.type == KEYUP: #FS checks if keys are no longer pressed
            if evnt.key == K_w: keyW = False
            if evnt.key == K_a: keyA = False
            if evnt.key == K_s: keyS = False
            if evnt.key == K_d: keyD = False
            if evnt.key == K_h: keyH = False
            if evnt.key == K_SPACE: keySpace = False
            if evnt.key == K_ESCAPE: keyEscape = False
        
    if cutscene == True: #FS for the cutscene
        drawCutscene() #JA Draws the cutscene at the beggining of the game
        if keySpace==True: cutscene = False #JA Draws cutscene for a specific amount of time
        if keyH==True:
            cutscene = False
            framerate = 90

    if (isAlive == True) and (cutscene == False): #FS while playing the game
        if keyW == True: 
            ship[1] -= 5 #ND moves ship up (Note origin is top left of screen and axis is flipped)
        if keyS == True:
            ship[1] += 5 #ND moves ship down
        if keyA == True:
            ship[0] -= 5 #ND moves ship left
        if keyD == True: #FS movement
            ship[0] += 5 #ND moves ship right
        if keySpace == True and time.get_ticks() - prevShoot > 1500:
            listBullets += genBullet(ship)
            prevShoot = time.get_ticks()
        ship = checkShipOnScreen(ship) #FS calls functions neccessary for each frame
        listJunk = createJunk(listJunk)
        listJunk = manipulateJunk(listJunk)
        isAlive = checkShipCollision(ship, listJunk)
        (listJunk, listBullets) = iterBullets(listJunk, listBullets)
        (points, currentScore) = iterPoints(ship, points, frenzy, currentScore)
        drawScene(ship, listJunk, isAlive, currentScore, points, listBullets, time.get_ticks()-prevShoot>1500) #FS draws scene finally. It is passed every element that needs to be drawn 
    if (isAlive == False) and (keyEscape ==  True): running = False #FS if dead and exits
    myClock.tick(framerate) #FS sets framerate. 

quit() #JA Quits game at the end
