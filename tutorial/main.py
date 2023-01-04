#sprite
import pygame
import random    #隨機模組
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#遊戲初始化和創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))  #畫面寬度高度
pygame.display.set_caption("第一個遊戲")           #遊戲視窗上方標題
clock = pygame.time.Clock()

#載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
#rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
rock_imgs = []
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.4)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):            #飛船
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38)) #image顯示的圖片 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()      #rect定位圖片 可以設定X,Y座標
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8                        #移動速度
        self.health = 100

    def update(self): 
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:            #移動鍵為D
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:            #移動鍵為A
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:            #讓圖片在下方位置
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Rock(pygame.sprite.Sprite):              #石頭
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()   #image顯示的圖片
        self.rect = self.image.get_rect()      #rect定位圖片 可以設定X,Y座標
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)  #垂直移動速度
        self.speedx = random.randrange(-3, 3)  #水平移動速度
        self.total_degree = 0
        self.rot_degree = 3                    #石頭旋轉角度
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_defree = self.rot_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT:             #石頭重複隨機跑出
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)  
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):              #子彈
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img   #image顯示的圖片
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()      #rect定位圖片 可以設定X,Y座標
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10  #垂直移動速度

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):       #8顆石頭
    new_rock()
score = 0
pygame.mixer.music.play(-1)

#遊戲迴圈
running=True
while running:
    clock.tick(FPS)                     #tick()裡填入的數字：在一秒鐘之內最多被執行幾次
    #取得輸入
    for event in pygame.event.get():    #回傳所有事件
        if event.type == pygame.QUIT:   #關閉視窗
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #更新遊戲
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits: 
        random.choice(expl_sounds).play()
        score += hit.radius
        new_rock()


    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)   #石頭碰撞到飛船關閉遊戲
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        if player.health <= 0:
            running = False

    #畫面顯示
    screen.fill(BLACK)    #((R,G,B))：紅綠藍
    screen.blit(background_img, (0,0)) #畫上背景圖片
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    pygame.display.update()

pygame.quit()