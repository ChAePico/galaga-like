import pygame
from pygame.sprite import Sprite
import random
import math
from time import sleep, time

# 게임에 사용되는 전역 변수 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
pad_width = 480
pad_height = 640
boss_pad_width=1280
boss_pad_height=720
fight_width = 36
fight_height = 38
enemy_width = 26
enemy_height = 20
bestScore=0
finalScore=0
bossKill=0

def gameover():
    global gamepad
    global finalScore, bestScore
    if finalScore>=bestScore:
        bestScore=finalScore
    dispMessage('YOU DIED')

def fallen():
    global gamepad
    global gamepad

    font = pygame.font.Font("optimusprinceps\\OptimusPrincepsSemiBold.ttf", 50)
    text = font.render('Dragon Fallen', True, WHITE)
    gamepad.blit(text, (pad_width/2-180, pad_height/2))
    pygame.display.update()
    sleep(3)

# 적을 맞춘 개수 계산
def drawScore(count):
    global gamepad

    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Kills: ' + str(count), True, WHITE)
    gamepad.blit(text, (0, 0))

def drawBestScore(score):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Best Score: ' + str(score), True, WHITE)
    gamepad.blit(text, (pad_width/2-50, 0))

def drawPassed(count):
    global gamepad

    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Passed: ' + str(count), True, RED)
    gamepad.blit(text, (pad_width-120, 0))


# 화면에 글씨 보이게 하기
def dispMessage(text):
    global gamepad

    textfont = pygame.font.Font("optimusprinceps\\OptimusPrincepsSemiBold.ttf", 80)
    text = textfont.render(text, True, RED)    
    textpos = text.get_rect()
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()
    

# 게임에 등장하는 객체를 그려줌
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x,y))

# 개발 중지
# def bossBasic():
#     #보스 등장. 4명의 보스 랜덤. 4명 다 나오면 5번째 보스 등장. 
#     global gamepad
#     global pad_width, pad_height
#     pad_width=boss_pad_width
#     pad_height=boss_pad_height
#     gamepad=pygame.display.set_mode((pad_width, pad_height))
#     pass
        
class Player(object):
    def __init__(self):
        self.x=pad_width*0.45
        self.y=pad_height*0.87
        self.image=pygame.image.load('images\\fighter.png')
        self.hpImage=pygame.image.load("images\\health.png")
        self.spImage=pygame.image.load("images\\stamina.png")
        self.sp=25
        self.hp=300
        self.x_change=0
        self.y_change=0
        self.x_speed=5
        self.canJump=True
        self.acc=7
        self.charging=1
        self.hpPos=8
        self.use=0
        self.shield=40
        Player.bullet_xy=[]
    def draw(self):
        global gamepad
        gamepad.blit(self.image, (self.x, self.y))
    def moveInput(self, event):
        global startTime
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.x_change -= self.x_speed
            elif event.key == pygame.K_d:
                self.x_change += self.x_speed
            elif event.key==pygame.K_s:
                self.y_change += self.x_speed
            elif event.key==pygame.K_w:
                self.y_change -= self.x_speed
            elif event.key==pygame.K_SPACE:
                startTime=time()
            elif event.key==pygame.K_r:
                if self.use==0:
                    self.use=1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.x_change = 0
            elif event.key==pygame.K_w or event.key==pygame.K_s:
                self.y_change=0
            elif event.key==pygame.K_SPACE:
                delta=time()-startTime
                self.charging*=delta*10
                if self.charging<1:
                    self.charging=1
                elif self.charging>7:
                    self.charging=7
                
    def moveX(self):
        self.x+=self.x_change
        if self.x<0:
            self.x=0
        elif self.x>pad_width-fight_width:
            self.x=pad_width-fight_width
        
    # 미사용 코드
    # def moveY(self):
    #     self.y+=self.y_change
    #     if self.y<0:
    #         self.y=0
    #     elif self.y>pad_height*0.87:
    #         self.y=pad_height*0.87

    # 개발 중지
    # def jump(self):
    #     if self.canJump==True:
    #         self.canJump=False
    #     elif self.canJump==False:
    #         if self.y<pad_height*0.87+0.1:
    #             #self.image=pygame.image.load("")
    #             self.y-=self.acc
    #             self.acc-=2
    #         elif self.y>=pad_height*0.87:
    #             #self.image=pygame.image.load("")
    #             self.y=pad_height*0.87
    #             self.canJump=True
    #             self.acc=7
    #             self.acc*=self.charging
    #             self.charging=1
    def shoot(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sp>=5:                       
                bullet_x = self.x + fight_width/2 - 5
                bullet_y = self.y - fight_height/2
                Player.bullet_xy.append([bullet_x, bullet_y])
                self.sp-=5
        else:
            self.sp+=1
            if self.sp>25:
                self.sp=25
    def isCollide(self, enemy_x, enemy_y):
        check=False
        if enemy_y-enemy_height<self.y< enemy_y + enemy_height:
            if (enemy_x > self.x and enemy_x < self.x + fight_width) or (enemy_x + enemy_width > self.x and enemy_x+ enemy_width < self.x + fight_width):
                check=True
                self.hp-=20
        return check
    def playerUI(self):
        global gamepad
        pygame.draw.rect(gamepad, (255, 255, 255), (pad_width/2-150, pad_height*0.93, 303, 15), 2)
        pygame.draw.rect(gamepad, (255, 255, 255), (pad_width/2-150, pad_height*0.95, 303, 15), 2)
        for i in range(self.hp):
            gamepad.blit(self.hpImage, (pad_width/2-148+i, pad_height*0.935))
        for i in range(self.sp):
            gamepad.blit(self.spImage, (pad_width/2-148+i*12, pad_height*0.955))
        font = pygame.font.SysFont(None, 24)
        text = font.render('Flask: ' + str(self.hpPos), True, (255, 165, 0))
        gamepad.blit(text, (pad_width-80, pad_height*0.94))
    def youDied(self):
        if self.hp<=0:
            self.hp=300
            self.sp=25
            gameover()
    def plusHP(self):
        if self.use==1 and self.hpPos>0:
            self.hpPos-=1
            self.hp+=45
            if self.hp>300:
                self.hp=300
            self.use=0
        

class Enemy(object):
    def __init__(self):
        self.x=random.randrange(0, pad_width-enemy_width)
        self.y=40
        self.image=pygame.image.load('images\\enemy.png')
        self.speed=4
        self.isTracker=False
    def draw(self):
        global gamepad
        gamepad.blit(self.image, (self.x, self.y))
    def normalMove(self):
        self.speed=4
        self.y+=self.speed
    def trackingMove(self, player):
        self.speed=7
        dirvect=pygame.math.Vector2(player.x-self.x, player.y-self.y)
        dirvect.normalize()
        dirvect.scale_to_length(self.speed)
        self.x+=dirvect.x
        self.y+=dirvect.y

class Dragon(object):
    def __init__(self):
        self.x=pad_width/2-233/2
        self.y=70
        self.dragonImage=pygame.image.load("images\\dragon.png")
        self.thunder1=pygame.image.load("images\\thunder1.png")
        self.thunder2=pygame.image.load("images\\thunder2.png")
        self.thunder3=pygame.image.load("images\\thunder3.png")
        self.hpImage=pygame.image.load("images\\health.png")
        self.dragonHp=450
        self.speed=3
        self.leftWing=0
        self.rightWing=0
        self.leftDamage=6
        self.rightDamage=6
        self.attackCount=0
        Dragon.attack1s=[]
        Dragon.attack2s=[]
        Dragon.attack3s=[]
    def attack1(self):
        tx=self.x+233/2
        ty=173
        Dragon.attack1s.append([self.thunder1,tx,ty])
    def attack2(self):
        x1=self.x+233/2
        x2=x1-110
        x3=x1+110
        Dragon.attack2s.append([x1, x2, x3])
    def attack3(self):
        x4=self.x+233/2
        Dragon.attack3s.append([x4, 173])
    def move(self):
        moveX=random.uniform(-1, 1)
        self.x+=moveX*10
        if self.x<0:
            self.x=0
        elif self.x>pad_width-233:
            self.x=pad_width-233
    def draw(self):
        global gamepad
        gamepad.blit(self.dragonImage, (self.x, self.y))
    def drawEffect(self, imageee, x, y):
        global gamepad
        gamepad.blit(imageee, (x, y))
    def dragonUI(self):
        global gamepad
        pygame.draw.rect(gamepad, (255, 255, 255), (pad_width/2-225, 30, 453, 13), 2)
        for i in range(self.dragonHp):
            gamepad.blit(self.hpImage, (pad_width/2-223+i, 32))
    def breakWing(self):
        global finalScore
        if self.leftWing>=15 and self.rightWing<15:
            self.leftDamage=10
            self.dragonImage=pygame.image.load("images\\dragonLeft.png")
            finalScore+=20
        elif self.rightWing>=15 and self.leftWing<15:
            self.rightDamage=10
            self.dragonImage=pygame.image.load("images\\dragonRight.png")
            finalScore+=20
        elif self.leftWing>=15 and self.rightWing>=15:
            self.leftDamage=10
            self.rightDamage=10
            self.dragonImage=pygame.image.load("images\\dragonBoth.png")
            finalScore+=50
    def win(self):
        if self.dragonHp<=0:
            self.dragonHp=450
            self.dragonImage=pygame.image.load("images\\dragon.png")
            self.leftWing=0
            self.rightWing=0
            fallen()
            return True

# 개발 중지
# class Solar(object):
#     def __init__(self):
#         self.x=pad_width-141
#         self.y=pad_height*0.87-147
#         self.image=pygame.image.load("images\\solar.png")
#         self.effect=pygame.image.load("images\\attack1.png")
#         self.lengthEffect=0 #0~16
#         self.effects=[]
#         self.effectY=pad_height*0.8
#     def attack1(self, player):
#         global gamepad
#         self.effect=pygame.image.load("images\\attack1.png")
#         self.lengthEffect+=1
#         for i in range(self.lengthEffect):
#             gamepad.blit(self.effect, (pad_width-80-i*80, self.effectY))
#         pygame.display.update()
#         clock.tick(60)
#     def draw(self):
#         global gamepad
#         gamepad.blit(self.image, (self.x, self.y))

# 게임 실행 메인 함수
def runGame():
    global gamepad, fighter, clock, dragon
    global bullet    
    global finalScore, bossKill
    #isShot = False
    shotcount = 0
    enemypassed = 0

    enemies=[]

    regenCount=0
    bossClock=0
    isBoss=False
    bossKill=0

    finalScore=0
        
    ongame = False
    while not ongame:
        regenCount+=1
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                ongame = True

            fighter.shoot(event)
            fighter.moveInput(event)

        gamepad.fill(BLACK)

        if regenCount==50 and isBoss==False:
            regenCount=0
            enemies.append(Enemy())
            if random.randint(0, 1)==1:
                enemies[-1].isTracker=True

        fighter.moveX()
        # if isBoss==True:
        #     fighter.x_speed=10
        #     fighter.jump()
        # elif isBoss==False:
        fighter.y=pad_height*0.87
        
        for enemy in enemies:
            if enemies:
                if enemy.isTracker==True:
                    enemy.trackingMove(fighter)
                else:
                    enemy.normalMove()
                enemy.draw()
                col=fighter.isCollide(enemy.x, enemy.y)
                if col==True:
                    enemies.remove(enemy)
                    finalScore-=5
                if col==False and enemy.y>pad_height*0.89:
                    enemies.remove(enemy)
                    enemypassed+=1
                    fighter.hp-=4
                    finalScore-=3
        fighter.plusHP()
        fighter.youDied()
        
        fighter.draw()

        fighter.playerUI()
        
       # 전투기 무기 발사 구현
        if len(Player.bullet_xy) != 0:
            for i, bxy in enumerate(Player.bullet_xy):
                bxy[1] -= 10
                Player.bullet_xy[i][1] = bxy[1]

                for enemy in enemies:
                    if bxy[1]<enemy.y:
                        if bxy[0]>enemy.x and bxy[0]<enemy.x+enemy_width:
                            Player.bullet_xy.remove(bxy)
                            shotcount+=1
                            finalScore+=10
                            enemies.remove(enemy)
                
                if isBoss==True:
                    if (dragon.x<=bxy[0]<=59+dragon.x):
                        if bxy[1]<dragon.y+87:
                            dragon.leftWing+=1
                            dragon.dragonHp-=dragon.leftDamage
                            Player.bullet_xy.remove(bxy)
                    if (dragon.x+178<=bxy[0]<=dragon.x+232):
                        if bxy[1]<dragon.y+87:
                            dragon.rightWing+=1
                            dragon.dragonHp-=dragon.rightDamage
                            Player.bullet_xy.remove(bxy)
                    if (dragon.x+59<bxy[0]<dragon.x+110):
                        if bxy[1]<dragon.y+76:
                            dragon.leftWing+=1
                            dragon.dragonHp-=dragon.leftDamage*2
                            Player.bullet_xy.remove(bxy)
                    if (dragon.x+125<bxy[0]<dragon.x+178):
                        if bxy[1]<dragon.y+76:
                            dragon.rightWing+=1
                            dragon.dragonHp-=dragon.rightDamage*2
                            Player.bullet_xy.remove(bxy)
                    if (dragon.x+110<=bxy[0]<=dragon.x+125):
                        if bxy[1]<dragon.y+84:
                            dragon.dragonHp-=25
                            Player.bullet_xy.remove(bxy)

                if bxy[1] <= 0:
                    try:
                        Player.bullet_xy.remove(bxy)
                    except:
                        pass

        if len(Player.bullet_xy) != 0:
            for bx, by in Player.bullet_xy:
                drawObject(bullet, bx, by)
        if shotcount>0 and shotcount%30==0:
            bossClock+=1
            regenCount=0
            enemies.clear()
            dragon.move()
            dragon.draw()
            dragon.dragonUI()
            dragon.breakWing()
            #if bossClock==30:
            if bossClock>=45-bossKill*6:
                chooseA=random.randint(0, 2)
                Dragon.attack2s.clear()
                if chooseA==0:
                    if len(Dragon.attack1s)<2:
                        dragon.attack1()
                elif chooseA==1:
                    dragon.attack2()
                elif chooseA==2:
                    if len(Dragon.attack3s)==0:
                        dragon.attack3()
                bossClock=0
            if Dragon.attack1s:
                for i, tdr in enumerate(Dragon.attack1s):
                    dirvect=pygame.math.Vector2(fighter.x-tdr[1], fighter.y-tdr[2])
                    dirvect.normalize()
                    dirvect.scale_to_length(dragon.speed)
                    tdr[1]+=dirvect.x
                    tdr[2]+=dragon.speed
                    Dragon.attack1s[i][1] = tdr[1]
                    Dragon.attack1s[i][2] = tdr[2]
                    if tdr[2]>fighter.y:
                        if tdr[1]>fighter.x-30 and tdr[1]<fighter.x+fight_width-10:
                            Dragon.attack1s.remove(tdr)
                            fighter.hp-=25
                    if tdr[2]>pad_height*0.89:
                        try:
                            Dragon.attack1s.remove(tdr)
                        except:
                            pass
            if Dragon.attack1s:
                for attt in Dragon.attack1s:
                    dragon.drawEffect(attt[0], attt[1], attt[2])
            if Dragon.attack2s:
                for laser in Dragon.attack2s:
                    if laser[0]<fighter.x+fight_width and fighter.x<laser[0]+10:
                        fighter.hp-=2
                    if laser[1]<fighter.x+fight_width and fighter.x<laser[1]+10:
                        fighter.hp-=1
                    if laser[2]<fighter.x+fight_width and fighter.x<laser[2]+10:
                        fighter.hp-=1
            if Dragon.attack2s:
                for att2 in Dragon.attack2s:
                    dragon.drawEffect(dragon.thunder2, att2[0], 173)
                    dragon.drawEffect(dragon.thunder2, att2[1], 173)
                    dragon.drawEffect(dragon.thunder2, att2[2], 173)
            if Dragon.attack3s:
                for i, atk3 in enumerate(Dragon.attack3s):
                    atk3[1]+=8
                    Dragon.attack3s[i][1]=atk3[1]
                    if atk3[1]>fighter.y:
                        if atk3[0]>fighter.x-25 and atk3[0]<fighter.x+fight_width:
                            Dragon.attack3s.remove(atk3)
                            fighter.hp-=40
                    if atk3[1]>pad_height*0.90:
                        try:
                            Dragon.attack3s.remove(atk3)
                        except:
                            pass
            if Dragon.attack3s:
                for attt in Dragon.attack3s:
                    dragon.drawEffect(dragon.thunder3, attt[0], attt[1])
            isBoss=True
            #bossBasic()
            if dragon.win()==True:
                isBoss=False
                finalScore+=200
                fighter.hpPos=8
                fighter.hp=300
                shotcount+=1
                bossKill+=1

        drawScore(shotcount)
        drawPassed(enemypassed)
        drawBestScore(bestScore)
        pygame.display.update()
        clock.tick(60)


    pygame.quit()

def initGame():
    global gamepad, fighter, clock, dragon
    global bullet, enemy

    pygame.init()
    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('MyGalaga')
    fighter=Player()
    dragon=Dragon()
    bullet = pygame.image.load('images\\bullet.png')
    clock = pygame.time.Clock()   


initGame()
runGame()