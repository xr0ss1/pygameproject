import pygame
import math
pygame.font.init()
W=640
H=320
FPS=30

mouse_down=0
from obj_classes import Player,Bullet,Camera,HUD
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
back_rect=background.get_rect(topleft=(0,0))

bul_list=[]
cam=Camera(0,0)
hud=HUD()
hero=Player(W//2)
def check_events():
	if key_events['key_left']:
		hero.move(0)
		
		
	if key_events['key_right']:
		hero.move(2)
		
		
	if key_events['key_up']:
		hero.move(1)
		
	if key_events['key_down']:
		hero.move(3)
		
while GEnable:
	sc.fill((0,0,0))
	sc.blit(background,(back_rect.x+cam.rect.x,back_rect.y+cam.rect.y))
	hero.draw(sc)
	hud.init_bul(sc,hero)
	mx,my=pygame.mouse.get_pos()
	text_test=tt.render('x= '+str(mx)+' y= '+str(my),True,(255,255,255))
	if len(bul_list)>0:
		for i in bul_list:
			i.update()
			i.draw(sc)
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
	if mouse_down==1:
		if hero.can_shoot==1:
			bul_list.append(Bullet(1,hero.rect.centerx,hero.rect.centery,event.pos[0],event.pos[1]))		
			hero.can_shoot=0
			hero.cur_ammo-=1
	check_events()
	hero.update(key_events,cam)
	
			
	
	
	
