import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''表示单个敌机的类'''
    def __init__(self,ai_game,num):
        '''初始化敌机并设置其初始位置'''
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.num=num
        
        name=['images/0.bmp',
              'images/1.bmp','images/2.bmp','images/3.bmp','images/4.bmp',
              'images/5.bmp','images/6.bmp','images/7.bmp','images/8.bmp',
              'images/9.bmp','images/10.bmp','images/11.bmp','images/12.bmp',
              'images/13.bmp','images/14.bmp','images/15.bmp','images/16.bmp',
              'images/17.bmp','images/18.bmp','images/19.bmp']
        
        #加载敌机图像并设置其rect属性
        self.image=pygame.image.load(name[self.num])
        self.rect=self.image.get_rect()

        #每个敌机最初都在屏幕左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height/8

        #存储敌机的精确水平位置
        self.x=float(self.rect.x)

    def check_edges(self):
        '''如果敌机处于屏幕边缘，就返回True'''
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right or self.rect.left<=0:
            return True
        
    def update(self):
        #左右移动敌机
        self.centerx+=(self.settings.alien_speed*
                 self.settings.fleet_direction)
        self.rect.centerx=self.centerx
