import pygame, sys, time, random

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120

#configurações de dificuldade
initial_difficulty = 10
max_difficulty = 60
difficulty = initial_difficulty

#tamanho da janela
frame_size_x = 720
frame_size_y = 480

#verifica se há erros encontrados
check_errors = pygame.init()
if check_errors[1] > 0:
    print(
        f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

#inicializar janela do jogo
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

#cores (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
purple = pygame.Color(255, 0, 255)
pink = pygame.Color(255, 105, 180)
#cor das frutas especiais

#carregar imagens
background_image = pygame.image.load('2.png')
#food_image = pygame.image.load('1.png') - não funcionou com png
#food_image = pygame.transform.scale(food_image,(250, 250))  #redimensiona a imagem da comida

#controlador do FPS
fps_controller = pygame.time.Clock()

#variáveis do jogo
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

special_food_pos = [
    random.randrange(1, (frame_size_x // 10)) * 10,
    random.randrange(1, (frame_size_y // 10)) * 10
]
special_food_spawn = False

direction = 'RIGHT'
change_to = direction
score = 0
fruits_eaten = 0
special_fruit_effect_duration = 2  #duração do efeito intermitente em segundos
special_fruit_active = False
special_fruit_end_time = 1

#Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('FIM DE JOGO', True,
                                       pygame.Color(128, 0, 128))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x // 2, frame_size_y // 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, purple, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


#pontuação
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x // 10, 15)

    else:
        score_rect.midtop = (frame_size_x // 2.05, int(frame_size_y / 1.25))
    game_window.blit(score_surface, score_rect)


#lógica principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    #pra cobra nao se mover na direção oposta instantaneamente
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    #movimentação da cobra
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    #mecanismo de crescimento da cobra
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

   #spawn de fruta
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

  #comida
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    #detecção de colisão
    #verifica se a cobra bate nas paredes
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()
        
    #verifica se a cobra colide consigo mesma
    for block in snake_body[1:]:  # Start from the second block (the head is at index 0)
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    #verifica se a cobre colide com a comida
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 0
        fruits_eaten += 1
        food_spawn = False
        if fruits_eaten % 2 == 0:
            difficulty = min(difficulty + 5, max_difficulty)
        if fruits_eaten % 2 == 0:  #gera frutas especiais a cada 5 frutas normais comidas #################
            special_food_spawn = True
        if special_food_spawn and snake_pos[0] == special_food_pos[0] and snake_pos[1] == special_food_pos[1]:
            score += 2  #frutas especiais dão pontos em dobro
            fruits_eaten += 1
            special_food_spawn = False
            special_fruit_active = True
            special_fruit_end_time = time.time() + special_fruit_effect_duration

    if not food_spawn:
        food_pos = [
            random.randrange(1, (frame_size_x // 10)) * 10,
            random.randrange(1, (frame_size_y // 10)) * 10
        ]
        food_spawn = True

    if special_food_spawn and not special_fruit_active:
        special_food_pos = [
            random.randrange(1, (frame_size_x // 10)) * 10,
            random.randrange(1, (frame_size_y // 10)) * 10
        ]
        special_food_spawn = True

    game_window.blit(background_image, (0, 0))
    for pos in snake_body:
        pygame.draw.rect(game_window, yellow, #cor da cobra
                         pygame.Rect(pos[0], pos[1], 10, 10))

    #cor e tamanho da maçã
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10)) 

    if special_food_spawn:
        pygame.draw.rect(
            game_window, pink,
            pygame.Rect(special_food_pos[0], special_food_pos[1], 30, 30))

    if special_fruit_active:
        if time.time() > special_fruit_end_time:
            special_fruit_active = False
        else:
            if int(time.time() * 10) % 2 == 0:
                overlay = pygame.Surface((frame_size_x, frame_size_y))
                overlay.set_alpha(128)  #transparência
                game_window.blit(overlay, (0, 0))

    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(difficulty)
