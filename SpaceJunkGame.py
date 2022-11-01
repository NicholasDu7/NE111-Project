import random
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
from pygame import * 
init()
SIZE = width, height = 1000, 700
screen = display.set_mode(SIZE)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
myClock = time.Clock()
running = True

keyA = False #key-related variables
keyW = False
keyS = False
keyD = False
keySpace = False
keyEscape = False

isAlive = True #game states
cutscene = True
currentScore = 0

ship = Rect(300, 100, 20, 20)
listJunk = []
scoreFont = font.SysFont("calibri",30)
mainTitleFont = font.SysFont('calibri', 60)
secondTitleFont = font.SysFont('calibri', 45)

def drawCutscene(): #used in the first five seconds to generate the cutscene
    screen.blit(mainTitleFont.render('SPACE JUNK', 1, WHITE), Rect(350, 150, 50, 50))
    screen.blit(scoreFont.render('Navigate the drone through the space junk debris field', 1, WHITE), Rect(175, 250, 50, 50))
    screen.blit(scoreFont.render('Use WASD to navigate', 1, WHITE), Rect(350, 300, 50, 50))
    display.flip()

def drawScene(shipRect, junk, life, finalScore): #used to draw the screen
    draw.rect(screen, BLACK, (0, 0, width, height))
    draw.rect(screen, RED, shipRect)
    for x in junk:
        draw.rect(screen, BLUE, x)
    if life == True:
        screen.blit(scoreFont.render("%20s" %((time.get_ticks() - 5000) // 200), 1, WHITE), Rect(800, 20, 50, 50))
    if life == False:
        screen.blit(scoreFont.render("%20s" %(finalScore), 1, WHITE), Rect(800, 20, 50, 50))
        screen.blit(mainTitleFont.render('YOU DIED', 1, WHITE), Rect(400, 200, 200, 100))
        screen.blit(secondTitleFont.render('Final Score: %20s' %finalScore, 1, WHITE), Rect(270, 300, 50, 50))
        screen.blit(secondTitleFont.render('Press [ESC] to exit', 1, WHITE), Rect(320, 400, 50, 50))
    display.flip()
    
def createJunk(junk): #generates the space junk
    num = random.random()
    if num < 0.09:
        junkSize = int(random.choices([10, 10, 10, 20, 20, 20, 30, 30, 30, 45, 45])[0])
        junk += [Rect(1000, random.randint(0, 700), junkSize, junkSize)]
        return junk
    else: return junk
    
def manipulateJunk(junk): #moves generated space junk
    newJunk = []
    while junk != []:
        junkItem = junk.pop()
        if junkItem[3] == 10: junkItem[0] -= 5
        if junkItem[3] == 20: junkItem[0] -= 3
        if junkItem[3] == 30: junkItem[0] -= 2
        if junkItem[3] == 45: junkItem[0] -= 1
        if junkItem[0] > -20: newJunk += [junkItem]
    return newJunk

def checkShipCollision(ship, listOfJunk): #checks to see if the ship has collided with space junk
    if ship.collidelist(listOfJunk) != -1:
        return False
    return True
    
def checkShipOnScreen(ship): #prevents the ship from moving off the screen
    if ship[0] < 0:
        ship[0] = 0
    if ship[0] > 980:
        ship[0] = 980
    if ship[1] < 0:
        ship[1] = 0
    if ship[1] > 680:
        ship[1] = 680
    return ship

while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False

        if evnt.type == KEYDOWN: #checks if keys are pressed
            if evnt.key == K_w: keyW = True
            if evnt.key == K_a: keyA = True
            if evnt.key == K_s: keyS = True
            if evnt.key == K_d: keyD = True
            if evnt.key == K_SPACE: keySpace = True
            if evnt.key == K_ESCAPE: keyEscape = True

        if evnt.type == KEYUP: #checks if keys are no longer pressed
            if evnt.key == K_w: keyW = False
            if evnt.key == K_a: keyA = False
            if evnt.key == K_s: keyS = False
            if evnt.key == K_d: keyD = False
            if evnt.key == K_SPACE: keySpace = False
            if evnt.key == K_ESCAPE: keyEscape = False
        
    if cutscene == True: #for the cutscene
        drawCutscene()
        if time.get_ticks() > 5000: cutscene = False

    if (isAlive == True) and (cutscene == False): #while playing the game
        if keyW == True:
            ship[1] -= 5
        if keyS == True:
            ship[1] += 5
        if keyA == True:
            ship[0] -= 5
        if keyD == True: #movement
            ship[0] += 5        
        ship = checkShipOnScreen(ship)
        listJunk = createJunk(listJunk)
        listJunk = manipulateJunk(listJunk)
        isAlive = checkShipCollision(ship, listJunk)
        drawScene(ship, listJunk, isAlive, currentScore)
    if (isAlive == False) and (currentScore == 0): #if dead
        currentScore = (time.get_ticks() - 5000) // 200
        drawScene(ship, listJunk, isAlive, currentScore)
    if (isAlive == False) and (keyEscape ==  True): running = False # if dead and exits
    myClock.tick(60)

quit()