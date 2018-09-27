import pygame
import math
import random
pygame.init()
pygame.mixer.init()

vector = pygame.math.Vector2

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Last Stand")
soundBG = pygame.mixer.Sound("Sprites\SoundBG.wav")
soundShot = pygame.mixer.Sound("Sprites\TripleShot.ogg")
def makeTextObjects(text,font):
    textSurf = font.render(text,True,(255,255,255))
    return textSurf, textSurf.get_rect()
def waveMessage(text):
    smallFont = pygame.font.SysFont("Arial", 30)
    textSurf, textRect = makeTextObjects(text,smallFont)
    textRect.x = 50
    textRect.y = 15
    screen.blit(textSurf, textRect)
def goldMessage(text):
    smallFont = pygame.font.SysFont("Arial", 30)
    textSurf, textRect = makeTextObjects(text,smallFont)
    textRect.x = 50
    textRect.y = 53
    screen.blit(textSurf,textRect)
def copyrightMessage(text):
    smallFont = pygame.font.SysFont("Arial", 15)
    textSurf, textRect = makeTextObjects(text,smallFont)
    textRect.x = 5
    textRect.y = 580
    screen.blit(textSurf,textRect)
def controlMessage(text):
    smallFont = pygame.font.SysFont("Arial", 25)
    textSurf, textRect = makeTextObjects(text,smallFont)
    textRect.x = 640
    textRect.y = 550
    screen.blit(textSurf,textRect)
class Player(pygame.sprite.Sprite):
    equipment = ["Gun","Tower","Wall","Mine"]
    equipmentCounter = 1
    equipmentImage = []
    soldier = []
    soldierCounter = 1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.soldier[0]
        self.original = self.image
        self.position = vector(100,100)
        self.rect = self.image.get_rect(center=self.position)
        self.life = 100
        self.angle = 0
        self.shoot = 0
        self.last = pygame.time.get_ticks()
        self.cooldown = 100
        self.lastTower = pygame.time.get_ticks()
        self.towerCooldown = 500
        self.lastWall = pygame.time.get_ticks()
        self.wallCooldown = 500
        self.lastMine = pygame.time.get_ticks()
        self.mineCooldown = 500
        self.gold = 10000
        self.towerCost = 1000
        self.wallCost = 100
        self.mineCost = 500
        self.hand = self.equipment[0]
        self.equipImage = self.equipmentImage[0]
    def update(self):
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_w]:
            self.position[1] -= 5
            self.image = self.soldier[self.soldierCounter]
            self.soldierCounter = (self.soldierCounter + 1) % len(self.soldier)
            self.original = self.image
            self.rotate()
        if keypress[pygame.K_s]:
            self.position[1] += 5
            self.image = self.soldier[self.soldierCounter]
            self.soldierCounter = (self.soldierCounter + 1) % len(self.soldier)
            self.original = self.image
            self.rotate()
        if keypress[pygame.K_a]:
            self.position[0] -= 5
            self.image = self.soldier[self.soldierCounter]
            self.soldierCounter = (self.soldierCounter + 1) % len(self.soldier)
            self.original = self.image
            self.rotate()
        if keypress[pygame.K_d]:
            self.position[0] += 5
            self.image = self.soldier[self.soldierCounter]
            self.soldierCounter = (self.soldierCounter + 1) % len(self.soldier)
            self.original = self.image
            self.rotate()
        if self.position[0] < 0:
            self.position[0] = 0
        if self.position[0] > screen.get_width():
            self.position[0] = screen.get_width()
        if self.position[1] < 0:
            self.position[1] = 0
        if self.position[1] > screen.get_height():
            self.position = screen.get_height()
        self.rect.center = self.position
    def rotate(self):
        self.mouseX,self.mouseY = pygame.mouse.get_pos()
        run,rise = (self.mouseX - self.rect.center[0],self.mouseY - self.rect.center[1])
        self.angle = math.degrees(math.atan2(rise,run)) + 90
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def health(self):
        self.bar_length = 100
        self.bar_height = 10

        if self.life < 0:
            self.life = 0
        self.fill = (self.life / 100) * self.bar_length
        self.fill_outline = pygame.Rect(self.rect.center[0]-50,self.rect.center[1]-80,self.fill,self.bar_height)
    def buy(self,cost):
        return self.gold - cost
    def change(self):
        self.hand = self.equipment[self.equipmentCounter]
        self.equipImage = self.equipmentImage[self.equipmentCounter]
        self.equipmentCounter = (self.equipmentCounter + 1) % len(self.equipment)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,position,angle):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Bullet.png"),(16,16))
        self.original = self.image
        self.position = position
        self.speed = 5
        self.rect = self.image.get_rect(center=self.position)
        self.velocityX = math.cos(math.radians(angle - 90)) * self.speed
        self.velocityY = math.sin(math.radians(angle - 90)) * self.speed
        self.image = pygame.transform.rotate(self.original,-angle)
    def update(self):
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY
        if self.rect.x < 0:
            self.kill()
        if self.rect.x > screen.get_width():
            self.kill()
        if self.rect.y < 0:
            self.kill()
        if self.rect.y > screen.get_height():
            self.kill()
class Castle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Tent.png"),(200,200))
        self.position = vector(screen.get_width() / 2, screen.get_height() / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.life = 5000
    def health(self):
        self.bar_length = 120
        self.bar_height = 10

        if self.life < 0:
            self.life = 0

        self.fill = (self.life / 2500) * self.bar_length
        self.fill_outline = pygame.Rect(self.rect.center[0]-122,self.rect.center[1]-120,self.fill,self.bar_height)
        pygame.draw.rect(screen,(0,255,0),self.fill_outline)
class Enemy(pygame.sprite.Sprite):
    direction = "None"
    def __init__(self,castleX,castleY):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Zombie.gif"),(32,32))
        self.original = self.image
        self.indicator = random.randrange(1,5)
        if self.indicator == 1:
            self.direction = "North"
        if self.indicator == 2:
            self.direction = "South"
        if self.indicator == 3:
            self.direction = "West"
        if self.indicator == 4:
            self.direction = "East"
        if self.direction == "North":
            self.position = vector(random.randrange(0,screen.get_width()),0)
        if self.direction == "South":
            self.position = vector(random.randrange(0,screen.get_width()),screen.get_height())
        if self.direction == "West":
            self.position = vector(0,random.randrange(0,screen.get_height()))
        if self.direction == "East":
            self.position = vector(screen.get_width(),random.randrange(0,screen.get_height()))
        self.rect = self.image.get_rect(center=self.position)
        self.castleX = castleX
        self.castleY = castleY
        self.life = 300
        self.damage = 5
        self.lastAttack = pygame.time.get_ticks()
        self.attackCooldown = 300
        self.enemyGold = random.randrange(50,70)
        self.speed = 0.7
    def move_castle(self):
        if self.rect.center[0] < self.castleX:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed
        if self.rect.center[1] < self.castleY:
            self.position[1] += self.speed
        else:
            self.position[1] -= self.speed
        self.rect.center = self.position
    def rotate_castle(self):
        run,rise = (self.castleX - self.rect.center[0],self.castleY - self.rect.center[1])
        self.angle = math.degrees(math.atan2(rise,run)) + 90
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def health(self):
        self.bar_length = 100
        self.bar_height = 5

        if self.life < 0:
            self.life = 0

        self.fill = (self.life / 300) * self.bar_length
        self.fill_outline = pygame.Rect(self.rect.center[0]-50,self.rect.center[1]-50,self.fill,self.bar_height)
        pygame.draw.rect(screen,(255,0,0),self.fill_outline)
    def attack(self,attackLife):
        return attackLife - self.damage
    def move_attack(self,position):
        if self.rect.center[0] < position[0]:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed
        if self.rect.center[1] < position[1]:
            self.position[1] += self.speed
        else:
            self.position[1] -= self.speed
        run, rise = (position[0] - self.rect.center[0],position[1] - self.rect.center[1])
        self.angle = math.degrees(math.atan2(rise,run)) + 90
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
class Boss(pygame.sprite.Sprite):
    direction = "None"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Boss.gif"),(64,64))
        self.original = self.image
        self.indicator = random.randrange(1,5)
        if self.indicator == 1:
            self.direction = "North"
        if self.indicator == 2:
            self.direction = "South"
        if self.indicator == 3:
            self.direction = "West"
        if self.indicator == 4:
            self.direction = "East"
        if self.direction == "North":
            self.position = vector(random.randrange(0,screen.get_width()),0)
        if self.direction == "South":
            self.position = vector(random.randrange(0,screen.get_width()),screen.get_height())
        if self.direction == "West":
            self.position = vector(0,random.randrange(0,screen.get_height()))
        if self.direction == "East":
            self.position = vector(screen.get_width(),random.randrange(0,screen.get_height()))
        self.rect = self.image.get_rect(center=self.position)
        self.life = 1000
        self.damage = 10
        self.lastAttack = pygame.time.get_ticks()
        self.attackCooldown = 500
        self.bossGold = random.randrange(250,500)
        self.speed = 0.5
    def move_castle(self,castleX,castleY):
        if self.rect.center[0] < castleX:
            self.position[0] += self.speed
        else:
            self.position[0] -= self.speed
        if self.rect.center[1] < castleY:
            self.position[1] += self.speed
        else:
            self.position[1] -= self.speed
        self.rect.center = self.position

        run,rise = (castleX - self.rect.center[0],castleY - self.rect.center[1])
        self.angle = math.degrees(math.atan2(rise,run)) + 90
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def move_attack(self,position):
        if self.rect.center[0] < position[0]:
            self.position[0] += 0.1
        else:
            self.position[0] -= 0.1
        if self.rect.center[1] < position[1]:
            self.position[1] += 0.1
        else:
            self.position[1] -= 0.1
        self.rect.center = self.position
        run,rise = (position[0] - self.rect.center[0],position[1] - self.rect.center[1])
        self.angle = math.degrees(math.atan2(rise,run)) + 90
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def attack(self,attackLife):
        return attackLife - self.damage
    def health(self):
        self.bar_length = 100
        self.bar_height = 10

        if self.life < 0:
            self.life = 0

        self.fill = (self.life / 1000) * self.bar_length
        self.fill_outline = pygame.Rect(self.rect.center[0]-50, self.rect.center[1]-50, self.fill, self.bar_height)
        pygame.draw.rect(screen,(255,0,0),self.fill_outline)
class Tower(pygame.sprite.Sprite):
    def __init__(self,position,angle):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\CannonTower.png"),(32,32))
        self.original = self.image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
        self.angle_speed = 1
        self.last = pygame.time.get_ticks()
        self.cooldown = 500
        self.life = 500
    def update(self):
        self.angle += self.angle_speed
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.life == 0:
            self.kill()
    def health(self):
        self.bar_length = 100
        self.bar_height = 10

        if self.life < 0:
            self.life = 0

        self.fill = (self.life / 500) * self.bar_length
        self.fill_outline = pygame.Rect(self.rect.center[0]-50,self.rect.center[1]-50,self.fill,self.bar_height)
        pygame.draw.rect(screen,(0,255,0),self.fill_outline)
class Missile(pygame.sprite.Sprite):
    def __init__(self,position,angle):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Missle.png"),(16,16))
        self.original = self.image
        self.position = position
        self.speed = 5
        self.rect = self.image.get_rect(center=self.position)
        self.velocityX = math.cos(math.radians(angle - 90)) * self.speed
        self.velocityY = math.sin(math.radians(angle - 90)) * self.speed
        self.image = pygame.transform.rotate(self.original,-angle)
    def update(self):
        self.rect.x += self.velocityX
        self.rect.y += self.velocityY
        if self.rect.x < 0:
            self.kill()
        if self.rect.x > screen.get_width():
            self.kill()
        if self.rect.y < 0:
            self.kill()
        if self.rect.y > screen.get_height():
            self.kill()
class Wall(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Wall.png"),(32,32))
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
        self.life = 1000
    def update(self):
        if self.life == 0:
            self.kill()
    def health(self):
        self.bar_length = 100
        self.bar_height = 10

        if self.life < 0:
            self.life = 0

        self.fill = (self.life / 1000) * self.bar_length
        self.fill_outline = pygame.Rect(self.rect.center[0]-50,self.rect.center[1]-50,self.fill,self.bar_height)
        pygame.draw.rect(screen,(0,255,0),self.fill_outline)

class Landmine(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.transform.scale(pygame.image.load("Sprites\Landmine.png"),(24,24))
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
        self.damage = 500
class Wave():
    def __init__(self):
        self.enemies = 20
        self.boss = 1
        self.bossSpawn = 5
        self.addBoss = 20
        self.wave = 0
        self.enemiesSpawn = 0
        self.enemiesKilled = 0
        self.bossKilled = 0
def Menu():
    global start, instruct, cancel
    keepGoing = True
    clock = pygame.time.Clock()
    backgroundImage = pygame.transform.scale(pygame.image.load("Sprites\MenuBG.jpg"),(800,600))
    startButton = pygame.transform.scale(pygame.image.load("Sprites\Play.png"),(200,50))
    instructionImage = pygame.transform.scale(pygame.image.load("Sprites\Controller.png"), (64,64))
    cancelImage = pygame.transform.scale(pygame.image.load("Sprites\Cancel.png"),(32,32))
    soundBG.play(-1)
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start.collidepoint(event.pos):
                    soundBG.stop()
                    Game()
                if instruct.collidepoint(event.pos):
                    soundBG.stop()
                    Instruction()
                if cancel.collidepoint(event.pos):
                    keepGoing = False
                    pygame.quit()
                    quit()
        screen.blit(backgroundImage,[0,0])
        start = screen.blit(startButton, (310,430))
        instruct = screen.blit(instructionImage, (720,535))
        cancel = screen.blit(cancelImage, (760,15))
        copyrightMessage("(c) Copyright Disclaimer. Credits to all images owner.")
        controlMessage("Controls");
        pygame.display.flip()
        clock.tick(60)
def Gameover():
    global tryAgain, home
    keepGoing = True
    clock = pygame.time.Clock()
    backgroundImage = pygame.transform.scale(pygame.image.load("Sprites\GameoverBG.jpg"), (800, 600))
    homeImage = pygame.transform.scale(pygame.image.load("Sprites\Home.png"),(48,48))
    restartImage = pygame.transform.scale(pygame.image.load("Sprites\Restart.png"),(48,48))
    soundBG.play(-1)
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if tryAgain.collidepoint(event.pos):
                    soundBG.stop()
                    Game()
                if home.collidepoint(event.pos):
                    soundBG.stop()
                    Menu()
        screen.blit(backgroundImage, [0, 0])
        tryAgain = screen.blit(restartImage,(610,330))
        home = screen.blit(homeImage,(670,330))
        copyrightMessage("(c) Copyright Disclaimer. Credits to all images owner.")
        pygame.display.flip()
        clock.tick(60)
def Instruction():
    global back
    keepGoing = True
    clock = pygame.time.Clock()
    backgroundImage = pygame.transform.scale(pygame.image.load("Sprites\InstructBG.jpg"), (800, 600))
    backImage = pygame.transform.scale(pygame.image.load("Sprites\Back.png"), (64,64))
    soundBG.play(-1)
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    soundBG.stop()
                    Game()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back.collidepoint(event.pos):
                    soundBG.stop()
                    Menu()
        screen.blit(backgroundImage, [0, 0])
        back = screen.blit(backImage,(720,525))
        copyrightMessage("(c) Copyright Disclaimer. Credits to all images owner.")
        pygame.display.flip()
        clock.tick(60)
def Game():
    global back
    keepGoing = True
    clock = pygame.time.Clock()
    bullets = pygame.sprite.Group()
    missiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    landmines = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    allSprite = pygame.sprite.RenderUpdates()
    backgroundImage = pygame.transform.scale(pygame.image.load("Sprites\Background.png"),(800,600))
    backImage = pygame.transform.scale(pygame.image.load("Sprites\Back.png"), (32, 32))
    Castle.containers = allSprite
    Player.containers = allSprite
    Bullet.containers = allSprite, bullets
    Enemy.containers = allSprite, enemies
    Tower.containers = allSprite, towers
    Wall.containers = allSprite, walls
    Landmine.containers = allSprite, landmines
    Boss.containers = allSprite, bosses
    Missile.containers = allSprite, missiles

    Player.equipmentImage.append(pygame.image.load("Sprites/rifle.png"))
    Player.equipmentImage.append(pygame.image.load("Sprites\cannon.png"))
    Player.equipmentImage.append(pygame.image.load("Sprites/brick.png"))
    Player.equipmentImage.append(pygame.transform.scale(pygame.image.load("Sprites\Landmine.png"),(24,24)))
    Player.soldier.append(pygame.transform.scale(pygame.image.load("Sprites\soldier1.png"),(64,64)))
    Player.soldier.append(pygame.transform.scale(pygame.image.load("Sprites\soldier2.png"),(64,64)))
    Player.soldier.append(pygame.transform.scale(pygame.image.load("Sprites\soldier3.png"),(64,64)))
    castle = Castle()
    player = Player()
    waveImage = pygame.image.load("Sprites\Skull.png")
    treasureImage = pygame.transform.scale(pygame.image.load("Sprites\Treasure.png"),(24,24))
    handImage = pygame.transform.scale(pygame.image.load("Sprites\Hand.png"),(24,24))

    wave = Wave()
    soundBG.play(-1)
    soundBG.set_volume(0.3)
    while keepGoing:
        if castle.life == 0:
            soundBG.stop()
            Gameover()
        if player.life == 0:
            soundBG.stop()
            Gameover()
        now = pygame.time.get_ticks()
        keypress = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot = 1
                if back.collidepoint(event.pos):
                    soundBG.stop()
                    Menu()
            if event.type == pygame.MOUSEBUTTONUP:
                player.shoot = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.change()
                if event.key == pygame.K_ESCAPE:
                    soundBG.stop()
                    Menu()
        screen.fill((255,255,255))
        screen.blit(backgroundImage,(0,0))
        screen.blit(waveImage,(20,20))
        screen.blit(treasureImage,(20,60))
        screen.blit(handImage,(20,100))
        screen.blit(player.equipImage,(50,100))
        back = screen.blit(backImage, (750, 550))
        waveMessage(str(wave.wave + 1))
        goldMessage(str(player.gold))
        copyrightMessage("(c) Copyright Disclaimer. Credits to all images owner.")
        castle.health()
        player.health()
        pygame.draw.rect(screen, (0, 255, 0), player.fill_outline)
        player.rotate()
        if keypress[pygame.K_n]:
            if wave.enemiesSpawn != wave.enemies:
                for x in range(0,wave.enemies):
                    enemies.add(Enemy(castle.rect.center[0], castle.rect.center[1]))
                    wave.enemiesSpawn += 1
                if wave.wave + 1 == wave.bossSpawn:
                    wave.bossSpawn += 5
                    if wave.wave + 1 == wave.addBoss:
                        wave.addBoss += 20
                        wave.boss += 1
                    for x in range(0,wave.boss):
                        bosses.add(Boss())
            if wave.enemiesKilled == wave.enemies:
                wave.enemiesSpawn = 0
                wave.enemiesKilled = 0
                wave.enemies += 2
                wave.wave += 1
        for enemy in enemies:
            enemy.move_castle()
            enemy.rotate_castle()
            enemy.health()
            if enemy.life == 0:
                player.gold += enemy.enemyGold
                enemy.kill()
                wave.enemiesKilled += 1
        for boss in bosses:
            boss.health()
            boss.move_castle(castle.rect.center[0],castle.rect.center[1])
            if boss.life == 0:
                boss.kill()
                wave.bossKilled += 1
        if player.shoot:
            if player.hand == "Gun":
                if now - player.last >= player.cooldown:
                    soundShot.play()
                    soundShot.set_volume(1);
                    player.last = now
                    bullets.add(Bullet(player.rect.center,player.angle))
        if keypress[pygame.K_SPACE]:
            if player.hand == "Tower":
                if player.gold >= player.towerCost:
                    if now - player.lastTower >= player.towerCooldown:
                        player.lastTower = now
                        towers.add(Tower(player.rect.center,player.angle))
                        player.gold = player.buy(player.towerCost)
            if player.hand == "Wall":
                if player.gold >= player.wallCost:
                    if now - player.lastWall >= player.wallCooldown:
                        player.lastWall = now
                        walls.add(Wall(player.rect.center))
                        player.gold = player.buy(player.wallCost)
            if player.hand == "Mine":
                if player.gold >= player.mineCost:
                    if now - player.lastMine >= player.mineCooldown:
                        player.lastMine = now
                        landmines.add(Landmine(player.rect.center))
                        player.gold = player.buy(player.mineCost)
        for bullet in bullets:
            for enemy in pygame.sprite.spritecollide(bullet,enemies,0):
                bullet.kill()
                enemy.life -= 10
            for boss in pygame.sprite.spritecollide(bullet,bosses,0):
                bullet.kill()
                boss.life -= 10
        for missile in missiles:
            for enemy in pygame.sprite.spritecollide(missile,enemies,0):
                missile.kill()
                enemy.life -= 15
            for boss in pygame.sprite.spritecollide(missile,bosses,0):
                missile.kill()
                boss.life -= 15
        for tower in towers:
            towerNow = pygame.time.get_ticks()
            if towerNow - tower.last >= tower.cooldown:
                tower.last = towerNow
                missiles.add(Missile(tower.rect.center,tower.angle))
        for tower in towers:
            for enemy in pygame.sprite.spritecollide(tower,enemies,0):
                if now - enemy.lastAttack >= enemy.attackCooldown:
                    enemy.lastAttack = now
                    tower.life = enemy.attack(tower.life)
                tower.health()
                enemy.move_attack(tower.rect.center)
            for boss in pygame.sprite.spritecollide(tower,bosses,0):
                if now - boss.lastAttack >= boss.attackCooldown:
                    boss.lastAttack = now
                    tower.life = boss.attack(tower.life)
                tower.health()
                enemy.move_attack(tower.rect.center)
        for wall in walls:
            for enemy in pygame.sprite.spritecollide(wall,enemies,0):
                if now - enemy.lastAttack >= enemy.attackCooldown:
                    enemy.lastAttack = now
                    wall.life = enemy.attack(wall.life)
                wall.health()
                enemy.move_attack(wall.rect.center)
            for boss in pygame.sprite.spritecollide(wall,bosses,0):
                if now - boss.lastAttack >= boss.attackCooldown:
                    boss.lastAttack = now
                    wall.life = boss.attack(wall.life)
                wall.health()
                boss.move_attack(wall.rect.center)
        for mine in landmines:
            for enemy in pygame.sprite.spritecollide(mine,enemies,0):
                enemy.life -= mine.damage
                mine.kill()
            for boss in pygame.sprite.spritecollide(mine,bosses,0):
                boss.life -= mine.damage
                mine.kill()
        for enemy in pygame.sprite.spritecollide(castle,enemies,0):
            if now - enemy.lastAttack >= enemy.attackCooldown:
                enemy.lastAttack = now
                castle.life = enemy.attack(castle.life)
        for enemy in pygame.sprite.spritecollide(player,enemies,0):
            if now - enemy.lastAttack >= enemy.attackCooldown:
                enemy.lastAttack = now
                player.life = enemy.attack(player.life)
            enemy.move_attack(player.rect.center)
        for boss in pygame.sprite.spritecollide(player,bosses,0):
            if now - boss.lastAttack >= boss.attackCooldown:
                boss.lastAttack = now
                player.life = boss.attack(player.life)
            boss.move_attack(player.rect.center)
        for boss in pygame.sprite.spritecollide(castle,bosses,0):
            if now - boss.lastAttack >= boss.attackCooldown:
                boss.lastAttack = now
                castle.life = boss.attack(castle.life)
        allSprite.update()
        allSprite.draw(screen)
        pygame.display.flip()
        clock.tick(60)
Menu()
pygame.quit()