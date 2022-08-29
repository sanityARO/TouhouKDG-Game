import pygame.font
from pygame.sprite import Group
from left import Left

class Scoreboard:
    '''显示得分信息的类'''
    def __init__(self,ai_game):
        #初始化显示得分涉及的属性
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=ai_game.settings
        self.stats=ai_game.stats

        #显示得分信息的字体设置
        self.text_color = 30,30,30
        self.font=pygame.font.SysFont(None,48)
        #准备初始得分图片和最高得分图片
        self.prep_score()
        self.prep_high_score()
        #命中率图片
        self.prep_goal_rate()
        #剩余自机数图像
        self.prep_left()

    def prep_score(self):
        '''将得分渲染为图像'''
        score_str=f"Score | {format(self.stats.score,',')}"
        self.score_image=self.font.render(score_str,True,
                        self.text_color,self.settings.bg_color)

        #在屏幕右上角显示得分
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=8

    def prep_high_score(self):
        '''将最高得分渲染为图像'''
        high_score_str=f"Record | {format(self.stats.high_score,',')}"
        self.high_score_image=self.font.render(high_score_str,True,
                        self.text_color,self.settings.bg_color)

        #在屏幕正上显示得分
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=16

    def prep_goal_rate(self):
        '''将命中率为图像'''
        if self.stats.all_num:
            goal_rate_str="On-target | {:.4f}%".format(
                round(self.stats.goal_num/self.stats.all_num*100,4))
        else:
            goal_rate_str="None"
        self.goal_rate_image=self.font.render(goal_rate_str,True,
                        self.text_color,self.settings.bg_color)

        #在自机正下方显示比率
        self.goal_rate_rect=self.goal_rate_image.get_rect()
        self.goal_rate_rect.top=self.score_rect.bottom
        self.goal_rate_rect.right=self.score_rect.right

    def prep_left(self):
        '''显示还剩多少自机'''
        self.lefts = Group()
        for left_number in range (self.stats.ships_left):
            left=Left(self.ai_game)
            left.rect.x=20+left_number*left.rect.width
            left.rect.y=11
            self.lefts.add(left)

    def check_high_score(self):
        '''检查是否诞生了新高分'''
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            self.prep_high_score()
        
    def show_score(self):
        '''在屏幕上显示得分'''
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.goal_rate_image,self.goal_rate_rect)
        self.lefts.draw(self.screen)
