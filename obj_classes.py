import pygame
import math
import random


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
			
			
	def init_guns(self):
			self.guns=[]
			self.guns.append([pygame.image.load('sprites/pl_pistol.png').convert_alpha(),7,25,7,35,20]		) # 2- shoot timer 3 - ammo count 4 - reload timer 5 - bullet speed
			self.guns.append([pygame.image.load('sprites/pl_auto.png').convert_alpha(),7,15,20,85,20]		) # 2- shoot timer 3 - ammo count 4 - reload timer 5 - bullet speed
	
	def switch_gun(self,_id):
		self.cur_gun=_id
		
		self.gun_image=self.guns[self.cur_gun][0]
		self.gun_rect=self.gun_image.get_rect(center=self.rect.center)
		self.rot_image=pygame.transform.rotate(self.gun_image,0)
		
		
		self.can_shoot=0
		self.gun_timer=self.guns[self.cur_gun][2]
		self.max_ammo=self.guns[self.cur_gun][3]
		self.cur_ammo=self.gammo[_id]
		self.bul_sp=self.guns[self.cur_gun][5]
		self.reload_timer=self.guns[self.cur_gun][4]
			
	def __init__(self,cam):
		self.gammo=[7,20]
		self.hp=100
		self.move_check=[0,0,0,0]
		self.anim_list={'move':[],'stand':[]}
		self.create_anim('sprites/pl_walk',6,'stand')
		self.create_anim('sprites/pl_walk',6,'move')
		self.cur_anim='--'
		self.change_anim('stand')
		self.init_guns()
		self.rect = self.images[0].get_rect(center=(cam.rect.width,cam.rect.height))
		
		
		self.hp=100
		self.speed = 0
		self.last_sd=-1
		self.max_speed=2
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
		self.bul_sp=self.guns[self.cur_gun][5]
		self.reload_timer=self.guns[self.cur_gun][4]
	def rotate(self,cam):
		mouse_x,mouse_y=pygame.mouse.get_pos()
		rel_x,rel_y=mouse_x-self.rect.x+cam.plpos[0],mouse_y-self.rect.y+cam.plpos[1]
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
		
	def move(self,*args):
		if abs(self.speed)<abs(self.max_speed):
			self.speed+=.1
		self.move_check[args[0]]=1
		self.change_anim('move')
	
	def shoot_timer(self,snd):
		if self.can_shoot==0:
			self.gun_timer-=1
			
			if self.gun_timer<=0:
				
				if self.cur_ammo>0:
					self.can_shoot=1
				
				self.gun_timer=self.guns[self.cur_gun][2]
			if self.cur_ammo<=0:
				if self.reload_timer==self.guns[self.cur_gun][4]:
					snd.play()
				self.reload_timer-=1
				if self.reload_timer<=0:
				
					self.reload_timer=self.guns[self.cur_gun][4]
					self.can_shoot=1
					self.cur_ammo=self.guns[self.cur_gun][3]
					self.gammo[self.cur_gun]=self.cur_ammo
		
	def anim_check(self,k_p):
		self.img_cnt+=1
		if self.img_cnt>=self.img_speed:
			self.cur_img+=1
			if self.cur_img>self.max_img-1:
				self.cur_img=0
			self.img_cnt=0
		if (not k_p['key_left']) and (not k_p['key_right'])and (not k_p['key_up'])and (not k_p['key_down']):
			self.change_anim('stand')
	def draw(self,par,cam):
		#self.image.rect.center=(-32,-32)
		#pygame.draw.circle(par,(150,150,0),(self.rect.centerx-cam.plpos[0],self.rect.centery-cam.plpos[1]),13)
		self.gun_rect=self.rot_image.get_rect(center=(self.rect.centerx-cam.plpos[0],self.rect.centery-cam.plpos[1]))
		self.legs_rect=self.leg_image.get_rect(center=(self.rect.centerx-cam.plpos[0],self.rect.centery-cam.plpos[1]))
		#par.blit(self.leg_image,self.legs_rect)
		par.blit(self.rot_image,self.gun_rect)
		#par.blit(self.rot_light,self.l_rect)
		rad=float(self.deg/(180/math.pi))
		dx=self.rect.x+int(math.cos(rad)*30)
		dy=self.rect.y+int(math.sin(rad)*30)
		#pygame.draw.line(par, (255,255,255), [],[dx,dy], 3)
	
	def update(self,k_p,cam,snd):
		if k_p['key_r']:
			if self.cur_ammo!=0:
				self.cur_ammo=0
				self.can_shoot=0
		self.shoot_timer(snd)
		self.image=self.images[self.cur_img]
		self.anim_check(k_p)
		self.rotate(cam)
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
		self.btype=[['sprites/bul1.png'],['sprites/bul2.png']]
		cam=args[5]
		self.tp=args[0]
		self.hp=2
		self.list=args[6]
		self.guns_list=args[7]
		self.image=pygame.image.load(self.btype[args[0]][0]).convert_alpha()
		self.rect = self.image.get_rect(center=(args[1]-cam.plpos[0],args[2]-cam.plpos[1]))
		self.xx=args[3]
		self.yy=args[4]
		self.speed=self.guns_list[args[0]][5]
		gip=((self.xx-self.rect.x)**2+(self.yy-self.rect.y)**2)**(1/2)
		d_gip=self.speed/gip
		self.dx=(self.xx-self.rect.x)*d_gip
		self.dy=(self.yy-self.rect.y)*d_gip
		rel_y=self.xx-(args[0]-cam.plpos[0])
		rel_x=self.xx-(args[1]-cam.plpos[1])
		self.angle=(180/math.pi)*(-math.atan2(rel_y,rel_x))
		self.image=pygame.transform.rotate(self.image,0)
		self.rect=self.image.get_rect(center=self.rect.center)
		self.active=1
		
	def draw(self,par,cam):
		if self.active==1:
			par.blit(self.image,self.rect)
	def destroy(self):
		self.list.remove(self)
		self.active=0
		print('minus bullet')
	def update(self):
		if self.active==1:
			self.rect.x+=self.dx
			self.rect.y+=self.dy
		if abs(self.rect.x)>2560 or abs(self.rect.y>1280):
			self.destroy()	
			print('123')
		

class Camera(pygame.sprite.Sprite):
	def __init__(self,x,y,w,h,cw,ch):
		self.rect = pygame.Rect(x,y,w,h)
		self.w=w
		self.h=h
		self.cw=cw
		self.ch=ch
		self.plpos=[0,0]
		self.statex='free'
		self.statey='free'
		self.zomb_cnt=0
	def move(self,x,y):
		
		if self.statex=='free':
			self.rect[0]+=x
			if (x>0 and self.rect[0]>=0) or (x<0 and self.rect[0]<-(self.cw-1280)+self.plpos[1]):
				self.statex='hold'
		if self.statex=='hold':
			self.plpos[0]+=x
			if abs(self.plpos[0])<=abs(x):
				self.statex='free'
		if self.statey=='free':
			self.rect[1]+=y
			if (y>0 and self.rect[1]>=0) or (y<0 and self.rect[1]<-(self.ch-640)):
				self.statey='hold'
		if self.statey=='hold':
			self.plpos[1]+=y
			if abs(self.plpos[1])<=abs(y):
				self.statey='free'

class HUD(pygame.sprite.Sprite):
	def __init__(self):
		self.bul_img=pygame.image.load('sprites/hud_bullet.png').convert_alpha()
		self.ebul_img=pygame.image.load('sprites/hud_bullet_empty.png').convert_alpha()
		self.bul_list=[]
	def init_bul(self,par,hero,cam):
		self.bul_list=[]
		for i in range(hero.max_ammo):
			if hero.cur_ammo>=i+1:
				img=self.bul_img
			else:
				img=self.ebul_img
			img_rect=pygame.Rect(0+(i)*15,cam.rect.width-25,10,20)
			par.blit(img,img_rect)
		
class Zombie(pygame.sprite.Sprite):
	def __init__(self,x,y,cam,wave):
		
		self.idle=pygame.image.load('sprites/zombie.png').convert_alpha()
		self.image=self.idle
		self.hit=[]
		self.hp=2+wave//2.5
		self.hit.append(pygame.image.load('sprites/zombiehit1.png').convert_alpha())
		self.hit.append(pygame.image.load('sprites/zombiehit2.png').convert_alpha())
		self.rect=self.image.get_rect(center=(x,y))
		self.speed=2+random.randint(0,wave/3.5)
		rel_y=cam.rect.centerx-x
		rel_x=cam.rect.centery-y
		self.angle=(180/math.pi)*(-math.atan2(rel_y,rel_x))
		self.rot_image=pygame.transform.rotate(self.image,self.angle)
		self.rot_rect=self.image.get_rect(center=(self.rect.centerx,self.rect.centery))
		self.target=cam
		self.active=1
		self.timer=5
	def draw(self,par,cam):
		if self.active==1:
			#pygame.draw.circle(par,(150,0,0),(self.rot_rect.center[0]+cam.rect.x,self.rot_rect.center[1]+cam.rect.y),25)
			par.blit(self.rot_image,(self.rot_rect.x+cam.rect.x,self.rot_rect.y+cam.rect.y))
		
	
	def rotation(self,cam):
		if self.active==1:
			rel_y=abs(cam.w-cam.rect.x-cam.plpos[0])-self.rect.centerx
			rel_x=abs(cam.h-cam.rect.y-cam.plpos[1])-self.rect.centery
			self.angle=-(180/math.pi)*(-math.atan2(rel_y,rel_x))-90
		
			self.rot_image=pygame.transform.rotate(self.image,self.angle)
			self.rot_rect=self.image.get_rect(center=(self.rect.centerx,self.rect.centery))
	
	def move(self):
		if self.active==1:
			dx=math.cos(math.radians(self.angle))*self.speed*2
			dy=math.sin(math.radians(self.angle))*self.speed*2
			self.rect.x+=dx
			self.rect.y-=dy
		
	def col_bul(self):
		pass
	
	def destroy(self,_list,i,cam,snd):
		
		if self.rect.collidepoint((i.rect.centerx-cam.rect.x,i.rect.centery-cam.rect.y)) and i.active==1:
			self.hp-=(2-i.tp)
			if self.hp<=0:
				_list.remove(self)
				self.active=0
				global zomb_cnt
				cam.zomb_cnt-=1
				a=random.randint(0,1)
				snd[a].play()
			i.destroy()
	
	def update(self,cam,hero,blist,_list,snd):
		if self.active==1:
			self.rotation(cam)
			self.move()
			if self.rect.collidepoint((cam.w-cam.rect.x-cam.plpos[0],cam.h-cam.rect.y-cam.plpos[1])):
				self.timer-=1
				if self.timer<=0:
					self.image=self.hit[random.randint(0,1)]
					self.timer=50
					hero.hp-=10
					a=random.randint(0,1)
					snd[a].play()
			else:
				self.image=self.idle
			for i in blist:
				
				self.destroy(_list,i,cam,snd)
				
		
		
		
	

