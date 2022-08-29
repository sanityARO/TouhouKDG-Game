import pygame

class Ship:
    '''管理自机'''

    def __init__(self,ai_game):
        #初始化自机并设置其初始位置
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()

        #加载自机并获取其外接矩形
        self.image=pygame.image.load('images/0.bmp')
        self.rect=self.image.get_rect()

        #对于每个新自机,都将其放在屏幕底部的中央
        self.rect.midbottom=self.screen_rect.midbottom

        #在自机xy属性中存储小数值
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

        #移动标志
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False

    def update(self):
        '''根据移动标志调整飞船位置'''
        #更新对象而不是rect对象的xy值
        if self.moving_right and self.rect.right<self.screen_rect.right+5:
            self.x+=self.settings.ship_speed
        if self.moving_left and self.rect.left>2:
            self.x-=self.settings.ship_speed
        if self.moving_up and self.rect.top>-1:
            self.y-=self.settings.ship_speed
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom+3:
            self.y+=self.settings.ship_speed

        #根据self.x y更新rect对象
        self.rect.x=self.x
        self.rect.y=self.y
            
    def blitme(self):
        '''在指定位置绘制自机'''
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        '''让飞船在屏幕底端居中'''
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)

    def screen_bottom_ship(self):
        '''让飞船在屏幕底端'''
        self.rect.bottom=self.screen_rect.bottom
        self.x=float(self.rect.x)
        self.y=float(self.rect.y)#这个y必须写！
