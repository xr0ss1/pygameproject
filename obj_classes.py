import pygame
import math
class Player(pygame.sprite.Sprite):
	def create_anim(self,filename,n,ind):
		for i in range(1,n):
			self.anim_list[ind].append(pygame.image.load(filename+str(i+1)+'.bmp').convert_alpha())

			
			
	def change_anim(self,ind):
		if self.cur_anim!=ind:
			self.images=[]
			self.cur_anim=ind
			for i in self.anim_list[ind]:
				self.images.append(i)
				self.cur_img=0
				self.img_cnt=0
				self.max_img=len(self.images)
			print(ind)
			
			
	def __init__(self,x):
		self.move_check=[0,0,0,0]
		self.anim_list={'move':[],'stand':[]}
		self.create_anim('sprites/s_pl_move',6,'stand')
		self.create_anim('sprites/s_pl_move',6,'move')
		self.cur_anim='--'
		self.change_anim('stand')
		
		self.rect = self.images[0].get_rect()
		self.rect.x=640
		self.rect.y=320
		self.rect.move_ip(32,32)
		
		self.speed = 0
		self.last_sd=-1
		self.max_speed=2
		self.cur_img=0
		self.img_cnt=0
		self.img_speed=60
		self.max_img=len(self.images)
		
		self.deg=0
		
		self.r_x=0
		self.r_y=0
		
		self.image=self.images[self.cur_img]
		self.rot_image=pygame.transform.rotate(self.image,0)
		
	def rotate(self):
		mouse_x,mouse_y=pygame.mouse.get_pos()
		rel_x,rel_y=mouse_x-self.rect.x,mouse_y-self.rect.y
		angle=(180/math.pi)*(-math.atan2(rel_y,rel_x))
		self.rot_image=pygame.transform.rotate(self.image,angle)
		
	def move(self,*args):
		if abs(self.speed)<abs(self.max_speed):
			self.speed+=.1
		self.move_check[args[0]]=1
		self.change_anim('move')
		
	def anim_check(self,k_p):
		self.img_cnt+=1
		if self.img_cnt>=self.img_speed:
			self.cur_img+=1
			if self.cur_img>self.max_img-1:
				self.cur_img=0
			self.img_cnt=0
		if (not k_p['key_left']) and (not k_p['key_right'])and (not k_p['key_up'])and (not k_p['key_down']):
			self.change_anim('stand')
	def draw(self,par):
		#self.image.rect.center=(-32,-32)
		self.rect=self.rot_image.get_rect(center=self.rect.center)
		par.blit(self.rot_image,self.rect)
		rad=float(self.deg/(180/math.pi))
		dx=self.rect.x+int(math.cos(rad)*30)
		dy=self.rect.y+int(math.sin(rad)*30)
		pygame.draw.line(par, (255,255,255), [self.rect.x, self.rect.y],[dx,dy], 3)
	
	def update(self,k_p):
		self.image=self.images[self.cur_img]
		self.anim_check(k_p)
		self.rotate()
		if abs(self.speed)>0.03 and(not k_p['key_up']) and (not k_p['key_down']):
			if self.speed>0:
				self.speed-=0.025
			if self.speed<0:
				self.speed+=0.025
		else:
			if (not k_p['key_up']) and (not k_p['key_down']):
				self.speed=0
		cnt=0
		for i in self.move_check:
			if i==1 :
				cnt+=1
		d_sp=self.speed
		if cnt>1:
			d_sp=self.speed/math.sin(math.radians(45))
		for i in range(len(self.move_check)):
			if self.move_check[i]==1:
				if i==0:
					self.rect.x-=d_sp
				if i==1:
					self.rect.y-=d_sp
				if i==2:
					self.rect.x+=d_sp
				if i==3:
					self.rect.y+=d_sp
			self.move_check[i]=0
			
		
class Bullet(pygame.sprite.Sprite):
	def __init__(self,*args):
		self.btype=[['sprites/bul1.png',20],['sprites/bul2.png',10]]
		print(self.btype[0][0])
		self.image=pygame.image.load(self.btype[args[0]][0]).convert_alpha()
		self.rect = self.image.get_rect(center=(args[1],args[2]))
		self.xx=args[3]
		self.yy=args[4]
		self.speed=self.btype[args[0]][1]
		gip=((self.xx-self.rect.x)**2+(self.yy-self.rect.y)**2)**(1/2)
		d_gip=self.speed/gip
		self.dx=(self.xx-self.rect.x)*d_gip
		self.dy=(self.yy-self.rect.y)*d_gip
		print(self.image,self.xx,self.yy,self.speed,self.dx,self.dy,self.rect)
	def draw(self,par):
		par.blit(self.image,self.rect)
	def update(self):
		self.rect.x+=self.dx
		self.rect.y+=self.dy
		
