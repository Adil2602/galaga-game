from typing import Any
import pygame
import sys
import random
from pygame.sprite import Sprite

pygame.init()



WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaga")

# sound = pygame.mixer.Sound('/home/adil/Desktop/game/lazer-lazernyiy-vyistrel-27908.mp3')

# Спрайты для игры (изображения)
player = pygame.image.load('/home/adil/Desktop/game/images/spaceship.png')
enemy = pygame.image.load('/home/adil/Desktop/game/images/ufo.png')
bullet = pygame.image.load('/home/adil/Desktop/game/images/bullet.png')
background = pygame.image.load('/home/adil/Desktop/game/images/background.jpg')

# Создаем игрока
class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2 ,HEIGHT - 50)
        
    def update(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5 
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5 
        
# Создаем врага
class Enemy(Sprite):
    def __init__(self, level=1) -> None:
        super().__init__()
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,WIDTH -self.rect.width)
        self.rect.y = random.randint(-100, - 50)
        self.speed = random.randint(0, 1) + level
        self.horizontal_direction = random.choice([-1, 1])

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-100, -50)
            self.rect.x = random.randint(0,WIDTH -self.rect.width)
            self.speed = random.randint(0, 1)
            self.horizontal_direction = random.choice([-1, 1])
        self.rect.x += self.horizontal_direction
        if self.rect.left > 0:
            self.rect.x -= 5
        if self.rect.right < WIDTH:
            self.rect.x += 5

        self.rect.x += self.speed * self.horizontal_direction
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.horizontal_direction = -self.horizontal_direction

level = 1  # начальный уровень
enemy_spawn_timer = pygame.time.get_ticks() + 5000
            
# Создаем пули
class Bullet(Sprite):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.image = bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    
    def update(self) -> None:
        self.rect.y -= 20
        if self.rect.y < 0:
            self.kill()
            

all_sprite = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()



player_1 = Player()
all_sprite.add(player_1)


# Цикл для создания врагов
for _ in range(10):
    enemy_1 = Enemy()  # Уровень по умолчанию равен 1
    all_sprite.add(enemy_1)
    enemies.add(enemy_1)

    
# Подсчёт очков
level = 1
score = 0
clock = pygame.time.Clock()
running = True
enemy_spawn_timer = pygame.time.get_ticks() + 5000
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_1 = Bullet(player_1.rect.centerx,player_1.rect.top)
                all_sprite.add(bullet_1)
                bullets.add(bullet_1)
                # sound.play()
    now = pygame.time.get_ticks()
    if now - enemy_spawn_timer > 2000:
        new_enemy = Enemy(level)
        all_sprite.add(new_enemy)
        enemies.add(new_enemy)
        enemy_spawn_timer = now

    all_sprite.update()

    hits = pygame.sprite.groupcollide(enemies,bullets,True,True)
    for hit in hits:
        score += 1
        

    hits_player = pygame.sprite.spritecollide(player_1,enemies,True)
    if hits_player: 
        running = False
        

    now = pygame.time.get_ticks()
    if now - enemy_spawn_timer > 2000:
        new_enemy = Enemy()
        all_sprite.add(new_enemy)
        enemies.add(new_enemy)
        enemy_spawn_timer = now
        
        
    screen.blit(background,(0, 0))
    all_sprite.draw(screen)


    front = pygame.font.Font(None, 36)
    text = front.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    font = pygame.font.Font(None, 36)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (10, 50))

    # После завершения игрового цикла
    if score >= 10:  # Задайте нужное вам количество очков для перехода на следующий уровень
        level += 1
        score = 0  # Сброс счетчика очков

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
sys.exit()
