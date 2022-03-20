from js import document, window
from math import pi
from random import random

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
  rect(0, 0, WIDTH, HEIGHT)

def move_paddle(evt):
    global x_bar_change
    # print(evt.keyCode)
    if evt.keyCode == 39:
        x_bar_change = 15
    elif evt.keyCode == 37:
        x_bar_change = -15        
    else:
        print("key not known")

def animate():
    
  global x, y, dx, dy
  global x_bar, x_bar_change
  
  x_bar += x_bar_change
  
  # clear screen
  ctx.fillStyle = "#FAF7F8"
  rect(0,0,WIDTH,HEIGHT)

  # draw green brick and check for brick hit
  ctx.fillStyle = "#00FF00"
  for a, b in blocks:
    if x + dx >= a - RAD and x + dx <= a + BLOCK_WIDTH + RAD and y + dy >= b - RAD and y + dy <= b + BLOCK_HEIGHT + RAD:
        blocks.remove((a, b))
        dy = - dy
        dy *= 0.9 + 0.2 * random()  
    else:
        rect(a, b, BLOCK_WIDTH, BLOCK_HEIGHT) 
   
  # bouncing off edge
  if x + dx > WIDTH or x + dx < 0:
    dx = -dx
  
  if y + dy < 0:
    dy = -dy
    
  # bouncing off bar
  if x + dx >= x_bar and x + dx <= x_bar + BAR_WIDTH and y + dy >= (HEIGHT - 2 * BAR_HEIGHT):
    dy = -dy
    dy *= 0.9 + 0.2 * random()
  
  if y + dy > HEIGHT:
    print("Game Over")
    window.clearInterval(intervalHandle)  

  x += dx
  y += dy
  
  # draw ball
  ctx.fillStyle = "#444444"   
  circle(x, y, RAD)
    
  # draw paddle
  ctx.fillStyle = "#FF0000"
  rect(x_bar, HEIGHT - 2 * BAR_HEIGHT, BAR_WIDTH, BAR_HEIGHT)
  
  x_bar_change = 0

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")

WIDTH = canvas.width
HEIGHT = canvas.height
RAD = 10
BAR_WIDTH = 60
BAR_HEIGHT = 10
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 40

x = 0
y = 0
dx = 2
dy = 3

blocks = [(300, 50), (300, 100)]

x_bar = (WIDTH - BAR_WIDTH) / 2
x_bar_change = 0

reset()
window.addEventListener('keydown', move_paddle, True)
intervalHandle = window.setInterval(animate, 10)
