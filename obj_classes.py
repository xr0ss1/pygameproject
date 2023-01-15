import pygame
class Player(pygame.sprite.Sprite):
	def create_anim(self,filename,n,ind):
		for i in range(1,n):
			self.anim_list[ind].append(pygame.image.load(filename+str(i+1)+'.bmp').convert_alpha())

			
			
	def change_anim(self,ind):
		self.images=[]
		for i in self.anim_list[ind]:
			self.images.append(i)
			self.cur_img=0
			self.img_cnt=0
			self.max_img=len(self.images)
			
			
	def __init__(self,x,filename,n):
		self.anim_list={'move':[],'stand':[]}
		self.create_anim(filename,n,'stand')
		self.change_anim('stand')
		self.rect = self.images[0].get_rect(center=(x,0))
		self.speed = .25
		self.cur_img=0
		self.img_cnt=0
		self.img_speed=20
		self.max_img=len(self.images)
		
	def move(self,*args):
		self.rect.x+=args[0]*self.speed
		self.rect.y+=args[1]
		self.anim_check()
		
	def anim_check(self):
		self.img_cnt+=1
		if self.img_cnt>=self.img_speed:
			self.cur_img+=1
			if self.cur_img>self.max_img-1:
				self.cur_img=0
			self.img_cnt=0
	def draw_self(self,par):
		par.blit(self.images[self.cur_img],self.rect)
	
	def update(self):
		pass
		
	
		
