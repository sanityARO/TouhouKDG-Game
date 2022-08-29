import pygame
from pygame.sprite import Sprite

class Left(Sprite):
    '''管理剩余自机'''

    def __init__(self,ai_game):
        super().__init__()
        #初始化自机并设置其初始位置
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()

        #加载自机并获取其外接矩形
        self.image=pygame.image.load('images/ship_left1.bmp')
        self.rect=self.image.get_rect()

        #对于每个新自机,都将其放在屏幕底部的中央
        self.rect.midbottom=self.screen_rect.midbottom

        #在自机xy属性中存储小数值
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)
