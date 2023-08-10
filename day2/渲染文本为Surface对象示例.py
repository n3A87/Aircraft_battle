import pygame

pygame.init()

# 设置显示窗口
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("文本渲染示例")

# 加载字体
font = pygame.font.Font(None, 36)

# 将文本渲染为Surface对象
text_surface = font.render("Hello, pygame!", True, (255, 255, 255))

# 主游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清空屏幕
    screen.fill((0, 0, 0))

    # 将文本Surface绘制到屏幕上，位置为(100, 100)
    screen.blit(text_surface, (100, 100))

    # 更新显示
    pygame.display.flip()

pygame.quit()
