class Settings:
    '''存储游戏中所有设置的类'''

    def __init__(self):
        '''初始化游戏设置'''
        #屏幕设置
        self.screen_width=1420
        self.screen_height=960
        '''
        self.screen_width_save=1420
        self.screen_height_save=960
        '''
        self.bg_color=(230,230,230)

        #自机设置
        self.ship_limit = 3 #5,3

        #子弹设置  (easy,hard):
        self.bullet_width= 125 #200,20
        self.bullet_height=22
        self.bullet_color=(204,0,0)
        self.bullets_allowed= 2 #7,5
        self.low_power= True #False,True

        #敌机设置
        self.fleet_drop_speed= 16 #10

        #加快游戏节奏的速度
        self.speedup_scale = 1.1
        #敌机分数的提高速度
        self.score_scale = 83/50
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.bullet_width= 125 
        self.ship_speed = 1.5
        self.bullet_speed= 1.0 #1.5,1.0
        self.alien_speed= 0.5 #0.3,0.5
        #fleet_direction为1右移，为-1左移
        self.fleet_direction=-1
        #计分
        self.alien_points=50

    def increase_speed(self):
        '''提高速度设置，和敌机分数'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)
        if self.bullet_width>20:
            self.bullet_width -= 15
