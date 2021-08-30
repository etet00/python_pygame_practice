import os
import random
import pygame
from player import Player
from rocks import Rocks
from points import Points
from explosion import Explosion
from treasures import Treasures

WIDTH, HEIGHT = 500, 600
SIZE = (WIDTH, HEIGHT)
FPS = 60

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE_SMOKE = (245, 245, 245)


def main():
    # 進行遊戲、音效的初始化 & 創建遊戲視窗，並使用tuple傳入視窗大小
    pygame.init()           # 遊戲初始化
    pygame.mixer.init()     # 音效初始化
    screen = pygame.display.set_mode(SIZE)
    # print(screen.get_width())
    pygame.display.set_caption("test game")  # 更改視窗上的名稱
    rock_icon = pygame.image.load(os.path.join("img", "r7.png")).convert()
    rock_icon.set_colorkey(BLACK)
    pygame.display.set_icon(rock_icon)
    clock = pygame.time.Clock()

    # 載入字體
    # font = pygame.font.match_font("Times New Roman")  # 載入電腦內建字體
    font = os.path.join("fonts","font.ttf")

    # 載入圖片
    background = pygame.image.load(os.path.join("img", "background.png")).convert()     # 載入背景圖片
    player_img = pygame.image.load(os.path.join("img", "f.png")).convert()              # 載入飛船圖片
    bullet_img = pygame.image.load(os.path.join("img", "b.png")).convert()              # 載入子彈圖片
    rock_imgs = []      # 載入不同石頭圖片
    for i in range(8):
        rock_img = pygame.image.load(os.path.join("img", f"r{i}.png")).convert()
        rock_imgs.append(rock_img)
    expl_imgs = []              # 載入石頭爆炸圖片
    player_expl_imgs = []       # 載入飛船死亡爆炸圖片
    for i in range(9):
        expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
        player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
        expl_img.set_colorkey(BLACK)     # 去背
        player_expl_img.set_colorkey(BLACK)
        expl_imgs.append(expl_img)
        player_expl_imgs.append(player_expl_img)

    treasure_imgs = []          # 載入掉落寶物圖片
    for i in range(2):
        treasure_img = pygame.image.load(os.path.join("img", f"t{i}.png")).convert()
        treasure_imgs.append(treasure_img)

    # 載入音樂與音效
    fire_sound = pygame.mixer.Sound(os.path.join("music", "laser1.mp3"))        
    fire_sound.set_volume(0.1)          # set_volume 為調整音效音量大小，傳入介於 0 到 1 之間的浮點數
    heal_sound = pygame.mixer.Sound(os.path.join("music", "heal.mp3"))        
    heal_sound.set_volume(0.5)          # set_volume 為調整音效音量大小，傳入介於 0 到 1 之間的浮點數
    levelup_sound = pygame.mixer.Sound(os.path.join("music", "levelup.mp3"))        
    levelup_sound.set_volume(0.55)          # set_volume 為調整音效音量大小，傳入介於 0 到 1 之間的浮點數
    rock_explosion_sound = []    
    for i in range(4):
        expl_s = pygame.mixer.Sound(os.path.join("music", f"explosion{i}.mp3"))
        expl_s.set_volume(0.1)
        rock_explosion_sound.append(expl_s)
    death_sound = pygame.mixer.Sound(os.path.join("music", "rumble.ogg"))
    pygame.mixer.music.load(os.path.join("music", "background.ogg"))
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)  #　argument -1 表示無線循環撥放背景音樂 　

    # # 建立物件並加入 pygame.sprite 群組
    # group_sprites = pygame.sprite.Group()   # 建立有有物件的 pygame.sprite 群組
    # group_rocks = pygame.sprite.Group()     # 建立岩石的 pygame.sprite 群組
    # group_potato = pygame.sprite.Group()    # 建立岩石馬鈴薯的 pygame.sprite 群組
    # group_bullets = pygame.sprite.Group()   # 建立子彈的 pygame.sprite 群組
    # group_treasures = pygame.sprite.Group() # 建立掉落寶物的 pygame.sprite 群組
    # player = Player(WHITE, WIDTH, HEIGHT, player_img, screen)   # 建立玩家物件
    # group_sprites.add(player)               # 將 player 物件加入群組
    # for _ in range(10):
    #     create_rocks(group_sprites, group_rocks, group_potato, rock_imgs)

    # # 建立計算遊戲分數之物件
    # cal_points = Points(font, 30, WHITE, screen)   # 字體名稱、大小、顏色以及寫入文字的遊戲視窗




    # 建立遊戲執行迴圈
    processing = True
    show_init_screen = True
    while processing:
        if show_init_screen:
            close_or_not = show_init(screen, font, clock, background)
            if close_or_not:
                break
            show_init_screen = False
            # 建立物件並加入 pygame.sprite 群組
            group_sprites = pygame.sprite.Group()   # 建立有有物件的 pygame.sprite 群組
            group_rocks = pygame.sprite.Group()     # 建立岩石的 pygame.sprite 群組
            group_potato = pygame.sprite.Group()    # 建立岩石馬鈴薯的 pygame.sprite 群組
            group_bullets = pygame.sprite.Group()   # 建立子彈的 pygame.sprite 群組
            group_treasures = pygame.sprite.Group() # 建立掉落寶物的 pygame.sprite 群組
            player = Player(WHITE, WIDTH, HEIGHT, player_img, screen)   # 建立玩家物件
            group_sprites.add(player)               # 將 player 物件加入群組
            for _ in range(10):
                create_rocks(group_sprites, group_rocks, group_potato, rock_imgs)

            # 建立計算遊戲分數之物件
            cal_points = Points(font, 30, WHITE, screen)   # 字體名稱、大小、顏色以及寫入文字的遊戲視窗

        clock.tick(FPS)  # 設定畫片更新頻率
        # 取得輸入
        for event in pygame.event.get():
            # print(event.type)
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.hidden == False:
                    if player.gun_level == 1:
                        shoot = player.shoot(BLACK, bullet_img, fire_sound)
                        group_sprites.add(shoot)
                        group_bullets.add(shoot)
                    if player.gun_level == 2:
                        s1, s2 = player.shoot2(BLACK, bullet_img, fire_sound)
                        group_sprites.add(s1, s2)
                        group_bullets.add(s1, s2)
                    if player.gun_level >= 3:
                        s1, s2, s3 = player.shoot3(BLACK, bullet_img, fire_sound)
                        group_sprites.add(s1, s2, s3)
                        group_bullets.add(s1, s2, s3)

        # 更新遊戲
        group_sprites.update()  # 去執行 group 裡面所有 sprite 的 update() 函式
        
        hits = pygame.sprite.groupcollide(group_rocks, group_bullets, True, True) # 判斷子彈與石頭碰撞，以字典紀錄
        for hit in hits:
            random.choice(rock_explosion_sound).play()
            explosion = Explosion(expl_imgs, hit.rect.center, 0)
            group_sprites.add(explosion)
            cal_points.add_point(hit.width)
            create_rocks(group_sprites, group_rocks, group_potato, rock_imgs)

        gets = pygame.sprite.groupcollide(group_potato, group_bullets, True, True) # 判斷子彈與馬鈴薯碰撞
        for get in gets:
            random.choice(rock_explosion_sound).play()
            explosion = Explosion(expl_imgs, get.rect.center, 0)
            group_sprites.add(explosion)
            cal_points.add_point(get.width)
            if random.random() > 0:
                treasure = Treasures(BLACK, WIDTH, HEIGHT, get.rect.center, treasure_imgs)
                group_sprites.add(treasure)
                group_treasures.add(treasure)
            create_rocks(group_sprites, group_rocks, group_potato, rock_imgs)

        eats = pygame.sprite.spritecollide(player, group_treasures, True)  # 判斷 player 與補誤的碰撞 
        for eat in eats:
            if eat.treasure_type == 0:
                heal_sound.play()
                player.plot_add_hp()
            elif eat.treasure_type == 1:
                levelup_sound.play()
                player.level_up()

        collisions = pygame.sprite.spritecollide(player, group_rocks, True, pygame.sprite.collide_circle)  # 判斷 player 與石頭碰撞，以圓形作判斷 
        for collision in collisions:
            processing = player.cal_damage(collision.radius, processing)
            if processing == False:
                player_explosion = Explosion(player_expl_imgs, player.rect.center, 2)
                death_sound.play()
                group_sprites.add(player_explosion)
                processing = player.end_or_conti(processing)
            random.choice(rock_explosion_sound).play()
            explosion = Explosion(expl_imgs, collision.rect.center, 1)
            group_sprites.add(explosion)
            create_rocks(group_sprites, group_rocks, group_potato, rock_imgs)
        
        collisions = pygame.sprite.spritecollide(player, group_potato, True, pygame.sprite.collide_circle)  # 判斷 player 與石頭碰撞，以圓形作判斷 
        for collision in collisions:
            processing = player.cal_damage(collision.radius, processing)
            if processing == False:
                player_explosion = Explosion(player_expl_imgs, player.rect.center, 2)
                death_sound.play()
                group_sprites.add(player_explosion)
                processing = player.end_or_conti(processing)
            random.choice(rock_explosion_sound).play()
            explosion = Explosion(expl_imgs, collision.rect.center, 1)
            group_sprites.add(explosion)
            create_rocks(group_sprites, group_rocks, group_potato, rock_imgs)
            
        if player.lives == 0 and not(player_explosion.alive()):
            processing = True
            show_init_screen = True

        # 畫面顯示
        screen.blit(background,(0,0))
        group_sprites.draw(screen)  # 將 group_sprites 內的物件畫在螢幕上
        cal_points.write_points()
        player.plot_hp()
        player.plot_lives()
        pygame.display.update()

    pygame.quit()


def show_init(screen, font, clock, background):
    screen.blit(background,(0,0))
    write_text(screen, "SPACE GAME", font, 60, WIDTH/2, HEIGHT/5)
    write_text(screen, "<--,-->  方向鍵  移動飛船", font, 30, WIDTH/2, HEIGHT/2)
    write_text(screen, "空白鍵  發射子彈", font, 30, WIDTH/2, HEIGHT/2 + 50)
    write_text(screen, "案任意鍵開始", font, 20, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    wait = True
    while wait:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                wait = False
                return False


def write_text(screen, text, font, size, x, y):
    out_font = pygame.font.Font(font, size)
    text_surface = out_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    screen.blit(text_surface, text_rect)


def create_rocks(group_sprites, group_rocks, group_potato, rock_imgs):
    t = random.choice(list(range(8)))
    if t == 7:
        rock_img = rock_imgs[t]
        potato_rock = Rocks(BLACK, WIDTH, HEIGHT, rock_img) # 建立障礙物物件
        group_sprites.add(potato_rock)                      # 將 rock 物件加入群組
        group_potato.add(potato_rock)
    else:
        rock_img = rock_imgs[t]
        rock = Rocks(BLACK, WIDTH, HEIGHT, rock_img)      # 建立障礙物物件
        group_sprites.add(rock)                           # 將 rock 物件加入群組
        group_rocks.add(rock)


if __name__ == "__main__":
    main()
