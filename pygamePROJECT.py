from obj_classes import Player, Bullet, Camera, HUD, Zombie
import pygame
import math
import random

pygame.init()
pygame.font.init()
W = 1280
H = 640
scene_w = 2560
scene_h = 1280
cam_w = 640
cam_h = 320
FPS = 60
death = 0
mouse_down = 0

sc = pygame.display.set_mode((W, H))
pygame.display.set_caption('zomb survive')
# pygame.display.set_icon(pygame.image.load('name'))
pygame.draw.rect(sc, (255, 255, 255), (10, 10, 50, 100))
GEnable = True
key_events = {'key_r': False, 'key_left': False, 'key_right': False, 'key_up': False, 'key_down': False, 'key_1': False,
              'key_2': False}  # задаем проверки которые используем
key_events_check = {'key_r': pygame.K_r, 'key_left': pygame.K_a, 'key_right': pygame.K_d, 'key_up': pygame.K_w,
                    'key_down': pygame.K_s, 'key_1': pygame.K_1, 'key_2': pygame.K_2}  # назначаем клавиши

tt = pygame.font.Font(None, 64)
text_test = tt.render('1232', True, (255, 255, 255))
wave_text = tt.render('Выживите пока вас не спасут', True, (255, 255, 255))

background = pygame.image.load('sprites/background.png').convert_alpha()
background_shadow = pygame.image.load('sprites/background_shadow.png').convert_alpha()
back_rect = background.get_rect(topleft=(0, 0))
back_rect1 = background.get_rect(topleft=(1280, 0))
back_rect2 = background.get_rect(topleft=(0, 640))
back_rect3 = background.get_rect(topleft=(1280, 640))

bul_list = []
zomb_list = []
cam = Camera(0, 0, cam_w, cam_h, scene_w, scene_h)
hud = HUD()
hero = Player(cam)

pygame.mixer.music.load("sound/back_m.mp3")
pygame.mixer.music.play(-1)
s_shot = pygame.mixer.Sound("sound/shot.mp3")
s_rel = pygame.mixer.Sound("sound/reload.wav")
s_zomb = [pygame.mixer.Sound("sound/zomb1.wav"), pygame.mixer.Sound("sound/zomb2.wav"),
          pygame.mixer.Sound("sound/zomb3.wav")]
s_hit = [pygame.mixer.Sound("sound/hit.wav"), pygame.mixer.Sound("sound/hit1.wav")]
zones_list = [[(0, 2560), (-50, -50)], [(0, 2560), (1400, 1400)], [(-50, -50), (0, 1280)], [(2610, 2610), (0, 1280)]]
waves = 5
cur_wave = 0
wave_data = [{'count': 10, 'min': 10, 'max': 30, 'maxzomb': 3, 'cnt': 5},
             {'count': 20, 'min': 20, 'max': 30, 'maxzomb': 5, 'cnt': 7},
             {'count': 25, 'min': 30, 'max': 30, 'maxzomb': 7, 'cnt': 9},
             {'count': 30, 'min': 100, 'max': 250, 'maxzomb': 8, 'cnt': 15},
             {'count': 30, 'min': 80, 'max': 200, 'maxzomb': 9, 'cnt': 20},
             {'count': 30, 'min': 70, 'max': 150, 'maxzomb': 10, 'cnt': 20}]
wave_timer = random.randint(150, 300)
print(wave_timer)

clock = pygame.time.Clock()
FPS = 60

zomb_created = 0
ending = 0

heli_img = pygame.image.load('sprites/heli_base.png').convert_alpha()
heli_top = pygame.image.load('sprites/heli_top.png').convert_alpha()
top = heli_top
heli_rect = heli_img.get_rect(center=(1280, -200))
heli_rect2 = heli_top.get_rect(center=heli_rect.center)


def heli_move(x, y):
    heli_rect.x += x
    heli_rect.y += y


def check_events():
    if key_events['key_left']:
        hero.move(0)

    if key_events['key_right']:
        hero.move(2)

    if key_events['key_up']:
        hero.move(1)

    if key_events['key_down']:
        hero.move(3)
    if key_events['key_1']:
        hero.switch_gun(0)
    if key_events['key_2']:
        hero.switch_gun(1)


def col_player():
    cp = pygame.sprite.spritecollide(hero, zomb_list, False, pygame.sprite.collide_circle)
    if cp:
        print('2')


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


bems = 0
ss = pygame.Surface((1280, 640))  # per-pixel alpha
ss.fill((0, 0, 0))  # notice the alpha value in the color
hs = pygame.Surface((1280, 640))
hs.fill((150, 0, 0))

b_a = 255
while GEnable:
    if hero.hp <= 0:
        death = 1
        ending = 1
    sc.fill((0, 0, 0))
    sc.blit(background, (back_rect.x + cam.rect.x, back_rect.y + cam.rect.y))
    sc.blit(background, (back_rect1.x + cam.rect.x, back_rect1.y + cam.rect.y))
    sc.blit(background, (back_rect2.x + cam.rect.x, back_rect2.y + cam.rect.y))
    sc.blit(background, (back_rect3.x + cam.rect.x, back_rect3.y + cam.rect.y))
    sc.blit(background_shadow, (back_rect.x + cam.rect.x, back_rect.y + cam.rect.y))
    bems += 25
    top = pygame.transform.rotate(heli_top, bems)
    heli_rect2 = top.get_rect(center=heli_rect.center)

    hero.draw(sc, cam)
    sc.blit(heli_img, (heli_rect.x + cam.rect.x, heli_rect.y + cam.rect.y))
    sc.blit(top, (heli_rect2.x + cam.rect.x, heli_rect2.y + cam.rect.y))

    hud.init_bul(sc, hero, cam)
    mx, my = pygame.mouse.get_pos()
    text_test = tt.render(str(cam.zomb_cnt) + ' ' + str(zomb_created) + ' ' + str(cur_wave), True, (255, 255, 255))
    if len(bul_list) > 0:
        for i in bul_list:
            i.update()
            i.draw(sc, cam)
    if len(zomb_list) > 0:
        for i in zomb_list:
            for j in zomb_list:
                if abs(j.rect.x - i.rect.x) < 30:
                    mn = min(i.rect.x, j.rect.x)
                    if i.rect.x == mn:
                        i.rect.x -= 1
                        j.rect.x += 1
                    else:
                        i.rect.x += 1
                        j.rect.x -= 1
                if abs(j.rect.y - i.rect.y) < 40:
                    mn = min(i.rect.y, j.rect.y)
                    if i.rect.y == mn:
                        i.rect.y -= 1
                        j.rect.y += 1
                    else:
                        i.rect.y += 1
                        j.rect.y -= 1

            i.update(cam, hero, bul_list, zomb_list, s_hit)
            i.draw(sc, cam)
    # sc.blit(text_test,(15,H-20))
    sc.blit(wave_text, (cam_w - 70, cam_h + 100))
    ss.set_alpha(b_a)
    hs.set_alpha((100 - hero.hp) / 150 * 255)
    if ending == 0:
        if b_a > 64:
            b_a -= .5
    if b_a >= 255:
        GEnable = False
    sc.blit(hs, (0, 0))
    sc.blit(ss, (0, 0))
    pygame.display.update()
    wave_timer -= 1
    if wave_timer <= 0:
        spawn_point = random.randint(0, 3)
        xx = random.randint(zones_list[spawn_point][0][0], zones_list[spawn_point][0][1])
        yy = random.randint(zones_list[spawn_point][1][0], zones_list[spawn_point][1][1])
        print(xx, yy)
        wave_timer = random.randint(wave_data[cur_wave]['min'], wave_data[cur_wave]['max'])
        if cam.zomb_cnt < wave_data[cur_wave]['maxzomb'] and zomb_created < wave_data[cur_wave]['cnt']:
            cam.zomb_cnt += 1
            zomb_list.append(Zombie(xx, yy, cam, cur_wave))
            zomb_created += 1
            print('zombie on', xx, yy)
            a = random.randint(0, 2)
            s_zomb[a].play()
            wave_text = tt.render('', True, (255, 255, 255))
        if (cam.zomb_cnt == 0) and (zomb_created >= wave_data[cur_wave]['cnt']):
            if cur_wave < waves:
                # new wave
                cur_wave += 1
                hero.hp += 15
                zomb_created = 0
                wave_timer = 500
                print('wave', cur_wave)
                wave_text = tt.render('WAVE ' + str(cur_wave), True, (255, 255, 255))
            else:
                ending = 1
    if ending == 1:
        if death == 0:
            heli_rect.x += ((hero.rect.centerx - cam.rect.x - (cam.plpos[0])) - heli_rect.x) / 100
            heli_rect.y += ((hero.rect.centery - cam.rect.y - (cam.plpos[1])) - heli_rect.y) / 100
        b_a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GEnable = False
        if event.type == pygame.KEYDOWN:
            for i in key_events:
                if event.key == key_events_check[i]:
                    key_events[i] = True
        if event.type == pygame.KEYUP:
            for i in key_events:
                if event.key == key_events_check[i]:
                    key_events[i] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = 1
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = 0
        if event.type == pygame.MOUSEMOTION:
            pass
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_down == 1:
        if hero.can_shoot == 1:
            bul_list.append(
                Bullet(hero.cur_gun, hero.rect.centerx, hero.rect.centery, mouse_x, mouse_y, cam, bul_list, hero.guns))
            hero.can_shoot = 0
            hero.cur_ammo -= 1
            hero.gammo[hero.cur_gun] = hero.cur_ammo
            s_shot.play()

    check_events()
    hero.update(key_events, cam, s_rel)
    clock.tick(FPS)
