import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    
    def __init__(self, ai_setting, screen, ship):
        super(Bullet, self).__init__()
        #super().__init__(ai_setting, screen, ship)
        self.screen = screen
        
        #�����ӵ�
        self.rect = pygame.Rect(
            0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #�����ӵ�λ��
        self.y = float(ship.rect.y)
        
        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor
        
    #�ӵ��˶�
    def update(self):
        self.y -= self.speed_factor
        #���±�ʾ�ӵ���rectλ��
        self.rect.y = self.y
            
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
