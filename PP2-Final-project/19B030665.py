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
width=800
height=600
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
desertimage1=pygame.image.load('media\\desert2-800-600.png')
desertimage2=pygame.image.load('media\\desert3-800-600.jpg')


pulyaSound=pygame.mixer.Sound('pulya.wav')
vzryvSound=pygame.mixer.Sound('vzryv.wav')
gta1=pygame.mixer.Sound('media\\gta1.wav')
gta2=pygame.mixer.Sound('media\\gta2.wav')
gta3=pygame.mixer.Sound('media\\gta3.wav')
gta4=pygame.mixer.Sound('media\\gta4.wav')

winsound=pygame.mixer.Sound('media\\win.wav')
losesound=pygame.mixer.Sound('media\\lose.wav')

class Tank:

    def __init__(self, x, y, color, ID=myname,nick='7879789798987'):
        self.id=ID
        self.me=False
        self.x = x
        self.y = y
        self.health=3
        self.score=0
        self.speed = 5
        self.color = color
        self.width = 31
        self.height= 31
        self.direction = 'RIGHT'
        self.rect = pygame.Rect(self.x, self.y, 31, 31)

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
        tanksurf = pygame.Surface((31, 31))
        tanksurf.set_colorkey((0,0,0))
        if self.me==True:
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
        self.rect = pygame.Rect(self.x, self.y, 31, 31)
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
        self.rect = pygame.Rect(self.x, self.y, 5, 15)

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
        x=tank.x + tank.width + 5
        y=tank.y + int(tank.width / 2)-5

    if tank.direction == 'LEFT':
        x=tank.x - int(tank.width / 2)-10
        y=tank.y + int(tank.width / 2)-5

    if tank.direction == 'UP':
        x=tank.x + int(tank.width / 2)-5
        y=tank.y - int(tank.width / 2)-10

    if tank.direction == 'DOWN':
        x=tank.x + int(tank.width / 2)-5
        y=tank.y + tank.width + int(tank.width / 2)

    p=Pulya(x,y,direction=tank.direction)
    p.id=tank.id
    p.speed=6
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
            vzryvSound.play()
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
                vzryvSound.play()
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
    pygame.mixer.music.pause()

    restart_single_player_loop=True
    selected=0
    while restart_single_player_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    gta1.play()
                    selected-=1
                elif event.key==pygame.K_DOWN:
                    gta1.play()
                    selected+=1
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Restart")
                        gta3.play()
                        loading()
                        pygame.mixer.music.stop()
                        single_player(nickname)
                        restart_single_player_loop=False
                    if selected==1:
                        gta3.play()
                        print("Main menu")
                        pygame.mixer.music.stop()
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
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2)-30, 200))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 270))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("Tanks Online")  

def score(tank):
    font = pygame.font.SysFont('doctrin.ttf', 32) 
    health=tank.health
    res = font.render('Health: ' + str(health), True, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    screen.blit(res, (50,40))
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
    screen.blit(title, (xy, 250))
    pygame.display.update()
    time.sleep(0.5)
    title=text_format("Loading.", font, 75, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (xy, 250))
    pygame.display.update()
    time.sleep(0.5)
    title=text_format("Loading..", font, 75, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (xy, 250))
    pygame.display.update()
    time.sleep(0.5)
    title=text_format("Loading...", font, 75, yellow)
    title_rect=title.get_rect()
    screen.blit(title, (xy, 250))
    pygame.display.update()
    time.sleep(0.5)

def escape_of_single_player():
    pygame.mixer.music.pause()
    escape_of_single_player_loop=True
    selected=0
    while escape_of_single_player_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    gta1.play()
                    selected-=1
                elif event.key==pygame.K_DOWN:
                    gta1.play()
                    selected+=1
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Continue")
                        gta3.play()
                        loading()
                        pygame.mixer.music.unpause()
                        return True
                    if selected==1:
                        gta3.play()
                        print("Main menu")
                        pygame.mixer.music.stop()
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
        pygame.display.set_caption("Tanks Online")   
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
                    gta1.play()
                elif event.key==pygame.K_DOWN:
                    selected+=1
                    gta1.play()
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print("Continue")
                        gta3.play()
                        loading()
                        return True
                    if selected==1:
                        gta3.play()
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
        pygame.display.set_caption("Tanks Online") 

def restart_of_multiplayer(winners):

    restart_of_multiplayer_loop=True
    selected=0
    while restart_of_multiplayer_loop:
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
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2), 240))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 300))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("Tanks Online") 


bullets=[]
def fuel_works(tank,bullets,fuels,time_counter,time_counter_time):
    if (datetime.now().second%10==1) and (len(fuels)<3):
        fuels.append( (random.randint(40,width), random.randint(40,height) ))
    
    for p in bullets:
        try:
            for i in range(len(fuels)):
                if (fuels[i][0]+40 > p.x > fuels[i][0] - 13 ) and ((fuels[i][1]+40> p.y > fuels[i][1] - 13)) and p.status==True :
                    vzryvSound.play()
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
            if datetime.now().second<time_counter_time[0]:
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
    tank.speed=3
    tank.me=True
    time_counter=[False]
    time_counter_time=[0]
    time_c=0
    bullets=[]
    fuels=[]
    
    level1 = [
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "             WWWWWWWWWWWWWWWW            ",
            "             W              W            ",
            "             W              W            ",
            "             W              W            ",
            "             W              W            ",
            "             WWWWWWWWWWWWWWWW            ",
            "                    W                    ",
            "                    W                    ",
            "                    W                    ",
            "                    W                    ",
            "       WWWWWWWWWWWWWWWWWWWWWWWWWWWWW     ",
            "                    W                    ",
            "                    W                    ",
            "                    W                    ",
            "                    W                    ",
            "                    W                    ",
            "                    W                    ",
            "                   W W                   ",
            "                 W    W                  ",
            "               W        W                ",
            "             W            W              ",
            "           W               W             ",
            "          W                 W            ",
            "                                         " ]
    level2=["                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "  WWWWWWWWWWWWWWWWWWWWWWWWWW             ",
            "  W                      WW              ",
            "  W                     WW               ",
            "  W                   WW                 ",
            "  W                 WW                   ",
            "  W               WW                     ",
            "  W                 WW                   ",
            "  W                   WW                 ",
            "  W                     WW               ",
            "  W                      WW              ",
            "  WWWWWWWWWWWWWWWWWWWWWWWWWW             ",
            "  W                                      ",
            "  W                                      ",
            "  W                                      ",
            "  W                                      ",
            "  W                                      ",
            "  W                                      ",
            "  W                                      ",
            "  W                                      ",]
    level3 = [
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ",
            "     WWWWWWW     WWWWWW       WWWWWWWWWW ",
            "     WWWWWWW     WWWWWW       WWWWWWWWWWW",
            "     WWWWWWW     WWWWWW       WWWWWWWWWW ",
            "     WWWWWWWWWWWWWWWWWW       WWWWWWWWWW ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ",
            "     WWWWW                          WWWW ",
            "     WWWWW                          WWWW ",
            "     WWWWW                          WWWW ",
            "     WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         " ]
    level4=[
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "         WWWWWWWWWWWWWWWWW               ",
            "         W               W               ",
            "         W               WWWWWWWWWWWWWWWW",
            "         W               W               ",
            "         W               W               ",
            "         W               W               ",
            "  wWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWw    ",
            "  W                                 W    ",
            "  W                                 W    ",
            "  W                                 W    ",
            "  W                                 W    ",
            "  W                                 W    ",
            "  WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW    "
            ]
    level5 = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "                                         ",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWW    W       W  W       WWWWWWWWW",
            "WWWWWWWWW   W  W    W      W    WWWWWWWWW",
            "WWWWWWWWW  W      W        W    WWWWWWWWW",
            "WWWWWWWWW  W               W    WWWWWWWWW",
            "WWWWWWWWW  W               W    WWWWWWWWW",
            "WWWWWWWWW   W             W     WWWWWWWWW",
            "WWWWWWWWW     W          W      WWWWWWWWW",
            "WWWWWWWWW       W     W         WWWWWWWWW",
            "WWWWWWWWW         W W           WWWWWWWWW",
            "WWWWWWWWW                       WWWWWWWWW"
            ]
    level6=[
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "WWWWWWWW WWWWWWWW      WWWWWWWWW        ",
            "W      W W      W              W        ",
            "W      W W      W              W        ",
            "WWWWWWWW WWWWWWWW              W        ",
            "W        W             WWWWWWWWW        ",
            "W        W             W                ",
            "W        W             W                ",
            "W        W             WWWWWWWWW        ",
            "                                        ",
            "                                        ",
            "WWWWWWWW WWWWWWWW      WWWWWWWWW        ",
            "W      W W      W              W        ",
            "W      W W      W              W        ",
            "WWWWWWWW WWWWWWWW              W        ",
            "W        W             WWWWWWWWW        ",
            "W        W             W                ",
            "W        W             W                ",
            "W        W             WWWWWWWWW        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "                                        ",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
            ]
    levels=[level1,level2,level3,level4,level5,level6]
    
    FPS = 80
    loading()
    clock = pygame.time.Clock()
    mainloop=True


    walls = []
    randomlevel=random.randint(0,5)
    print(randomlevel)
    level=levels[randomlevel]
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
    pygame.mixer.music.load('media\\single.mp3')
    pygame.mixer.music.play()
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
                if pressed[pygame.K_UP] :
                    tank.change_direction('UP')
                if pressed[pygame.K_LEFT] :
                    tank.change_direction('LEFT')
                if pressed[pygame.K_DOWN] :
                    tank.change_direction("DOWN")
                if pressed[pygame.K_RIGHT] :
                    tank.change_direction('RIGHT')
                
                if pressed[pygame.K_SPACE]:
                    pulyaSound.play()
                    give_coordinates(tank,bullets)
        #fill_edges()
        if tank.health<1:
            restart_single_player(nickname)
            mainloop=False
        score(tank)
        pygame.display.flip()
    pygame.mixer.music.stop()


def sorted_list_of_players(players):
    for i in range(len(players)):
        for j in range(len(players)):
            if players[i].score>players[j].score:
                players[i],players[j]=players[j],players[i]
            if players[i].score==players[j].score:
                if players[i].health>players[j].health:
                    players[i],players[j]=players[j],players[i]
    return players

            
def choose_room():

    choose_room_loop=True
    selected=0
    room=1
    while choose_room_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                    gta1.play()
                elif event.key==pygame.K_DOWN:
                    selected+=1
                    gta1.play()
                if selected==0:
                    if event.key==pygame.K_RIGHT:
                        room+=1
                        gta2.play()
                    elif event.key==pygame.K_LEFT:
                        room-=1
                        gta2.play()
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        gta3.play()
                        print('room-'+str(room))
                        loading()
                        return 'room-'+str(room)
                    if selected==1:
                        gta3.play()
                        print("Main menu")
                        loading()
                        return False
                    
        if selected<0:
            selected=0
        elif selected>1:
            selected=1
        if room<1:
            room=1
        elif room>30:
            room=30
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("Multilayer", font, 90, yellow)

        if selected==0:
            text_single_player=text_format("Room:", font, 75, white)
            text_room=text_format(str(room), font, 75, white)
        else:
            text_single_player = text_format("Room", font, 75, black)
            text_room=text_format(str(room), font, 75, black)

        if selected==1:
            text_multiplayer=text_format("Main menu", font, 75, white)
        else:
            text_multiplayer = text_format("Main menu", font, 75, black)


        title_rect=title.get_rect()
        single_rect=text_single_player.get_rect()
        multi_rect=text_multiplayer.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_single_player,( 220, 200))
        screen.blit(text_room,(490,200))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2)-10, 270))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("Tanks Online") 




remainingtime=120   
winners=[]
losers=[]
kicked=[]

def screen_win(score):
    print(1032)
    screen.blit(desertimage2,(0,0))
    title=text_format("You win the game! Keep it up", font, 50, yellow)
    screen.blit(title, (80, 200))
    title=text_format("Score:"+str(score), font, 40, black)
    screen.blit(title, (350, 300))
    pygame.display.update()
    
    winsound.play()
  
    time.sleep(4)
k=0    
def screen_lose(score):
    global k
    if k==0:
        screen.blit(desertimage2,(0,0))
        title=text_format("You lose the game! Don't give up", font, 50, yellow)
        screen.blit(title, (80, 200))
        title=text_format("Score:"+str(score), font, 40, black)
        screen.blit(title, (350, 300))
        pygame.display.update()

        losesound.play()

        time.sleep(4)
        k+=1
def screen_kicked(score):
    screen.blit(desertimage2,(0,0))
    title=text_format("You kicked for staying AFK", font, 50, yellow)
    screen.blit(title, (80, 200))
    title=text_format("Score:"+str(score), font, 40, black)
    screen.blit(title, (350, 300))
    pygame.display.update()

    losesound.play()

    time.sleep(4)

room_full=False

def room_full_func():
    screen.blit(desertimage2,(0,0))
    title=text_format("This room is full, choose another", font, 50, yellow)
    screen.blit(title, (80, 200))
    pygame.display.update()
    time.sleep(2)


def restart_of_multiplaye(winners,losers,room,mytank):
    print(1078)

    global screen_lose,screen_win

    g=False
    gg=0
    for i in range(len(winners)):
        if winners[i]['tankId']==mytank.id:
            print(1083)
            print(winners[i]['tankId'])
            print(mytank.id)
            print()
            g=True
            gg=winners[i]["score"]

    o=False
    oo=0
    for i in range(len(losers)):
        if losers[i]['tankId']==mytank.id:
            print(1094)
            print(losers[i]['tankId'])
            print(mytank.id)
            print()
            o=True
            oo=losers[i]["score"]

    if g:
        print(1108)
        screen_win(gg)
    elif o:
        print(1105)
        screen_lose(oo)
    ###
    font = "docktrin.ttf"
    print(room)
    print(winners,1054)
    print(losers,1055)

    text_winners=[]
    text_losers=[]

    screen.blit(img,(0,0))
    title=text_format("Winners", font, 75, yellow)
    losers_text=text_format("Losers", font, 75, yellow)

    winners_texx=text_format("tankID    score", font, 20, (36,100,100))
    losers_texx=text_format("tankID    score", font, 20, (36,100,100))

    for i in range( len( winners)):
        text_winners.append( text_format(str(winners[i]['tankId'])+'   '+str(winners[i]['score']), font, 20, black))

    if losers!=[]:
        for i in range( len( losers)):
            text_losers.append( text_format(str(losers[i]['tankId'])+'   '+str(losers[i]['score']), font, 20, black))

    '''
    title_rect=title.get_rect()
    if losers!=[]:
        losers_rect=losers_text.get_rect()

    winners_rect=[]
    losers_rect=[]

    for i in range( len( winners)):
        winners_rect.append(text_winners[i].get_rect())

    if losers!=[]:
        for i in range( len( losers)):
            losers_rect.append(text_losers[i].get_rect())
    '''
    # Main Menu Text
    
    screen.blit(title, (80, 80))
    screen.blit(losers_text, (500, 80))
    screen.blit(winners_texx,(80,150))
    screen.blit(losers_texx,(500,150))
    for i in range( len( winners)):
        screen.blit(text_winners[i],(80,200+50*i))
    if losers!=[]:
        for i in range( len( losers)):
            screen.blit(text_losers[i],(500,200+50*i))
        
    pygame.display.update()
    time.sleep(4)

    ###
    print(1165)
    restart_of_multiplayer_loop=True
    selected=0
    room=(room[5:])
    room=int(room)
    while restart_of_multiplayer_loop:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                    gta1.play()
                elif event.key==pygame.K_DOWN:
                    selected+=1
                    gta1.play()
                if selected==1:
                    if event.key==pygame.K_RIGHT:
                        room+=1
                        gta2.play()
                    elif event.key==pygame.K_LEFT:
                        room-=1
                        gta2.play()
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        print('Restart')
                        gta3.play()
                        loading()
                        return True,room
                        #return 'room-'+str(room)
                    if selected==1:
                        gta3.play()
                        print(" Room")
                        loading()
                        return True,room
                    if selected==2:
                        gta3.play()
                        print("Main menu")
                        loading()
                        return False,''
                    
        if selected<0:
            selected=0
        elif selected>2:
            selected=2
        if room<1:
            room=1
        elif room>30:
            room=30
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("Multilayer", font, 90, yellow)

        if selected==0:
            text_restart=text_format("Restart", font, 75, white)
        else:
            text_restart = text_format("Restart", font, 75, black)

        if selected==1:
            text_single_player=text_format("Room:", font, 75, white)
            text_room=text_format(str(room), font, 75, white)
        else:
            text_single_player = text_format("Room", font, 75, black)
            text_room=text_format(str(room), font, 75, black)

        if selected==2:
            text_multiplayer=text_format("Main menu", font, 75, white)
        else:
            text_multiplayer = text_format("Main menu", font, 75, black)


        title_rect=title.get_rect()
        restart_rect=text_restart.get_rect()
        single_rect=text_single_player.get_rect()
        multi_rect=text_multiplayer.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_restart, (screen_width/2 - (multi_rect[2]/2)-30, 200))
        screen.blit(text_single_player,( 210, 300))
        screen.blit(text_room,(480,300))
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 400))

        pygame.display.update()
        clock.tick(30)
        pygame.display.set_caption("Tanks Online") 

def multiplayer(nickname,room='',toke='',tankid=''):
    global k
    k=0
    myname=nickname    
    global players
    mytank=Tank(200,200,(0,255,0))
    mytank.me=True
    players = [mytank]
    
    global tankId
    global token

    tankId=''
    token=''

    mytank=Tank(200,200,(0,255,0))
    players = [mytank]
    #bullets_info=[]
    bullets=[]
    #players_info=[]
    previous_info={}

    
    
    mainloop =True

    def parsing_all_info(all_info):
        
        #---------------------------------------------------------------------------------

        for i in range(len(all_info["gameField"]['tanks'])):
            f=False
            for g in range(len(players)):
                if (all_info["gameField"]['tanks'][i]['id']==players[g].id):
                    players[g].id=all_info["gameField"]['tanks'][i]['id']
                    players[g].x=all_info["gameField"]['tanks'][i]['x']
                    players[g].y=all_info["gameField"]['tanks'][i]['y']
                    players[g].direction=all_info["gameField"]['tanks'][i]['direction']
                    players[g].width=all_info["gameField"]['tanks'][i]['width']
                    players[g].height=all_info["gameField"]['tanks'][i]['height']
                    players[g].health=all_info["gameField"]['tanks'][i]['health']
                    players[g].score=all_info["gameField"]['tanks'][i]['score'] 
                    f=True
            if (all_info["gameField"]['tanks'][i]['id']==mytank.id):
                mytank.me=True
                mytank.id=all_info["gameField"]['tanks'][i]['id']
                mytank.x=all_info["gameField"]['tanks'][i]['x']
                mytank.y=all_info["gameField"]['tanks'][i]['y']
                mytank.direction=all_info["gameField"]['tanks'][i]['direction']
                mytank.width=all_info["gameField"]['tanks'][i]['width']
                mytank.height=all_info["gameField"]['tanks'][i]['height']
                mytank.health=all_info["gameField"]['tanks'][i]['health']
                mytank.score=all_info["gameField"]['tanks'][i]['score'] 

            if f==False and (all_info["gameField"]['tanks'][i]['id'] != myname):
                print('New player joined the game: ',all_info["gameField"]['tanks'][i]['id'])
                x = all_info["gameField"]['tanks'][i]['x']
                y = all_info["gameField"]['tanks'][i]['y']  
                p = Tank( x, y, (255,0,50) )
                p.id = all_info["gameField"]['tanks'][i]['id']
                p.direction = all_info["gameField"]['tanks'][i]['direction']
                players.append(p)

        for i in range(len(all_info["gameField"]['bullets'])):
            f=False
            for g in range(len(bullets)):
                if (all_info["gameField"]['bullets'][i]['owner']==bullets[g].id):
                    bullets[g].id=all_info["gameField"]['bullets'][i]['owner']
                    bullets[g].x=all_info["gameField"]['bullets'][i]['x']
                    bullets[g].y=all_info["gameField"]['bullets'][i]['y']
                    bullets[g].direction=all_info["gameField"]['bullets'][i]['direction']
                    #bullets[g].width=all_info["gameField"]['bullets'][i]['width']
                    #bullets[g].height=all_info["gameField"]['bullets'][i]['height']

                    f=True
            if f==False:
                if all_info["gameField"]['bullets'][i]['owner']==mytank.id:
                    pulyaSound.play()
                print('New player joined the game: ',all_info["gameField"]['bullets'][i]['owner'])
                x = all_info["gameField"]['bullets'][i]['x']
                y = all_info["gameField"]['bullets'][i]['y']  
                p = Pulya( x, y )
                p.id = all_info["gameField"]['bullets'][i]['owner']
                p.direction = all_info["gameField"]['bullets'][i]['direction']
                bullets.append(p)
        # print('Len of bullets: '+str(len(bullets)))

        #---------------------------------------------------------------------------------

        deleting_players_list=[]
        for i in range(len(players)):
            f=False
            for g in range(len(all_info["gameField"]['tanks'])):
                if all_info["gameField"]['tanks'][g]['id']==players[i].id:
                    f=True
            if f==False:
                deleting_players_list.append(players[i])
        
        for i in range( len( deleting_players_list )):
            players.remove( deleting_players_list[i] )

        deleting_bullets_list=[]
        for i in range(len(bullets)):
            f=False
            for g in range(len(all_info["gameField"]['bullets'])):
                if all_info["gameField"]['bullets'][g]['owner']==bullets[i].id:
                    f=True
            if f==False:
                deleting_bullets_list.append(bullets[i])
        
        for i in range( len( deleting_bullets_list )):
            bullets.remove( deleting_bullets_list[i] )

        #---------------------------------------------------------------------------------
        print('Number of players: '+ str(len(players)))
        for i in range(len(players)):
            print('player{id},: x:{x} y:{y}'.format(id=players[i].id,x=players[i].x,y=players[i].y))

        print('Number of bullets: '+ str(len(players)))
        for i in range(len(bullets)):
            print('bullet{id},: x:{x} y:{y}'.format(id=bullets[i].id,x=bullets[i].x,y=bullets[i].y))
        #---------------------------------------------------------------------------------
        # try:
        #     for i in range( len( all_info["gameField"]['winners'] )):
        #         winners.append(all_info["gameField"]['winners'][i])

        #     for i in range( len( all_info["gameField"]['losers'] )):
        #         losers.append(all_info["gameField"]['losers'][i])
        # except:
        #     pass
        #---------------------------------------------------------------------------------
        
        global remainingtime
        try:
            print('remaining time 1040'+str(all_info['remainingTime']))
            remainingtime=all_info['remainingTime']
            print('remaining time 1042'+str(remainingtime))
        except:
            pass
        #---------------------------------------------------------------------------------

        global winners
        global losers
        print(all_info,1314)
        print(str(all_info['winners'])+' 1109')
        print(str(winners)+' 1110')
        if all_info['winners']!=[]:
            winners=all_info['winners']
            #restart=restart_of_multiplayer()
            
            losers=all_info['losers']

                

        #---------------------------------------------------------------------------------



        #---------------------------------------------------------------------------------
        
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
        global tankId
        global token
        tankId=body['tankId']
        token=body['token']
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
            #pulyaSound.play()
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
    

    callback_queue=str(uuid.uuid4())        
    corr_id = str(uuid.uuid4())
    class Consuming(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            self.channel = connection.channel()
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)
            def callback(ch,method,properties,body):

                body=json.loads(body)
                if properties.correlation_id=='healthcheck':
                    state,result=healthcheck_info(body)
                if properties.correlation_id=='register':
                    state,result=register_info(body)
                if properties.correlation_id=='turn_tank':
                    state,result=turn_tank_info(body)
                if properties.correlation_id=='fire_bullet':
                    state,result=fire_bullet_info(body)
                print(state,result)
                
            self.channel.basic_consume(queue=self.callback_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
               


    
    class Producer(Thread):

        def __init__(self):
            Thread.__init__(self)
            global winners
            global losers
            winners=[]
            losers=[]
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX'))) 
            self.channel = connection.channel()
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)

        def run(self):
            pass

        def close(self):
            self.channel.close()

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



    print('1355')
    if room=='':
        room=choose_room()
    try:
        if room[:4]=='room':
            pass
    except:
        mainloop=False

    if mainloop==True: 
        con = Consuming()
        con.start()
        prd = Producer()
        prd.start()
        clock=pygame.time.Clock()
        prd.healthcheck()
      
        print('1538')
        prd.register(room)
        trying=True
        while trying:
            if tankId!='':
                trying=False
        mytank.id=tankId

        print('1365')
        event_queue='event.state.'+str(room)


    class Consuming_Game(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            self.channel = connection.channel()
            self.event_queue=str(uuid.uuid4())
            self.channel.queue_declare(queue=self.event_queue,exclusive=True,auto_delete=True)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.event_queue,routing_key=event_queue)
            def callback(ch,method,properties,body):
                print('callback 1235')
                body=json.loads(body)
                parsing_all_info(body)
                if body['winners']!=[]:
                    self.close()           
            self.channel.basic_consume(queue=self.event_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
            exit()    


    if mainloop==True:
        print('remainingtime 1268'+str(remainingtime))


        con_game=Consuming_Game()
        con_game.daemon=True
        con_game.start()
    restarting=False
    pygame.mixer.music.load('music.mp3')
    #pygame.mixer.music.load('media\\multi.mp3')
    pygame.mixer.music.play()
    while mainloop:
        restarting=True
        mill = clock.tick(FPS)
        screen.blit(desertimage2,(0,0))

        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prd.close()
                con.close()
                con_game.close
                exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    a=escape_of_multiplayer()
                    if a==False:
                        restarting=False
                        mainloop=False

        if pressed[pygame.K_SPACE]:
            prd.fire_bullet(token)
            #pulyaSound.play()
            #give_coordinates(mytank,bullets)
        if pressed[pygame.K_UP]:
            mytank.direction='UP'
            prd.turn_tank(token,'UP')
        if pressed[pygame.K_DOWN]:
            mytank.direction='DOWN'
            prd.turn_tank(token,'DOWN')
        if pressed[pygame.K_RIGHT]:
            mytank.direction='RIGHT'
            prd.turn_tank(token,'RIGHT')
        if pressed[pygame.K_LEFT]:
            mytank.direction='LEFT'
            prd.turn_tank(token,'LEFT')
        if pressed[pygame.K_TAB]:
            a=sorted_list_of_players(players)
            font = pygame.font.Font('freesansbold.ttf', 16)
            #global remainingtime
            print('remainingtime 1315' + str(remainingtime))
            text = font.render('Remaining time : ' + str(remainingtime), True, (160,200,255))
            textRect = text.get_rect() 
            textRect.center = ((470), int(170))
            #screen.blit(text, textRect)

            text = font.render('Players       Score    Health', True, (160,200,255))
            textRect = text.get_rect() 
            textRect.center = ((400), int(200))
            screen.blit(text, textRect)
            for i in range ( len( a )):
                if a[i].id==mytank.id:
                    text = font.render('You'+'            '+str(a[i].score)+'            '+str(a[i].health), True, (0,50,255))
                    textRect = text.get_rect() 
                    textRect.center = ((385), int(250+50*i))
                    screen.blit(text, textRect)
                else:
                    text = font.render(str(a[i].id)+'         '+str(a[i].score)+'            '+str(a[i].health), True, (255,255,255))
                    textRect = text.get_rect() 
                    textRect.center = ((385), int(250+50*i))
                    screen.blit(text, textRect)
        
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Remaining time : ' + str(remainingtime), True, (160,200,255))
        screen.blit(text, (550,550))

                
        def fire():       
                prd.fire_bullet(token)
                #pulyaSound.play()
                #give_coordinates(mytank,bullets)
        def up():
                mytank.direction='UP'
                prd.turn_tank(token,'UP')
        def down():
                mytank.direction='DOWN'
                prd.turn_tank(token,'DOWN')
        def right():
                mytank.direction='RIGHT'
                prd.turn_tank(token,'RIGHT')
        def left():
                mytank.direction='LEFT'
                prd.turn_tank(token,'LEFT')


        if winners!=[]:
            mainloop=False

        if kicked!=[]:
            print(kicked,1688)
            for i in range(len(kicked)):
                        print(kicked)
                        if kicked[i]['tankId']==mytank.id:
                            global screen_kicked
                            screen_kicked(kicked[i]['score'])
                            kicked.remove(kicked[i])
        if players!=[]:
            if mytank not in players:
                screen_lose(mytank.score)
        
        try:

            for i in range( len( players)):
                font = pygame.font.Font('freesansbold.ttf', 14) 
                text = font.render(players[i].id, True, (255,255,255))
                textRect = text.get_rect() 
                textRect.center = (int(players[i].x+10), int(players[i].y-22))
                screen.blit(text, textRect)

            

            for i in range(len(players)):
                print('drawing player')
                players[i].move()

            for i in range(len(bullets)):
                print('drawing bullet')
                bullets[i].move()
            
        except:
            pass
            
        print(str(winners)+' 1458')

        
        print()
        clock.tick(10)
        pygame.display.flip()
        global restart_of_multiplaye
    pygame.mixer.music.stop()
    if restarting==True:
        k=0
        print('1699')
        print(winners)
        print(losers)
        if losers!=[]:
            restart,room=restart_of_multiplaye(winners,losers,room,mytank)
        else:
            restart,room=restart_of_multiplaye(winners,[],room,mytank)

        if restart==True:
            multiplayer(nickname,'room-'+str(room))
    else:
            #pass
            con_game.close()
            con.close()
            prd.close()


def multiplayer_with_AI(nickname,room='',toke='',tankid=''):
    global k
    k=0
    myname=nickname    
    global players
    mytank=Tank(200,200,(0,255,0))
    mytank.me=True
    players = [mytank]
    
    global tankId
    global token

    tankId=''
    token=''

    mytank=Tank(200,200,(0,255,0))
    players = [mytank]
    #bullets_info=[]
    bullets=[]
    #players_info=[]
    previous_info={}

    
    
    mainloop =True

    def parsing_all_info(all_info):
        
        #---------------------------------------------------------------------------------

        for i in range(len(all_info["gameField"]['tanks'])):
            f=False
            for g in range(len(players)):
                if (all_info["gameField"]['tanks'][i]['id']==players[g].id):
                    players[g].id=all_info["gameField"]['tanks'][i]['id']
                    players[g].x=all_info["gameField"]['tanks'][i]['x']
                    players[g].y=all_info["gameField"]['tanks'][i]['y']
                    players[g].direction=all_info["gameField"]['tanks'][i]['direction']
                    players[g].width=all_info["gameField"]['tanks'][i]['width']
                    players[g].height=all_info["gameField"]['tanks'][i]['height']
                    players[g].health=all_info["gameField"]['tanks'][i]['health']
                    players[g].score=all_info["gameField"]['tanks'][i]['score'] 
                    f=True
            if (all_info["gameField"]['tanks'][i]['id']==mytank.id):
                mytank.me=True
                mytank.id=all_info["gameField"]['tanks'][i]['id']
                mytank.x=all_info["gameField"]['tanks'][i]['x']
                mytank.y=all_info["gameField"]['tanks'][i]['y']
                mytank.direction=all_info["gameField"]['tanks'][i]['direction']
                mytank.width=all_info["gameField"]['tanks'][i]['width']
                mytank.height=all_info["gameField"]['tanks'][i]['height']
                mytank.health=all_info["gameField"]['tanks'][i]['health']
                mytank.score=all_info["gameField"]['tanks'][i]['score'] 

            if f==False and (all_info["gameField"]['tanks'][i]['id'] != myname):
                print('New player joined the game: ',all_info["gameField"]['tanks'][i]['id'])
                x = all_info["gameField"]['tanks'][i]['x']
                y = all_info["gameField"]['tanks'][i]['y']  
                p = Tank( x, y, (255,0,50) )
                p.id = all_info["gameField"]['tanks'][i]['id']
                p.direction = all_info["gameField"]['tanks'][i]['direction']
                players.append(p)

        for i in range(len(all_info["gameField"]['bullets'])):
            f=False
            for g in range(len(bullets)):
                if (all_info["gameField"]['bullets'][i]['owner']==bullets[g].id):
                    bullets[g].id=all_info["gameField"]['bullets'][i]['owner']
                    bullets[g].x=all_info["gameField"]['bullets'][i]['x']
                    bullets[g].y=all_info["gameField"]['bullets'][i]['y']
                    bullets[g].direction=all_info["gameField"]['bullets'][i]['direction']
                    #bullets[g].width=all_info["gameField"]['bullets'][i]['width']
                    #bullets[g].height=all_info["gameField"]['bullets'][i]['height']

                    f=True
            if f==False:
                if all_info["gameField"]['bullets'][i]['owner']==mytank.id:
                    pulyaSound.play()
                print('New player joined the game: ',all_info["gameField"]['bullets'][i]['owner'])
                x = all_info["gameField"]['bullets'][i]['x']
                y = all_info["gameField"]['bullets'][i]['y']  
                p = Pulya( x, y )
                p.id = all_info["gameField"]['bullets'][i]['owner']
                p.direction = all_info["gameField"]['bullets'][i]['direction']
                bullets.append(p)
        # print('Len of bullets: '+str(len(bullets)))

        #---------------------------------------------------------------------------------

        deleting_players_list=[]
        for i in range(len(players)):
            f=False
            for g in range(len(all_info["gameField"]['tanks'])):
                if all_info["gameField"]['tanks'][g]['id']==players[i].id:
                    f=True
            if f==False:
                deleting_players_list.append(players[i])
        
        for i in range( len( deleting_players_list )):
            players.remove( deleting_players_list[i] )

        deleting_bullets_list=[]
        for i in range(len(bullets)):
            f=False
            for g in range(len(all_info["gameField"]['bullets'])):
                if all_info["gameField"]['bullets'][g]['owner']==bullets[i].id:
                    f=True
            if f==False:
                deleting_bullets_list.append(bullets[i])
        
        for i in range( len( deleting_bullets_list )):
            bullets.remove( deleting_bullets_list[i] )

        #---------------------------------------------------------------------------------
        print('Number of players: '+ str(len(players)))
        for i in range(len(players)):
            print('player{id},: x:{x} y:{y}'.format(id=players[i].id,x=players[i].x,y=players[i].y))

        print('Number of bullets: '+ str(len(players)))
        for i in range(len(bullets)):
            print('bullet{id},: x:{x} y:{y}'.format(id=bullets[i].id,x=bullets[i].x,y=bullets[i].y))
        #---------------------------------------------------------------------------------
        # try:
        #     for i in range( len( all_info["gameField"]['winners'] )):
        #         winners.append(all_info["gameField"]['winners'][i])

        #     for i in range( len( all_info["gameField"]['losers'] )):
        #         losers.append(all_info["gameField"]['losers'][i])
        # except:
        #     pass
        #---------------------------------------------------------------------------------
        
        global remainingtime
        try:
            print('remaining time 1040'+str(all_info['remainingTime']))
            remainingtime=all_info['remainingTime']
            print('remaining time 1042'+str(remainingtime))
        except:
            pass
        #---------------------------------------------------------------------------------

        global winners
        global losers
        print(all_info,1314)
        print(str(all_info['winners'])+' 1109')
        print(str(winners)+' 1110')
        if all_info['winners']!=[]:
            winners=all_info['winners']
            #restart=restart_of_multiplayer()
            print(losers,1323)
            losers=all_info['losers']

                

        #---------------------------------------------------------------------------------



        #---------------------------------------------------------------------------------
        
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
        global tankId
        global token
        tankId=body['tankId']
        token=body['token']
        return True,text

    def turn_tank_info(body):
        if body['status']==200:
            #pulyaSound.play()

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
            pulyaSound.play()

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
    

    callback_queue=str(uuid.uuid4())        
    corr_id = str(uuid.uuid4())
    class Consuming(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            self.channel = connection.channel()
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)
            def callback(ch,method,properties,body):

                body=json.loads(body)
                if properties.correlation_id=='healthcheck':
                    state,result=healthcheck_info(body)
                if properties.correlation_id=='register':
                    state,result=register_info(body)
                if properties.correlation_id=='turn_tank':
                    state,result=turn_tank_info(body)
                if properties.correlation_id=='fire_bullet':
                    state,result=fire_bullet_info(body)
                print(state,result)
                
            self.channel.basic_consume(queue=self.callback_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
               


    
    class Producer(Thread):

        def __init__(self):
            Thread.__init__(self)
            global winners
            global losers
            winners=[]
            losers=[]
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX'))) 
            self.channel = connection.channel()
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)

        def run(self):
            pass

        def close(self):
            self.channel.close()

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


    
    
    print('1355')
    if room=='':
        room=choose_room()
    try:
        if room[:4]=='room':
            pass
    except:
        mainloop=False

    if mainloop==True:
        con = Consuming()
        con.start()
        prd = Producer()
        prd.start()
        clock=pygame.time.Clock()
        prd.healthcheck()   
        print('1538')
        prd.register(room)
        trying=True
        while trying:
            if tankId!='':
                trying=False
        mytank.id=tankId

        print('1365')
        event_queue='event.state.'+str(room)


    class Consuming_Game(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            self.channel = connection.channel()
            self.event_queue=str(uuid.uuid4())
            self.channel.queue_declare(queue=self.event_queue,exclusive=True,auto_delete=True)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.event_queue,routing_key=event_queue)
            def callback(ch,method,properties,body):
                print('callback 1235')
                body=json.loads(body)
                parsing_all_info(body)
                if body['winners']!=[]:
                    self.close()           
            self.channel.basic_consume(queue=self.event_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
            exit()    


    if mainloop==True:
        print('remainingtime 1268'+str(remainingtime))


        con_game=Consuming_Game()
        con_game.daemon=True
        con_game.start()
    restarting=False
    pygame.mixer.music.load('media\\multi_with_ai.mp3')
    pygame.mixer.music.play()
    while mainloop:
        restarting=True
        mill = clock.tick(FPS)
        screen.blit(desertimage2,(0,0))

        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prd.close()
                con.close()
                con_game.close
                exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    a=escape_of_multiplayer()
                    if a==False:
                        restarting=False
                        mainloop=False

        if pressed[pygame.K_SPACE]:
            prd.fire_bullet(token)
            #give_coordinates(mytank,bullets)
        if pressed[pygame.K_UP]:
            mytank.direction='UP'
            prd.turn_tank(token,'UP')
        if pressed[pygame.K_DOWN]:
            mytank.direction='DOWN'
            prd.turn_tank(token,'DOWN')
        if pressed[pygame.K_RIGHT]:
            mytank.direction='RIGHT'
            prd.turn_tank(token,'RIGHT')
        if pressed[pygame.K_LEFT]:
            mytank.direction='LEFT'
            prd.turn_tank(token,'LEFT')
        if pressed[pygame.K_TAB]:
            a=sorted_list_of_players(players)
            font = pygame.font.Font('freesansbold.ttf', 16)
            #global remainingtime
            print('remainingtime 1315' + str(remainingtime))
            text = font.render('Remaining time : ' + str(remainingtime), True, (160,200,255))
            textRect = text.get_rect() 
            textRect.center = ((470), int(170))
            #screen.blit(text, textRect)

            text = font.render('Players       Score    Health', True, (160,200,255))
            textRect = text.get_rect() 
            textRect.center = ((400), int(200))
            screen.blit(text, textRect)
            for i in range ( len( a )):
                if a[i].id==mytank.id:
                    text = font.render('You'+'            '+str(a[i].score)+'            '+str(a[i].health), True, (0,50,255))
                    textRect = text.get_rect() 
                    textRect.center = ((385), int(250+50*i))
                    screen.blit(text, textRect)
                else:
                    text = font.render(str(a[i].id)+'         '+str(a[i].score)+'            '+str(a[i].health), True, (255,255,255))
                    textRect = text.get_rect() 
                    textRect.center = ((385), int(250+50*i))
                    screen.blit(text, textRect)
        
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render('Remaining time : ' + str(remainingtime), True, (160,200,255))
        screen.blit(text, (550,550))

                
        def fire():       
                prd.fire_bullet(token)
                #give_coordinates(mytank,bullets)
        def up():
                mytank.direction='UP'
                prd.turn_tank(token,'UP')
        def down():
                mytank.direction='DOWN'
                prd.turn_tank(token,'DOWN')
        def right():
                mytank.direction='RIGHT'
                prd.turn_tank(token,'RIGHT')
        def left():
                mytank.direction='LEFT'
                prd.turn_tank(token,'LEFT')


        if winners!=[]:
            mainloop=False

        if kicked!=[]:
            print(kicked,1688)
            for i in range(len(kicked)):
                        print(kicked)
                        if kicked[i]['tankId']==mytank.id:
                            global screen_kicked
                            screen_kicked(kicked[i]['score'])
                            kicked.remove(kicked[i])
        if winners!=[]:
            mainloop=False
        if players!=[]:
            if mytank not in players:
                screen_lose(mytank.score)
        
        try:

            for i in range( len( players)):
                font = pygame.font.Font('freesansbold.ttf', 14) 
                text = font.render(players[i].id, True, (255,255,255))
                textRect = text.get_rect() 
                textRect.center = (int(players[i].x+10), int(players[i].y-22))
                screen.blit(text, textRect)

            

            for i in range(len(players)):
                print('drawing player')
                players[i].move()

            for i in range(len(bullets)):
                print('drawing bullet')
                bullets[i].move()
            
        except:
            pass
            
        print(str(winners)+' 1458')
        import math
        def distance(x,y,bx,by):
            d=((x-bx)**2+(y-by)**2)**(1/2)
            if d>200:
                return False
            else:
                return True

        def distance_players(x,y,bx,by):
            d=((x-bx)**2+(y-by)**2)**(1/2)
            if d>50:
                return False
            else:
                return True

        a=players#.remove(mytank)
        for a in players :
          #if distance_players(mytank.x,mytank.y,a.x,a.y):

            if mytank.direction=='UP':

                if a.direction=='UP':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            up()

                        elif mytank.y-5 > a.y:
                            fire()
                            

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            down()
                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            up()
                        elif mytank.y-5 > a.y:
                            fire()
                            left()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:

                            left()
                            fire()
                            

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            right()
                    

                elif a.direction=='LEFT':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            up()
                        elif mytank.y-5 > a.y:
                            fire()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()
                            up()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            right()
                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            up()

                        elif mytank.y-5 > a.y:
                            fire()


                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()
                            up()

                        elif mytank.y-5 > a.y:

                            left()

                        elif mytank.y+25 < a.y:

                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()
                    

            elif mytank.direction=='DOWN':
                
                if a.direction=='UP':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            right()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            left()

                        elif mytank.y+25 < a.y:
                            down()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            down()
                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            right()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()
                            right()

                        elif mytank.y+25 < a.y:
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()
                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            right()
                    

                elif a.direction=='LEFT':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            right()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()
                            down()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            right()


                elif a.direction=='RIGHT':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            left()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()
                            down()

                        elif mytank.y-5 > a.y:
                            left()

                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()
                    

            elif mytank.direction=='LEFT':
                
                if a.direction=='UP':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            up()

                        elif mytank.y-5 > a.y:
                            left()

                        elif mytank.y+25 < a.y:
                            down()
                        

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()
                            
                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            down()
                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            left()
                        elif mytank.y-5 > a.y:
                            fire()
                            right()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            down()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            right()
                    

                elif a.direction=='LEFT':

                    if mytank.x+25>a.x>mytank.x-5:
                        
                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            right()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()

                        elif mytank.y-5 > a.y:
                            pass

                        elif mytank.y+25 < a.y:
                            up()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()
                            up()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            right()

                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            left()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()
                            
                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            up()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            right()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()

                    

            elif mytank.direction=='RIGHT':
                
                if a.direction=='UP':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            right()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            right()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            left()

                        elif mytank.y+25 < a.y:
                            down()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            down()

                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            right()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()
                            right()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            right()

                    

                elif a.direction=='LEFT':

                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            up()

                        elif mytank.y-5 > a.y:
                            right()

                        elif mytank.y+25 < a.y:
                            right()

                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+25>a.x>mytank.x-5:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()
                            left()

                        elif mytank.y-5 > a.y:
                            up()
                            fire()

                        elif mytank.y+25 < a.y:
                            down()
                            fire()

                    elif mytank.x-5 > a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            left()
                            fire()
                            up()

                        elif mytank.y-5 > a.y:
                            left()

                        elif mytank.y+25 < a.y:
                            left()

                    elif mytank.x+25 < a.x:

                        if mytank.y+25>a.y>mytank.y-5:
                            fire()

                        elif mytank.y-5 > a.y:
                            up()

                        elif mytank.y+25 < a.y:
                            down()
        #   else:
        #     if mytank.direction=='UP':

        #         if a.direction=='UP':

        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #         elif a.direction== 'DOWN':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'LEFT':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:

        #         elif a.direction== 'RIGHT':

        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:

        #     elif mytank.direction== 'DOWN':
                
        #         if a.direction=='UP':

        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #         elif a.direction== 'DOWN':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'LEFT':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'RIGHT':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:

                
        #     elif mytank.direction== 'LEFT':

                
        #         if a.direction=='UP':

        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #         elif a.direction== 'DOWN':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'LEFT':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'RIGHT':

        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:

        #     elif mytank.direction== 'RIGHT':
                
        #         if a.direction=='UP':

        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #         elif a.direction== 'DOWN':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'LEFT':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:
        #         elif a.direction== 'RIGHT':
        #             if mytank.x+35>a.x>mytank.x-5:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x-5 > a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:

        #                 elif mytank.y+35 < a.y:

        #             elif mytank.x+35 < a.x:

        #                 if mytank.y+35>a.y>mytank.y-5:

        #                 elif mytank.y-5 > a.y:
                            
        #                 elif mytank.y+35 < a.y:




       # --------------------------------------------------

        # for a in bullets:
        #     if distance(mytank.x,mytank.y,a.x,a.y):
        #         if mytank.direction=='UP':
                    
        #             if a.direction=='UP':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         left()
                            
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

                            

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass
                            
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
                        
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass


        #             elif a.direction=='DOWN':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         pass
                        
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass
                        
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass
                        
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass


        #             elif a.direction=='LEFT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass
                        
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()
                            
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass
                        
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #             elif a.direction=='RIGHT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         down()
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         down()
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #         elif mytank.direction=='DOWN':

        #             if a.direction=='UP':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         right()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #             elif a.direction=='DOWN':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         up()

        #                     elif mytank.y+40<a.y:
        #                         left()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         up()

        #                     elif mytank.y+40<a.y:
        #                         up()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #             elif a.direction=='LEFT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         left()

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()


        #             elif a.direction=='RIGHT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         left()

        #                     elif mytank.y+40<a.y:
        #                         left()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         left()

        #                     elif mytank.y+40<a.y:
        #                         left()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         left()

        #                     elif mytank.y+40<a.y:
        #                         left()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
                            
        #         elif mytank.direction=='LEFT':

        #             if a.direction=='UP':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         right()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         down()

        #                     elif mytank.y+40<a.y:
        #                         down()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         down()

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         down()

        #                     elif mytank.y+40<a.y:
        #                         down()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         down()

        #             elif a.direction=='DOWN':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         right()
        #                     elif mytank.y+40<a.y:
        #                         up()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         up()

        #                     elif mytank.y+40<a.y:

        #                         up()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         up()

        #                     elif mytank.y+40<a.y:
        #                         up()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #             elif a.direction=='LEFT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()
                                
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         right()

        #                     elif mytank.y+40<a.y:
        #                         right()

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #             elif a.direction=='RIGHT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
        #         elif mytank.direction=='RIGHT':

        #             if a.direction=='UP':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass
        #                     elif mytank.y+40<a.y:
        #                         pass
                                
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass
                                
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         down()
        #                     elif mytank.y+40<a.y:
        #                         down()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         down()
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         down()
        #                     elif mytank.y+40<a.y:
        #                         down()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         down()

        #             elif a.direction=='DOWN':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         up()
        #                     elif mytank.y+40<a.y:
        #                         down()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         up()
        #                     elif mytank.y+40<a.y:
        #                         up()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #             elif a.direction=='LEFT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass
                                
        #                     elif mytank.y+40<a.y:
        #                         pass

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass

        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()

        #             elif a.direction=='RIGHT':

        #                 if mytank.x+35>a.x>mytank.x-5:

        #                     if mytank.y-30 >a.y:
        #                         left()
        #                     elif mytank.y+40<a.y:
        #                         left()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         up()
        #                 elif mytank.x-5>a.x:

        #                     if mytank.y-30 >a.y:
        #                         left()
        #                     elif mytank.y+40<a.y:
        #                         left()
        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         down()
        #                 elif mytank.x+35<a.x:

        #                     if mytank.y-30 >a.y:
        #                         pass

        #                     elif mytank.y+40<a.y:
        #                         pass

        #                     elif mytank.y+35>a.y>mytank.y-5:
        #                         pass


        print()
        clock.tick(10)
        pygame.display.flip()
        global restart_of_multiplaye
    pygame.mixer.music.stop()
    if restarting==True:
        k=0
        print('1699')
        print(winners)
        print(losers)
        if losers!=[]:
            restart,room=restart_of_multiplaye(winners,losers,room,mytank)
        else:
            restart,room=restart_of_multiplaye(winners,[],room,mytank)

        if restart==True:
            multiplayer_with_AI(nickname,'room-'+str(room))
    else:
            #pass
            con_game.close()
            con.close()
            prd.close()

# Game Initialization


# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width=800
screen_height=600
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
img=pygame.image.load('media\\800-600.png')

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
        screen.blit(text_nickname, (screen_width/2 - (nickname_rect[2]/2), screen_height-300))#(screen_width/2 - (nickname_rect[2]/2), 260)
        screen.blit(text_n,(screen_width/2 - (n_rect[2]/2), screen_height-350))
        screen.blit(text_conf, (screen_width/2 - (conf_rect[2]/2), screen_height-100))
        
        pygame.display.update()
    return nickname
         




'''def multiplayer_with_AII(nickname):
    myname=nickname    
    global players
    mytank=Tank(200,200,(0,255,0))
    mytank.me=True
    players = [mytank]
    
    global tankId
    global token

    tankId=''
    token=''

    mytank=Tank(200,200,(0,255,0))
    players = [mytank]
    #bullets_info=[]
    bullets=[]
    #players_info=[]
    previous_info={}

    
    
    mainloop =True

    def parsing_all_info(all_info):
        
        #---------------------------------------------------------------------------------

        for i in range(len(all_info["gameField"]['tanks'])):
            f=False
            for g in range(len(players)):
                if (all_info["gameField"]['tanks'][i]['id']==players[g].id):
                    players[g].id=all_info["gameField"]['tanks'][i]['id']
                    players[g].x=all_info["gameField"]['tanks'][i]['x']
                    players[g].y=all_info["gameField"]['tanks'][i]['y']
                    players[g].direction=all_info["gameField"]['tanks'][i]['direction']
                    players[g].width=all_info["gameField"]['tanks'][i]['width']
                    players[g].height=all_info["gameField"]['tanks'][i]['height']
                    players[g].health=all_info["gameField"]['tanks'][i]['health']
                    players[g].score=all_info["gameField"]['tanks'][i]['score'] 
                    f=True
            if (all_info["gameField"]['tanks'][i]['id']==mytank.id):
                mytank.me=True
                mytank.id=all_info["gameField"]['tanks'][i]['id']
                mytank.x=all_info["gameField"]['tanks'][i]['x']
                mytank.y=all_info["gameField"]['tanks'][i]['y']
                mytank.direction=all_info["gameField"]['tanks'][i]['direction']
                mytank.width=all_info["gameField"]['tanks'][i]['width']
                mytank.height=all_info["gameField"]['tanks'][i]['height']
                mytank.health=all_info["gameField"]['tanks'][i]['health']
                mytank.score=all_info["gameField"]['tanks'][i]['score'] 

            if f==False and (all_info["gameField"]['tanks'][i]['id'] != myname):
                print('New player joined the game: ',all_info["gameField"]['tanks'][i]['id'])
                x = all_info["gameField"]['tanks'][i]['x']
                y = all_info["gameField"]['tanks'][i]['y']  
                p = Tank( x, y, (255,0,50) )
                p.id = all_info["gameField"]['tanks'][i]['id']
                p.direction = all_info["gameField"]['tanks'][i]['direction']
                players.append(p)

        for i in range(len(all_info["gameField"]['bullets'])):
            f=False
            for g in range(len(bullets)):
                if (all_info["gameField"]['bullets'][i]['owner']==bullets[g].id):
                    bullets[g].id=all_info["gameField"]['bullets'][i]['owner']
                    bullets[g].x=all_info["gameField"]['bullets'][i]['x']
                    bullets[g].y=all_info["gameField"]['bullets'][i]['y']
                    bullets[g].direction=all_info["gameField"]['bullets'][i]['direction']
                    #bullets[g].width=all_info["gameField"]['bullets'][i]['width']
                    #bullets[g].height=all_info["gameField"]['bullets'][i]['height']

                    f=True
            if f==False:
                print('New player joined the game: ',all_info["gameField"]['bullets'][i]['owner'])
                x = all_info["gameField"]['bullets'][i]['x']
                y = all_info["gameField"]['bullets'][i]['y']  
                p = Pulya( x, y )
                p.id = all_info["gameField"]['bullets'][i]['owner']
                p.direction = all_info["gameField"]['bullets'][i]['direction']
                bullets.append(p)
        # print('Len of bullets: '+str(len(bullets)))

        #---------------------------------------------------------------------------------

        deleting_players_list=[]
        for i in range(len(players)):
            f=False
            for g in range(len(all_info["gameField"]['tanks'])):
                if all_info["gameField"]['tanks'][g]['id']==players[i].id:
                    f=True
            if f==False:
                deleting_players_list.append(players[i])
        
        for i in range( len( deleting_players_list )):
            players.remove( deleting_players_list[i] )

        deleting_bullets_list=[]
        for i in range(len(bullets)):
            f=False
            for g in range(len(all_info["gameField"]['bullets'])):
                if all_info["gameField"]['bullets'][g]['owner']==bullets[i].id:
                    f=True
            if f==False:
                deleting_bullets_list.append(bullets[i])
        
        for i in range( len( deleting_bullets_list )):
            bullets.remove( deleting_bullets_list[i] )

        #---------------------------------------------------------------------------------
        print('Number of players: '+ str(len(players)))
        for i in range(len(players)):
            print('player{id},: x:{x} y:{y}'.format(id=players[i].id,x=players[i].x,y=players[i].y))

        print('Number of bullets: '+ str(len(players)))
        for i in range(len(bullets)):
            print('bullet{id},: x:{x} y:{y}'.format(id=bullets[i].id,x=bullets[i].x,y=bullets[i].y))
        #---------------------------------------------------------------------------------
        # try:
        #     for i in range( len( all_info["gameField"]['winners'] )):
        #         winners.append(all_info["gameField"]['winners'][i])

        #     for i in range( len( all_info["gameField"]['losers'] )):
        #         losers.append(all_info["gameField"]['losers'][i])
        # except:
        #     pass
        #---------------------------------------------------------------------------------
        
        global remainingtime
        try:
            print('remaining time 1040'+str(all_info['remainingTime']))
            remainingtime=all_info['remainingTime']
            print('remaining time 1042'+str(remainingtime))
        except:
            pass
        #---------------------------------------------------------------------------------

        global winners
        global losers
        print(str(all_info['winners'])+' 1109')
        print(str(winners)+' 1110')
        if all_info['winners']!=[]:
            winners=all_info['winners']
            losers=all_info['losers']
            #restart=restart_of_multiplayer()
            

                

        #---------------------------------------------------------------------------------



        #---------------------------------------------------------------------------------
        
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
        global tankId
        global token
        tankId=body['tankId']
        token=body['token']
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
    

    callback_queue=str(uuid.uuid4())        
    corr_id = str(uuid.uuid4())
    class Consuming(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            self.channel = connection.channel()
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)
            def callback(ch,method,properties,body):

                body=json.loads(body)
                if properties.correlation_id=='healthcheck':
                    state,result=healthcheck_info(body)
                if properties.correlation_id=='register':
                    state,result=register_info(body)
                if properties.correlation_id=='turn_tank':
                    state,result=turn_tank_info(body)
                if properties.correlation_id=='fire_bullet':
                    state,result=fire_bullet_info(body)
                print(state,result)
                
            self.channel.basic_consume(queue=self.callback_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
            exit()    


    
    class Producer(Thread):

        def __init__(self):
            Thread.__init__(self)
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX'))) 
            self.channel = connection.channel()
            self.callback_queue=callback_queue
            self.channel.queue_declare(queue=self.callback_queue)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.callback_queue)

        def run(self):
            pass

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
    
    print('1355')
    room=choose_room()
    try:
        if room[:4]=='room':
            pass
    except:
        mainloop=False

    if mainloop==True:   
        print('1387')
        prd.register(room)
        trying=True
        while trying:
            if tankId!='':
                trying=False
        mytank.id=tankId

        print('1365')
        event_queue='event.state.'+str(room)


    class Consuming_Game(Thread):

        def run(self):
            connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
            print("Consuming started!")
            self.channel = connection.channel()
            self.event_queue=str(uuid.uuid4())
            self.channel.queue_declare(queue=self.event_queue,exclusive=True,auto_delete=True)
            self.channel.queue_bind(exchange='X:routing.topic', queue=self.event_queue,routing_key=event_queue)
            def callback(ch,method,properties,body):
                print('callback 1235')
                body=json.loads(body)
                parsing_all_info(body)           
            self.channel.basic_consume(queue=self.event_queue,on_message_callback=callback, auto_ack=True)
            self.channel.start_consuming()

        def close(self):
            self.channel.close()
            exit()    


    if mainloop==True:
        print('remainingtime 1268'+str(remainingtime))


        con_game=Consuming_Game()
        con_game.start()
    while mainloop:
        mill = clock.tick(FPS)
        screen.blit(desertimage2,(0,0))
        #fill_edges()
        #score()
        #delete_bad_status_bullets()
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prd.close()
                con.close()
                con_game.close
                exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    a=escape_of_multiplayer()
                    if a==False:
                        
                        mainloop=False

        def fire():       
                prd.fire_bullet(token)
                #pulyaSound.play()
                #give_coordinates(mytank,bullets)
        def up():
                mytank.direction='UP'
                prd.turn_tank(token,'UP')
        def down():
                mytank.direction='DOWN'
                prd.turn_tank(token,'DOWN')
        def right():
                mytank.direction='RIGHT'
                prd.turn_tank(token,'RIGHT')
        def left():
                mytank.direction='LEFT'
                prd.turn_tank(token,'LEFT')
        if pressed[pygame.K_TAB]:
            a=sorted_list_of_players(players)
            font = pygame.font.Font('freesansbold.ttf', 14)
            #global remainingtime
            print('remainingtime 1315' + str(remainingtime))
            text = font.render('Remaining time : ' + str(remainingtime), True, (160,200,255))
            textRect = text.get_rect() 
            textRect.center = ((470), int(170))
            screen.blit(text, textRect)
            text = font.render('players    health    score', True, (160,200,255))
            textRect = text.get_rect() 
            textRect.center = ((450), int(200))
            screen.blit(text, textRect)
            for i in range ( len( a )):
                text = font.render(str(a[i].id)+'         '+str(a[i].health)+'         '+str(a[i].score), True, (255,255,255))
                textRect = text.get_rect() 
                textRect.center = ((450), int(250+50*i))
                screen.blit(text, textRect)

        if winners!=[]:
            restart=restart_of_multiplaye(winners)
        
        try:
            for i in range( len( players)):
                font = pygame.font.Font('freesansbold.ttf', 14) 
                text = font.render(players[i].id, True, (255,255,255))
                textRect = text.get_rect() 
                textRect.center = (int(players[i].x+10), int(players[i].y-22))
                screen.blit(text, textRect)

            for i in range(len(players)):
                print('drawing player')
                players[i].move()

            for i in range(len(bullets)):
                print('drawing bullet')
                bullets[i].move()
   
        except:
            pass
        
        print(str(winners)+' 1458')

        #AI---------------------------------------------------------------------------
        def distance(a,b):
            c=(a.x-b.x)**2+(a.y-b.y)**2
            return c

        a=players#.remove(mytank)
        for a in players :
            if mytank.direction=='UP':

                if a.direction=='UP':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            up()

                        elif mytank.y-15 > a.y:
                            fire()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 > a.y:
                            down()
                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            up()
                        elif mytank.y-15 > a.y:
                            fire()
                            left()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            rigth()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            right()
                    

                elif a.direction=='LEFT':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            up()
                        elif mytank.y-15 > a.y:
                            fire()
                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            up()

                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 < a.y:
                            right()
                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            up()

                        elif mytank.y-15 > a.y:
                            fire()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            up()
                        elif mytank.y-15 > a.y:
                            fire()
                            left()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()
                    

            elif mytank.direction=='DOWN':
                
                if a.direction=='UP':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            right()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            left()

                        elif mytank.y+45 < a.y:
                            down()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 < a.y:
                            down()
                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            right()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()
                            right()

                        elif mytank.y+45 < a.y:
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()
                        elif mytank.y+45 < a.y:
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            right()
                    

                elif a.direction=='LEFT':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            right()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()
                            down()

                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 < a.y:
                            fire()
                            right()

                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            left()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()
                            down()

                        elif mytank.y-15 > a.y:
                            left()

                        elif mytank.y+45 < a.y:
                            fire()
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()
                    

            elif mytank.direction=='LEFT':
                
                if a.direction=='UP':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            up()

                        elif mytank.y-15 > a.y:
                            left()

                        elif mytank.y+45 < a.y:
                            fire()
                            down()
                        

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()
                            
                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 < a.y:
                            down()
                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            left()
                        elif mytank.y-15 > a.y:
                            fire()
                            right()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            down()

                        elif mytank.y-15 > a.y:
                            fire()
                            up()

                        elif mytank.y+45 < a.y:
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            right()
                            fore()
                            up()

                        elif mytank.y+45 < a.y:
                            right()
                    

                elif a.direction=='LEFT':

                    if mytank.x+45>a.x>mytank.x-15:
                        
                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            right()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()

                        elif mytank.y-15 > a.y:
                            fire()

                        elif mytank.y+45 < a.y:
                            right()
                            fire()
                            up()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()
                            up()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()
                            right()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()
                            right()

                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            left()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()
                            
                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            up()

                        elif mytank.y-15 > a.y:
                            fire()
                            up()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            right()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()

                    

            elif mytank.direction=='RIGHT':
                
                if a.direction=='UP':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            right()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            right()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            left()

                        elif mytank.y+45 < a.y:
                            down()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()

                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 < a.y:
                            down()

                    
                            
                elif a.direction=='DOWN':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            right()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()
                            right()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()

                        elif mytank.y-15 > a.y:
                            fire()
                            up()

                        elif mytank.y+45 < a.y:
                            right()

                    

                elif a.direction=='LEFT':

                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            up()

                        elif mytank.y-15 > a.y:
                            right()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()
                            right()

                    

                elif a.direction=='RIGHT':
                    
                    if mytank.x+45>a.x>mytank.x-15:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()
                            left()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()

                    elif mytank.x-15 > a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            left()
                            fire()
                            up()

                        elif mytank.y-15 > a.y:
                            up()
                            fire()
                            left()

                        elif mytank.y+45 < a.y:
                            down()
                            fire()
                            left()

                    elif mytank.x+45 < a.x:

                        if mytank.y+45>a.y>mytank.y-15:
                            fire()

                        elif mytank.y-15 > a.y:
                            up()

                        elif mytank.y+45 < a.y:
                            down()

                    


        clock.tick(10)
        pygame.display.flip()
'''

# Main Menu
def main_menu():

    menu=True
    selected=0
    import uuid
    nickname='Change_this'
    
    while menu:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected-=1
                    gta1.play()
                elif event.key==pygame.K_DOWN:
                    selected+=1
                    gta1.play()
                if event.key==pygame.K_RETURN:
                    if selected==0:
                        gta3.play()
                        print("Single Player")
                        single_player(nickname)

                    if selected==1:
                        gta3.play()
                        print("Multiplayer")
                        try:
                            multiplayer(nickname)
                        except:
                            pass
                    if selected==2:
                        gta3.play()
                        print("Multiplayer with AI")
                        try:
                            multiplayer_with_AI(nickname)
                        except:
                            pass
                    if selected==3:
                        gta3.play()
                        print('Change name')
                        nickname = change_name(nickname)
                    if selected==4:
                        gta3.play()
                        pygame.quit()
                        quit()
        if selected<0:
            selected=0
        elif selected>4:
            selected=4
        # Main Menu UI
        screen.blit(img,(0,0))
        title=text_format("Tanks Online", font, 90, yellow)

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
        screen.blit(text_single_player, (screen_width/2 - (single_rect[2]/2), 200)) #240
        screen.blit(text_multiplayer, (screen_width/2 - (multi_rect[2]/2), 270)) #300
        screen.blit(text_multiplayer_with_ai, (screen_width/2 - (multi_ai_rect[2]/2), 340)) #360
        screen.blit(text_change_name,(screen_width/2 - (change_name_rect[2]/2), 410)) #420
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 480)) #480
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Tanks Online")

#Initialize the Game
main_menu()
pygame.quit()
quit()

pygame.quit()