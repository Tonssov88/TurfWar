import pygame
from classes import *
size = (1000, 600)
screen = pygame.display.set_mode(size)

def createPlayer(x, y): # Creating player list of all the different objects
  pBody = Body(x + 30, y + 50, 50, 100, screen)
  pHead = Head(x + 35, y, 40, 40, screen)
  pLArm = Hands(x, y + 110, 20, 20, "left", screen)
  pRArm = Hands(x + 90, y + 110, 20, 20, "right", screen)
  pLFoot = Foot(x + 30, y + 180, 20, 20, "left", screen)
  pRFoot = Foot(x + 60, y + 180, 20, 20, "right", screen)
  player = [pBody, pHead, pLArm, pRArm, pLFoot, pRFoot]
  return player

# This function manages most things attack (punch) related. Does not manage collision and deduction of hp.
def playerAttack(player):
  if player[0].changeX < 0:
    player[0].attackSide = "left"
  elif player[0].changeX > 0:
    player[0].attackSide = "right"
  if player[0].isAttack:
    if player[0].attackSide == "left" and player[2].attackCounter == 0:
      player[2].attack()
      for object in player:
        if not 0 < object.jumpCounter < 40:
          object.changeX = 0
          player[0].isJump = False
    elif player[0].attackSide == "right" and player[3].attackCounter == 0:
      player[3].attack()
      for object in player:
        if not 0 < object.jumpCounter < 40:
          object.changeX = 0
          player[0].isJump = False
      
  if 0 < player[2].attackCounter <= player[2].lenOfAttack:
    player[2].attack()
    for object in player:
      if not 0 < object.jumpCounter < 40:
        object.changeX = 0
        player[0].isJump = False
  if 0 < player[3].attackCounter <= player[3].lenOfAttack:
    player[3].attack()
    for object in player:
      if not 0 < object.jumpCounter < 40:
        object.changeX = 0
        player[0].isJump = False

def playerKick(player): # Function for kicking 
  if player[0].changeX < 0:
    player[0].attackSide = "left"
  elif player[0].changeX > 0:
    player[0].attackSide = "right"
  if player[0].isKick:
    if player[0].attackSide == "left" and player[4].kickCounter == 0:
      player[4].kick()
      for object in player:
        if not 0 < object.jumpCounter < 40:
          object.changeX = 0
          player[0].isJump = False
    elif player[0].attackSide == "right" and player[5].kickCounter == 0:
      player[5].kick()
      for object in player:
        if not 0 < object.jumpCounter < 40:
          object.changeX = 0
          player[0].isJump = False
  if 0 < player[4].kickCounter <= player[4].lenOfKick:
    player[4].kick()
    for object in player:
      if not 0 < object.jumpCounter < 40:
        object.changeX = 0
        player[0].isJump = False
  if 0 < player[5].kickCounter <= player[5].lenOfKick:
    player[5].kick()
    for object in player:
      if not 0 < object.jumpCounter < 40:
        object.changeX = 0
        player[0].isJump = False

def keepPlayerInBounds(player): # Keeps the player within the bounds of the screen 
  if player[2].x + player[2].changeX < 0 or player[3].x + player[3].width + player[3].changeX > 1000:
    for object in player:
      object.changeX = 0

def checkCollision(p1, p2, hitSound): # Checks collision between the two players
  if p1[0].x < p2[0].x:
    p1Side = "left"
    p2Side = "right"
  else:
    p1Side = "right"
    p2Side = "left"
  # Check if p1 is hit
  if p2[0].attackSide == "left":
    if p2[0].isAttack or 0 < p2[2].attackCounter <= p2[2].lenOfAttack:
      p1[0].checkCollision(p2[2], "attack")
  if p2[0].attackSide == "right":
    if p2[0].isAttack or 0 < p2[3].attackCounter <= p2[3].lenOfAttack:
      p1[0].checkCollision(p2[3], "attack")
  if not p1[0].isShielded:
    for i in p1[0].attackCollidedWith:
      if i == p2[2] or i == p2[3]:
        p1[0].hp -= 0.5
    for part in p1:
      if len(p1[0].attackCollidedWith) != 0 or 0 < part.attackStunCounter:
        part.playerAttackStunned(p1Side)
  elif p1[0].isShielded:
    for i in p1[0].attackCollidedWith:
      if i == p2[2] or i == p2[3]:
        p2[0].hp -= 10
    for part in p2:
      if len(p1[0].attackCollidedWith) != 0 or 0 < part.attackStunCounter:
        part.playerAttackStunned(p2Side)

  if p2[0].attackSide == "left":
    if p2[0].isKick or 0 < p2[4].kickCounter <= p2[4].lenOfKick:
      p1[0].checkCollision(p2[4], "kick")
  if p2[0].attackSide == "right":
    if p2[0].isKick or 0 < p2[5].kickCounter <= p2[5].lenOfKick:
      p1[0].checkCollision(p2[5], "kick") 
  if not p1[0].isShielded:
    for i in p1[0].kickCollidedWith:
      if i == p2[4] or i == p2[5]:
        p1[0].hp -= 1
    for part in p1:
      if len(p1[0].kickCollidedWith) != 0 or 0 < part.kickStunCounter:
        part.playerKickStunned(p1Side)
  elif p1[0].isShielded:
    for i in p1[0].kickCollidedWith:
      if i == p2[4] or i == p2[5]:
        p2[0].hp -= 10
    for part in p2:
      if len(p1[0].kickCollidedWith) != 0 or 0 < part.kickStunCounter:
        part.playerKickStunned(p2Side)
  
  # Check if p2 is hit
  if p1[0].attackSide == "left":
    if p1[0].isAttack or 0 < p1[2].attackCounter <= p1[2].lenOfAttack:
      p2[0].checkCollision(p1[2], "attack")
  if p1[0].attackSide == "right":
    if p1[0].isAttack or 0 < p1[3].attackCounter <= p1[3].lenOfAttack:
      p2[0].checkCollision(p1[3], "attack")
  if not p2[0].isShielded:
    for i in p2[0].attackCollidedWith:
      if i == p1[2] or i == p1[3]:
        p2[0].hp -= 0.5
    for part in p2:
      if len(p2[0].attackCollidedWith) != 0 or 0 < part.attackStunCounter:
        part.playerAttackStunned(p2Side)
  elif p2[0].isShielded:
    for i in p2[0].attackCollidedWith:
      if i == p1[2] or i == p1[3]:
        p1[0].hp -= 10
    for part in p1:
      if len(p2[0].attackCollidedWith) != 0 or 0 < part.attackStunCounter:
        part.playerAttackStunned(p1Side)
  
  if p1[0].attackSide == "left":
    if p1[0].isKick or 0 < p1[4].kickCounter <= p1[4].lenOfKick:
      p2[0].checkCollision(p1[4], "kick")
  if p1[0].attackSide == "right":
    if p1[0].isKick or 0 < p1[5].kickCounter <= p1[5].lenOfKick:
      p2[0].checkCollision(p1[5], "kick")
  if not p2[0].isShielded:
    for i in p2[0].kickCollidedWith:
      if i == p1[4] or i == p1[5]:
        p2[0].hp -= 1
    for part in p2:
      if len(p2[0].kickCollidedWith) != 0 or 0 < part.kickStunCounter:
        part.playerKickStunned(p2Side)
  elif p2[0].isShielded:
    for i in p2[0].kickCollidedWith:
      if i == p1[4] or i == p1[5]:
        p1[0].hp -= 10
    for part in p1:
      if len(p2[0].kickCollidedWith) != 0 or 0 < part.kickStunCounter:
        part.playerKickStunned(p1Side)

  if len(p1[0].attackCollidedWith) != 0 \
  or len(p2[0].attackCollidedWith) != 0 \
  or len(p1[0].kickCollidedWith) != 0 \
  or len(p2[0].kickCollidedWith) != 0:
    if not p1[0].hitSoundIsPlayed:
      hitSound.play()
      p1[0].hitSoundIsPlayed = True
  else:
    p1[0].hitSoundIsPlayed = False