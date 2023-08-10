import pygame

screen_rect = pygame.Rect(0,0,480,700) # 创建矩形

class Game():
    def __init__(self):
        self.main_window = pygame.display.set_mode(screen_rect.size) # 创建窗口对象
        self.game_over = False # 初始化结束
        self.game_pause = False #初始化暂停
        self.create_image() #绘制图像

    # 复位方法
    def game_reset(self):
        self.game_over = False
        self.game_pause = False

    # 游戏启动方法
    def game_start(self):
        clock = pygame.time.Clock() #创建时钟对象
        while True:
            if self.eventHandler(): #调用方法，监听事件
                print("事件监听中。。。")
                return
            if self.game_over: #结束？
                print("游戏结束了，按空格重新开始")
            elif self.game_pause: #暂停？
                print("游戏暂停了，按空格继续")
            else:
                print("游戏进⾏中")

            self.main_window.blit(self.bg, self.bg_rect) #创建背景
            self.main_window.blit(self.hero, self.hero_rect) #创建英雄

            pygame.display.update() #刷新界面
            clock.tick(1)

    # 监听事件方法
    def eventHandler(self):
        for event in pygame.event.get():  # 获取用户交互
            if event.type == pygame.QUIT:  # 叉掉
                print("点击了关闭")
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # 按键esc
                print("按下了esc")
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # 按键空格
                print("按下了空格")
                if self.game_over:  # 如果游戏结束，复位重启
                    self.game_reset()
                else:  # 游戏没结束，暂停
                    self.game_pause = not self.game_pause
        return False

    # 绘制图像方法
    def create_image(self):
        self.bg = pygame.image.load("./res/images/background.png") #下载
        self.bg_rect = self.bg.get_rect()

        self.hero = pygame.image.load("./res/images/me1.png")
        self.hero_rect = self.hero.get_rect()
        self.hero_rect.center = self.bg_rect.center


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.game_start()
    pygame.quit()