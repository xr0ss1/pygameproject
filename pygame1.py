import pygame
import math
pygame.font.init()
W=1200
H=640
from obj_classes import Player,Bullet
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('бимбим бамбам')
#pygame.display.set_icon(pygame.image.load('name'))
pygame.draw.rect(sc,(255,255,255),(10,10,50,100))
GEnable=True
key_events={'key_left':False,'key_right':False,'key_up':False,'key_down':False}#задаем проверки которые используем
key_events_check={'key_left':pygame.K_LEFT,'key_right':pygame.K_RIGHT,'key_up':pygame.K_UP,'key_down':pygame.K_DOWN} #назначаем клавиши

tt=pygame.font.Font(None, 12)
text_test=tt.render('1232',True,(255,255,255))

background=Surface(W*2,H*2)

bul_list=[]
camera=[0,0]
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
	hero.draw(sc)
	text_test=tt.render(str(hero.speed),True,(255,255,255))
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
			bul_list.append(Bullet(1,hero.rect.centerx,hero.rect.centery,event.pos[0],event.pos[1]))
		if event.type==pygame.MOUSEMOTION:
			pass
			
	check_events()
	hero.update(key_events)
	
			
	
	
	
