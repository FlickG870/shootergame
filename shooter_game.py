import pygame
import random
import time

pygame.init()

clock = pygame.time.Clock()
rungame = True
finish = False
FPS = 60
winSize = [700, 500] 
#создай окно игры


pygame.mixer.init()
sound_fire = pygame.mixer.Sound('fire.ogg')
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
vol = 0.3
pygame.mixer.music.set_volume(vol)

score = 0
lost = 0

pygame.display.set_caption('Galaxy Game')
win = pygame.display.set_mode(winSize)
background = pygame.transform.scale(pygame.image.load('galaxy.jpg'), winSize)
f1 = pygame.font.SysFont('Arlal', 36)
f2 = pygame.font.SysFont('Arial', 60)
f3 = pygame.font.SysFont('Arial', 48)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img_name, length, width, x, y, speed):
        super().__init__()
        sprite = pygame.image.load(img_name)
        self.image = pygame.transform.scale(sprite, [length, width])
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, [self.rect.x, self.rect.y])

class Player(GameSprite):
    def __init__(self, img_name, length, width, x, y, speed):
        super().__init__(img_name, length, width, x, y, speed)
        self.bullet_count = 5
        self.time_reload = 2
        self.time_start_reload = 0
        
    def move(self):
        list_key = pygame.key.get_pressed()
        if list_key[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if list_key[pygame.K_d] and self.rect.x < 645:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', 30, 30, self.rect.x+12, self.rect.y, 4)  
        bullets.add(bullet)
        self.bullet_count -= 1
        if self.bullet_count <= 0:
            self.time_start_reload = time.time()
            self.bullet_count = 5

class Ufo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= winSize[1]:
            global lost
            lost += 1
            self.rect.y = -55
            self.rect.x = random.randint(0, 700-55)
            self.speed = random.randint(1, 2)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            self.kill()

player = Player('rocket.png', 55, 75, 333, 420, 3)
bullets = pygame.sprite.Group()
ufos = pygame.sprite.Group()
for i in range(6):
    lost -= 1 
    ufo = Ufo('ufo.png', 75, 75, 0, 700, 2)
    ufos.add(ufo)

while rungame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                vol -= 0.1
                pygame.mixer.music.set_volume(vol)
            elif event.key == pygame.K_2:
                vol += 0.1          
                pygame.mixer.music.set_volume(vol) 
            elif event.key == pygame.K_SPACE and finish == False:
                if (time.time()-player.time_start_reload) >= player.time_reload:
                    sound_fire.play()
                    player.fire()

    if finish == False:
        collides = pygame.sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            lost -= 1 
            ufo = Ufo('ufo.png', 75, 75, 0, 700, 2)
            ufos.add(ufo)     

        player.move()   
        ufos.update() 
        bullets.update()

        score_text = f1.render('Счёт: '+str(score), True, (255, 255, 255))
        lost_text = f1.render('Пропущено: '+str(lost), True, (255, 255, 255)) 
        bullet_text = f3.render(str(player.bullet_count), True, (255, 255, 255)) 

        win.blit(background, [0, 0])
        win.blit(score_text, [20, 20]) 
        win.blit(lost_text, [20, 60])
        win.blit(bullet_text, [650, 450])

        player.reset()
        ufos.draw(win)
        bullets.draw(win)

        if score >= 10:
            finish = True
            win_text = f2.render('YOU WIN! :)', True, (60, 255, 0))
            win.blit(win_text, [250, 225])
        if lost >= 3 or pygame.sprite.spritecollide(player, ufos, False):
            finish = True
            lose_text = f2.render('YOU LOSE! :(', True, (252, 91, 96)) 
            win.blit(lose_text, [250, 225])

    pygame.display.update()
    clock.tick(FPS) 