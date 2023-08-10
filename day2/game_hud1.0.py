from game_items import *
screen_rect = pygame.Rect(0,0,480,700)

#控制面板类
class HUDPanel(object):
    margin = 10 #边距
    white = (255, 255, 255) #白色
    gray = (64, 64, 64) #灰色

    def __init__(self, display_group):
        self.score = 0  # 游戏分数
        self.live_count = 3  # 默认3条命
        self.level = 1  # 游戏的级别 1级
        self.best_score = 0  # 最好成绩
        # 显示状态精灵,以元组的形式将图⽚名称传递到初始化⽅法
        self.status_sprite = StatusButton(('pause.png', 'resume.png'),
                                          display_group) #最后一个参数代表加入到display_group小组里
        self.status_sprite.rect.topleft = (self.margin, self.margin) #(x,y)
        # 显示炸弹精灵
        self.bomb_sprite = GameSprite('bomb.png', 0, display_group)
        self.bomb_sprite.rect.bottomleft = (self.margin, screen_rect.bottom -
                                            self.margin)
        # 显示⽣命计数精灵
        self.life_sprite = GameSprite('life.png', 0, display_group)
        self.life_sprite.rect.bottomright = (screen_rect.w - self.margin * 6,
                                             screen_rect.bottom - self.margin)
        # ------------------------标签精灵
        # 得分标签
        self.score_label = Label(f"{self.score}", 32, self.gray, display_group)
        self.score_label.rect.midleft = (self.status_sprite.rect.right,
                                         self.status_sprite.rect.centery)
        # 炸弹计数标签
        self.bomb_label = Label("X 3", 32, self.gray, display_group)
        self.bomb_label.rect.midleft = (self.bomb_sprite.rect.right + self.margin,
                                        self.bomb_sprite.rect.centery)
        # # ⽣命计数标签
        self.lives_label = Label(f"X {self.live_count}", 32, self.gray,
                                 display_group)
        self.lives_label.rect.midright = (screen_rect.right - self.margin,
                                          self.life_sprite.rect.centery)
        # 最好成绩标签，屏幕中⼼
        self.best_score_label = Label(f"Best: {self.best_score}", 36, self.white,
                                      display_group)
        self.best_score_label.rect.center = screen_rect.center
        # 游戏状态标签
        self.status_sprite_label = Label("Game Paused", 40, self.white,
                                         display_group)
        self.status_sprite_label.rect.midbottom = (screen_rect.centerx,
                                                   self.best_score_label.rect.top -
                                                   2 * self.margin)
        # 提示标签
        self.tip_label = Label("press spacebar to continue", 30, self.white,
                               display_group)
        self.tip_label.rect.midtop = (screen_rect.centerx,
                                      self.best_score_label.rect.bottom + 2 *
                                      self.margin)