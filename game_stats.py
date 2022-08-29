class GameStats:
    '''跟踪游戏的统计信息'''
    def __init__(self,ai_game):
        '''初始化统计信息'''
        self.settings=ai_game.settings
        self.reset_stats()

        #让游戏一开始处于非活动状态
        self.game_active=False

        #help txt
        self.show_txt=False

        #任何情况下都不应该重置最高分
        try:
            with open('SaveData.json','r') as hi:
                self.high_score=eval(hi.read())
        except:
            self.high_score=0

    def reset_stats(self):
        '''初始化在游戏运行期间可能变化的统计信息'''
        self.ships_left=self.settings.ship_limit
        #得分
        self.score=0
        #计算命中率所需数据
        self.all_num=0
        self.goal_num=0
