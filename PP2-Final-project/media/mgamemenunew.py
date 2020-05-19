import pygame
import random
import time
import uuid
import json
import pika
from threading import Thread       
from pygame.locals import *
import os
from datetime import datetime 
myname='Bauyrzhan'
pygame.init()
width=1000
height=800
screen = pygame.display.set_mode((width, height))
wallImage=pygame.image.load('wall.jpg')
wall_range=20
eu=pygame.image.load('media\\eu.png')
ed=pygame.image.load('media\\ed.png')
el=pygame.image.load('media\\el.png')
er=pygame.image.load('media\\er.png')
tu=pygame.image.load('media\\tu.png')
td=pygame.image.load('media\\td.png')
tl=pygame.image.load('media\\tl.png')
tr=pygame.image.load('media\\tr.png')
bu=pygame.image.load('media\\bu.png')
bd=pygame.image.load('media\\bd.png')
bl=pygame.image.load('media\\bl.png')
br=pygame.image.load('media\\br.png')
fuelImage=pygame.image.load('media\\fuel.png')
desertimage1=pygame.image.load('media\\desert1000-800.jpg')
desertimage2=pygame.image.load('media\\desert2-800-600.png')
#pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play()

#pulyaSound=pygame.mixer.Sound('pulya.wav')
#vzryvSound=pygame.mixer.Sound('vzryv.wav')

class Tank:

    def __init__(self, x, y, color, ID=myname,nick='7879789798987'):
        self.id=ID
        self.nick=nick
        self.x = x
        self.y = y
        self.health=3
        self.score=0
        self.speed = 5
        self.color = color
        self.width = 40
        self.height= 40
        self.direction = 'RIGHT'
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def draw(self):
        '''tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.width), 2)
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

        if self.direction == 'RIGHT':
            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction == 'LEFT':
            pygame.draw.line(screen, self.color, tank_c, (
            self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)

        if self.direction =='UP':
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)

        if self.direction == 'DOWN':
            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)'''
        tanksurf = pygame.Surface((40, 40))
        tanksurf.set_colorkey((0,0,0))
        if self.id==self.nick:
            if self.direction=='UP':
                tanksurf.blit(tu,(0,0))
            if self.direction=='DOWN':
                tanksurf.blit(td,(0,0))
            if self.direction=='RIGHT':
                tanksurf.blit(tr,(0,0))
            if self.direction=='LEFT':
                tanksurf.blit(tl,(0,0))
        else:
            if self.direction=='UP':
                tanksurf.blit(eu,(0,0))
            if self.direction=='DOWN':
                tanksurf.blit(ed,(0,0))
            if self.direction=='RIGHT':
                tanksurf.blit(er,(0,0))
            if self.direction=='LEFT':
                tanksurf.blit(el,(0,0))
                
        screen.blit(tanksurf, (self.x, self.y))


    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        if self.direction == "LEFT":
            self.x -= self.speed
        if self.direction == "RIGHT":
            self.x += self.speed
        if self.direction == "UP":
            self.y -= self.speed
        if self.direction == 'DOWN':
            self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.draw()
    
class Pulya:
    def __init__(self,x=0,y=0,color=(80,255,30),direction='LEFT',speed=8):
        self.id=myname
        self.x=x
        self.y=y
        self.color=color
        self.speed=speed
        self.direction=direction
        self.status=True
        self.distance=0
        self.radius=7
        self.rect = pygame.Rect(self.x, self.y, 13, 13)

    def move(self):
        if self.direction == 'LEFT':
            self.x -= self.speed
        if self.direction == 'RIGHT':
            self.x += self.speed
        if self.direction == 'UP':
            self.y -= self.speed
        if self.direction == 'DOWN':
            self.y += self.speed
        self.distance+=1
        if self.distance>1200:
            self.status=False
        self.draw()

    def draw(self):
        if self.status==True:
            #pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
            bulletsurf = pygame.Surface((19, 19))
            bulletsurf.set_colorkey((0,0,0))
            if self.direction=='UP':
                bulletsurf.blit(bu,(0,0))
            if self.direction=='DOWN':
                bulletsurf.blit(bd,(0,0))
            if self.direction=='RIGHT':
                bulletsurf.blit(br,(0,0))
            if self.direction=='LEFT':
                bulletsurf.blit(bl,(0,0))
            self.rect = pygame.Rect(self.x, self.y, 13, 13)
            screen.blit(bulletsurf, (self.x, self.y))


def give_coordinates(tank,bullets):
    if tank.direction == 'RIGHT':
        x=tank.x + tank.width + int(tank.width / 2)
        y=tank.y + int(tank.width / 2)-5

    if tank.direction == 'LEFT':
        x=tank.x - int(tank.width / 2)
        y=tank.y + int(tank.width / 2)-5

    if tank.direction == 'UP':
        x=tank.x + int(tank.width / 2)-5
        y=tank.y - int(tank.width / 2)

    if tank.direction == 'DOWN':
        x=tank.x + int(tank.width / 2)-5
        y=tank.y + tank.width + int(tank.width / 2)

    p=Pulya(x,y,direction=tank.direction)
    p.id=tank.id
    bullets.append(p)

def collision_single_player(tank,bullets,walls):
    #столкновение танка со стенкой
    
    if (tank.x<-41):
        tank.x=width
    elif tank.x>width:
        tank.x=-40
    if (tank.y<-41):
        tank.y=height
    elif tank.y>height:
        tank.y=-40

    #столкновение пули с танком
    for p in bullets:
        if (tank.x+tank.width > p.x > tank.x - 13 ) and ((tank.y+tank.width> p.y > tank.y - 13)) and p.status==True:
            #vzryvSound.play()
            p.color=(0,0,0)
            tank.health-=1
            p.status=False
            tank.x=random.randint(50,width-70)
            tank.y=random.randint(50,height-70)


    #выход пули  с другой стороны
    for p in bullets:
        if p.x<0:
            p.x=width
        if p.x>width:
            p.x=0
        if p.y>height:
            p.y=0
        if p.y<0:
            p.y=height
    deleting_list=[]
    for i in range(len(walls)):
        if tank.rect.colliderect(walls[i].rect):
            print('detected')
            print(walls[i],i)
            if tank.direction == 'RIGHT': # Moving right; Hit the left side of the walls[i]                
                tank.x = walls[i].rect.left -40
                tank.health-=1
                deleting_list.append(walls[i])
            if tank.direction == 'LEFT': # Moving left; Hit the right side of the walls[i]                
                tank.x = walls[i].rect.right
                tank.health-=1
                deleting_list.append(walls[i])
            if tank.direction == 'DOWN': # Moving down; Hit the top side of the walls[i]                
                tank.y = walls[i].rect.top -40
                tank.health-=1
                deleting_list.append(walls[i])
            if tank.direction == 'UP': # Moving up; Hit the bottom side of the walls[i]                
                tank.y = walls[i].rect.bottom
                tank.health-=1
                deleting_list.append(walls[i])
    try:
        for i in range(len(deleting_list)):
            walls.remove(deleting_list[i])
    except:
        pass

    deleting_list=[]
    for i in range(len(walls)):
        for p in bullets:
            if p.rect.colliderect(walls[i].rect):
                print('detected')
                print(walls[i],i)
                if p.direction == 'RIGHT': # Moving right; Hit the left side of the walls[i]                
                    p.x = walls[i].rect.left -40
                    p.status=False
                    deleting_list.append(walls[i])
                if p.direction == 'LEFT': # Moving left; Hit the right side of the walls[i]                
                    p.x = walls[i].rect.right
                    p.status=False
                    deleting_list.append(walls[i])
                if p.direction == 'DOWN': # Moving down; Hit the top side of the walls[i]                
                    p.y = walls[i].rect.top -40
                    p.status=False
                    deleting_list.append(walls[i])
                if p.direction == 'UP': # Moving up; Hit the bottom side of the walls[i]                
                    p.y = walls[i].rect.bottom
                    p.status=False
                    deleting_list.append(walls[i])

    try:
        for i in range(len(deleting_list)):
            walls.remove(deleting_list[i])
    except:
        pass

    

def collision():
    #столкновение танка со стенкой
    for tank in players:
        if (tank.x<-41):
            tank.x=width
        elif tank.x>width:
            tank.x=-40
        if (tank.y<-41):
            tank.y=height
        elif tank.y>height:
            tank.y=-40

    #столкновение пули с танком
    for p in bullets:
        for tank in players:
            if (tank.x+tank.width+p.radius-2 > p.x > tank.x - p.radius+2 ) and ((tank.y+tank.width + p.radius -2> p.y > tank.y - p.radius+2)) and p.status==True:
                #vzryvSound.play()
                p.color=(0,0,0)
                tank.health-=1
                p.status=False
                
                tank.x=random.randint(50,width-70)
                tank.y=random.randint(50,height-70)

    #выход пули  с другой стороны
    for p in bullets:
        if p.x<0:
            p.x=width
        if p.x>width:
            p.x=0
        if p.y>height:
            p.y=0
        if p.y<0:
            p.y=height

def restart_single_player(nickname):
    

    restart_single_player_loop=True
    selected=0
    while restart_single_player_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                elif event.key==pygame.K_DOWN:
                    selected+=1
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Restart")
                        loading()
                        single_player(nickname)
                        restart_single_player_loop=False
                    if selected==1:
                        print("Main menu")
                        restart_single_player_loop=False
                    
        if selected<0:
            selected=0
        elif selected>1:
            selected=1
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("Single Player", font, 90, yellow)

        if selected==0:
            text_single_player=text_format("Restart", font, 75, white)
        else:
            text_single_player = text_format("Restart", font, 75, black)

        if selected==1:
            text_multiplayer=text_format("Main menu", font, 75, white)
        else:
            text_multiplayer = text_format("Main menu", font, 75, black)


        title_rect=title.get_rect()
        single_rect=text_single_player.get_rect()
        multi_rect=text_multiplayer.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2), 300))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 370))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("World of Tanks Online")  

def score(tank):
    font = pygame.font.SysFont('docktrin.ttf', 32) 
    health=tank.health
    res = font.render('Health: ' + str(health), True, (20, 20, 255))
    screen.blit(res, (870,5))
    #pygame.display.flip()
    




'''def quit():
    score1=tanks[1].score
    score2=tanks[0].score
    screen.fill((210, 160, 190))
    res = font.render('G A M E   O V E R!', True, (0, 90, 255))
    res1 = font.render('total score of GREEN player: ' + str(score1), True, (0, 90, 255))
    res2 = font.render('total score of PINK player: ' + str(score2), True, (0, 90, 255))
    screen.blit(res, (150,150))
    screen.blit(res1, (200,250))
    screen.blit(res2, (200,300))
    time.sleep(3)
    pygame.quit()'''

def fill_edges():
    for i in range(width//wall_range):
        screen.blit(wallImage,(wall_range*i,0))
        screen.blit(wallImage,(wall_range*i,height-wall_range))

    for i in range(height//wall_range):
        screen.blit(wallImage,(0,i*wall_range))
        screen.blit(wallImage,(width-wall_range,i*wall_range))





clock = pygame.time.Clock()
#############################################################################################################################################################################    
#############################################################################################################################################################################
def loading():
    screen.blit(img,(0,0))
    title=text_format("Loading", font, 75, yellow)
    title_rect=title.get_rect()
    xy=screen_width/2 - (title_rect[2]/2)
    screen.blit(title, (xy, 300))
    pygame.display.update()
    time.sleep(0.5)
    title=text_format("Loading.", font, 75, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (xy, 300))
    pygame.display.update()
    time.sleep(0.5)
    title=text_format("Loading..", font, 75, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (xy, 300))
    pygame.display.update()
    time.sleep(0.5)
    title=text_format("Loading...", font, 75, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (xy, 300))
    pygame.display.update()
    time.sleep(0.5)

def escape_of_single_player():

    escape_of_single_player_loop=True
    selected=0
    while escape_of_single_player_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                elif event.key==pygame.K_DOWN:
                    selected+=1
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Continue")
                        loading()
                        return True
                    if selected==1:
                        print("Main menu")
                        return False
                    
        if selected<0:
            selected=0
        elif selected>1:
            selected=1
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("Single Player", font, 90, yellow)

        if selected==0:
            text_single_player=text_format("Continue", font, 75, white)
        else:
            text_single_player = text_format("Continue", font, 75, black)

        if selected==1:
            text_multiplayer=text_format("Main menu", font, 75, white)
        else:
            text_multiplayer = text_format("Main menu", font, 75, black)


        title_rect=title.get_rect()
        single_rect=text_single_player.get_rect()
        multi_rect=text_multiplayer.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2), 240))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 300))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("World of Tanks Online")   
def escape_of_multiplayer():

    escape_of_multiplayer_loop=True
    selected=0
    while escape_of_multiplayer_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                elif event.key==pygame.K_DOWN:
                    selected+=1
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Continue")
                        loading()
                        return True
                    if selected==1:
                        print("Main menu")
                        loading()
                        return False
                    
        if selected<0:
            selected=0
        elif selected>1:
            selected=1
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("Multilayer", font, 90, yellow)

        if selected==0:
            text_single_player=text_format("Continue", font, 75, white)
        else:
            text_single_player = text_format("Continue", font, 75, black)

        if selected==1:
            text_multiplayer=text_format("Main menu", font, 75, white)
        else:
            text_multiplayer = text_format("Main menu", font, 75, black)


        title_rect=title.get_rect()
        single_rect=text_single_player.get_rect()
        multi_rect=text_multiplayer.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2), 240))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 300))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("World of Tanks Online") 

bullets=[]
def fuel_works(tank,bullets,fuels,time_counter,time_counter_time):
    if (datetime.now().second%10==1) and (len(fuels)<3):
        fuels.append( (random.randint(40,width), random.randint(40,height) ))
    
    for p in bullets:
        try:
            for i in range(len(fuels)):
                if (fuels[i][0]+40 > p.x > fuels[i][0] - 13 ) and ((fuels[i][1]+40> p.y > fuels[i][1] - 13)) and p.status==True :
                    #vzryvSound.play()
                    fuels.pop(i)
                    p.status=False
        except:
            pass
    g=int
    for i in range(len(fuels)):
        if (fuels[i][0]+40 > tank.x > fuels[i][0] - 40 ) and (fuels[i][1]+40> tank.y > fuels[i][1] - 40):
            time_counter[0]=True
            time_counter_time[0]=datetime.now().second+5
            g=i
    try:
        fuels.pop(g)
    except:
        pass

    if time_counter[0]==True:
            if datetime.now().second!=time_counter_time[0]:
                tank.speed=10
                for p in bullets:
                    p.speed=16
            else :
                tank.speed=5
                for p in bullets:
                    p.speed=8
                time_counter[0]=False

    for fuel in fuels:
        fuelsurf = pygame.Surface((40, 40))
        fuelsurf.set_colorkey((0,0,0))
        fuelsurf.blit(fuelImage,(0,0))
        screen.blit(fuelsurf, (fuel[0], fuel[1]))
    #pygame.display.flip()
    

def single_player(nickname):
    myname=nickname
    tank = Tank(100, 100, (100, 230, 40),ID=myname,nick=nickname)
    time_counter=[False]
    time_counter_time=[0]
    time_c=0
    bullets=[]
    fuels=[]
    
    level1 = [
            "                                                  ",
            "                                                  ",
            "                              WWWWWW              ",
            "                        WWWW       W              ",
            "                        W        WWWW             ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            "      W   W   W           W   W   W W         W   ",
            " WW   W   WWWWW      WW   W   WWWWW W    WW   W   ",
            "  W      WW           W      WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                              WWWWWW              ",
            "                        WWWW       W              ",
            "                        W        WWWW             ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            "      W   W   W           W   W   W W         W   ",
            " WW   W   WWWWW      WW   W   WWWWW W    WW   W   ",
            "  W      WW           W      WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            "      W   W   W           W   W   W W         W   ",
            " WW   W   WWWWW      WW   W   WWWWW W    WW   W   ",
            "  W      WW           W      WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  "  ]
    level2=["                                                  ",
            "                                                  ",
            "                              WWWWWW              ",
            "                        WWWW       W              ",
            "                        W        WWWW             ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            "      W   W   W           W   W   W W         W   ",
            " WW   W   WWWWW      WW   W   WWWWW W    WW   W   ",
            "  W      WW           W      WW           W      W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWW       WWW       WWWW                   WWWWWWW",
            "WWW WWWWW WWW WWWWW WWWWWWWWWWWWWWWWWWWWW  WWWWWWW",
            "WWW WWWWW WWW WWWWW WWWWWWWWWWWWWWWWWWWWW  WWWWWWW",
            "WWW WWWWW WWW WWWWW WWWWWWWWWWWWWWWWWWWWW  WWWWWWW",
            "WWW WWWWW WWW WWWWW WWWWWWWWWWWWWWWWWWWWW  WWWWWWW",
            "WWW       WWW       WWWWWWWWWWWWWWWWWWWWW  WWWWWWW",
            "WWW WWWWWWWWW WWWWWWWWWWWWWWW              WWWWWWW",
            "WWW WWWWWWWWW WWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWW",
            "WWW WWWWWWWWW WWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWW",
            "WWW WWWWWWWWW WWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWW",
            "WWW WWWWWWWWW WWWWWWWWWWWWWWW  WWWWWWWWWWWWWWWWWWW",
            "WWW WWWWWWWWW WWWWWWWWWWWWWWW             WWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" ]
    level3 = [
            "                                                  ",
            "                                                  ",
            "                              WWWWWW              ",
            "                        WWWW       W              ",
            "                        W        WWWW             ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            "      W   W   W           W   W   W W         W   ",
            " WW   W   WWWWW      WW   W   WWWWW W    WW   W   ",
            "  W      WW           W      WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                              WWWWWW              ",
            "                        WWWW       W              ",
            "                        W        WWWW             ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  W   ",
            " WW  WWWWWWW     WWWWWW       WWWWWWWWWWWWWW  W   ",
            "  W  WWWWWWW     WWWWWW       WWWWWWWWWWWWWW     W",
            "     WWWWWWW     WWWWWW       WWWWWWWWWWWWWW      ",
            "     WWWWWWWWWWWWWWWWWW       WWWWWWWWWWWWWW  W   ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW      ",
            "     WWWWW                          WWWWWWWW      ",
            "     WWWWW                          WWWWWWWW      ",
            "     WWWWW                          WWWWWWWW      ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW  W   ",
            " WW   W   WWWWW      WW   W   WWWWW W    WW   W   ",
            "  W      WW           W      WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  " 


            ]
    level4=[
            "                               WWWWWWWWWWWWWWWWWWW",
            "                                                  ",
            "                              WWWWWW              ",
            "                  WWWWWWWWWWWWWWWWWWWWW           ",
            "                  WWWWWWWWWWWWWWWWWWWWW           ",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            " WWWWWWWWWWWWWWWWWWWWWWW  W   W   W W         W   ",
            " WWWWWWWWWWWWWWWWWWWWWWW  W   WWWWW W    WW   W   ",
            " WWWWWWWWWWWWWWWWWWWWWWW     WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  ",
            "                      WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                      WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                      WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                      WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                      WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                     W     WWWW                   ",
            "                        W     W W                 ",
            "                                  WWW W           ",
            "                        WWW WWW   W W             ",
            "      W WWW   WWWW    WWW  W W W W    W W     W   ",
            " WW   W WWW   WWWW    WWW  W W W W    W W W   W   ",
            "  W     WWW   WWWW    WWW  W W W W    W W W      W",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "      W WWW   WWWW    WWW  W W W W    W W     W   ",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "      W WWW   WWWW    WWW  W W W W    W W     W   ",
            " WW   W WWW   WWWW    WWW  W W W W    W W W   W   ",
            "  W     WWW   WWWW    WWW  W W W W    W W W      W",
            "        WWW   WWWW    WWW  W W W W    W W         ",
            "      W WWW   WWWW    WWW  W W W W    W W     W   ",
            "                                                  " 
            ]
    level5 = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "                                                  ",
            "      W   W   W                               W   ",
            " WW   W   WWWWW                          WW   W   ",
            "  W      WW                               W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWW                 WWWWWW       ",
            "           WWWWWWWWW                 WWWWWW       ",
            "           WWWWWWWWW                 WWWWWW       ",
            "           WWWWWWWWW                 WWWWWW       ",
            "      W   WWWWWWWWWW                 WWWWWW   W   ",
            " WW   W   WWWWWWWWWW                 WWWWWW   W   ",
            "  W      WWWWWWWWWWW                 WWWWWW      W",
            "           WWWWWWWWW                 WWWWWW       ",
            "      W    WWWWWWWWW                 WWWWWW   W   ",
            "           WWWWWWWWW                 WWWWWW       ",
            "           WWWWWWWWW                 WWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "           WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW       ",
            "      W   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW   W   ",
            " WW   W   WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW   W   ",
            "  W      WW           W      WW           W      W",
            "                                                  ",
            "      W        W          W        W          W   ",
            "                                                  " 
            ]
    level6=[
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                        W                        ",
            "                        W    WWWWWW              ",
            "                        WWW       W              ",
            "                        W       WWWW             ",
            "                     W  W WWWW                   ",
            "                        W    W W                 ",
            "                        W        WWW W           ",
            "                        WW WWW   W W             ",
            "      W   W   W         WW   W   W W         W   ",
            " WW   W   WWWWW      WW WW   WWWWW W    WW   W   ",
            "  W      WW           W W   WW           W      W",
            "                        W                        ",
            "      W        W        WW        W          W   ",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                        W                        ",
            "                        W                        ",
            "                        W    WWWWWW              ",
            "                        WWW       W              ",
            "                        W       WWWW             ",
            "                     W  W WWWW                   ",
            "                        W    W W                 ",
            "                        W        WWW W           ",
            "                        WW WWW   W W             ",
            "      W   W   W         WW   W   W W         W   ",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "  W      WW           W W   WW           W      W",
            "                        W                        ",
            "      W        W        WW        W          W   ",
            "                        W                        ",
            "                     W  W WWWW                   ",
            "                        W    W W                 ",
            "                        W        WWW W           ",
            "                        WW WWW   W W             ",
            "      W   W   W         WW   W   W W         W   ",
            " WW   W   WWWWW      WW WW   WWWWW W    WW   W   ",
            "  W      WW           W W   WW           W      W",
            "                        W                        ",
            "      W        W        WW        W          W   ",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" 
            ]
    levels=[level1,level2,level3,level4,level5,level6]
    
    FPS = 30
    loading()
    clock = pygame.time.Clock()
    mainloop=True


    walls = []
    level=levels[random.randint(0,5)]
    #---------------------------------
    class Wall(object):
        def __init__(self, pos):
            walls.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 20, 20)
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            x += 20
        y += 20
        x = 0
    #---------------------------------
    
    while mainloop:
        
        mill = clock.tick(FPS)
        screen.blit(desertimage1,(0,0))
        
        for wall in walls:
            pygame.draw.rect(screen, (0, 0, 0), wall.rect)
            screen.blit(wallImage,(wall.rect))

        tank.move()
        for p in bullets:
            p.move()
        collision_single_player(tank,bullets,walls)
        #fill_edges()

        fuel_works(tank,bullets,fuels,time_counter,time_counter_time)
        

        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_ESCAPE:
                    mainloop=escape_of_single_player()
                    
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_w] :
                    tank.change_direction('UP')
                if pressed[pygame.K_a] :
                    tank.change_direction('LEFT')
                if pressed[pygame.K_s] :
                    tank.change_direction("DOWN")
                if pressed[pygame.K_d] :
                    tank.change_direction('RIGHT')
                
                if pressed[pygame.K_SPACE]:
                    #pulyaSound.play()
                    give_coordinates(tank,bullets)
        #fill_edges()
        if tank.health<1:
            restart_single_player(nickname)
            mainloop=False
        score(tank)
        pygame.display.flip()
    
def multiplayer(nickname):
    myname=nickname    
    global players
    mytank=Tank(200,200,(0,255,0))
    players = [mytank]
    

    bullets_info=[]
    bullets=[]
    players_info=[]


    def parsing_all_info(all_info):
        
        #all_info=json.load(all_info)
        #print(type(all_info))
        #print(all_info)

        #for i in range(len(all_info["gameField"]['tanks'])):
        #    all_info["gameField"]['tanks'][0]
        #print(type(all_info["gameField"]['tanks']))
        #print(all_info)
        for i in range(len(all_info["gameField"]['tanks'])):
            f=False
            for g in range(len(players)):
                if (all_info["gameField"]['tanks'][i]['id']==players[g].id) and (all_info["gameField"]['tanks'][i]['id'] != myname):
                    players[g].id=all_info["gameField"]['tanks'][i]['id']
                    players[g].x=all_info["gameField"]['tanks'][i]['x']
                    players[g].y=all_info["gameField"]['tanks'][i]['y']
                    players[g].direction=all_info["gameField"]['tanks'][i]['direction']
                    players[g].width=all_info["gameField"]['tanks'][i]['width']
                    players[g].height=all_info["gameField"]['tanks'][i]['height']
                    players[g].health=all_info["gameField"]['tanks'][i]['health']
                    players[g].score=all_info["gameField"]['tanks'][i]['score'] 
                    f=True
            if f==False and (all_info["gameField"]['tanks'][i]['id'] != myname):
                print('New player joined the game: ',all_info["gameField"]['tanks'][i]['id'])
                x = all_info["gameField"]['tanks'][i]['x']
                y = all_info["gameField"]['tanks'][i]['y']  
                p = Tank( x, y, (255,0,50) )
                p.id = all_info["gameField"]['tanks'][i]['id']
                p.direction = all_info["gameField"]['tanks'][i]['direction']
                players.append(p)




        '''for a in range(len(all_info["gameField"]['tanks'])):
            if p in players:
                #p=Tank(all_info["gameField"]['tanks'][a]['x'],all_info["gameField"]['tanks'][a]['y'],1,(255,0,50))
                p.id=all_info["gameField"]['tanks'][a]['id']
                p.direction=all_info["gameField"]['tanks'][a]['direction']
                p.width=all_info["gameField"]['tanks'][a]['width']
                p.height=all_info["gameField"]['tanks'][a]['height']
                p.health=all_info["gameField"]['tanks'][a]['health']
                p.score=all_info["gameField"]['tanks'][a]['score']
            else:
                p=Tank(all_info["gameField"]['tanks'][a]['x'],all_info["gameField"]['tanks'][a]['y'],1,(255,0,50))
                players.append(p)'''
        #print(players)
        '''for a in range(len(all_info["gameField"]['tanks'])):
            #for i in range(len(all_info["gameField"]['bullets'])):

            if a not in bullets_info:
                print('true')
                bullets_info.append(all_info["gameField"]['tanks'][a])
                p=Tank(all_info["gameField"]['tanks'][a]['x'],all_info["gameField"]['tanks'][a]['y'],5,(255,0,50))
                p.id=all_info["gameField"]['tanks'][a]['id']
                p.direction=all_info["gameField"]['tanks'][a]['direction']
                p.width=all_info["gameField"]['tanks'][a]['width']
                p.height=all_info["gameField"]['tanks'][a]['height']
                p.health=all_info["gameField"]['tanks'][a]['health']
                p.score=all_info["gameField"]['tanks'][a]['score']
                p.id=all_info["gameField"]['tanks'][a]['id']
                give_coordinates(p)'''
    def healthcheck_info(body):
        if body['status']==200:

            if body['message']=="OK":
                text='server is up and running.'

            return True,text

        else:
            text='server is unavailable.'

            try:
                text=body['message']
            except:
                pass

            return False,text

    def register_info(body):
        text=body
        return True,text

    def turn_tank_info(body):
        if body['status']==200:
            text='tank has seccessfully turned'
            return True,text
        else:
            text='something wrong with tank turn'

            try:
                text=body['message']
            except:
                pass

            return False,text
        

    def fire_bullet_info(body):
        if body['status']==200:
            text='bullet has seccessfully fired'
            return True,text
        else:
            text='something wrong with bullet fire'

            try:
                text=body['message']
            except:
                pass


            return False,text



    loading()
    mainloop =True
    callback_queue="Bauyrzhans queue"        
    corr_id = str(uuid.uuid4())
    class Consuming(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = connection.channel()
            self.channel.exchange_declare(exchange='X:routing.topic',exchange_type='topic')
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)#routing_key=callback_queue
            def callback(ch,method,properties,body):
                #print(body)
                #print(ch)
                body=json.loads(body)
                parsing_all_info(body)
                print(body)
                print('callback function 330')

                if properties.correlation_id=='healthcheck':
                    result=healthcheck_info()
                if properties.correlation_id=='register':
                    result=register_info()
                if properties.correlation_id=='turn_tank':
                    result=turn_tank_info()
                if properties.correlation_id=='fire_bullet':
                    result=fire_bullet_info()

                
            self.channel.basic_consume(queue=self.callback_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
            exit()    

    class Producer(Thread):

        def __init__(self):
            Thread.__init__(self)
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX'))) 
            #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = connection.channel()
            self.channel.exchange_declare(exchange='X:routing.topic',exchange_type='topic')
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)

        def run(self):
            pass

        def sendmessage(self,message):
            #self.channel = connection.channel()
            #self.channel.exchange_declare(exchange='123',exchange_type='topic')
            mess=json.dumps(message)
            self.channel.basic_publish(
                exchange='123',
                routing_key='squeue',
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=corr_id,
                ),
                body=mess)
            print('message sended!')

        def healthcheck(self):
            #
            corr_id='healthcheck'
            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key='tank.request.healthcheck',
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=corr_id,
                ),
                body='')
            print('Healthcheck message sended!')

        def register(self,roomId):

            text={"roomId":str(roomId)}
            text=json.dumps(text)
            corr_id='register'

            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key='tank.request.register',
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=corr_id,
                ),
                body=text)
            print('Registration message sended!')
        
        def turn_tank(self,token,direction):

            text={
                  "token":str(token),
                  "direction":str(direction)
                }
            text=json.dumps(text)
            corr_id='turn_tank'

            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key='tank.request.turn',
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=corr_id,
                ),
                body=text)
            print('Turn_tank message sended!')
        
        def fire_bullet(self,token):

            text={"token":str(token),}
            text=json.dumps(text)
            corr_id='fire_bullet'

            self.channel.basic_publish(
                exchange='X:routing.topic',
                routing_key='tank.request.fire',
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=corr_id,
                ),
                body=text)
            print('Fire_bullet message sended!')

        def close(self):                                                                   
            self.channel.close()
            exit()

    con = Consuming()
    con.start()
    prd = Producer()
    prd.start()
    clock=pygame.time.Clock()
    prd.healthcheck()
    while mainloop:
        mill = clock.tick(FPS)
        screen.fill((0, 0, 0))
        #fill_edges()
        #score()
        #delete_bad_status_bullets()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prd.close()
                con.close()
                exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    a=escape_of_multiplayer()
                    if a==False:
                        prd.close()
                        con.close()
                        mainloop=False

                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_SPACE]:
                    my_info=My_info_bullets()
                    #prd.sendmessage(my_info)
                    #pulyaSound.play()
                    give_coordinates(mytank)
                if pressed[pygame.K_UP]:
                    mytank.direction='UP'
                if pressed[pygame.K_DOWN]:
                    mytank.direction='DOWN'
                if pressed[pygame.K_RIGHT]:
                    mytank.direction='RIGHT'
                if pressed[pygame.K_LEFT]:
                    mytank.direction='LEFT'
        #print(players)

        '''for a in range(len(players)): 
            x = players[a]['x']
            y = players[a]['y']  
            p = Tank( x, y, (255,0,50) )
            p.id = players[a]['id']
            p.direction = players[a]['direction']
            p.move
            print('new tank')'''
        for i in range(len(players)):
            players[i].move()
        #collision()

        #for p in bullets:
        #    p.move()

        #for tank in tanks:
         #   print(tank.direction)
        #print(Direction)


        my_info=My_info()
        print(my_info)
        print('Number of players: '+ str(len(players)))
        for i in range(len(players)):
            print('player{id},: x:{x} y:{y}'.format(id=players[i].id,x=players[i].x,y=players[i].y))

        #prd.sendmessage(my_info)
        print()
        clock.tick(10)
        pygame.display.flip()


# Game Initialization


# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width=1000
screen_height=800
screen=pygame.display.set_mode((screen_width, screen_height))

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText


# Colors
white=(255, 200, 150)
black=(0, 50, 50)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "docktrin.ttf"

#image
img=pygame.image.load('media\\1000-800.png')

# Game Framerate
clock = pygame.time.Clock()
FPS=30

#

def change_name(nickname):
    
    change_name_loop=True
    
    while change_name_loop:
        for event in pygame.event.get():
            
            if event.type==pygame.QUIT:
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key>=97 and event.key<=122:
                    nickname+=chr(event.key)
                elif event.key==pygame.K_BACKSPACE:
                    nickname=nickname[:-1]

                if event.key==pygame.K_RETURN or event.key==pygame.K_ESCAPE:
                    change_name_loop=False

        title=text_format("Enter your nickname", font, 80, yellow)
        text_nickname=text_format(nickname, font, 50, white)
        text_n=text_format('Nickname:',font, 50, black)
        text_conf=text_format('Press Enter to confirm',font, 60, black)

        title_rect=title.get_rect()
        nickname_rect=text_nickname.get_rect()
        n_rect=text_n.get_rect()
        conf_rect=text_conf.get_rect()

        screen.blit(img,(0,0))
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_nickname, (screen_width/2 - (nickname_rect[2]/2), screen_height-500))#(screen_width/2 - (nickname_rect[2]/2), 260)
        screen.blit(text_n,(screen_width/2 - (n_rect[2]/2), screen_height-570))
        screen.blit(text_conf, (screen_width/2 - (conf_rect[2]/2), screen_height-100))
        
        pygame.display.update()
    return nickname
         

# Main Menu
def main_menu():

    menu=True
    selected=0
    import uuid
    nickname='Change_this_text_to_your_name'
    
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                elif event.key==pygame.K_DOWN:
                    selected+=1
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Single Player")
                        single_player(nickname)
                    if selected==1:
                        print("Multiplayer")
                        multiplayer(nickname)
                    if selected==2:
                        print("Multiplayer with AI")
                    if selected==3:
                        print('Change name')
                        nickname = change_name(nickname)
                    if selected==4:
                        pygame.quit()
                        quit()
        if selected<0:
            selected=0
        elif selected>4:
            selected=4
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("World of Tanks", font, 90, yellow)

        if selected==0:
            text_single_player=text_format("Single Player", font, 75, white)
        else:
            text_single_player = text_format("Single Player", font, 75, black)

        if selected==1:
            text_multiplayer=text_format("Multiplayer", font, 75, white)
        else:
            text_multiplayer = text_format("Multiplayer", font, 75, black)

        if selected==2:
            text_multiplayer_with_ai=text_format("Multiplayer with AI" ,font, 75, white)
        else:
            text_multiplayer_with_ai = text_format("Multiplayer with AI", font, 75, black)

        if selected==3:
            text_change_name=text_format("Change name", font, 75, white)
        else:
            text_change_name = text_format("Change name", font, 75, black)

        if selected==4:
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect=title.get_rect()
        single_rect=text_single_player.get_rect()
        multi_rect=text_multiplayer.get_rect()
        multi_ai_rect=text_multiplayer_with_ai.get_rect()
        change_name_rect=text_change_name.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2), 300)) #240
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 370)) #300
        screen.blit(text_multiplayer_with_ai, (screen_width/2 - (multi_ai_rect[2]/2), 440)) #360
        screen.blit(text_change_name,(screen_width/2 - (change_name_rect[2]/2), 510)) #420
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 580)) #480
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("World of Tanks Online")

#Initialize the Game
main_menu()
pygame.quit()
quit()

pygame.quit()