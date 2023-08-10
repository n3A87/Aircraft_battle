import pygame
from pygame.sprite import Sprite

#游戏精灵类
class GameSprite(Sprite):
    res_path = './res/images/'
    def __init__(self, image_name, speed, *group):
        super().__init__(*group)
        self.image = pygame.image.load(self.res_path+image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed

#背景类
class Background(GameSprite):
    def __init__(self, isalt, *groups):
        super().__init__('background.png', 1, *groups) #传入背景照片，背景移动速度
        if isalt: #判断背景1or2
            self.rect.y = -self.rect.h

    def update(self, *args):
        super().update() #调用方法
        if self.rect.y >= self.rect.h: #超出边界
            self.rect.y = - self.rect.h

#状态按钮类
class StatusButton(GameSprite):
    def __init__(self,image_names,*groups):
        super().__init__(image_names[0],0,*groups) #初始化pause.png
        self.images = [pygame.image.load(self.res_path + name) for name in image_names]

    def switch_status(self,is_pause):
        self.image = self.images[1 if is_pause else 0 ]

#标签类
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