import pygame
import math
class Player(pygame.sprite.Sprite):
	def create_anim(self,filename,n,ind):
		for i in range(0,n):
			self.anim_list[ind].append(pygame.image.load(filename+str(i+1)+'.png').convert_alpha())

			
			
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
			
	def init_guns(self):
			self.guns=[]
			self.guns.append([pygame.image.load('sprites/pl_pistol.png').convert_alpha(),20,100,7,300]		)
			
	def __init__(self,x):
		self.move_check=[0,0,0,0]
		self.anim_list={'move':[],'stand':[]}
		self.create_anim('sprites/pl_walk',6,'stand')
		self.create_anim('sprites/pl_walk',6,'move')
		self.cur_anim='--'
		self.change_anim('stand')
		self.init_guns()
		self.rect = self.images[0].get_rect(center=(320,160))
		
		
		self.hp=100
		self.speed = 0
		self.last_sd=-1
		self.max_speed=1
		self.cur_img=0
		self.img_cnt=0
		self.img_speed=120
		self.max_img=len(self.images)
		
		self.deg=0
		self.legs_deg=0
		self.r_x=0
		self.r_y=0
		
		self.image=self.images[self.cur_img]
		
		
		self.cur_gun=0
		
		self.gun_image=self.guns[self.cur_gun][0]
		self.leg_image=pygame.transform.rotate(self.image,self.legs_deg)
		self.gun_rect=self.gun_image.get_rect(center=self.rect.center)
		self.legs_rect=self.gun_image.get_rect(center=self.rect.center)
		self.rot_image=pygame.transform.rotate(self.gun_image,0)
		
		self.can_shoot=1
		self.gun_timer=self.guns[self.cur_gun][2]
		self.max_ammo=self.guns[self.cur_gun][3]
		self.cur_ammo=self.max_ammo
		self.reload_timer=self.guns[self.cur_gun][4]
	def rotate(self):
		mouse_x,mouse_y=pygame.mouse.get_pos()
		rel_x,rel_y=mouse_x-self.rect.x,mouse_y-self.rect.y
		angle=(180/math.pi)*(-math.atan2(rel_y,rel_x))
		if angle<0:
			angle=180+(180+angle)
		legs_deg=self.legs_deg
		if (legs_deg<315)and(legs_deg>45):
			if (abs(legs_deg-angle))<=90:
				self.rot_image=pygame.transform.rotate(self.gun_image,angle)
		else:
			if legs_deg==315:
				if (angle>=225 and angle<=360)or(angle<=45 and angle>=0):
					self.rot_image=pygame.transform.rotate(self.gun_image,angle)
			if legs_deg==45:
				if (angle>=315 and angle<=360)or(angle<=135 and angle>=0):
					self.rot_image=pygame.transform.rotate(self.gun_image,angle)
			if legs_deg==0:
				if (angle>=270 and angle<=360)or(angle<=90 and angle>=0):
					self.rot_image=pygame.transform.rotate(self.gun_image,angle)
		self.rot_image=pygame.transform.rotate(self.gun_image,angle)
		self.leg_image=pygame.transform.rotate(self.image,self.legs_deg)
		
	def move(self,*args):
		if abs(self.speed)<abs(self.max_speed):
			self.speed+=.1
		self.move_check[args[0]]=1
		self.change_anim('move')
	
	def shoot_timer(self):
		if self.can_shoot==0:
			self.gun_timer-=1
			
			if self.gun_timer<=0:
				print('shoot')
				if self.cur_ammo>0:
					self.can_shoot=1
				
				self.gun_timer=self.guns[self.cur_gun][2]
			if self.cur_ammo<=0:
				print(str(self.reload_timer))
				self.reload_timer-=1
				if self.reload_timer<=0:
					print('reloaded')
					self.reload_timer=self.guns[self.cur_gun][4]
					self.can_shoot=1
					self.cur_ammo=self.guns[self.cur_gun][3]
		
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
		self.gun_rect=self.rot_image.get_rect(center=self.rect.center)
		self.legs_rect=self.leg_image.get_rect(center=self.rect.center)
		#par.blit(self.leg_image,self.legs_rect)
		par.blit(self.rot_image,self.gun_rect)
		rad=float(self.deg/(180/math.pi))
		dx=self.rect.x+int(math.cos(rad)*30)
		dy=self.rect.y+int(math.sin(rad)*30)
		#pygame.draw.line(par, (255,255,255), [],[dx,dy], 3)
	
	def update(self,k_p,cam):
		self.shoot_timer()
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
		bems=self.move_check
		if cnt>1:
			d_sp=self.speed/math.sin(math.radians(45))
			
			if bems[0]==1 and bems[1]==1:
				self.legs_deg=135
			if bems[1]==1 and bems[2]==1:
				self.legs_deg=45
			if bems[2]==1 and bems[3]==1:
				self.legs_deg=315
			if bems[3]==1 and bems[0]==1:
				self.legs_deg=225
		else:
			if bems[0]==1:
				self.legs_deg=180
			if bems[1]==1:
				self.legs_deg=90
			if bems[2]==1:
				self.legs_deg=0
			if bems[3]==1:
				self.legs_deg=270
		for i in range(len(self.move_check)):
			if self.move_check[i]==1:
				if i==0:
					cam.move(d_sp,0)
				if i==1:
					cam.move(0,d_sp)
				if i==2:
					cam.move(-d_sp,0)
				if i==3:
					cam.move(0,-d_sp)
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

class Camera(pygame.sprite.Sprite):
	def __init__(self,x,y):
		self.rect = pygame.Rect(x,y,320,160)
	def move(self,x,y):
		self.rect[0]+=x
		self.rect[1]+=y
class zombie(pygame.sprite.Sprite):
	pass

class HUD(pygame.sprite.Sprite):
	def __init__(self):
		self.bul_img=pygame.image.load('sprites/hud_bullet.png').convert_alpha()
		self.ebul_img=pygame.image.load('sprites/hud_bullet_empty.png').convert_alpha()
		self.bul_list=[]
	def init_bul(self,par,hero):
		self.bul_list=[]
		for i in range(hero.max_ammo):
			if hero.cur_ammo>=i+1:
				img=self.bul_img
			else:
				img=self.ebul_img
			img_rect=pygame.Rect(0+(i)*15,320-25,10,20)
			par.blit(img,img_rect)
		


