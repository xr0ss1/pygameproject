import pygame
W=600
H=400
from obj_classes import Player
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption('бимбим бамбам')
#pygame.display.set_icon(pygame.image.load('name'))
pygame.draw.rect(sc,(255,255,255),(10,10,50,100))
GEnable=True
key_events={'key_left':False,'key_right':False,}#задаем проверки которые используем
key_events_check={'key_left':pygame.K_LEFT,'key_right':pygame.K_RIGHT} #назначаем клавиши
hero=Player(W//2,'sprites/s_pl_move',6)
def check_events():
	if key_events['key_left']:
		hero.move(-1,0)
		
	if key_events['key_right']:
		hero.move(1,0)
while GEnable:
	sc.fill((0,0,0))
	hero.draw_self(sc)
	
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
	check_events()
	
	
	
