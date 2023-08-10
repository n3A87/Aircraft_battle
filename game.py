import pygame
import random
from game_items import *
from game_hud import *
from game_music import *
screen_rect = pygame.Rect(0,0,480,700)

class Game():
    def __init__(self):
        self.main_window = pygame.display.set_mode(screen_rect.size) #创建游戏窗口
        self.game_over = False #游戏结束标志位
        self.game_pause = False #游戏暂停标志位

        self.all_groups = pygame.sprite.Group() #初始化大精灵组
        self.enemies_groups = pygame.sprite.Group() #初始化敌机精灵组
        self.all_groups.add(Background(False), Background(True)) #背景12实例化
        self.hud_panel = HUDPanel(self.all_groups) #面板实例化
        self.hero = Hero(self.all_groups) #英雄飞机实例化
        self.hud_panel.show_bomb(self.hero.bomb_count) #显示炸弹数量
        self.create_enemies() #游戏一开始敌机就出现
        # 创建音乐对象
        self.mp = MusicPlayer("game_music.ogg",["bullet.wav","enemy1_down.wav","me_down.wav","use_bomb.wav"])
        # 播放背景音乐
        self.mp.play_bg()



    def game_reset(self):
        self.game_over = False
        self.game_pause = False
        self.hud_panel.panel_reset()
        self.hero.rect.midbottom = HERO_DEFAULT_MID_BOTTOM
        for enemy in self.enemies_groups:
            enemy.kill()
        for bullet in self.hero.bullets_group:
            bullet.kill()
        self.create_enemies()


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
            if not self.game_pause and not self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    print('BBBBBBBB')
                    self.mp.play_sound("use_bomb.wav")
                    # for enemy in self.enemies_groups:
                    #     enemy.is_alive = False
                    score = self.hero.blowup(self.enemies_groups) # 消耗所有敌机 返回得分
                    self.hud_panel.current_score(score)
                    self.hud_panel.show_bomb(self.hero.bomb_count) # 显示最新的炸弹数量
                elif event.type == HERO_DEAD_EVENT:
                    print("英雄飞机挂了。。。")
                    self.hud_panel.live_count -= 1
                    self.hud_panel.show_lives()
                elif event.type == HERO_POWER_OFF_EVENT:
                    self.hero.is_power = False
                    pygame.time.set_timer(HERO_POWER_OFF_EVENT,0)
                elif event.type == HERO_FIRE_EVENT:
                    print("发射子弹了。。。")
                    self.hero.fire(self.all_groups)


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
                self.check_collide()

            self.all_groups.draw(self.main_window)
            pygame.display.update()
            clock.tick(60) # 保证流畅的⽤户交互

    def create_enemies(self):
        # groups把两个精灵组组成一个元组。为了方便将新创建的敌机对象同时添加到两个精灵组中
        # 好处是敌机对象就可以同时被管理和绘制在整个游戏中，同时也方便对敌机的统一处理。
        groups = (self.all_groups,self.enemies_groups)
        for i in range(10):
            Enemy(*groups) # 创建了一个敌机对象，并将它同时添加到两个精灵组中

    def check_collide(self):
        if not self.hero.is_power:
            collide_enemies = pygame.sprite.spritecollide(self.hero, self.enemies_groups,False,pygame.sprite.collide_mask)
            collide_enemies = list(filter(lambda x:x.is_alive, collide_enemies))
            if len(collide_enemies):
                self.mp.play_sound("me_down.wav")
                self.hero.is_alive = False
                print("撞了。。。。。。")
            for enemy in collide_enemies:
                self.mp.play_sound("enemy1_down.wav")
                enemy.is_alive = False

        hit_enemies = pygame.sprite.groupcollide(self.enemies_groups,self.hero.bullets_group,False,True,pygame.sprite.collide_mask)

        for enemy in hit_enemies:
            if enemy.is_alive:
                self.hud_panel.current_score(100)
            self.mp.play_sound("enemy1_down.wav")
            enemy.is_alive=False



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('3A87⻜机⼤战')
    game = Game()
    game.game_start()
    pygame.quit()