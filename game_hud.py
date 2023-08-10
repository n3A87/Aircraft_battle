from game_items import *
screen_rect = pygame.Rect(0,0,480,700)

class HUDPanel(object):
    margin = 10
    white = (255, 255, 255)
    gray = (64, 64, 64)
    record_filename = "record.txt"

    def __init__(self, display_group):
        self.score = 0  # 游戏分数
        self.live_count = 3  # 默认3条命
        self.level = 1  # 游戏的级别 1级
        self.best_score = 0  # 最好成绩
        self.load_best_score()  # 获取上次最好成绩
        # 显示状态精灵,以元组的形式将图⽚名称传递到初始化⽅法
        self.status_sprite = StatusButton(('pause.png', 'resume.png'),
                                          display_group)
        self.status_sprite.rect.topleft = (self.margin, self.margin)
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
        self.best_score_label = Label(f"Best: {self.best_score}", 36, self.white)
        # 游戏状态标签
        self.status_sprite_label = Label("Game Paused", 40, self.white)
        # 提示标签
        self.tip_label = Label("press spacebar to continue", 30, self.white)

    def show_bomb(self,count):
        self.bomb_label.set_text(f"{count}")
        self.bomb_label.rect.midleft = (self.bomb_sprite.rect.right + self.margin,
                                        self.bomb_sprite.rect.centery)

    def show_lives(self):
        self.lives_label.set_text(f"X {self.live_count}")
        self.lives_label.rect.midright = (screen_rect.right - self.margin,
                                          self.bomb_sprite.rect.centery)

    def current_score(self, enemy_score):
        self.score += enemy_score
        self.best_score = self.score if self.score > self.best_score else self.best_score
        self.score_label.set_text(f"{self.score}")
        self.score_label.rect.midleft = (self.status_sprite.rect.right,
                                         self.status_sprite.rect.centery)

    def save_best_score(self):
        file = open(f"{self.record_filename}", "w")

        file.write(f"{self.best_score}")
        file.close()

    def load_best_score(self):
        try:
            # 读取⽂件内容
            file = open(self.record_filename, 'r')
            content = file.read()
            file.close()
            # 转换内容为数字
            self.best_score = int(content)
        except (FileNotFoundError, ValueError):
            print('读取最⾼得分⽂件，发⽣异常')

    def panel_paused(self, game_over, display_group):
        if display_group.has(self.best_score_label, self.status_sprite_label,
                             self.tip_label):
            return
        status = "Game Over!" if game_over else "Game paused!"
        tip = "Press spacebar to "
        tip += "play again" if game_over else "continue"

        self.best_score_label.set_text(f"Best:{self.best_score}")
        self.status_sprite_label.set_text(status)
        self.tip_label.set_text(tip)

        self.best_score_label.rect.center = screen_rect.center
        self.status_sprite_label.rect.midbottom = (self.best_score_label.rect.centerx,
                                                   self.best_score_label.rect.top - 2 * self.margin)
        self.tip_label.rect.midtop = (self.best_score_label.rect.centerx,
                                      self.best_score_label.rect.bottom + 2 * self.margin)

        display_group.add(self.best_score_label, self.status_sprite_label,
                          self.tip_label)

        self.status_sprite.switch_status(True)

    def panel_resume(self, display_group):
        display_group.remove(self.best_score_label, self.status_sprite_label, self.tip_label)
        self.status_sprite.switch_status(False)

    def panel_reset(self):
        # 游戏结束后 需要重置
        # 1.英雄⻜机的数量为3 得分为 0 炸弹为 3
        self.score = 0 # 初始化游戏得分
        self.live_count = 3 # 默认3条⽣命
        self.show_lives()
        # 炸弹数量
        self.show_bomb(3)

