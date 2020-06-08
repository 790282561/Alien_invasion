import sys
import pygame
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep

def check_keydown_events(event, ai_setting, screen, bullets, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_setting, screen, bullets, ship)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_setting, screen, bullets, ship):
    if len(bullets) <= ai_setting.bullet_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)

def check_up_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = Fa.lse
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_setting, screen, sb, ship, bullets, stats, \
    play_button,aliens):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #飞船向右移动
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(
                event, ai_setting, screen, bullets, ship)
        elif event.type == pygame.KEYUP:
            check_up_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, \
                ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_setting, screen, stats, sb, play_button, \
    ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单机Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
         #重置游戏统计信息
         ai_setting.initialize_dynamic_settings()
         stats.reset_stats()
         stats.game_active = True
         
         #重置记分牌图形
         sb.prep_score()
         sb.prep_high_score()
         sb.prep_level()
         sb.prep_ships()
         
         #清空外星人列表和子弹列表
         aliens.empty()
         bullets.empty()
         
         #创建一群新的外星人，并让飞船居中
         create_fleet(ai_setting, screen, aliens, ship)
         ship.center_ship()
         
         #隐藏光标
         pygame.mouse.set_visible(False)
         
def update_screen(ai_setting, screen, sb, ship, aliens, bullets, \
    stats, play_button):
    """更新屏幕上的图像，并切换到新屏幕上"""
    #每次循环时都重新绘制屏幕
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    #显示分数
    sb.show_score()
    
    #如果游戏处于非活动状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()
        
    
def update_bullets(ai_setting, screen, stats, sb, aliens, ship, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, stats, sb, aliens, ship, bullets)
    print(len(bullets))
    
def check_bullet_alien_collisions(ai_setting, screen, stats, sb, aliens, ship, bullets):
    #检查是否有子击中了外星人
    #如果是这样，就删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        #如果整群外星人都被消灭，就提高一个等级
        bullets.empty()
        ai_setting.increase_speed()
        
        #提高等级
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_setting, screen, aliens, ship)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points * len(aliens)
            sb.prep_score()
        check_high_scores(stats, sb)
        
def get_number_aliens_x(ai_setting, alien_width):
    #计算每行可以容纳多少外星人
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    #创建一个外星人并将其放在当前行
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * \
    (row_number - 1)
    aliens.add(alien)
  
def create_fleet(ai_setting, screen, aliens, ship):
    #创建外星人群
    #创建一个外星人，并计算每行可以容纳多少个外星人
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_y(ai_setting, alien.rect.height, ship.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, \
                row_number)

def get_number_y(ai_setting, alien_height, ship_height):
    #计算可以容纳多少行
    available_space_y = ai_setting.screen_height - ship_height - \
        (3 * alien_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def ship_hit(ai_setting, stats, screen, sb, aliens, ship, bullets):
    """响应被外星人碰到的飞船"""
    if stats.ships_left > 0:
        #飞船生命-1
        stats.ships_left -= 1
        
        #更新记分牌
        sb.prep_ships()
        
        #复位外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        
        #创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_setting, screen, aliens, ship)
        ship.center_ship()
        
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_aliens(ai_setting, stats, screen, sb, aliens, ship, bullets):
    """检查是否外星人处于屏幕边缘，并更新正群外星人的位置"""
    check_fleet_edges(ai_setting, aliens)
    aliens.update()

    """检测外星人和飞船之间的碰撞"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, stats, screen, sb, aliens, ship, bullets)

    """检测是否有外星人到达了屏幕底端"""
    check_aliens_bottom(ai_setting, stats, screen, sb, aliens, ship, bullets)
def update_ship(ship):
    ship.update()

def check_fleet_edges(ai_setting, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break
            
def change_fleet_direction(ai_setting, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1

def check_aliens_bottom(ai_setting, stats, screen, sb, \
                 aliens, ship, bullets):
    """检测是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样进行处理
            ship_hit(ai_setting, stats, screen, sb, aliens, ship, bullets)
            break

def check_high_scores(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
