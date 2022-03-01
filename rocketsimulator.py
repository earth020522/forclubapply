import pygame
import keyboard
import math
import os
import time

pygame.init()

#screen size
size=[800,600]
screen=pygame.display.set_mode(size)

pygame.display.set_caption("Rocket Simulator")

done=False
clock=pygame.time.Clock()
font= pygame.font.SysFont("consolas",20)
current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

falcon9=pygame.image.load(os.path.join(image_path, 'falcon.png'))

#varibales
#falcon 9 for example
#추력:8450000N, 비추력 282초
#1단 시간 170초
#즉 1초에 8450000N이라고 보면 1초당 2417.6kg 사용, 즉 1kg당 3495.2N의 힘
height=0 #in meter
height=float(height)
weight=22200 #in kilogram
fuel=400000 #연로랑 산화제 구분 안함.
fuelpower=3495.2
fuelpersec=0
rocketv=0 #in m/s
rocketa=0
rockettilt=0
load=10000
g=0
turnedon=0
lasth=0
xcor=0
xv=0
xa=0
#t=timefromshoot
em=5970000000000000000000000 #kg, earth mass
er=6371000 #m
gc=6.67*0.00000000001 #using m, kg

def printText(msg, color, pos=(10,10)):
    textSurface= font.render(msg,True, color,None)
    textRect= textSurface.get_rect()
    textRect.topleft=pos
 
    screen.blit(textSurface, textRect)

while not done:
    #FPS
    clock.tick(30)
    
    #variable setting
    g=gc*(em/((er+height)*(er+height)))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
    
    #test-----------------------
    if keyboard.is_pressed("u"):
        height=height+300
    if keyboard.is_pressed("i"):
        height=height+1
    if keyboard.is_pressed("y"):
        height=height+10000
    #----------------------------
    if keyboard.is_pressed("up"):
        fuelpersec=fuelpersec+10
    if fuelpersec>=10:
        if keyboard.is_pressed("down"):
            fuelpersec=fuelpersec-10
    if keyboard.is_pressed("right"):
        fuelpersec=fuelpersec+100
    if fuelpersec>=100:
        if keyboard.is_pressed("left"):
            fuelpersec=fuelpersec-100
    if keyboard.is_pressed("q"):
        if rockettilt==359:
            rockettilt=0
        else:
            rockettilt=rockettilt+1
    if keyboard.is_pressed("e"):
        if rockettilt==0:
            rockettilt=359
        else:
            rockettilt=rockettilt-1
    if keyboard.is_pressed("r"):
        height=0 #in meter
        height=float(height)
        weight=22200 #in kilogram
        fuel=400000 #연로랑 산화제 구분 안함.
        fuelpower=3495.2
        fuelpersec=0
        rocketv=0 #in m/s
        rocketa=0
        rockettilt=0
        g=0
        turnedon=0
        lasth=0
        xcor=0
        xv=0
        xa=0
    if keyboard.is_pressed("space"):
        turnedon=1
    if keyboard.is_pressed("s"):
        turnedon=0
    if turnedon==1:    
        if (fuel-fuelpersec/30)>=0:
            fuel=fuel-fuelpersec/30
            rocketa=(fuelpersec*fuelpower*math.cos(rockettilt*(math.pi/180))-(fuel+weight+load)*g)/(fuel+weight+load)
            xa=fuelpersec*fuelpower*math.sin(rockettilt*(math.pi/180))
            if height>=0:
                lastrv=rocketv
                lastx=xv
                rocketv=rocketv+rocketa*(1/30)
                xv=xv+xa*(1/30)
                height=height+(1/2)*(lastrv+rocketv)*(1/30)
                xcor=xcor+(1/2)*(lastx+xv)*(1/30)
                height=round(height,4)
                xcor=round(xcor,4)
        if (fuel-fuelpersec/30)<0:
            fuel=0
            fuelpersec=0
            rocketa=(fuelpersec*fuelpower-(fuel+weight+load)*g)/(fuel+weight+load)
            if height>=0:
                lastrv=rocketv
                rocketv=rocketv+rocketa*(1/30)
                height=height+(1/2)*(lastrv+rocketv)*(1/30)
                height=round(height,4)

    #if keyboard.is_pressed("l"):
        #launch start


    #black at 80000m
    if height<=80000:
        screen.fill((200-height*0.0025,200-height*0.0025,255-height*0.0025))
    else:
        screen.fill((0,0,55))

    pygame.draw.rect(screen, (0,0,0), [10,10,200,20])
    pygame.draw.rect(screen, (0,0,0), [10,35,200,20])
    pygame.draw.rect(screen, (0,0,0), [10,60,200,20])
    pygame.draw.rect(screen, (0,0,0), [10,85,200,20])
    pygame.draw.rect(screen, (0,0,0), [10,110,200,20])
    pygame.draw.rect(screen, (0,0,0), [10,135,200,20])
    pygame.draw.rect(screen, (0,0,0), [10,160,200,20])

    if height<300:
        pygame.draw.rect(screen, (0,150,0), [0,300+height,800,400])
    printText("height : "+str(height), (255,255,255))
    printText("g.const : "+str(g), (255,255,255),(10,35))
    printText("fuelpersec : "+str(fuelpersec), (255,255,255),(10,60))
    printText("fuel : "+str(fuel), (255,255,255),(10,85))
    printText("rocketa : "+str(rocketa), (255,255,255),(10,110))
    printText("rocketv : "+str(rocketv), (255,255,255),(10,135))
    printText("rockettile : "+str(rockettilt),(255,255,255),(10,160))
    pygame.draw.rect(screen, (255,255,255), [600,0,200,600])
    pygame.draw.rect(screen, (5,5,5), [690,570-height*0.005375,20,30])

    rotated=pygame.transform.rotate(falcon9,rockettilt)
    rect=rotated.get_rect()
    rect.center=(300,300)
    screen.blit(rotated,rect)
    pygame.display.flip()
    

    
