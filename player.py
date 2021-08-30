import pygame
from pygame import Surface
from pygame.sprite import Sprite
from pygame.key import get_pressed
from bullets import Bullets


# 繼承 pygame 內建的 Sprite 類別
class Player(Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, COLOR, WIDTH, HEIGHT, img, screen):
        Sprite.__init__(self)    # Call the parent class (Sprite) constructor
        self.width = WIDTH       # 遊戲視窗的寬度
        self.height = HEIGHT     # 遊戲視窗的長度
        self.color = COLOR
        self.screen = screen
        self.speed_x = 4         # 控制左右橫移的速度
        self.hp = 100            # 初始化血量
        self.lives = 3           # 設定初始有 3 條命
        self.total_damage = 0    # 初始化傷害量
        self.damage = 0          # 初始化傷害量
        self.hidden = False
        self.hidden_time = 0
        self.gun_level = 1       # 設定
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.transform.scale(img,(50,50))  # 調整圖片的像素大小
        self.image.set_colorkey(self.color)               # 去背
        self.live_img = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.radius = (self.rect.width / 2) * 0.5
        # pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)  # 測適用
        self.rect.centerx = self.width/2
        self.rect.bottom = self.height-10

    def update(self):
        self.hide_or_not()
        self.move()
        self.limit_location()

    # 控制移動
    def move(self):
        press_key = get_pressed()
        if press_key[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        elif press_key[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
    
    # 控制物件不超出視窗外
    def limit_location(self):
        if self.rect.right >= self.width:    
            self.rect.right = self.width
        elif self.rect.left <= 0:
            self.rect.left = 0
    
    def shoot(self, bullets_color, img, fire_sound):
        s = Bullets(bullets_color, self.width, self.height, self.rect.centerx, self.rect.top + 10, img)
        fire_sound.play()
        return s

    def shoot2(self, bullets_color, img, fire_sound):
        s1 = Bullets(bullets_color, self.width, self.height, self.rect.centerx + 20, self.rect.centery, img)
        s2 = Bullets(bullets_color, self.width, self.height, self.rect.centerx - 20, self.rect.centery, img)
        fire_sound.play()
        return s1, s2
            
    def shoot3(self, bullets_color, img, fire_sound):
        s = Bullets(bullets_color, self.width, self.height, self.rect.centerx, self.rect.top + 10, img)
        s1 = Bullets(bullets_color, self.width, self.height, self.rect.centerx + 20, self.rect.centery, img)
        s2 = Bullets(bullets_color, self.width, self.height, self.rect.centerx - 20, self.rect.centery, img)
        fire_sound.play()
        return s, s1, s2    

    def cal_damage(self, damage, processing):
        # self.damage = damage
        self.hp -= damage
        self.total_damage += damage
        if self.total_damage >= 100:
            processing = False
        # self.plot_hp()
        return processing

    def plot_hp(self):
        if self.hp < 0:
            self.hp = 0
        self.plot()

    def end_or_conti(self, processing):
        if self.lives >= 0:
            self.lives -= 1
            self.hide_or_not()
            self.hp = 100              # 復活初始化
            self.gun_level = 1         # 初始化子彈等級
            self.total_damage = 0
            processing = True
        return processing
    
    def hide_or_not(self):
        if self.total_damage >= 100:
            self.hidden = True
            self.hidden_time = pygame.time.get_ticks()
            self.rect.center = ( self.width / 2, self.height + 1000)
        elif self.hidden == True and pygame.time.get_ticks() - self.hidden_time > 1000: # 1000 單位為 ms
            self.hidden = False
            self.rect.centerx = self.width/2
            self.rect.bottom = self.height-10

    def plot_lives(self):
        for i in range(self.lives):
            live_img_rect = self.live_img.get_rect()
            live_img_rect.x = self.width - 3 * 45 + i * 42
            live_img_rect.y = 10
            self.screen.blit(self.live_img, live_img_rect)
    
    def plot_add_hp(self):
        self.hp += 20 
        if self.hp > 100:
            self.hp = 100
        self.plot()

    def plot(self):
        BAR_LENGTH = 100
        BAR_WIDTH = 10
        fill_hp = (self.hp / 100) * BAR_LENGTH
        frame = pygame.Rect(5, 15, BAR_LENGTH, BAR_WIDTH)
        fill = pygame.Rect(5, 15, fill_hp, BAR_WIDTH)
        pygame.draw.rect(self.screen, (255, 255, 255), frame, 2)
        pygame.draw.rect(self.screen, (0, 255, 0), fill)

    def level_up(self):
        self.gun_level += 1
