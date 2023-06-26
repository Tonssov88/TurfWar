import pygame

##
# Turf War - ICS3UC-04 CPT
#
# @author Tony Atanassov and Benjamin Lee
# @course ICS3UC
# @date 2023/06/14 - LastModified
#
# Pygame base template for opening a window - MVC version
# Simpson College Computer Science
# http://programarcadegames.com/
#

## Pygame setup
import pygame
from subprograms import *
from classes import *

pygame.init()
size = (1000, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Turf War")

## MODEL - Data use in system
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

skyColour = [135, 206, 235]

#Decides if players have control of their characters
gameState = False #used to stop movement during start screen

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
font = pygame.font.SysFont('Calibri', 25, True, False)

#LOADING IMAGES
#Start Screen
startScreen = pygame.image.load("startScreen.png").convert()
# Creating the platform
platformImage = pygame.image.load("platform.png").convert()
platformImage.set_colorkey(BLACK)
#Head and Body
headBodyImage = pygame.image.load("flowerHeadBody.png").convert()
headBodyImage.set_colorkey(WHITE)
#Right Hand
rightHandImage = pygame.image.load("hand-right.png").convert()
rightHandImage.set_colorkey(BLACK)
#Left Foot
leftFootImage = pygame.image.load("foot-left.png").convert()
leftFootImage.set_colorkey(BLACK)
#Right Foot
rightFootImage = pygame.image.load("foot-right.png").convert()
rightFootImage.set_colorkey(BLACK)
#Left Hand
leftHandImage = pygame.image.load("hand-left.png").convert()
leftHandImage.set_colorkey(BLACK)
#Sun and Moon
sunImage = pygame.image.load("sun.png").convert()
sunImage.set_colorkey(BLACK)
moonImage = pygame.image.load("moon.png").convert()
moonImage.set_colorkey(BLACK)
# Win Screens
player1WinScreen = pygame.image.load("player1wins.png").convert()
player1WinScreen.set_colorkey(BLACK)
player2WinScreen = pygame.image.load("player2wins.png").convert()
player2WinScreen.set_colorkey(BLACK)


# LOADING SOUNDS

hitSound = pygame.mixer.Sound("hitSound.wav")
jumpSound = pygame.mixer.Sound("jumpSound.ogg")
moogCity = pygame.mixer.Sound("moogCity.ogg")
moogCity.play(-1)


#Creating platform object
platform = Platform(0, 550, 1000, 50)

#initializing the day Timer 
dayTimer = 0

# Creating the player
player1 = createPlayer(100, 300)
player2 = createPlayer(790, 300)
allObjects = []
for i in range(len(player1)):
  allObjects.append(player1[i])
  allObjects.append(player2[i])

## Main Program Loop
while not done:
  ## CONTROL
  # Check for events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
  pressed = pygame.key.get_pressed()  
  #Player 1 Movement
  if gameState == True:
    if not player1[0].isStunned: # check if not stunned
      if pressed[pygame.K_RIGHT] and player1[0].isAttack == False: # Check input and not attacking
        for object in player1: # Move all objects in player1
          object.changeX = 3
          
      if pressed[pygame.K_LEFT] and player1[0].isAttack == False: # Check input and not attacking
        for object in player1:
          object.changeX = -3
          
      if not pressed[pygame.K_RIGHT] and not pressed[pygame.K_LEFT] and player1[0].isAttack == False: #if left and right are pressed at same time
        for object in player1:
          object.changeX = 0
          
      if pressed[pygame.K_UP] and player1[0].isAttack == False: # Check input and not attacking
        player1[0].isJump = True
      else:
        player1[0].isJump = False
        
      if pressed[pygame.K_b]: # Check input 
        if not player1[0].attackOnCooldown: #check if cooldown is active 
          player1[0].isAttack = True
          player1[0].attackOnCooldown = True
      else:
        player1[0].isAttack = False # Set attack to false if no attack input
        
      if pressed[pygame.K_n]: #Check input
        if not player1[0].kickOnCooldown: #Check if kick cooldown is active 
          player1[0].isKick = True
          player1[0].kickOnCooldown = True
      else:
        player1[0].isKick = False #Set kick to false if no kick input
        
      if pressed[pygame.K_m]: # Check for dash input
        for object in player1:
          object.dashing = True
      if pressed[pygame.K_v]: # check for shield input
        # Shield function only starts when counter is greater than 0
        # Once shield is over the counter resets to 0
        # When player presses shield button, counter turns to 1, allowing function to work
        if player1[0].shieldCounter == 0 and not player1[0].shieldOnCooldown: # check cooldown
          player1[0].shieldCounter = 1
          player1[0].shieldOnCooldown = True
  
  
    #Player 2 Movement / Copy of Player 1 but with different keys
    if not player2[0].isStunned: # Check if not stunned
      if pressed[pygame.K_d] and player2[0].isAttack == False: #Check input and if not attacking 
        for object in player2:
          object.changeX = 3
      if pressed[pygame.K_a] and player2[0].isAttack == False: #Check input and if not attacking 
        for object in player2:
          object.changeX = -3
      if not pressed[pygame.K_d] and not pressed[pygame.K_a] and player2[0].isAttack == False: #check if left and right are pressed
        for object in player2:
          object.changeX = 0
      if pressed[pygame.K_w] and player2[0].isAttack == False: #Check input and if not attacking 
        player2[0].isJump = True
      else:
        player2[0].isJump = False
      if pressed[pygame.K_r]:#Check input 
        if not player2[0].attackOnCooldown: #Check cooldown
          player2[0].isAttack = True
          player2[0].attackOnCooldown = True
      else:
        player2[0].isAttack = False #set to false if not attacking
        
      if pressed[pygame.K_t]: #Check input 
        if not player2[0].kickOnCooldown: #Check cooldown
          player2[0].isKick = True
          player2[0].kickOnCooldown = True
      else:
        player2[0].isKick = False # set to false if not kicking
      if pressed[pygame.K_y]: # check for dash input
        for object in player2:
          object.dashing = True
      if pressed[pygame.K_e]: #Check for shield input
        if player2[0].shieldCounter == 0 and not player2[0].shieldOnCooldown:
          player2[0].shieldCounter = 1
          player2[0].shieldOnCooldown = True
  
  # Game logic
  #Adding to dayTimer for day night cycle
  dayTimer += 1

  #Dashing Function
  for object in player1:
    if object.dashCounter > 3:
      object.dashing = False
      object.dashCounter += 1
    object.dash()
  for object in player2:
    if object.dashCounter > 3:
      object.dashing = False
      object.dashCounter += 1
    object.dash()

  # Managing cooldowns for attacks, kicks, and blocks
  if player1[0].attackOnCooldown:
    if player1[0].attackCooldown > 0:
      player1[0].isAttack = False
    player1[0].attackCooldown += 1
    if player1[0].attackCooldown == 40:
      player1[0].attackCooldown = 0
      player1[0].attackOnCooldown = False
  if player2[0].attackOnCooldown:
    if player2[0].attackCooldown > 0:
      player2[0].isAttack = False
    player2[0].attackCooldown += 1
    if player2[0].attackCooldown == 40:
      player2[0].attackCooldown = 0
      player2[0].attackOnCooldown = False

  if player1[0].kickOnCooldown:
    if player1[0].kickCooldown > 0:
      player1[0].isKick = False
    player1[0].kickCooldown += 1
    if player1[0].kickCooldown == 80:
      player1[0].kickCooldown = 0
      player1[0].kickOnCooldown = False
  if player2[0].kickOnCooldown:
    if player2[0].kickCooldown > 0:
      player2[0].isKick = False
    player2[0].kickCooldown += 1
    if player2[0].kickCooldown == 80:
      player2[0].kickCooldown = 0
      player2[0].kickOnCooldown = False

  if player1[0].shieldOnCooldown:
    player1[0].shieldCooldown += 1
    if player1[0].shieldCooldown == 80:
      player1[0].shieldCooldown = 0
      player1[0].shieldOnCooldown = False
  if player2[0].shieldOnCooldown:
    player2[0].shieldCooldown += 1
    if player2[0].shieldCooldown == 80:
      player2[0].shieldCooldown = 0
      player2[0].shieldOnCooldown = False
  for object in allObjects:
    object.colour = skyColour

  # Check time of day to change colour of sky
  if dayTimer >= 0 and dayTimer < 1800:
    skyColour = [135, 206, 235]
    dayState = True
  elif dayTimer >= 1800 and dayTimer <3600:
    skyColour = [12, 20, 69]
    dayState = False    
  else:
    dayTimer = 0

  # Shielding players
  player1[0].shield()
  player2[0].shield()
  
  # Making player attack
  playerAttack(player1)
  playerAttack(player2)
  playerKick(player1)
  playerKick(player2)

  # Reset collision variable before checking so that collision from previous frames don't interfere with calculations
  player1[0].attackCollidedWith = []
  player1[0].kickCollidedWith = []
  player2[0].attackCollidedWith = []
  player2[0].kickCollidedWith = []
  
  # Checking collision
  # Collision must go near last in game logic so that it is not tampered by other logic
  # Check if p1 is hit
  checkCollision(player1, player2, hitSound)
    

  # Making player jump if they press up key
  if player1[0].isJump and player1[0].jumpCounter == 0:
    jumpSound.play()
  elif player2[0].isJump and player2[0].jumpCounter == 0:
    jumpSound.play()
  for object in player1:
    if player1[0].isJump or 0 < object.jumpCounter < 40:
      object.jump()
  for object in player2:
    if player2[0].isJump or 0 < object.jumpCounter < 40:
      object.jump()

  # Checking if out of bounds
  # player = [pBody, pHead, pLArm, pRArm, pLFoot, pRFoot]
  keepPlayerInBounds(player1)
  keepPlayerInBounds(player2)

  # Updating the coordinates
  for object in allObjects:
    object.update()

  ## VIEW
  # Clear screen
  screen.fill(skyColour)
  # DRAW CODE
  #Bliting platform image
  screen.blit(platformImage, [0,501])

  #Depending on day/night cycle, a different image is blited
  if dayState: # Sun
    screen.blit(sunImage, [480, 30])
  else: # Moon
    screen.blit(moonImage, [480, 30])
  
  ## Drawing the player
  # Head and Body
  screen.blit(headBodyImage, [player1[1].x- 25, player1[1].y - 25])
  screen.blit(headBodyImage, [player2[1].x- 25, player2[1].y - 25])

  # Bliting the images for the hands of both players
  screen.blit(rightHandImage, [player1[3].x-3, player1[3].y])
  screen.blit(leftHandImage, [player1[2].x-3, player1[2].y])
  screen.blit(rightHandImage, [player2[3].x-3, player2[3].y])
  screen.blit(leftHandImage, [player2[2].x-3, player2[2].y])
  
  # Bliting the images for the feet of both players
  screen.blit(rightFootImage, [player2[5].x-3, player2[5].y])
  screen.blit(leftFootImage, [player2[4].x-3, player2[4].y])
  screen.blit(rightFootImage, [player1[5].x-3, player1[5].y])
  screen.blit(leftFootImage, [player1[4].x-3, player1[4].y])
  

  # Drawing health bars
  player1[0].drawHealthBar("left", dayState, gameState) # pass player, if its day or not and if the game is done 
  player2[0].drawHealthBar("right", dayState, gameState)

  # Drawing shields 
  if player1[0].isShielded:
    pygame.draw.rect(screen, (0, 255, 0), [player1[0].x - 30, player1[0].y - 50, player1[0].width + 60, player1[0].height + 100], 5)
  if player2[0].isShielded:
    pygame.draw.rect(screen, (0, 255, 0), [player2[0].x - 30, player2[0].y - 50, player2[0].width + 60, player2[0].height + 100], 5)

  # Drawing win screens
  if player1[0].hp <= 0:
    screen.blit(player2WinScreen, [0,0])
    # gameState = False
  if player2[0].hp <= 0:
    screen.blit(player1WinScreen, [0,0])
    # gameState = False

  if gameState == False:
    screen.blit(startScreen, [0,0])
    if pressed[pygame.K_RETURN]:
      gameState = True
  
  # Update Screen
  pygame.display.flip()
  clock.tick(60)

# Close the window and quit
pygame.quit()