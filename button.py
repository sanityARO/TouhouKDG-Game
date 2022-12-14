import pygame.font

class Button:
    def __init__(self,ai_game,msg,mid,n):
        '''初始化按钮属性'''
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.n=n
        self.mid=mid

        #设置按钮尺寸和其他属性
        if self.mid:
            self.width,self.height=200,50
            self.button_color=(192,192,192)  #默认透明
            self.text_color=(255,45,81)
        else:
            #help txt的尺寸和普通按钮尺寸不同
            self.width,self.height=440,38
            self.button_color=(212,212,212)
            self.text_color=(30,30,30)
            
        self.font=pygame.font.SysFont(None,48)

        #创建按钮的rect对象，并使其居中
        self.rect=pygame.Rect(0,0,self.width,self.height)

        if self.mid:
            self.rect.centerx=self.screen_rect.centerx
            self.rect.centery=self.screen_rect.centery+self.height * (self.n-1)
        else:
            self.rect.left=20
            self.rect.bottom=self.screen_rect.bottom+self.height * (self.n-5)

        #按钮的标签只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self,msg):
        '''将msg渲染为图像，并使其在按钮上居中'''
        self.msg_image=self.font.render(msg,True,self.text_color,
                                        self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center

    def draw_button(self):
        #绘制一个中颜色填充的按钮，再绘制文本
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
