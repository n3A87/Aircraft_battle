import pygame
from game_items import *
from game_hud import *
screen_rect = pygame.Rect(0,0,480,700)

class Game():
    def __init__(self):
        self.main_window = pygame.display.set_mode(screen_rect.size)
        self.game_over = False
        self.game_pause = False

        self.all_groups = pygame.sprite.Group() # 创建精灵组
        # self.all_groups.add(Background(False), Background(True))
        bg1 = Background(False, self.all_groups) # 背景1实例化
        bg2 = Background(True, self.all_groups) # 背景2实例化，并且都加入到all_groups精灵组中
        self.hero = GameSprite("me1.png",0,self.all_groups) #英雄实例化
        self.hero.rect.center = screen_rect.center #英雄位置
        self.hud_panel = HUDPanel(self.all_groups) #控制面板，把控制面板里的元素全加入到all_groups精灵组中

    def game_reset(self):
        self.game_over = False
        self.game_pause = False

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
                if self.game_over:
                    self.game_reset()
                else:
                    self.game_pause = not self.game_pause
        return False

    def game_start(self):
        clock = pygame.time.Clock()
        while True:
            if self.eventHandler():
                print("事件监听中。。。")
                return
            if self.game_over:
                print("游戏结束了，按空格重新开始")
            elif self.game_pause:
                print("游戏暂停了，按空格继续")
            else:
                print("游戏进⾏中")

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