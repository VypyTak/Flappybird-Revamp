import pygame
import random
 
pygame.init()
 
width, height = 600, 800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Grumpy Bird")
 
clock = pygame.time.Clock()
#RGB
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
 
font = pygame.font.Font(None, 36)
 
#load images
bird_jump_img = pygame.image.load("jump.png").convert_alpha()
bird_fall_img = pygame.image.load("fall.png").convert_alpha()
bird_rect = bird_fall_img.get_rect()

background = pygame.image.load("bg.jpg").convert()
background_x = 0
 
bird_x = 50
bird_y = height // 2
bird_velocity = 0
gravity = 0.5
jump = -10
 
pipe_width = 70
pipe_gap = 200
pipe_velocity = -5
pipe_frequency = 1500
 
score =0
start_time = pygame.time.get_ticks()
 
pipes = []
pipe_timer = 0
 
def create_pipe():
    pipe_height = random.randint(100, height -100 - pipe_gap)
    top_pipe = pygame.Rect(width, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(width, pipe_height + pipe_gap, pipe_width, height - pipe_height - pipe_gap)
    pipes.append(top_pipe)
    pipes.append(bottom_pipe)
 
def wait_for_key():
    waiting = True
    while waiting:
        screen.fill(WHITE)
        screen.blit(background, (background_x, 0))
        bird_rect.topleft = (bird_x, bird_y)
        screen.blit(bird_fall_img, bird_rect.topleft)
        message = font.render("Press any key to start", True, BLACK)
        screen.blit(message, (width // 2 - message.get_width() //2, height // 2 - message.get_height() //2))
        pygame.display.flip()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                waiting = False

def gameover():
    waiting = True
    while waiting:
        message = font.render("GAME OVER, Final score {score}", True, BLACK)
        screen.blit(message, (width // 2 - message.get_width() //2, height // 2 - message.get_height() //2))
        pygame.display.flip()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                waiting = False
 
running = True
wait_for_key()

while running:
    screen.fill(WHITE)
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + background.get_width(), 0))
    background_x -= 1

    if background_x <= -background.get_width():
        background_x = 0
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump
 
    bird_velocity += gravity
    bird_y += bird_velocity
    bird_rect.topleft = (bird_x, bird_y)
 
    if bird_velocity < 0:
        bird_img = bird_jump_img
    else:
        bird_img = bird_fall_img
 
    current_time = pygame.time.get_ticks()
    if current_time - pipe_timer > pipe_frequency:
        create_pipe()
        pipe_timer = current_time
 
    for pipe in pipes:
        pipe.x += pipe_velocity
        if pipe.colliderect(bird_rect):
            running = False
 
    pipes = [pipe for pipe in pipes if pipe.right > 0]
 
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)
 
    screen.blit(bird_img, bird_rect.topleft)
 
    if bird_y < 0 or bird_y > height:
        running = False
 
    score = (pygame.time.get_ticks() - start_time) // 1000
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10,10))
 
    pygame.display.flip()
    clock.tick(60)
 
gameover()
pygame.quit()
 