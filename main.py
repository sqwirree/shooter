from pygame import *
from random import randint

# ! Основные переменные для проекта
FPS = 60
GAME_FINISHED, GAME_RUN = False, True
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480
CLOCK = time.Clock()

# ! Создание окна игры
WINDOW = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display.set_caption("Shooter")

mixer.init()
font.init()

mixer.music.load("music.mp3")
mixer.music.play()

fire_sound = mixer.Sound("fire_.mp3")
loose_sound = mixer.Sound("loose.mp3")
pooled_sound = mixer.Sound("pooled.mp3")
win_sound = mixer.Sound("pobeda.mp3")
loosed_sound = mixer.Sound("loosed.mp3")

KILLS, LOST = 0,0

score_font = font.SysFont("Arial", 72, True)
main_font = font.SysFont("Arial", 72, True)



# ! Классы
class GameSprite(sprite.Sprite):
    def __init__(self, img, position, size, speed):
        super().__init__()
        
        self.image = transform.smoothscale(
            image.load(img),
            size
        )
        
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        
        self.speed = speed
        self.width, self.height = size
        
    def reset(self):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    fire_delay = FPS * 0.25
    fire_timer = fire_delay
    can_fire = True
    def update(self):

        if not self.can_fire:
            if self.fire_timer > 0:
                self.fire_timer -= 1
            else:
                self.fire_timer = self.fire_delay
                self.can_fire = True
        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[K_d]:
            if self.rect.x < WINDOW_WIDTH - self.width:
                self.rect.x += self.speed

        if keys[K_SPACE] and self.can_fire:
            self.fire()
            self.can_fire = False
            mixer.Sound.play(fire_sound)
    def fire(self):
        new_bullet = Bullet(img="fire.png",
                            position=(self.rect.centerx - 4, self.rect.y),
                                      size=(8,8),
                                      speed=10)
        bullets_group.add(new_bullet)
        

            
            
class Enemy(GameSprite):
    def update(self):
        global LOST

        self.rect.y += self.speed

        if self.rect.y >= WINDOW_HEIGHT or sprite.collide_rect(self, player):
            LOST += 1
            mixer.Sound.play(loose_sound)
            self.kill()

class Bullet(GameSprite):
    def update(self):
        global KILLS
        self.rect.y -= self.speed
        if sprite.spritecollide(self, enemy_group, True):
            KILLS += 1
            mixer.Sound.play(pooled_sound)
            self.kill()
        if self.rect.y <= 0:
            self.kill()


bg = GameSprite(img="bg.png",
                position=(0, 0),
                size=(WINDOW_WIDTH, WINDOW_HEIGHT),
                speed=0)
player = Player(img="player.png",
                position=(5, WINDOW_HEIGHT-64),
                size=(80, 80),
                speed=7)

walls_group = sprite.Group()
enemys_spawn_delay = FPS
enemys_spawn_timer=enemys_spawn_delay
enemy_group=sprite.Group()
bullets_group=sprite.Group()




# ! Игровой цикл
while GAME_RUN:
    
    for ev in event.get():
        if ev.type == QUIT:
            GAME_RUN = False  
    bg.reset()
    player.reset()
    enemy_group.draw(WINDOW)
    bullets_group.draw(WINDOW)

    kills = score_font.render("kills:"+ str(KILLS), True, (0, 128, 0))
    lost = score_font.render("lost:" + str(LOST), True, (0, 128, 0))

    if KILLS >= 15:
        screen_text = main_font.render("Ті победил", True, (0, 255, 0))
        WINDOW.blit(screen_text, (WINDOW_WIDTH / 2 - screen_text.get_width() / 2,
                                  WINDOW_HEIGHT / 2 - screen_text.get_height() / 2))
        mixer.Sound.play(win_sound)
        GAME_FINISHED = True

    if LOST >= 1:
        screen_text = main_font.render("Ті проиграл                   ", True, (0, 255, 0))
        WINDOW.blit(screen_text, (WINDOW_WIDTH / 2 - screen_text.get_width() / 2,
                                  WINDOW_HEIGHT / 2 - screen_text.get_height() / 2))
        mixer.Sound.play(loosed_sound)
        GAME_FINISHED = True
    WINDOW.blit(kills, (5, 5))
    WINDOW.blit(lost, (5, 60))
    # ? Логика игры (работает пока не проиграем/выиграем)
    if not GAME_FINISHED:
        player.update()
        enemy_group.update()
        bullets_group.update()
        if enemys_spawn_timer > 0:
            enemys_spawn_timer -= 1
        else:
            new_enemy = Enemy(img="enemy.png",
                position=(randint(100, WINDOW_WIDTH-100), -100),
                size=(80, 80),
                speed=randint(2, 7))
            enemy_group.add(new_enemy)
            enemys_spawn_timer = enemys_spawn_delay
    display.update()
    CLOCK.tick(FPS)