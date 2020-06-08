import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """飞船自身属性"""

    def __init__(self, ai_setting, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        self.image_old = pygame.image.load("ship.png")
        self.image = pygame.transform.scale(self.image_old, \
                                            (40, 50))  # 宽度*高度
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标记
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < \
                self.screen_rect.right:
            self.rect.centerx += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ai_setting.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.rect.centery -= self.ai_setting.ship_speed_factor
        if self.moving_down and self.rect.bottom < \
                self.screen_rect.bottom:
            self.rect.centery += self.ai_setting.ship_speed_factor

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
