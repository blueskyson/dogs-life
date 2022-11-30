import pygame
from enum import Enum

class DogState(Enum):
    RUN = 'run'
    JUMP = 'jump'

class Dog:
    default_x = 80
    default_y = 285
    default_jump_velocity = 9.5

    def __init__(self):
        self.width = 87
        self.height = 54
        self.scale = 2
        self.running = []
        for i in range(1, 7):
            img = pygame.image.load(f"assets/dog/Shepherd_walk_{i}.png")
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (self.width * self.scale, self.height * self.scale))
            self.running.append(img)
        self.jumping = []
        for i in range(1, 6):
            img = pygame.image.load(f"assets/dog/Shepherd_run_{i}.png")
            img = pygame.transform.flip(img, True, False)
            img = pygame.transform.scale(img, (self.width * self.scale, self.height * self.scale))
            self.jumping.append(img)

        self.x = self.default_x
        self.y = self.default_y
        self.state = DogState.RUN
        self.step = 0
        self.img = self.running[0]
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.run_speed = 2
        self.jump_speed = 4
        self.jump_velocity = self.default_jump_velocity

    def update(self, userInput):
        if self.state == DogState.RUN:
            self.run()
        elif self.state == DogState.JUMP:
            self.jump()
        self.rect = pygame.Rect(self.x, self.y, self.width * self.scale, self.height * self.scale)
        
        if userInput[pygame.K_UP] and self.state != DogState.JUMP:
            self.state = DogState.JUMP
            self.step = 0
    
    def run(self):
        self.img = self.running[self.step // self.run_speed]
        self.step += 1
        if self.step >= len(self.running) * self.run_speed:
            self.step = 0
    
    def jump(self):
        self.img = self.jumping[self.step // self.jump_speed]
        self.step += 1
        if self.step >= len(self.jumping) * self.jump_speed:
            self.step = 0

        delta = self.jump_velocity * 4
        if self.jump_velocity < 0 and self.y - delta > self.default_y:
            self.y = self.default_y
            self.jump_velocity = self.default_jump_velocity
            self.state = DogState.RUN
            self.step = 0
        else:
            self.y -= delta
            self.jump_velocity -= 0.8