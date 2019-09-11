import pygame
import random
import sys
from pygame.locals import *

windowwidth = 600
windowheight = 600
textcolr = (255,255,255)
backgroundcolor = (0,0,0)
fps = 40
baddieminsize = 10
baddiemaxsize = 40
baddieminspeed = 1
baddiemaxspeed = 8
addnewbaddierate = 6
playermoverate = 5


#退出游戏
def terminate():
    pygame.quit()
    sys.exit()

# 循环等待
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

# 碰撞
def playerHasHitBaddie(PlayerRect, baddies):
    for b in baddies:
        if PlayerRect.colliderect(b["rect"]):
            return True
    return False

# 显示文本信息
def drawText(text,font,surface,x,y):
    textobj = font.render(text,1,textcolr)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# 设置界面元素
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode([windowwidth,windowheight])
pygame.display.set_caption("躲避者")
pygame.mouse.set_visible(True)
font = pygame.font.SysFont(None,48)

#设置声音
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# 设置img
playerImg = pygame.image.load("player.png")
playerRect = playerImg.get_rect()
baddieImg = pygame.image.load("baddie.png")


# 开始文本框信息
drawText("Dodger",font,windowSurface,(windowwidth/3),(windowheight/3))
drawText("Press a key to start",font,windowSurface,(windowwidth/3)-30,(windowheight/3)+50)
pygame.display.update()
waitForPlayerToPressKey()



topScore = 0 #最高分数
number = 0

while True:
    
    # 设置游戏开始
    baddies = []
    score = 0
    playerRect.topleft = (windowwidth / 2, windowheight - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    playerRect = playerImg.get_rect()
 
    
    while True: 
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            # 用户按下时触发
            if event.type == KEYDOWN:
                if event.key == ord('z'):#反向
                    reverseCheat = True 
                if event.key == ord('x'):#减速
                    slowCheat =True 
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP or event.key == ord('w'):
                    moveDown= False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown= True

            # 用户松开时触发
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
            
            # 跟随鼠标移动
            if event.type == MOUSEMOTION:
                playerRect.move_ip(event.pos[0] - playerRect.centerx,event.pos[1] - playerRect.centery)


        # 增加 baddies
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == addnewbaddierate:
            baddieAddCounter = 0
            baddiesize = random.randint(baddieminsize,baddiemaxsize)
            newbaddie = {
                        'rect':pygame.Rect(random.randint(0,windowwidth-baddiesize),0-baddiesize,baddiesize,baddiesize),
                        'speed':random.randint(baddieminspeed,baddiemaxspeed),
                        'surface':pygame.transform.scale(baddieImg,(baddiesize,baddiesize)),
                    }
            baddies.append(newbaddie)

        #设置人物移动
        if moveLeft and playerRect.left>0:
            playerRect.move_ip(-1*playermoverate,0)     
        if moveRight and playerRect.right < windowwidth:
            playerRect.move_ip(playermoverate, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playermoverate)
        if moveDown and playerRect.bottom < windowheight:
            playerRect.move_ip(0, playermoverate)
            
        #设置鼠标光标位置
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        #设置baddies下落
        for bad in baddies:
            if not reverseCheat and not slowCheat:
                bad['rect'].move_ip(0,bad['speed'])
            elif reverseCheat:
                bad['rect'].move_ip(0, -5)
            elif slowCheat:
                bad['rect'].move_ip(0, 1)

        for bad in baddies[:]:
            if bad['rect'].top > windowheight:
                baddies.remove(bad)

        # draw the gane word on the window   
        windowSurface.fill(backgroundcolor)
        # graw score
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('number: %s' %(number), font , windowSurface,10, 80)

        # draw player's rectangle
        
        windowSurface.blit(playerImg, playerRect)
        
        # draw baddie
        for bad in baddies:
            windowSurface.blit(bad['surface'], bad['rect'])

        pygame.display.update()

        


         # 碰撞检测
        # if playerHasHitBaddie(playerRect, baddies):
        #     number +=1

        for bad in baddies:
            if playerRect.colliderect(bad["rect"]): 
                number += 1
                baddies.remove(bad)
                

        if number ==4:
            number =0
            if score > topScore:
                topScore = score
            break   

        # if playerHasHitBaddie(playerRect, baddies) and number ==4:
        #     number=0
        #     if score > topScore:
        #         topScore = score # set new top score
        #     break

        mainClock.tick(fps)


    # 游戏结束.   
    pygame.mixer.music.stop() 
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (windowwidth / 3), (windowheight / 3))
    drawText('Press a key to play again.', font, windowSurface, (windowwidth / 3) - 80, (windowheight / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()


    gameOverSound.stop()


