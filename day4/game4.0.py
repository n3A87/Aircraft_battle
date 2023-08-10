import pygame
import random
from game_items import *
from game_hud import *
screen_rect = pygame.Rect(0,0,480,700)

class Game():
    def __init__(self):
        self.main_window = pygame.display.set_mode(screen_rect.size)
        self.game_over = False
        self.game_pause = False

        self.all_groups = pygame.sprite.Group()
        self.enemies_groups = pygame.sprite.Group()
        # self.all_groups.add(Background(False), Background(True))
        bg1 = Background(False, self.all_groups)
        bg2 = Background(True, self.all_groups)
        # 最初self.hero = GameSprite("me1.png", 0, self.all_groups)
        # 然后self.hero = Plane(("me1.png", "me2.png"), 10,0,"me_down.wav",[f"me_destroy_{i}.png" for i in range(1,5)], self.all_groups)
        #    self.hero.rect.center = screen_rect.center

        self.hud_panel = HUDPanel(self.all_groups)
        self.hero = Hero(self.all_groups)
        self.hud_panel.show_bomb(self.hero.bomb_count)
        self.create_enemies()

    def game_reset(self):
        self.game_over = False
        self.game_pause = False
        self.hud_panel.panel_reset()

    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("点击了关闭")
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("按下了esc")
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("按下了空格")
                if self.game_pause:
                    self.game_reset()
                else:
                    self.game_pause = not self.game_pause
            if not self.game_pause and not self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    print('BBBBBBBB')
                    # for enemy in self.enemies_groups:
                    #     enemy.is_alive = False
                    score = self.hero.blowup(self.enemies_groups) # 消耗所有敌机 返回得分
                    self.hud_panel.current_score(score)
                    self.hud_panel.show_bomb(self.hero.bomb_count) # 显示最新的炸弹数量
        return False

    def game_start(self):
        clock = pygame.time.Clock()
        frame_count = 0
        while True:
            self.game_over = self.hud_panel.live_count == 0
            if self.eventHandler():
                print("事件监听中。。。")
                self.hud_panel.save_best_score()
                return
            if self.game_over:
                print("游戏结束了，按空格重新开始")
                self.hud_panel.panel_paused(True, self.all_groups)
            elif self.game_pause:
                print("游戏暂停了，按空格继续")
                self.hud_panel.panel_paused(False, self.all_groups)
            else:
                print("游戏进⾏中")
                self.hud_panel.panel_resume(self.all_groups)
                # self.hud_panel.current_score(1)
                frame_count = (frame_count + 1) % FRAME_INTERVAL # 降低逐动画的动画顿率
                self.all_groups.update(frame_count == 0) # 不是每帧都更新。60帧每秒的话，只更新6次

            self.all_groups.draw(self.main_window)
            pygame.display.update()
            clock.tick(60) # 保证流畅的⽤户交互

    def create_enemies(self):
        # groups把两个精灵组组成一个元组。为了方便将新创建的敌机对象同时添加到两个精灵组中
        # 好处是敌机对象就可以同时被管理和绘制在整个游戏中，同时也方便对敌机的统一处理。
        groups = (self.all_groups,self.enemies_groups)
        for i in range(10):
            Enemy(*groups) # 创建了一个敌机对象，并将它同时添加到两个精灵组中


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('ZUA版-⻜机⼤战')
    game = Game()
    game.game_start()
    pygame.quit()