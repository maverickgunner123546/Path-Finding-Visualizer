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

n=75
m=75

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
		
def draw_grid(x,y,red_arr,display_screen,blocks,goal,start,path_x,path_y,green_arr):
	
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
			if(path_x*STEP_X+GAP*path_x==c1 and path_y*STEP_Y+GAP*path_y==c2):
				pygame.draw.rect(display_screen,GREEN,rect)
				green_arr.append((path_x,path_y))
			if(green_arr.count((j,i))>0):
				pygame.draw.rect(display_screen,GREEN,rect)


	
def fun_make_grid():
	
	
	print("\nGrid>")
	for i in range(n):
		for j in range(m):
			print("(",i,",",j,")",end="  ")
		print("\n")
	
	cost=0.00000000000001
	
	cost_2=0
	grid_val_right_2=[[cost_2 for i in range(m)] for j in range(n)]
	grid_val_left_2=[[cost_2 for i in range(m)] for j in range(n)]
	grid_val_up_2=[[cost_2 for i in range(m)] for j in range(n)]
	grid_val_down_2=[[cost_2 for i in range(m)] for j in range(n)]
	grid_val_right=[[0 for i in range(m)] for j in range(n)]
	
	for i in range(n):
		for j in range(m):
			if(j!=m-1):
				grid_val_right[i][j]=cost
			else:
				grid_val_right[i][j]=(INT_MAX)
				
	print("\nRight move costs >")
	for i in grid_val_right:
		for j in i:
			print(j,end=" ")
		print("\n")
		
	grid_val_left=[[0 for i in range(m)] for j in range(n)]
	for i in range(len(grid_val_right)):
		for j in range(len(grid_val_right[i])):
			if(j==0):
				grid_val_left[i][j]=INT_MAX
			else:
				grid_val_left[i][j]=grid_val_right[i][j-1]
				
	
				
	print("\nLeft move costs > ")
	for i in grid_val_left:
		for j in i:
			print(j,end=" ")
		print("\n")
	
	grid_val_up=[[0 for i in range(m)] for j in range(n)]
	
	for i in range(n):
		for j in range(m):
			if(i!=0):
				grid_val_up[i][j]=cost
			else:
				grid_val_up[i][j]=(INT_MAX)
		
		
	print("\nUp move costs > ")	
	for i in grid_val_up:
		for j in i:
			print(j,end=" ")
		print("\n")
		
		
	grid_val_down=[[0 for i in range(m)] for j in range(n)]
	for i in range(len(grid_val_up)):
		if(i==len(grid_val_up)-1):
			for j in range(len(grid_val_up[i])):
				grid_val_down[i][j]=(INT_MAX)
		else:	
			for j in range(len(grid_val_up[i])):
				grid_val_down[i][j]=(grid_val_up[i+1][j])
	
			
	print("\nDown move costs >")
	for i in grid_val_down:
		for j in i:
			print(j,end=" ")
		print("\n")
		
	print("Enter the x coordinate of the start point> ")
	x1=(int)(input())
	print("Enter the y coordinate of the start point> ")
	y1=(int)(input())
	print("Enter the x coordinate of the end point> ")
	x2=(int)(input())
	print("Enter the y coordinate of the end point> ")
	y2=(int)(input())
	
	heuristics=[[0 for i in range(m)] for j in range(n)]

	for i in range(len(heuristics)):
		for j in range(len(heuristics[i])):
				heuristics[i][j]=(math.sqrt( (i-y2)*(i-y2) + (j-x2)*(j-x2) ))
	
		
	print("\nStraight line distance from destination or Heuristics\n >")
	for i in range(len(heuristics)):
		for j in range(len(heuristics)):
			print(heuristics[i][j],end=" ")
		print("\n")
	
	
	print("\nGet path from (",x1,",",y1,") to (",x2,",",y2,")\n")
	
	distance=[[0 for i in range(m)] for j in range(n)]
	for i in range(len(heuristics)):
		for j in range(len(heuristics[i])):
			distance[i][j]=(INT_MAX/2)
			
	
	
	distance[y1][x1]=0
	print("\nDistances> ")
	for i in range(len(distance)):
		for j in range(len(distance[i])):
			print(distance[i][j],end=" ")
		print("")
		
	
	
	blocks=[]
	tops=4
	bottoms=n-4
	block_no=(int)((n*m)/2.7)
	for i in range(block_no):
		bx=random.randint(0,m-4)
		by=random.randint(0,n-4)
		if((bx==x1 and by==y1) or (by==y2 and bx==x2)):
			continue
		else:
			blocks.append((bx,by))
	''''for i in range(0,m,4):
		for j in range(tops,n):
			if((j==y1 and i==x1) or (i==x2 and j==y2)):
				continue
			else:
				blocks.append((i,j))
	for i in range(2,m,4):
		for j in range(0,bottoms):
			if((j==y1 and i==x1) or (i==x2 and j==y2)):
				continue
			else:
				blocks.append((i,j))'''
				
	q1=PriorityQueue()
	q1.put((heuristics[y1][x1],(x1,y1)))
	path=[]
	
	distance_2=[[INT_MAX for i in range(n)] for j in range(m)]
	distance_2[x1][y1]=0
	
	while(q1.qsize()):
		ele=q1.get()
		ver_x=ele[1][0]
		ver_y=ele[1][1]
		if(blocks.count((ver_x,ver_y))>0):
			continue
		path.append((ver_x,ver_y))
		if(ver_y==y2 and ver_x==x2):
			break
		if(ver_y+1<n):	
			if(distance[ver_y][ver_x] +grid_val_down[ver_y][ver_x]<distance[ver_y+1][ver_x]):
				distance[ver_y+1][ver_x]=distance[ver_y][ver_x] +grid_val_down[ver_y][ver_x]
			if(distance_2[ver_x][ver_y]+grid_val_down_2[ver_y][ver_x]<distance_2[ver_x][ver_y+1]):
				distance_2[ver_x][ver_y+1]= distance_2[ver_x][ver_y]+ grid_val_down_2[ver_y][ver_x]
				q1.put((heuristics[ver_y+1][ver_x],(ver_x,ver_y+1)))
		if(ver_y-1>=0):
			if(distance[ver_y][ver_x] +grid_val_up[ver_y][ver_x]<distance[ver_y-1][ver_x]):
				distance[ver_y-1][ver_x]=distance[ver_y][ver_x] +grid_val_up[ver_y][ver_x]
			if(distance_2[ver_x][ver_y]+grid_val_up_2[ver_y][ver_x]<distance_2[ver_x][ver_y-1]):
				distance_2[ver_x][ver_y-1]= distance_2[ver_x][ver_y]+ grid_val_up_2[ver_y][ver_x]
				q1.put((heuristics[ver_y-1][ver_x],(ver_x,ver_y-1)))
		if(ver_x+1<m):		
			if(distance[ver_y][ver_x] +grid_val_right[ver_y][ver_x]<distance[ver_y][ver_x+1]):
				distance[ver_y][ver_x+1]=distance[ver_y][ver_x] +grid_val_right[ver_y][ver_x]
			if(distance_2[ver_x][ver_y]+grid_val_right_2[ver_y][ver_x]<distance_2[ver_x+1][ver_y]):
				distance_2[ver_x+1][ver_y]=distance_2[ver_x][ver_y]+grid_val_right_2[ver_y][ver_x]
				q1.put((heuristics[ver_y][ver_x+1],(ver_x+1,ver_y)))
		if(ver_x-1>=0):		
			if(distance[ver_y][ver_x] +grid_val_left[ver_y][ver_x]<distance[ver_y][ver_x-1]):
				distance[ver_y][ver_x-1]=distance[ver_y][ver_x] +grid_val_left[ver_y][ver_x]
			if(distance_2[ver_x][ver_y]+grid_val_left_2[ver_y][ver_x]<distance_2[ver_x-1][ver_y]):
				distance_2[ver_x-1][ver_y]=distance_2[ver_x][ver_y]+grid_val_left_2[ver_y][ver_y]
				q1.put((heuristics[ver_y][ver_x-1],(ver_x-1,ver_y)))
    
	red_arr=[]
	display_screen=fun_get_display()
	for i in path:
		draw_grid(i[0],i[1],red_arr,display_screen,blocks,(x2,y2),(x1,y1),-1,-1,[])
		pygame.display.flip()
		pygame.time.wait(0)
	
	q2=deque()
	path_2=[]
	q2.append((x2,y2))
	is_found=False
	while(len(q2)):
		ele=q2.popleft()
		ver_x=ele[0]
		ver_y=ele[1]
		path_2.append((ver_x,ver_y))
		if(ver_x==x1 and ver_y==y1):
			is_found=True;
			break
		min_indices=(INT_MAX,INT_MAX)
		min_dis=INT_MAX
		if(ver_x+1<m and red_arr.count((ver_x+1,ver_y))>0):
			if(min_dis>distance[ver_y][ver_x+1]):
				min_indices=(ver_x+1,ver_y)
				min_dis=distance[ver_y][ver_x+1]
		if(ver_x-1>=0 and red_arr.count((ver_x-1,ver_y))>0):
			if(min_dis>distance[ver_y][ver_x-1]):
				min_indices=(ver_x-1,ver_y)
				min_dis=distance[ver_y][ver_x-1]
		if(ver_y+1<n and red_arr.count((ver_x,ver_y+1))>0):
			if(min_dis>distance[ver_y+1][ver_x]):
				min_indices=(ver_x,ver_y+1)
				min_dis=distance[ver_y+1][ver_x]
		if(ver_y-1>=0 and red_arr.count((ver_x,ver_y-1))>0):
			if(min_dis>distance[ver_y-1][ver_x]):
				min_indices=(ver_x,ver_y-1)
				min_dis=distance[ver_y-1][ver_x]
		if(min_indices[0]!=INT_MAX):
			q2.append(min_indices)
	green_arr=[]
	path_2.reverse()
	if(is_found):
		for i in path_2:
			draw_grid(-1,-1,red_arr,display_screen,blocks,(x2,y2),(x1,y1),i[0],i[1],green_arr)
			pygame.display.flip()
		
		
		
def main():
	grid_1=1
	fun_make_grid()
	fun_events()


main()
