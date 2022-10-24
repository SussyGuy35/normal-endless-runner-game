import pygame
from sys import exit
from random import randint
#pyinstaller splash screen
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    print("Not using pyinstaller splash screen")
#func
def display_score():
    current_time = (int((pygame.time.get_ticks() - start_time)/1000) - start_time)*2
    score_surf = font0.render(f'{current_time}m',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    pygame.draw.rect(screen,'#c0e8ec',pygame.Rect(score_rect.x-2, score_rect.y-2,score_rect.width+2,score_rect.height-5))
    screen.blit(score_surf,score_rect)
    return current_time
def obstacle_movement(obstacle_list):
    global speed
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= int(speed)
            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.right >= 0]    
        return obstacle_list  
    else: return []    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True        
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        #jump
        player_surf = player_jump
    else:
        #walk
        player_index += 0.1
        if player_index > len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        output_path = os.path.join(base_path, relative_path)
    except Exception:
        output_path = relative_path

    return output_path
# init thing
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
width = 800
height = 400
framerate = 60
title = 'Just a normal endless runner game'
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()
icon = pygame.image.load(resource_path('graphics/icon.ico'))
pygame.display.set_icon(icon)
bg_music = pygame.mixer.Sound(resource_path('audio/music.mp3'))
bg_music.set_volume(0.8)
bg_music.play(loops = -1)
font0 = pygame.font.Font(resource_path('font/Pixeltype.ttf'), 50)
game_active = False
start_time = 0
jump_key = 0
score = 0
dead_sound_played = False
speed = 5
spw_spd = 1500
last_spw_x = randint(width+100,width+300) 

sky_surf = pygame.image.load(resource_path('graphics/Sky.png')).convert()
ground_surf = pygame.image.load(resource_path('graphics/ground.png')).convert()
ground_x = width
jump_sound = pygame.mixer.Sound(resource_path('audio/jump.wav'))
jump_sound.set_volume(0.7)
dead_sound = pygame.mixer.Sound(resource_path('audio/dead.wav'))
dead_sound.set_volume(0.7)
ground_sound = pygame.mixer.Sound(resource_path('audio/ground.wav'))
ground_sound.set_volume(0.9)
# obstacles
# snail
snail_frame_1 = pygame.image.load(resource_path('graphics/snail/snail1.png')).convert_alpha()
snail_frame_2 = pygame.image.load(resource_path('graphics/snail/snail2.png')).convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
#fly
fly_frame_1 = pygame.image.load(resource_path('graphics/fly/fly1.png')).convert_alpha()
fly_frame_2 = pygame.image.load(resource_path('graphics/fly/fly2.png')).convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list=[]

player_walk_1 = pygame.image.load(resource_path('graphics/player/player_walk_1.png')).convert_alpha()
player_walk_2 = pygame.image.load(resource_path('graphics/player/player_walk_2.png')).convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load(resource_path('graphics/player/jump.png')).convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_vsp = 0
# intro screen
player_stand = pygame.image.load(resource_path('graphics/player/player_stand.png')).convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = font0.render('Just a normal endless runner game',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = font0.render('Press space!',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,340))

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,spw_spd)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

# main loop
while True:
    # now u can close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    jump_key = framerate*0.1
                elif event.key == pygame.K_DOWN and player_rect.bottom < 300:
                    ground_sound.play()
                    player_vsp = max(player_vsp,35)
            if event.type == obstacle_timer:
                if spw_spd > 500: speed += 0.1
                if randint(0,2):
                    if last_spw_x >= width+100: 
                        spw_x = randint(width+200,width+300) 
                        last_spw_x = spw_x
                    else: 
                        spw_x = randint(width+100,width+300)
                        last_spw_x = spw_x
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (spw_x,300)))
                else:  
                    if last_spw_x >= width+100: 
                        spw_x = randint(width+200,width+300) 
                        last_spw_x = spw_x
                    else: 
                        spw_x = randint(width+100,width+300)
                        last_spw_x = spw_x
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (spw_x,210)))
                spw_spd = max(500,spw_spd - 25)
                pygame.time.set_timer(obstacle_timer,spw_spd)   
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]    

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    obstacle_rect_list=[]
                    speed = 5
                    spw_spd = 1500
                    jump_key = 0
                    player_rect.midbottom = (80,300)
                    player_vsp = 0
                    start_time = int((pygame.time.get_ticks() - start_time)/1000)
                    dead_sound_played = False
                    game_active = True
               
    # Game
    if game_active:
        jump_key -= 1
        if jump_key <0: jump_key = 0
        screen.blit(sky_surf,(0,0))
        ground_x -= speed/2
        if ground_x <= 0: ground_x = width
        screen.blit(ground_surf,(ground_x - width,300))
        screen.blit(ground_surf,(ground_x,300))
        score = display_score()    
      
        # player
        player_vsp += 1
        player_rect.y+=player_vsp
        if player_rect.bottom > 300: player_rect.bottom = 300
        if jump_key >0:
            if player_rect.bottom >= 300: 
                jump_sound.play()
                player_vsp = -20
                jump_key = 0
        player_animation()        
        screen.blit(player_surf,player_rect)
        
        # obstacles movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        # collision
        game_active = collisions(player_rect,obstacle_rect_list)
    # Menu
    else:
        if not dead_sound_played and score != 0: 
            dead_sound.play()
            dead_sound_played = True
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        score_message = font0.render(f'You just run {score}m!',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)
        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)
    # update the display
    pygame.display.update()
    clock.tick(framerate)