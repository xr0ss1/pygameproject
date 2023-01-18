import pygame
import math
pygame.font.init()
W=1280	
H=640
scene_w=2560
scene_h=1280
cam_w=640
cam_h=320
FPS=30

mouse_down=0
from obj_classes import Player,Bullet,Camera,HUD,Zombie
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('бимбим бамбам')
#pygame.display.set_icon(pygame.image.load('name'))
pygame.draw.rect(sc,(255,255,255),(10,10,50,100))
GEnable=True
key_events={'key_left':False,'key_right':False,'key_up':False,'key_down':False}#задаем проверки которые используем
key_events_check={'key_left':pygame.K_a,'key_right':pygame.K_d,'key_up':pygame.K_w,'key_down':pygame.K_s} #назначаем клавиши

tt=pygame.font.Font(None, 12)
text_test=tt.render('1232',True,(255,255,255))

background=pygame.image.load('sprites/background.png').convert_alpha()
background_shadow=pygame.image.load('sprites/background_shadow.png').convert_alpha()
back_rect=background.get_rect(topleft=(0,0))
back_rect1=background.get_rect(topleft=(1280,0))
back_rect2=background.get_rect(topleft=(0,640))
back_rect3=background.get_rect(topleft=(1280,640))

bul_list=[]
zomb_list=[]
cam=Camera(0,0,cam_w,cam_h,scene_w,scene_h)
hud=HUD()
hero=Player(cam)
def check_events():
	if key_events['key_left']:
		hero.move(0)
		
		
	if key_events['key_right']:
		hero.move(2)
		
		
	if key_events['key_up']:
		hero.move(1)
		
	if key_events['key_down']:
		hero.move(3)
zomb_list.append(Zombie(200,200,cam))

def col_player():
		cp=pygame.sprite.spritecollide(hero,zomb_list, False, pygame.sprite.collide_circle)
		if cp:
			print('2')
				
				
		
while GEnable:
	sc.fill((0,0,0))
	sc.blit(background,(back_rect.x+cam.rect.x,back_rect.y+cam.rect.y))
	sc.blit(background,(back_rect1.x+cam.rect.x,back_rect1.y+cam.rect.y))
	sc.blit(background,(back_rect2.x+cam.rect.x,back_rect2.y+cam.rect.y))
	sc.blit(background,(back_rect3.x+cam.rect.x,back_rect3.y+cam.rect.y))
	sc.blit(background_shadow,(back_rect.x+cam.rect.x,back_rect.y+cam.rect.y))
	hero.draw(sc,cam)
	hud.init_bul(sc,hero,cam)
	mx,my=pygame.mouse.get_pos()
	text_test=tt.render('x= '+str(mx)+' y= '+str(my),True,(255,255,255))
	if len(bul_list)>0:
		for i in bul_list:
			i.update()
			i.draw(sc)
	if len(zomb_list)>0:
		for i in zomb_list:
			i.update(cam,hero)
			i.draw(sc,cam)
	sc.blit(text_test,(15,H-20))
	pygame.display.update()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GEnable=False
		if event.type==pygame.KEYDOWN:
			for i in key_events:
				if event.key==key_events_check[i]:
					key_events[i]=True
		if event.type==pygame.KEYUP:
			for i in key_events:
				if event.key==key_events_check[i]:
					key_events[i]=False
		if event.type==pygame.MOUSEBUTTONDOWN:
			mouse_down=1
		if event.type==pygame.MOUSEBUTTONUP:
			mouse_down=0
		if event.type==pygame.MOUSEMOTION:
			pass
	mouse_x,mouse_y=pygame.mouse.get_pos()
	if mouse_down==1:
		if hero.can_shoot==1:
			bul_list.append(Bullet(1,hero.rect.centerx,hero.rect.centery,mouse_x,mouse_y,cam))		
			hero.can_shoot=0
			hero.cur_ammo-=1
		
	
	check_events()
	hero.update(key_events,cam)
	
			
	
	
	
