import sys
from time import sleep
from random import randint
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class TouhouKDG:
    '''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏，创建游戏资源'''
        pygame.init()
        self.settings=Settings()

        #窗口化与全屏
        
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        '''
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        '''
            
        pygame.display.set_caption("Touhou KDG -- presented by SANITY")

        #创建一个用于存储游戏统计信息的实例，并创建计分板
        self.stats=GameStats(self)
        self.sb=Scoreboard(self)

        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()

        #创建play按钮，help,reset
        self.newgame_button=Button(self,'New Game',True,-1.5)
        self.continue_button=Button(self,'Continue',True,0)
        self.help_button=Button(self,'Help',True,1.5)
        self.reset_button=Button(self,'Reset',True,3)
        self.exit_button=Button(self,'Exit',True,4.5)
        self.show_help1=Button(self,"click or Space.............fire",False,0)
        self.show_help2=Button(self,"arrows or W/S/A/D..move",False,1)
        self.show_help3=Button(self,"Backspace or P......pause",False,2)
        self.show_help4=Button(self,"Delete..........................exit",False,3)
        self.show_help5=Button(self,"Help:",False,-1)
        
    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()            
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            
    def _check_events(self):
         #监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
                
            elif event.type==pygame.KEYDOWN:
                #test: print(event.key)
                self._check_keydown_events(event)
                    
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type==pygame.MOUSEBUTTONDOWN:
                if self.stats.game_active:
                    self._fire_bullet()
                else:
                    mouse_pos=pygame.mouse.get_pos()
                    self._check_button(mouse_pos)

    def _check_button(self,mouse_pos):
        '''玩家点击按钮事件'''
        if self.newgame_button.rect.collidepoint(mouse_pos):
            #重设游戏设置
            self.settings.initialize_dynamic_settings()
            self._start_game()
            
        elif self.continue_button.rect.collidepoint(mouse_pos):
            self._continue_game()
            
        elif self.help_button.rect.collidepoint(mouse_pos):
            if not self.stats.show_txt:
                #画出提示框
                self.stats.show_txt=True
            else:
                self.stats.show_txt=False
        
        elif self.reset_button.rect.collidepoint(mouse_pos):
            self.stats.high_score=0
            self.sb.prep_high_score()

        elif self.exit_button.rect.collidepoint(mouse_pos):
            self._end_game()

        else:
            #取消help界面
            self.stats.show_txt=False

    def _start_game(self):
        #取消help界面
        self.stats.show_txt=False
        
        #重置统计信息
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_goal_rate()
        self.stats.game_active=True

        #清空余下的敌机和子弹
        self.aliens.empty()
        self.bullets.empty()

        #创建一群新敌机并让自机居中
        self._create_fleet()
        self.ship.center_ship()

        #隐藏光标
        pygame.mouse.set_visible(False)

    def _continue_game(self):
        #取消help界面
        self.stats.show_txt=False
        
        if not self.stats.score:
            self._start_game()
        else:
            self.stats.game_active=True
            pygame.mouse.set_visible(False)

    def _end_game(self):
        with open('SaveData.json','w') as hi:
            hi.write(str(self.stats.high_score))
        sys.exit()

    def _help_pause(self):
        #冻结画面
        self.stats.game_active=False
        #取消隐藏光标
        pygame.mouse.set_visible(True)
        #画出提示框
        self.stats.show_txt=True

    def _check_keydown_events(self,event):
        if event.key in [pygame.K_RIGHT,pygame.K_d]:
            self.ship.moving_right=True
        elif event.key in [pygame.K_LEFT,pygame.K_a]:
            self.ship.moving_left=True
        elif event.key in [pygame.K_UP,pygame.K_w]:
            self.ship.moving_up=True
        elif event.key in [pygame.K_DOWN,pygame.K_s]:
            self.ship.moving_down=True
        elif (self.stats.game_active) and event.key in [pygame.K_p,
                                                        pygame.K_BACKSPACE]:
            #帮助和暂停
            self._help_pause()
        elif (not self.stats.game_active) and event.key in [pygame.K_p,
                                                            pygame.K_BACKSPACE,
                                                            pygame.K_SPACE]:
            self._continue_game()
        elif event.key == pygame.K_DELETE:
            self._end_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        
    def _check_keyup_events(self,event):
        if event.key in [pygame.K_RIGHT,pygame.K_d]:
            self.ship.moving_right=False
        elif event.key in [pygame.K_LEFT,pygame.K_a]:
            self.ship.moving_left=False
        elif event.key in [pygame.K_UP,pygame.K_w]:
            self.ship.moving_up=False
        elif event.key in [pygame.K_DOWN,pygame.K_s]:
            self.ship.moving_down=False

    def _fire_bullet(self):
        '''创建一颗子弹,并将其加入到编组bullets当中'''
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
            self.stats.all_num+=1
            

    def _update_bullets(self):
        '''更新子弹位置并删除消失的子弹'''
        #更新子弹位置
        self.bullets.update()
        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)                
                #再次更新命中率
                self.sb.prep_goal_rate()
                
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''检查是否有子弹击中敌机，删除被击中的'''
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,self.settings.low_power,True)

        if collisions:
            for aliens in collisions.values():
                self.stats.goal_num+=1
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_goal_rate()
            
        if not self.aliens:
            self.start_new_level()                 

    def start_new_level(self):
        #自机移动到底部, 删除现有子弹并新建一群敌机
        self.bullets.empty()
        self.ship.screen_bottom_ship()
        sleep(0.1)
        self._create_fleet()
        self.settings.increase_speed()

    def _update_aliens(self):
        '''检测到达边缘，更新敌机群中所有敌机的位置'''
        self._check_fleet_edges()
        self.aliens.update()

        #检测自机和敌机之间的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #检测是否有敌机到达屏幕底部
        self._check_aliens_bottom()
        
    def _create_fleet(self):
        '''创建敌机群'''
        #创建一个敌机并计算一行可容纳多少敌机
        alien=Alien(self,0)
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-alien_width/2*2
        number_aliens_x =int( available_space_x // (1.75*alien_width))

        #计算屏幕可容纳多少敌机
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-
                           (2*alien_height)-ship_height)
        number_rows=int(available_space_y//(1.6*alien_height))
        
        #创建敌机群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                num=randint(1,19)
                self._create_alien(alien_number,row_number,num)

    def _create_alien(self,alien_number,row_number,num):
        #创建一个敌机并将其加入当前行
        alien=Alien(self,0)
        alienn=Alien(self,num)
        alien_width,alien_height=alien.rect.size
        alienn.centerx=alien_width*1.8+1.75*alien_width*alien_number
        alienn.rect.centerx=alienn.centerx
        alienn.rect.bottom=alien.rect.height*1.8+1.6*alien.rect.height*row_number
        self.aliens.add(alienn)

    def _check_fleet_edges(self):
        #有敌机到达边缘
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()             
                break

    def _change_fleet_direction(self):
        #整群敌机下移，并改变方向
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _check_aliens_bottom(self):
        #检查是否有外星人到达了屏幕底部
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        '''响应自机被敌机撞到'''

        if self.stats.ships_left>0:
            #将剩余自机-1
            self.stats.ships_left -= 1
            self.sb.prep_left()

            #清空敌机和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的敌机，并将自机放到屏幕底端的中央
            self.ship.center_ship()
            self._create_fleet()

            #暂停
            sleep(0.5)
        else:
            self.stats.game_active=False
            pygame.mouse.set_visible(True)
        #print(self.stats.ships_left)   #test
        
    def _update_screen(self):
        #每次循环重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.aliens.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.sb.show_score()

        #如果游戏处于非活动状态，就绘制按钮
        if not self.stats.game_active:
            self.continue_button.draw_button()
            self.newgame_button.draw_button()
            self.help_button.draw_button()
            self.reset_button.draw_button()
            self.exit_button.draw_button()

        if self.stats.show_txt:
            self.show_help1.draw_button()
            self.show_help2.draw_button()
            self.show_help3.draw_button()
            self.show_help4.draw_button()
            self.show_help5.draw_button()
        
        #让最近绘制的屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    '''创建实例并运行游戏'''
    ai = TouhouKDG()
    ai.run_game()
