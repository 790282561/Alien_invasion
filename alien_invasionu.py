import pygame
from pygame.sprite import Group
from alien import Alien
from setting import Settings
import game_functions as gf
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()

    #创建setting模块的实例
    ai_setting = Settings()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("外星人入侵")
    
    #创建alien的实例
    alien = Alien(ai_setting, screen)
    #创建飞船实例
    ship = Ship(ai_setting, screen)
    #创建储存游戏状态的实例，并创建记分牌
    stats = GameStats(ai_setting)
    sb = Scoreboard(ai_setting, screen, stats)
    
    bullets = Group()#子弹编组
    aliens = Group()#外星人编组
    
    #创建外星人群
    gf.create_fleet(ai_setting, screen, aliens, ship)
    
    #创建play按钮
    play_button = Button(ai_setting, screen, "Play")
    
    #开始游戏主循环
    while True:
        gf.check_events(ai_setting, screen, sb, ship, bullets, stats, \
            play_button,aliens)
        if stats.game_active:
            gf.update_ship(ship)
            gf.update_aliens(ai_setting, stats, screen, sb, aliens, ship, bullets)
            gf.update_bullets(ai_setting, screen, stats, sb, aliens, ship, bullets)
        gf.update_screen(ai_setting, screen, sb, ship, aliens, bullets, \
            stats, play_button)
        pygame.display.flip() #最近绘制的图像可见

run_game()
