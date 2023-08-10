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
        # self.all_groups.add(Background(False), Background(True))
        bg1 = Background(False, self.all_groups)
        bg2 = Background(True, self.all_groups)
        self.hero = GameSprite("me1.png",0,self.all_groups)
        self.hero.rect.center = screen_rect.center
        self.hud_panel = HUDPanel(self.all_groups)

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
                    self.hud_panel.show_bomb(random.randint(1, 10))
                    self.hud_panel.live_count -= 1
                    self.hud_panel.show_lives()
                    self.hud_panel.current_score(random.randint(1, 10))
        return False

    def game_start(self):
        clock = pygame.time.Clock()
        while True:
            self.game_over = self.hud_panel.live_count == 0 # 增加游戏结束条件
            if self.eventHandler():
                print("（人为关闭游戏了没）事件监听中。。。游戏结束了。。。")
                self.hud_panel.save_best_score() # 存最好成绩
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
                self.hud_panel.current_score(1)

            self.all_groups.draw(self.main_window)
            self.all_groups.update()
            pygame.display.update()
            clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('ZUA版-⻜机⼤战')
    game = Game()
    game.game_start()
    pygame.quit()