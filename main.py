import sys
import random
import pygame
from pygame.locals import QUIT
from sprites import Dog
pygame.init()

# global settings
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FONT = pygame.font.Font("freesansbold.ttf", 30)
GAME_SPEED = 20
REFRESH_INTERVAL = 30

DOG = Dog()
CLOUD = pygame.image.load("assets/other/Cloud.png")
GROUND = pygame.image.load("assets/other/Track.png")
CACTUSES = []
for i in range(1, 4):
    CACTUSES.append(pygame.image.load(f"assets/cactus/SmallCactus{i}.png"))
    CACTUSES.append(pygame.image.load(f"assets/cactus/LargeCactus{i}.png"))

# start game
def play():
    # init game states
    global ground_x, ground_y, score, cloud_x, cloud_y
    global frame_count, cactus, cactus_x, cactus_rect
    clock = pygame.time.Clock()
    score = 0
    ground_x = 0
    ground_y = 380
    cloud_y = random.randint(100, 250)
    cloud_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
    cactus = random.choice(CACTUSES)
    cactus_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
    cactus_rect = (cactus_x, 0, 0, 0)
    frame_count = 0

    def render_ground():
        global ground_x, ground_y
        img_width = GROUND.get_width()
        SCREEN.blit(GROUND, (ground_x, ground_y))
        SCREEN.blit(GROUND, (img_width + ground_x, ground_y))
        if ground_x <= -img_width:
            SCREEN.blit(GROUND, (img_width + ground_x, ground_y))
            ground_x = 0
        pygame.draw.rect(SCREEN, (240, 134, 80), \
            (0, ground_y + GROUND.get_height(), SCREEN_WIDTH, SCREEN_HEIGHT - (ground_y + GROUND.get_height())))
        ground_x -= GAME_SPEED

    def render_score():
        global score
        score_surface = FONT.render("Score: " + str(score), True, (0, 0, 0))
        score += 1
        SCREEN.blit(score_surface, (800, 40))

    def render_dog(userInput):
        SCREEN.blit(DOG.img, (DOG.x, DOG.y))
        DOG.update(userInput)
    
    def render_cloud():
        global cloud_x, cloud_y
        SCREEN.blit(CLOUD, (cloud_x, cloud_y))
        cloud_x -= 5
        if cloud_x < -150:
            cloud_y = random.randint(100, 250)
            cloud_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
    
    def render_cactus():
        global cactus, cactus_x, cactus_rect
        cactus_rect = (cactus_x, ground_y - (cactus.get_height() - 15), cactus.get_width(), cactus.get_height())
        SCREEN.blit(cactus, cactus_rect)
        cactus_x -= (20 + frame_count // 100)
        if cactus_x < -150:
            cactus_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
            cactus = random.choice(CACTUSES)

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        SCREEN.fill((135, 206, 235))
        render_cloud()
        render_score()
        render_dog(pygame.key.get_pressed())
        render_cactus()
        render_ground()
        clock.tick(REFRESH_INTERVAL)
        pygame.display.update()
        frame_count += 1

        if DOG.rect.colliderect(cactus_rect):
            pygame.time.delay(2000)
            break

# main
pygame.display.set_caption("dog's life")
while True:
    SCREEN.fill((255, 255, 255))
    menu_img = DOG.jumping[4]
    SCREEN.blit(menu_img, (SCREEN_WIDTH // 2 - menu_img.get_width() // 2, SCREEN_HEIGHT // 2 - 140))

    text = FONT.render("Press any Key to Start", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, textRect)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            play()