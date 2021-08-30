import random
import pygame
from pygame.sprite import Sprite
# from pygame.key import get_pressed


class Treasures(Sprite):
    def __init__(self, COLOR, WIDTH, HEIGHT, center, imgs):
        Sprite.__init__(self)    # Call the parent class (Sprite) constructor
        self.width = WIDTH       # 遊戲視窗的寬度
        self.height = HEIGHT     # 遊戲視窗的長度
        self.color = COLOR       # (255,255,255)
        self.speed_y = 3         # 控制寶物掉落速度
        self.img_list = imgs
        self.treasure_type = random.choice(list(range(2)))
        self.image = pygame.transform.scale(self.img_list[self.treasure_type],(40,40))
        self.image.set_colorkey(self.color)       
        # self.image = Surface([10, 20]) # [width, height]
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.auto_move()
        self.out_screen()

    # 控制移動
    def auto_move(self):
        self.rect.y += self.speed_y
    
    # 清除超出視窗外的物件
    def out_screen(self):
        if self.rect.top > self.height:    
            self.kill()
