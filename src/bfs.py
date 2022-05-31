
import random
import math
import pygame
from queue import PriorityQueue
from collections import deque


RED=(255,0,0)
WHITE=(255,255,255)
CREAM_YELLOW=(254, 250, 224)
L_GREEN=(233, 237, 201)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)

INT_MAX=1000000000
SCREEN_WIDTH=1100
SCREEN_HEIGHT=600
STEP_X=0.0
STEP_Y=0.0
BLOCK_SIZE=28

n=70
m=70


pygame.init()
def fun_get_display():
	display_screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	pygame.display.set_caption("Grids")
	display_screen.fill(L_GREEN)
	return display_screen



def fun_events():
	running=True
	while(running):
		for event in pygame.event.get():
			if(event.type==pygame.QUIT):
				running=False
		pygame.display.flip()
		
def draw_grid(x,y,red_arr,display_screen,blocks,goal,start,green_x,green_y,green_arr):
	
	STEP_X=SCREEN_WIDTH/m
	STEP_Y=SCREEN_HEIGHT/n
	GAP=max(STEP_X,STEP_Y)/7
	for i in range(n):
		for j in range(m):
			c1=j*STEP_X+GAP*j
			c2=i*STEP_Y+GAP*i
			rect=pygame.Rect(c1,c2,STEP_X,STEP_Y)
			if(blocks.count((j,i))>0):
				pygame.draw.rect(display_screen,BLACK,rect)
			elif(x*STEP_X+GAP*x==c1 and y*STEP_Y+GAP*y==c2):
				pygame.draw.rect(display_screen,RED,rect)
				red_arr.append((x,y))
			elif(red_arr.count((j,i))>0):
				pygame.draw.rect(display_screen,RED,rect)
			else:
				pygame.draw.rect(display_screen,CREAM_YELLOW,rect)
			if(j==goal[0] and i==goal[1]):
				pygame.draw.rect(display_screen,GREEN,rect)
			if(j==start[0] and i==start[1]):
				pygame.draw.rect(display_screen,BLUE,rect)
			if(green_x*STEP_X+GAP*green_x==c1 and green_y*STEP_Y+GAP*green_y==c2):
				pygame.draw.rect(display_screen,GREEN,rect)
				green_arr.append((green_x,green_y))
			if(green_arr.count((j,i))>0):
				pygame.draw.rect(display_screen,GREEN,rect)
		
	
def fun_make_grid():

	print("\nGrid>")
	for i in range(n):
		for j in range(m):
			print("(",i,",",j,")",end="  ")
		print("\n")
	
	
		
	print("Enter the x coordinate of the start point> ")
	x1=(int)(input())
	print("Enter the y coordinate of the start point> ")
	y1=(int)(input())
	print("Enter the x coordinate of the end point> ")
	x2=(int)(input())
	print("Enter the y coordinate of the end point> ")
	y2=(int)(input())
	
	
	
	print("\nGet path from (",x1,",",y1,") to (",x2,",",y2,")\n")
	
	
	
	blocks=[]
	
	
	q1=deque()
	q1.append((x1,y1))
	path=[]
	visited=[[False for i in range(m)] for j in range(n)]
	distance=[[INT_MAX for i in range(m)] for j in range(n)]
	distance[y1][x1]=0
	while(len(q1)):
		ele=q1.popleft()
		ver_x=ele[0]
		ver_y=ele[1]
		if(blocks.count((ver_x,ver_y))>0):
			continue
		path.append((ver_x,ver_y))
		visited[ver_y][ver_x]=True
		if(ver_y==y2 and ver_x==x2):
			break
		if(ver_y+1<n and visited[ver_y+1][ver_x]==False):
			q1.append((ver_x,ver_y+1))
			visited[ver_y+1][ver_x]=True
			distance[ver_y+1][ver_x]=distance[ver_y][ver_x]+1
		if(ver_y-1>=0 and visited[ver_y-1][ver_x]==False):
			q1.append((ver_x,ver_y-1))
			visited[ver_y-1][ver_x]=True
			distance[ver_y-1][ver_x]=distance[ver_y][ver_x]+1
		if(ver_x+1<m and visited[ver_y][ver_x+1]==False):
			q1.append((ver_x+1,ver_y))
			visited[ver_y][ver_x+1]=True
			distance[ver_y][ver_x+1]=distance[ver_y][ver_x]+1
		if(ver_x-1>=0 and visited[ver_y][ver_x-1]==False):
			q1.append((ver_x-1,ver_y))
			visited[ver_y][ver_x-1]=True
			distance[ver_y][ver_x-1]=distance[ver_y][ver_x]+1
    
	red_arr=[]
	display_screen=fun_get_display()
	for i in path:
		draw_grid(i[0],i[1],red_arr,display_screen,blocks,(x2,y2),(x1,y1),-1,-1,[])
		pygame.display.flip()
		pygame.time.wait(0)
	
	path_2=[]
	q2=deque()
	q2.append((x2,y2))
	
	while(len(q2)):
		ele=q2.popleft()
		ver_x=ele[0]
		ver_y=ele[1]
		path_2.append((ver_x,ver_y))
		
		if(ver_x==x1 and ver_y==y1):
			is_found=True
			break
		min_dis=INT_MAX
		min_ind=(INT_MAX,INT_MAX)
	
		if(ver_x+1<m and red_arr.count((ver_x+1,ver_y))>0 and distance[ver_y][ver_x+1]==distance[ver_y][ver_x]-1):
				q2.append((ver_x+1,ver_y))
		elif(ver_x-1>=0 and red_arr.count((ver_x-1,ver_y))>0 and distance[ver_y][ver_x-1]==distance[ver_y][ver_x]-1):
				q2.append((ver_x-1,ver_y))
		elif(ver_y+1<n and red_arr.count((ver_x,ver_y+1))>0 and distance[ver_y+1][ver_x]==distance[ver_y][ver_x]-1):
				q2.append((ver_x,ver_y+1))
		elif(ver_y-1>=0 and red_arr.count((ver_x,ver_y-1))>0 and distance[ver_y-1][ver_x]==distance[ver_y][ver_x]-1):
				q2.append((ver_x,ver_y-1))
			
	path_2.reverse()
	green_arr=[]
	for i in path_2:
		draw_grid(-1,-1,red_arr,display_screen,blocks,(x2,y2),(x1,y1),i[0],i[1],green_arr)
		pygame.display.flip()
		
		
def main():
	grid_1=1
	fun_make_grid()
	fun_events()


main()
