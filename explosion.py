import pygame
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, img_list, center, expl_type):
        Sprite.__init__(self)    # Call the parent class (Sprite) constructor
        self.frame = 0
        self.img_list = img_list
        self.expl_type = expl_type
        self.expl_size()
        self.image = img_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update_time = pygame.time.get_ticks()
        self.frame_rate = 70
        
    def update(self):
        self.explosion()

    def explosion(self):
        now = pygame.time.get_ticks()
        if now - self.last_update_time >= self.frame_rate:
            self.last_update_time = now
            self.frame += 1
            if self.frame == len(self.img_list):
                self.kill()
            else:
                self.image = self.img_list[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

    def expl_size(self):
        if self.expl_type == 0:
            size = 70
        elif self.expl_type == 1:
            size = 20
        else:
            return
        for i in range(len(self.img_list)):
            self.img_list[i] = pygame.transform.scale(self.img_list[i], (size, size))  # 調整圖片的像素大小