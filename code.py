from js import document, window
from math import pi
from random import random

##############
# GLOBAL VARIABLES
##############

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")

# coordinates of top left of each block
blocks = [(300, 50), (300, 100), (150,50)]

# paddle settings:  bar_left_coordinate, next_change
paddle_settings = [(SCREEN_WIDTH - BAR_WIDTH) // 2, 0]

# ball settings: ball_x, ball_y, change_x, change_y]
ball_settings = [0, 0, 2, 3]

#############
# CONSTANTS
############

SCREEN_WIDTH = canvas.width
SCREEN_HEIGHT = canvas.height
RAD = 10
BAR_WIDTH = 60
BAR_HEIGHT = 10
BAR_MOVE_STEP = 15
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 40

#############
# SUBPROGRAMS
#############

def circle(x, y, r):
  ctx.beginPath()
  ctx.arc(x, y, r, 0, pi * 2, True)
  ctx.fill()

def rect(x, y, w, h):
  ctx.beginPath()
  ctx.rect(x,y,w,h)
  ctx.closePath()
  ctx.fill()

def reset():
  ctx.fillStyle = "#FAF7F8"
  rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

def move_paddle(evt):
    # print(evt.keyCode)
    if evt.keyCode == 39:
        paddle_settings[1] = BAR_MOVE_STEP
    elif evt.keyCode == 37:
        paddle_settings[1] = -BAR_MOVE_STEP        
    else:
        print("key not known")

def animate():
  
  x, y, dx, dy = ball_settings

  # change ball location
  x += dx
  y += dy
  
  # update paddle x-coordinate
  paddle_settings[0] += paddle_settings[1]
  paddle_settings[1] = 0
  
  # clear screen
  reset()

  # draw green brick and check for brick hit
  ctx.fillStyle = "#00FF00"
  for a, b in blocks:
    if x >= a - RAD and x <= a + BLOCK_WIDTH + RAD and y >= b - RAD and y <= b + BLOCK_HEIGHT + RAD:
        blocks.remove((a, b))
        dy = - dy
        dy *= 0.9 + 0.2 * random()  
    else:
        rect(a, b, BLOCK_WIDTH, BLOCK_HEIGHT) 
   
  # bouncing off edge
  if x > WIDTH or x < 0:
    dx = -dx
    x += dx
  
  if y < 0:
    dy = -dy
    y += dy
    
  # bouncing off bar
  if x >= x_bar and x <= x_bar + BAR_WIDTH and y >= (SCREEN_HEIGHT - 2 * BAR_HEIGHT):
    dy = -dy * (0.9 + 0.2 * random())
    y += dy
  
  # check for lost game
  if y > HEIGHT:
    print("Game Over")
    window.clearInterval(intervalHandle)  
  
  # draw ball
  ctx.fillStyle = "#444444"   
  circle(x, y, RAD)
    
  # draw paddle
  ctx.fillStyle = "#FF0000"
  rect(paddle_settings[0], SCREEN_HEIGHT - 2 * BAR_HEIGHT, BAR_WIDTH, BAR_HEIGHT)
  
  # update ball settings
  ball_settings[0] = x
  ball_settings[1] = y
  ball_settings[2] = dx
  ball_settings[3] = dy

reset()
window.addEventListener('keydown', move_paddle, True)
intervalHandle = window.setInterval(animate, 10)
