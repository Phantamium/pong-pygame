import pygame
import random

pygame.init() #boots all of them up at once (all the subsystems that is in pygame)

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

#define some colors
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
GREEN  = (0,   200, 100)
PURPLE = (120, 80,  220)

#idk what these do yet...
left_y  = 250
right_y = 250
ball_x = 295
ball_y = 295
ball_vx = -4   # velocity: moves 4 pixels right every frame
ball_vy = -3   # velocity: moves 3 pixels down every frame
left_score = 0
right_score = 0
prev_ball_x = ball_x   # removes the problem of tunneling (ball passing through the paddle at high pixel speeds)

font = pygame.font.SysFont("monospace", 64, bold=True)

#game loop
running = True
while running:

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    #left-paddle (W and S)
    if keys[pygame.K_w] and left_y > 0:
        left_y -= 10
    if keys[pygame.K_s] and left_y < 520:
        left_y += 10
    
    # Right paddle — arrow keys
    if keys[pygame.K_UP] and right_y >0:
        right_y -= 10
    if keys[pygame.K_DOWN] and right_y < 520:
        right_y += 10
    
    # Move the ball
    ball_x += ball_vx
    ball_y += ball_vy

    # Bounce off top and bottom walls
    if ball_y <= 0 or ball_y >= 590:
        ball_vy *= -1

    # Ball goes off left or right — reset to center
    if ball_x < 0:
        right_score += 1
        ball_x = 395
        ball_y = 295
        ball_vy = random.choice([-3, -2, -1, 1, 2, 3])
        ball_vx = -4
    if ball_x > 800:    
        left_score += 1
        ball_x = 395
        ball_y = 295
        ball_vy = random.choice([-3, -2, -1, 1, 2, 3])
        ball_vx = 4
    
    # ball hits paddle
    # if (((ball_x >= 36) and (ball_x <= 46)) and ((ball_y > (left_y)) and (ball_y < (left_y + 80)))) or (((ball_x >= 754) and (ball_x <= 762)) and ((ball_y > (right_y)) and (ball_y < (right_y + 80)))):
    #     ball_vx *= -1

     # Left paddle — did ball cross x=42 from right to left?
    if prev_ball_x >= 42 and ball_x <= 42 and (left_y < ball_y < left_y + 80):
        ball_x = 42
        ball_vx *= -1.2
        if abs(ball_vx) > 15:
            ball_vx = 15

    # Right paddle — did ball cross x=758 from left to right?
    if prev_ball_x <= 758 and ball_x >= 758 and (right_y < ball_y < right_y + 80):
        ball_x = 758
        ball_vx *= -1.2
        if abs(ball_vx) > 15:
            ball_vx = -15

    #draw
    screen.fill(BLACK)

    # Left paddle
    pygame.draw.rect(screen, GREEN, (30, left_y, 12, 80))

    # Right paddle
    pygame.draw.rect(screen, PURPLE, (758, right_y, 12, 80))

    # Ball
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, 10, 10))

    #dashed line
    for y in range(0, 600, 20):
        pygame.draw.rect(screen, WHITE, (395, y, 10, 10))
        
    #prints the score
    left_text  = font.render(str(left_score),  True, GREEN)
    right_text = font.render(str(right_score), True, PURPLE)
    screen.blit(left_text,  (200, 20))
    screen.blit(right_text, (560, 20))

    if left_score == 10:
        break
    elif right_score == 10:
        break

    # pygame.draw.rect(surface, color, (x, y, width, height))
    pygame.display.flip()

    #tick - will experiment with it later~      
    clock.tick(60)


 
pygame.quit()