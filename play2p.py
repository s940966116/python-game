# encoding: utf-8
import socket
import os, sys, random
import pygame 
from pygame.locals import *
import time
from drew import *
#con for 2P
HOST = socket.gethostname()
PORT = 8000

# 視窗大小.
canvas_width = 800
canvas_height = 600
 
# 顏色.
block = (0,0,0)
 
# 磚塊數量串列.
bricks_list = []
 
# 移動速度.
dx =  8
dy = -8
score = 0
#初始狀態
start = 1
# 遊戲狀態.
# 0:等待開球
# 1:遊戲進行中
game_mode = 0
mode = 0
#建立socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#-------------------------------------------------------------------------
#連接server
def init_connecting(client):
    global connection
    if not connection:
        client.connect((HOST, PORT))
        connection = 1

#-------------------------------------------------------------------------
# 函數:秀字.
#-------------------------------------------------------------------------
def showFont( text, x, y, font, color):
    global canvas    
    text = font.render(text, 1, color) 
    canvas.blit( text, (x,y))

#-------------------------------------------------------------------------
# 函數:碰撞判斷.
#   x       : x 
#   y       : y 
#   boxRect : 矩形
#-------------------------------------------------------------------------
def isCollision( x, y, boxRect):
    if (x >= boxRect[0] and x <= boxRect[0] + boxRect[2] and y >= boxRect[1] and y <= boxRect[1] + boxRect[3]):
        return True;          
    return False;  
 
#-------------------------------------------------------------------------
# 函數:初始遊戲.
#-------------------------------------------------------------------------
def resetGame():
    # 宣告使用全域變數.
    global game_mode, brick_num, bricks_list, dx, dy, score
    # 磚塊
    for bricks in bricks_list:
        # 亂數磚塊顏色
        r = random.randint(100,200)
        g = random.randint(100,200)
        b = random.randint(100,200)
        bricks.color = [r,g,b]        
        # 開啟磚塊.
        bricks.visivle = True
    # 0:等待開球
    game_mode = 0
    # 磚塊數量.
    brick_num = 99    
    # 移動速度.
    dx =  8
    dy = -8
    dx1 = 8 
    dy1 = -8
    
    score = 0
#msg = (連接狀態,遊戲狀態,輸贏)
def judge(msg):
    global start, client
    s = msg.split(",")
    if s[2] == "win":
        client.send("connect,end,lose".encode('utf-8'))
        canvas.blit(background, (0,0))
        showFont( "You lose!!!!", 220, 200, font2, (255, 0, 0))
        showFont( "Score:" + str(score), 200, 250, font2, (255, 0, 0))
        pygame.display.update()
        start = 1
        resetGame()
        time.sleep(3)
        
    elif s[2] == "lose":
        client.send("connect,end,win".encode('utf-8'))
        canvas.blit(background, (0,0))
        showFont( "You win!!!!", 220, 200, font2, (255, 0, 0))
        showFont( "Score:" + str(score), 200, 250, font2, (255, 0, 0))
        pygame.display.update()
        start = 1
        resetGame()
        time.sleep(3)
        
connection = 0       
ack = 1
# 初始.
pygame.init()
# 顯示Title.
pygame.display.set_caption("打磚塊遊戲")
# 建立畫佈大小.
canvas = pygame.display.set_mode((canvas_width, canvas_height))
background = pygame.image.load("./pic3.jpg")
# 時脈.
clock = pygame.time.Clock()
 
# 設定字型-黑體.
font = pygame.font.SysFont('SimHei', 30)
font1 = pygame.font.SysFont('SimHei', 70)
font2 = pygame.font.SysFont('arias', 120)
font3 = pygame.font.SysFont('arias', 140)
# 底板.
paddle_x = 0
paddle_y = (canvas_height - 48)
paddle = Box(pygame, canvas, "paddle", [paddle_x, paddle_y, 100, 24], (200,200,200))

# 球.
ball_x = paddle_x
ball_y = paddle_y
ball   = Circle(pygame, canvas, "ball", [ball_x, ball_x], 8, (255,255,255))

# 建立磚塊
brick_num = 0
brick_x = 70
brick_y = 60
brick_w = 0
brick_h = 0
for i in range(0, 99):
    if((i % 11)==0):
        brick_w = 0
        brick_h = brick_h + 18        
    bricks_list.append (Box(pygame, canvas, "brick_"+str(i), [  brick_w + brick_x, brick_h+ brick_y, 58, 16], [255,255,255]))
    brick_w = brick_w + 60
# 初始遊戲.
resetGame()

button1 = button(pygame, canvas, "Start Game", [250, 210, 300, 80], (0, 201, 87), showFont, font1)
button2 = button(pygame, canvas, "  Multiplay", [250, 280, 300, 80], (0, 201, 87), showFont, font1)
button3 = button(pygame, canvas, " End Game", [250, 350, 300, 80], (0, 201, 87), showFont, font1)

#-------------------------------------------------------------------------    
# 主迴圈.
#-------------------------------------------------------------------------
running = True
while running:
    canvas.blit(background, (0,0))
    #初始畫面
    while start:
        showFont('Breakout clone', 100, 100, font2, (255, 227, 132))
        button1.update()
        button2.update()
        button3.update()

        for event in pygame.event.get():
            # 離開遊戲.
            if event.type == pygame.QUIT:
                running = False
                start = 0
                mode = 0
            # 判斷按下按鈕
            if event.type == pygame.KEYDOWN:
                # 判斷按下ESC按鈕
                if event.key == pygame.K_ESCAPE:
                    running = False
                    start = 0
                    mode = 0
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if isCollision(pos[0], pos[1], button1.rect):
                    game_mode = 0
                    mode = 1
                    start = 0
                elif isCollision(pos[0], pos[1], button2.rect):
                    game_mode = 1
                    mode = 2
                    start = 0
                    ack = 1
                    msg = "connect,none,none"
                    init_connecting(client)
                    while True:
                        client.send(msg.encode('utf-8'))
                        canvas.blit(background, (0,0))
                        showFont("Connecting...", 180, 250, font2, (255, 0, 0))
                        pygame.display.update()  
                        reply = (client.recv(1024)).decode('utf-8')
                        reply = reply.split(",")
                        print(reply)
                        if reply[0] == "connect":
                            client.send(msg.encode('utf-8'))
                            break
                    for i in range(4):
                        if i != 3:
                            canvas.blit(background, (0,0))
                            showFont(str(3-i), 400, 300, font3, (255, 0, 0))
                            pygame.display.update()  
                        else:
                            canvas.blit(background, (0,0))
                            showFont("start!", 350, 300, font3, (255, 0, 0))
                            pygame.display.update()
                        time.sleep(1)
                elif isCollision(pos[0], pos[1], button3.rect):
                    running = False
                    mode = 0
                    start = 0
                    
        pygame.display.update()    
    #---------------------------------------------------------------------
    # 判斷輸入.
    #---------------------------------------------------------------------
    for event in pygame.event.get():
        # 離開遊戲.
        if event.type == pygame.QUIT:
            running = False
            mode = 0
        # 判斷按下按鈕
        if event.type == pygame.KEYDOWN:
            # 判斷按下ESC按鈕
            if event.key == pygame.K_ESCAPE:
                running = False
                mode = 0
                
        # 判斷Mouse.
        if event.type == pygame.MOUSEMOTION:
            paddle_x = pygame.mouse.get_pos()[0] - 50

        if event.type == pygame.MOUSEBUTTONDOWN:
            if(game_mode == 0):
                game_mode = 1
 
    #---------------------------------------------------------------------    
    # 清除畫面.
#    canvas.fill(block)
#    canvas.blit(background, (0,0))
    # 磚塊
    if mode == 0:
        canvas.blit(background, (0,0))
        showFont("Bye Bye~~~", 200, 250, font2, (255, 69, 0))
        pygame.display.update()
        time.sleep(3)
    elif mode == 1:
        for bricks in bricks_list:
            # 球碰磚塊.
            if(isCollision( ball.pos[0], ball.pos[1], bricks.rect)):
                if(bricks.visivle):                
                    # 扣除磚塊.
                    brick_num = brick_num -1
                    score += 1
                    # 初始遊戲.
                    if(brick_num <= 0):
                        
                        canvas.blit(background, (0,0))
                        showFont( "Score:" + str(score), 8, 2, font2, (255, 0, 0))
                        resetGame()
                        break
                    # 球反彈.
                    dy = -dy; 
                # 關閉磚塊.
                bricks.visivle = False
     
            # 更新磚塊.        
            bricks.update()
                
        #顯示磚塊數量.
        showFont("bricks number:"+str(brick_num),   8, 20, font, (255, 0, 0))            
        
        # 秀板子.
        paddle.rect[0] = paddle_x
        paddle.update()
        
     
        # 碰撞判斷-球碰板子.
        if(isCollision( ball.pos[0], ball.pos[1], paddle.rect)):        
            # 球反彈.
            dy = -dy;         
                
        # 球.
        # 0:等待開球
        if(game_mode == 0):
            ball.pos[0] = ball_x = paddle.rect[0] + ( (paddle.rect[2] - ball.radius) >> 1 )
            ball.pos[1] = ball_y = paddle.rect[1] - ball.radius        
        # 1:遊戲進行中
        elif(game_mode == 1):
            ball_x += dx
            ball_y += dy
            #判斷死亡.
            if(ball_y + dy > canvas_height - ball.radius):
                canvas.blit(background, (0,0))
                start = 1     
                showFont( "Score:" + str(score), 200, 250, font2, (255, 0, 0))
                pygame.display.update()
                resetGame()
                time.sleep(3)
            # 右牆或左牆碰撞.
            if(ball_x + dx > canvas_width - ball.radius or ball_x + dx < ball.radius):
                dx = -dx
            # 下牆或上牆碰撞
            if(ball_y + dy > canvas_height - ball.radius or ball_y + dy < ball.radius):        
                dy = -dy
            ball.pos[0] = ball_x
            ball.pos[1] = ball_y
     
        # 更新球.
        ball.update()
     
        # 顯示中文.
        showFont( "Score:" + str(score), 8, 2, font, (255, 0, 0))    
        # 更新畫面.
        
    elif mode == 2:
        for bricks in bricks_list:
            # 球碰磚塊.
            if(isCollision( ball.pos[0], ball.pos[1], bricks.rect)):
                if(bricks.visivle):                
                    # 扣除磚塊.
                    brick_num = brick_num -1
                    score += 1
                    # 初始遊戲.
                    if(brick_num <= 0):
                        ack = 0
                        client.send("connect,end,win".encode('utf-8'))
                        time.sleep(1)
                        canvas.blit(background, (0,0))
                        showFont( "You win!!!!", 220, 200, font2, (255, 0, 0))
                        showFont( "Score:" + str(score), 200, 250, font2, (255, 0, 0))
                        pygame.display.update()
                        time.sleep(3)
                        start = 1
                        client.close()
                        resetGame()
                        break
                    # 球反彈.
                    dy = -dy; 
                # 關閉磚塊.
                bricks.visivle = False
     
            # 更新磚塊.        
            bricks.update()
                
        #顯示磚塊數量.
        showFont("bricks number:"+str(brick_num),   8, 20, font, (255, 0, 0))            
        
        # 秀板子.
        paddle.rect[0] = paddle_x
        paddle.update()

        # 碰撞判斷-球碰板子.
        if(isCollision(ball.pos[0], ball.pos[1], paddle.rect)):        
            # 球反彈.
            dy = -dy;       
    
                
        # 球.
        # 0:等待開球
        if(game_mode == 0):
            ball.pos[0] = ball_x = paddle.rect[0] + ( (paddle.rect[2] - ball.radius) >> 1 )
            ball.pos[1] = ball_y = paddle.rect[1] - ball.radius  
       
        # 1:遊戲進行中
        elif(game_mode == 1):
            ball_x += dx
            ball_y += dy
            #判斷死亡.
            if(ball_y + dy > canvas_height - ball.radius):
                ack = 0
                canvas.blit(background, (0,0))
                showFont( "You lose!!!!", 220, 200, font2, (255, 0, 0))
                showFont( "Score:" + str(score), 200, 250, font2, (255, 0, 0))
                client.send("connect,end,lose".encode('utf-8'))
                pygame.display.update()
                resetGame()
                time.sleep(3)
                start = 1
            # 右牆或左牆碰撞.
            if(ball_x + dx > canvas_width - ball.radius or ball_x + dx < ball.radius):
                dx = -dx
            # 下牆或上牆碰撞
            if(ball_y + dy > canvas_height - ball.radius or ball_y + dy < ball.radius):        
                dy = -dy
            ball.pos[0] = ball_x
            ball.pos[1] = ball_y
            
     
        # 更新球.
        ball.update()
     
        # 顯示中文.
        showFont( "Score:" + str(score), 8, 2, font, (255, 0, 0))
        if ack:
            client.send("connect,start,none".encode('utf-8'))
        msg = (client.recv(1024)).decode('utf-8')
        judge(msg)
    pygame.display.update()
    clock.tick(60)
 
# 離開遊戲.
pygame.quit()