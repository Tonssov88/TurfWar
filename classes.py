import pygame

class Player(): # Player parent class
  def __init__(self, x, y, width, height, screen):
    self.x = x
    self.y = y
    self.originalX = x
    self.originalY = y
    self.width = width
    self.height = height
    self.screen = screen
    self.changeX = 0
    self.changeY = 0
    self.jumpCounter = 0
    self.attackStunCounter = 0
    self.attackStunLength = 20
    self.kickStunCounter = 0
    self.kickStunLength = 40
    self.dashing = False
    self.dashCounter = 0
    self.isStunned = False
    
  def jump(self): 
    if self.y >= self.originalY and self.jumpCounter > 0:
      self.changeY = 0
      self.y = self.originalY
      self.jumpCounter = 0
    else:
      if self.jumpCounter == 0:
        self.changeY = -10
      self.jumpCounter += 1
      self.changeY += 0.5

  def dash(self):
    if self.dashing == True:
      if self.dashCounter <= 3:
        self.dashCounter += 1
        self.changeX = self.changeX * 6
      if self.dashCounter >= 30:
        self.dashCounter = 0
    else:
      if not self.dashCounter <= 3:
        self.dashCounter += 1
      if self.dashCounter >= 30:
        self.dashCounter = 0
  def update(self):
    self.x += self.changeX
    self.y += self.changeY
  # Side refers to which player is on right or left
  def playerAttackStunned(self, side): 
    if self.attackStunCounter < self.attackStunLength:
      if self.attackStunCounter < (self.attackStunLength/2):
        if side == "left":
          self.changeX = -5
        else:
          self.changeX = 5
      else:
        self.changeX = 0
      self.attackStunCounter += 1
      self.isStunned = True
    else:
      self.attackStunCounter = 0
      self.isStunned = False

  def playerKickStunned(self, side): 
    if self.kickStunCounter < self.kickStunLength:
      if self.kickStunCounter < self.kickStunLength/2:
        if side == "left":
          self.changeX = -10
        else:
          self.changeX = 10
      else:
        self.changeX = 0
      self.kickStunCounter += 1
      self.isStunned = True
    else:
      self.kickStunCounter = 0
      self.isStunned = False
  

class Body(Player):
  def __init__(self, x, y, width, height,screen):
    super().__init__(x, y, width, height, screen)
    self.attackSide = "left"
    self.isJump = False
    self.hp = 100
    self.attackCollidedWith = []
    self.kickCollidedWith = []
    self.isAttack = False
    self.isKick = False
    self.attackCooldown = 0
    self.attackOnCooldown = False
    self.kickCooldown = 0
    self.kickOnCooldown = False
    self.isShielded = False
    self.shieldCounter = 0
    self.shieldCooldown = 0
    self.shieldOnCooldown = False
    self.hitSoundIsPlayed = False
  def checkCollision(self, other, typeOfMove):
    if self.x < other.x:
      leftObject = self
      rightObject = other
    else:
      leftObject = other
      rightObject = self
    if rightObject.x < (leftObject.x + leftObject.width):
      if leftObject.y < rightObject.y < (leftObject.y + leftObject.height) \
      or leftObject.y > rightObject.y > (leftObject.y + leftObject.height) \
      or rightObject.y < leftObject.y < (rightObject.y + rightObject.height) \
      or rightObject.y > leftObject.y > (rightObject.y + rightObject.height):
        if typeOfMove == "attack":
          self.attackCollidedWith.append(other)
        elif typeOfMove == "kick":
          self.kickCollidedWith.append(other)
  def drawHealthBar(self, side, dayState, gameState):
    font = pygame.font.SysFont('times new roman', 25, True, False)
    player1Name = font.render("Player 1 - Arrows",True, (255, 255, 255))
    player2Name = font.render("Player 2 - WASD",True, (255, 255, 255))
    if dayState and self.hp <100 and gameState:
      self.hp += 0.0220
    if side == "left":
      self.screen.blit(player1Name, [50, 20])
      pygame.draw.rect(self.screen, (0, 0, 0), [50, 50, 200, 30], 0)
      pygame.draw.rect(self.screen, (0, 255, 0), [50, 50, self.hp*2, 30], 0)
    if side == "right":
      self.screen.blit(player2Name, [725, 20])
      pygame.draw.rect(self.screen, (0, 0, 0), [750, 50, 200, 30], 0)
      pygame.draw.rect(self.screen, (0, 255, 0), [(750 + 200 - self.hp*2), 50, self.hp*2, 30], 0)
  def shield(self):
    if 0 < self.shieldCounter < 40:
      self.isShielded = True
      self.shieldCounter += 1
    else:
      self.isShielded = False
      self.shieldCounter = 0
      

class Hands(Player):
  def __init__(self, x, y, width, height, side, screen):
    super().__init__(x, y, width, height, screen)
    self.side = side
    self.attackCounter = 0
    self.lenOfAttack = 20
  def attack(self):
    if self.attackCounter < self.lenOfAttack:
      if self.attackCounter == 0:
        if self.side == "left":
          self.x -= 70
          self.y -= 50
        else:
          self.x += 70
          self.y -= 50
      self.attackCounter += 1
    else:
      if self.side == "left":
        self.x += 70
        self.y += 50
      else:
        self.x -= 70
        self.y += 50
      self.attackCounter = 0
  def jump(self):
    if self.attackCounter == 0:
      if self.y >= self.originalY and self.jumpCounter > 0:
        self.changeY = 0
        self.y = self.originalY
        self.jumpCounter = 0
      else:
        if self.jumpCounter == 0:
          self.changeY = -10
        self.jumpCounter += 1
        self.changeY += 0.5
    else:
      if (self.y >= self.originalY - 50) and (self.jumpCounter > 0):
        self.changeY = 0
        self.y = self.originalY - 50
        self.jumpCounter = 0
      else:
        if self.jumpCounter == 0:
          self.changeY = -10
        self.jumpCounter += 1
        self.changeY += 0.5

class Head(Player): 
  def __init__(self, x, y, width, height, screen):
    super().__init__(x, y, width, height, screen)
    
class Foot(Player):
  def __init__(self, x, y, width, height, side, screen):
    super().__init__(x, y, width, height, screen)
    self.side = side
    self.kickCounter = 0
    self.lenOfKick = 40
  def kick(self):
    if self.kickCounter < self.lenOfKick:
      if self.kickCounter == 0:
        if self.side == "left":
          self.x -= 140
          self.y -= 80
        else:
          self.x += 140
          self.y -= 80
      self.kickCounter += 1
    else:
      if self.side == "left":
        self.x += 140
        self.y += 80
      else:
        self.x -= 140
        self.y += 80
      self.kickCounter = 0
      
  def jump(self):
    if self.kickCounter == 0:
      if self.y >= self.originalY and self.jumpCounter > 0:
        self.changeY = 0
        self.y = self.originalY
        self.jumpCounter = 0
      else:
        if self.jumpCounter == 0:
          self.changeY = -10
        self.jumpCounter += 1
        self.changeY += 0.5
    else:
      if (self.y >= self.originalY - 80) and (self.jumpCounter > 0):
        self.changeY = 0
        self.y = self.originalY - 80
        self.jumpCounter = 0
      else:
        if self.jumpCounter == 0:
          self.changeY = -10
        self.jumpCounter += 1
        self.changeY += 0.5
  
class Platform():
  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height