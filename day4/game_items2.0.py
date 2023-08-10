import pygame
import random
from pygame.sprite import Sprite

screen_rect = pygame.Rect(0,0,480,700)
FRAME_INTERVAL = 10
HERO_BOMB_COUNT = 3
HERO_DEFAULT_MID_BOTTOM = (screen_rect.centerx, screen_rect.bottom - 90)

class GameSprite(Sprite):
    res_path = './res/images/'
    def __init__(self, image_name, speed, *group):
        super().__init__(*group)
        self.image = pygame.image.load(self.res_path+image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed

class Background(GameSprite):
    def __init__(self, isalt, *groups):
        super().__init__('background.png', 1, *groups)
        if isalt:
            self.rect.y = -self.rect.h

    def update(self, *args):
        super().update()
        if self.rect.y >= self.rect.h:
            self.rect.y = - self.rect.h

class StatusButton(GameSprite):
    def __init__(self,image_names,*groups):
        super().__init__(image_names[0],0,*groups)
        self.images = [pygame.image.load(self.res_path + name) for name in image_names]

    def switch_status(self,is_pause):
        self.image = self.images[1 if is_pause else 0 ]

class Label(pygame.sprite.Sprite):
    font_path = "./res/font/MarkerFelt.ttc"
    def __init__(self,text,size,color,*group):
        super().__init__(*group)
        self.font = pygame.font.Font(self.font_path,size)
        self.color = color
        self.image = self.font.render(text,True,self.color)
        self.rect = self.image.get_rect()

    def set_text(self,text):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()


class Plane(GameSprite):
    def __init__(self, normal_names, speed, value, wav_name, destroy_names, *groups):
        super().__init__(normal_names[0],speed,*groups)
        self.is_alive = True # 飞机默认是活着
        self.value = value # 飞机的分值
        self.wav_name = wav_name # 飞机的音效文件

        # 飞机要显示的图片
        self.destroy_images = [pygame.image.load(self.res_path+name) for name in destroy_names]
        self.destroy_index = 0

        self.normal_images = [pygame.image.load(self.res_path+name) for name in normal_names]
        self.normal_index = 0

    def reset_plane(self):
        self.is_alive = True
        self.normal_index = 0
        self.destroy_index = 0

        self.image = self.normal_images[0]


    def update(self, *args):
        if not args[0]:  # 判断frame_count == 0这个条件，决定是否执行后续图片更新的操作
            return

        if self.is_alive:
            self.image = self.normal_images[self.normal_index]
            count = len(self.normal_images)
            self.normal_index = (self.normal_index + 1) % count
        else:
            # 如果⻜机被摧毁了默认摧毁下标就是0 ，⼩于被摧毁的列表⻓度，那就展示被摧毁的过程，如果下标超过⻓度，说明这⼀轮播放完毕，那就重置⻜机了
            if self.destroy_index < len(self.destroy_images):
                self.image = self.destroy_images[self.destroy_index]
                self.destroy_index += 1
            else:
                self.reset_plane()

class Enemy(Plane):
    def __init__(self, *groups):
        super().__init__(['enemy1.png'],random.randint(1,3),1000,'enemy1_down.wav',[f"enemy1_down{i}.png" for i in range(1,5)],*groups)
        self.rect.bottom = random.randint(0, screen_rect.h - self.rect.h) - self.rect.h # 保证敌机在游戏界面内，不会超出屏幕底部
        self.rect.x = random.randint(0,screen_rect.width - self.rect.width)

    def reset_plane(self):
        super().reset_plane()
        # 为节省资源，敌机飞出屏幕后，重置敌人飞机
        self.rect.bottom = random.randint(0, screen_rect.h - self.rect.h) - self.rect.h  # 保证敌机在游戏界面内，不会超出屏幕底部
        self.rect.x = random.randint(0, screen_rect.width - self.rect.width)

    def update(self, *args):
        super().update(*args)

        self.rect.y += self.speed
        if self.rect.y > screen_rect.h:
            print("飞出屏幕外了")
            self.reset_plane()

class Hero(Plane):
    def __init__(self, *groups):
        super().__init__(("me1.png","me2.png"),random.randint(1,3),100,"me_down.wav",[f"enemy1_down{i}.png" for i in range(1,5)], *groups)
        self.is_power = False
        self.bomb_count = HERO_BOMB_COUNT
        self.rect.midbottom = HERO_DEFAULT_MID_BOTTOM

    def update(self, *args):
        super().update(*args)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        elif keys[pygame.K_LEFT]:
            self.rect.x -= 10
        elif keys[pygame.K_UP]:
            self.rect.y -= 10
        elif keys[pygame.K_DOWN]:
            self.rect.y += 10

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right>screen_rect.right:
            self.rect.right = screen_rect.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom>screen_rect.bottom:
            self.rect.bottom = screen_rect.bottom

    def blowup(self, eneimes_groups):
        if not self.is_alive or self.bomb_count <= 0:
            return 0
        self.bomb_count -= 1
        count = 0
        for enemy in eneimes_groups:
            if enemy.rect.bottom > 0:
                enemy.is_alive = False
                count += enemy.value
        print('#####', count)
        return count



