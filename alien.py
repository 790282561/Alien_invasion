import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, ai_setting, screen):
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        
        #加载外星人图像，并设置其rect属性
        #elf.image = pygame.image.load("alien.png")
        self.image_old = pygame.image.load("alien.png")
        self.image = pygame.transform.scale(self.image_old, \
            (40, 50))#宽度*高度
        self.rect = self.image.get_rect()
        
        #每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
    
    def update(self):
        self.x += (self.ai_setting.alien_speed_factor * \
            self.ai_setting.fleet_direction)
        self.rect.x = self.x  #通过x确认rect.x的位置坐标
        
    def blitme(self):
        """在指定的位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果外星人位于屏幕边缘，返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
