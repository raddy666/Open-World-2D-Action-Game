import pgzrun
import pygame
import os
import random
import math

os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH = 1500
HEIGHT = 800
TITLE = "BLACKTOP BLOOD"
CAMERA_ZOOM = 2.0
TILE_SIZE = 18
MAP_TILES_WIDTH = 200
MAP_TILES_HEIGHT = 150
MAP_WIDTH = MAP_TILES_WIDTH * TILE_SIZE
MAP_HEIGHT = MAP_TILES_HEIGHT * TILE_SIZE

camera_x = 0
camera_y = 0

              
music_system = {
    'bgmusic_volume': 0.4,    
    'hurt_volume': 0.7,       
    'die_volume': 0.3,          
    'carstart_volume': 0.4, 
    'drive_volume': 0.4,      
    'gameover_volume': 0.9, 
    'katana_volume': 0.7,      
    'rifle_volume': 0.8,      
    'magic_volume': 0.7,       
    'bossmagic_volume': 0.8, 
    'whip_volume': 0.8,     
    'carstart_playing': False, 
    'drive_channel': None   
}

            
game_state = {
    'alive': True,
    'death_timer': 0,
    'death_delay': 80,
    'in_car': False,
    'car_type': None,
    'car_angle': 0,
    'car_speed': 0,
    'game_started': False,  
    'show_start_menu': True 
}

              
player = Actor('idle')
player.x = 500
player.y = 500
player_walk_speed = 1
player_run_speed = 2

              
player_weapon = {
    'type': 'none', 
    'attacking': False,
    'attack_frame': 0,
    'attack_delay': 0,
    'shoot_animation_done': False  
}

                   
GUN_CONFIG = {
    'scale': 0.8,           
    'offset_x': 5,       
    'offset_y': 5,        
    'image': None     
}

               
bullets = []  

                      
BULLET_CONFIG = {
    'speed': 8,            
    'scale': 1.0,          
    'lifetime': 120    
}

            
npcs = []  
dead_bodies = []

                   
NPC_CONFIG = {
    'max_population': 200,       
    'walk_speed': 1.0,            
    'run_speed': 2.0,            
    'animation_speed': 8,        
    'decision_interval': 300,     
    'sidewalk_preference': 0.9,  
}

       
level_system = {
    'current_level': 0,  
    'completed_levels': [],  
    'active': False,  
    'red_lights': [
        {'x': 53 * TILE_SIZE, 'y': 50 * TILE_SIZE, 'level': 1, 'active': True},
        {'x': 150 * TILE_SIZE, 'y': 60 * TILE_SIZE, 'level': 2, 'active': False},
        {'x': 70 * TILE_SIZE, 'y': 127 * TILE_SIZE, 'level': 3, 'active': False}
    ]
}

               
player_health = {
    'current': 15,
    'max': 15
}

        
enemies = []
enemy_bullets = []  
enemy_magic = []    

                     
ENEMY_CONFIG = {

    'enemy1': {'health': 3, 'damage': 1, 'type': 'melee', 'attack_anim': 'slash', 'frame_size': 192},
    'enemy2': {'health': 3, 'damage': 1, 'type': 'melee', 'attack_anim': 'slash', 'frame_size': 64},
    'enemy3': {'health': 3, 'damage': 1, 'type': 'ranged', 'attack_anim': 'shoot', 'frame_size': 64},
    
    'enemy4': {'health': 6, 'damage': 2, 'type': 'melee', 'attack_anim': 'slash', 'frame_size': 192},
    'enemy5': {'health': 6, 'damage': 2, 'type': 'melee', 'attack_anim': 'slash', 'frame_size': 192},
    'enemy6': {'health': 6, 'damage': 2, 'type': 'magic', 'attack_anim': 'spellcast', 'frame_size': 64},
    
    'boss': {'health': 15, 'damage': 3, 'type': 'boss', 'attack_anim': 'slash', 'frame_size': 192}
}

ENEMY_SPRITESHEETS = {}

                   
start_menu_images = {}
button_rects = {}  

def load_all_sounds():
        sounds.bgmusic = pygame.mixer.Sound('music/bgmusic.mp3')
        sounds.hurt = pygame.mixer.Sound('music/hurt.mp3')
        sounds.die = pygame.mixer.Sound('music/die.mp3')
        sounds.carstart = pygame.mixer.Sound('music/carstart.mp3')
        sounds.drive = pygame.mixer.Sound('music/drive.mp3')
        sounds.gameover = pygame.mixer.Sound('music/gameover.mp3')
        sounds.katana = pygame.mixer.Sound('music/katana.mp3')
        sounds.rifle = pygame.mixer.Sound('music/rifle.mp3')
        sounds.magic = pygame.mixer.Sound('music/magic.mp3')
        sounds.bossmagic = pygame.mixer.Sound('music/bossmagic.mp3')
        sounds.whip = pygame.mixer.Sound('music/whip.mp3')
        
                     
        sounds.bgmusic.set_volume(music_system['bgmusic_volume'])
        sounds.hurt.set_volume(music_system['hurt_volume'])
        sounds.die.set_volume(music_system['die_volume'])
        sounds.carstart.set_volume(music_system['carstart_volume'])
        sounds.drive.set_volume(music_system['drive_volume'])
        sounds.gameover.set_volume(music_system['gameover_volume'])
        sounds.katana.set_volume(music_system['katana_volume'])
        sounds.rifle.set_volume(music_system['rifle_volume'])
        sounds.magic.set_volume(music_system['magic_volume'])
        sounds.bossmagic.set_volume(music_system['bossmagic_volume'])
        sounds.whip.set_volume(music_system['whip_volume'])


def play_bgmusic():
    try:
        sounds.bgmusic.play(loops=-1)  
    except:
        pass

def stop_all_sounds():
    pygame.mixer.stop()
    music_system['carstart_playing'] = False
    music_system['drive_channel'] = None

def load_start_menu_images():

        start_menu_images['background'] = pygame.image.load('images/startmenu.png')
        start_menu_images['start_normal'] = pygame.image.load('images/startbuttonnormal.png')
        start_menu_images['start_hover'] = pygame.image.load('images/startbuttonhover.png')
        start_menu_images['exit_normal'] = pygame.image.load('images/exitbuttonnormal.png')
        start_menu_images['exit_hover'] = pygame.image.load('images/exitbuttonhover.png')

menu_state = {
    'start_hover': False,
    'exit_hover': False
}
                    
ENEMY_FRAME_COUNTS = {
    'idle': 2,
    'walk': 9,
    'run': 8,
    'hurt': 6,
    'slash': 6,
    'shoot': 13,
    'spellcast': 7,
    'whip': 8  
}

BOSS_FRAME_COUNTS = {
    'idle': 2,
    'walk': 9,
    'hurt': 6,
    'slash': 8,  
    'spellcast': 7,
    'whip': 8
}

                    
ENEMY_FRAME_SIZES = {
    'enemy1': {'idle': 64, 'walk': 64, 'run': 64, 'hurt': 64, 'slash': 192},
    'enemy2': {'idle': 64, 'walk': 64, 'run': 64, 'hurt': 64, 'slash': 64},
    'enemy3': {'idle': 64, 'walk': 64, 'run': 64, 'hurt': 64, 'shoot': 64},
    'enemy4': {'walk': 64, 'hurt': 64, 'slash': 192},  
    'enemy5': {'walk': 64, 'hurt': 64, 'slash': 192},  
    'enemy6': {'idle': 64, 'walk': 64, 'hurt': 64, 'spellcast': 64},
    'boss': {'idle': 64, 'walk': 128, 'hurt': 64, 'slash': 192, 'spellcast': 64, 'whip': 192}
}

              
ENEMY_STATE_IDLE = 0
ENEMY_STATE_WALKING = 1
ENEMY_STATE_ATTACKING = 2
ENEMY_STATE_HURT = 3
ENEMY_STATE_DEAD = 4

                  
NPC_SPRITESHEETS = {}

            
NPC_STATE_IDLE = 0
NPC_STATE_WALKING = 1
NPC_STATE_RUNNING = 2
NPC_STATE_HURT = 3

def load_npc_spritesheets():

        for i in range(1, 10):
            NPC_SPRITESHEETS[f'npc{i}'] = {
                'idle': pygame.image.load(f'images/npc{i}idle.png'),
                'walk': pygame.image.load(f'images/npc{i}walk.png'),
                'run': pygame.image.load(f'images/npc{i}run.png'),
                'hurt': pygame.image.load(f'images/npc{i}hurt.png')
            }

def load_enemy_spritesheets():

        for i in range(1, 7):
            ENEMY_SPRITESHEETS[f'enemy{i}'] = {}
            animations = ['hurt']
            
            if i in [1, 2, 3]:  
                animations.extend(['idle', 'walk', 'run'])
            elif i in [4, 5]:  
                animations.extend(['walk']) 
            elif i == 6:  
                animations.extend(['idle', 'walk'])

                               
            if i in [1, 2, 4, 5]:  
                animations.append('slash')
            if i == 3:  
                animations.append('shoot')
            if i == 6:  
                animations.append('spellcast')
            
            for anim in animations:
                    ENEMY_SPRITESHEETS[f'enemy{i}'][anim] = pygame.image.load(f'images/enemy{i}{anim}.png')
        
                   
        ENEMY_SPRITESHEETS['boss'] = {}
        boss_anims = ['idle', 'walk', 'hurt', 'slash', 'spellcast', 'whip']
        for anim in boss_anims:
                ENEMY_SPRITESHEETS['boss'][anim] = pygame.image.load(f'images/boss{anim}.png')

def get_enemy_frame(enemy_type, state, direction, frame_index):
    if enemy_type not in ENEMY_SPRITESHEETS:
        return None
    
    state_map = {
        ENEMY_STATE_IDLE: 'idle',
        ENEMY_STATE_WALKING: 'walk',
        ENEMY_STATE_ATTACKING: None, 
        ENEMY_STATE_HURT: 'hurt',
        ENEMY_STATE_DEAD: 'hurt'
    }
    
    anim_name = state_map.get(state)
    
    if state == ENEMY_STATE_ATTACKING:
        config = ENEMY_CONFIG.get(enemy_type, {})
        anim_name = config.get('attack_anim', 'slash')
    
    if state == ENEMY_STATE_IDLE and enemy_type in ['enemy4', 'enemy5']:
        anim_name = 'walk'
        frame_index = 0  
    
    if not anim_name or anim_name not in ENEMY_SPRITESHEETS[enemy_type]:
        return None
    
    spritesheet = ENEMY_SPRITESHEETS[enemy_type][anim_name]
    
    frame_size = ENEMY_FRAME_SIZES[enemy_type].get(anim_name, 64)
    
    if anim_name == 'hurt':
        row = 0  
    else:
        row = DIRECTION_ROWS.get(direction, 0)

    frame_x = frame_index * frame_size
    frame_y = row * frame_size
    
    frame = spritesheet.subsurface(pygame.Rect(frame_x, frame_y, frame_size, frame_size))
    return frame


def spawn_enemy(enemy_type, spawn_x, spawn_y):
    for attempt in range(50):
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-100, 100)
        x = spawn_x + offset_x
        y = spawn_y + offset_y
        
        if is_on_walkable_surface(x, y) and not check_object_collision(x, y, radius=15):
            config = ENEMY_CONFIG[enemy_type]
            
            enemy = {
                'type': enemy_type,
                'x': float(x),
                'y': float(y),
                'direction': 'down',
                'state': ENEMY_STATE_IDLE,
                'current_frame': 0,
                'frame_delay': 0,
                'health': config['health'],
                'max_health': config['health'],
                'damage': config['damage'],
                'attack_cooldown': 0,
                'attack_range': 40 if config['type'] in ['melee', 'boss'] else 200,
                'attacking': False,
                'alive': True,
                'death_timer': 0
            }
            
            enemies.append(enemy)
            return True
    
    return False

def start_level(level_num):
                                
    level_system['current_level'] = level_num
    level_system['active'] = True

    spawn_light = None
    for light in level_system['red_lights']:
        if light['level'] == level_num:
            spawn_light = light
            break
    
    if not spawn_light:
        return
    
    spawn_x = spawn_light['x']
    spawn_y = spawn_light['y']
    
    enemies.clear()
    enemy_bullets.clear()
    enemy_magic.clear()
    
    if level_num == 1:
        for _ in range(2):
            spawn_enemy('enemy1', spawn_x, spawn_y)
            spawn_enemy('enemy2', spawn_x, spawn_y)
            spawn_enemy('enemy3', spawn_x, spawn_y)
    
    elif level_num == 2:
        for _ in range(3):
            spawn_enemy('enemy4', spawn_x, spawn_y)
            spawn_enemy('enemy5', spawn_x, spawn_y)
            spawn_enemy('enemy6', spawn_x, spawn_y)
    
    elif level_num == 3:
        spawn_enemy('enemy1', spawn_x, spawn_y)
        spawn_enemy('enemy2', spawn_x, spawn_y)
        spawn_enemy('enemy3', spawn_x, spawn_y)
        spawn_enemy('enemy4', spawn_x, spawn_y)
        spawn_enemy('enemy5', spawn_x, spawn_y)
        spawn_enemy('enemy6', spawn_x, spawn_y)
        spawn_enemy('boss', spawn_x, spawn_y)
    
    print(f"Level {level_num} started! Enemies spawned: {len(enemies)}")

def check_level_complete():
    if not level_system['active']:
        return
    
    alive_enemies = [e for e in enemies if e['alive']]
    
    if len(alive_enemies) == 0:
        level_num = level_system['current_level']
        level_system['completed_levels'].append(level_num)
        level_system['active'] = False
        
        for light in level_system['red_lights']:
            if light['level'] == level_num:
                light['active'] = False
        
        if level_num < 3:
            for light in level_system['red_lights']:
                if light['level'] == level_num + 1:
                    light['active'] = True
        
        print(f"Level {level_num} COMPLETE!")
        
        player_health['current'] = player_health['max']

def check_player_red_light_collision():
    if level_system['active']:
        return False
    
                       
    if 'light_cooldown' not in level_system:
        level_system['light_cooldown'] = 0
    
    if level_system['light_cooldown'] > 0:
        level_system['light_cooldown'] -= 1
        return False
    
    for light in level_system['red_lights']:
        if light['active'] and light['level'] not in level_system['completed_levels']:
            dx = player.x - light['x']
            dy = player.y - light['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < 30:  
                start_level(light['level'])
                level_system['light_cooldown'] = 180 
                return True
    
    return False

def check_enemy_car_collision(enemy):
    if not game_state['in_car']:
        return False
    
    enemy_radius = 15
    car_radius = 20
    
    dx = enemy['x'] - player.x
    dy = enemy['y'] - player.y
    distance = (dx * dx + dy * dy) ** 0.5
    
    if distance < (enemy_radius + car_radius):
        return True
    
    return False

def check_enemy_traffic_collision():
    for enemy in enemies[:]:
        if not enemy['alive']:
            continue
        
        for car in traffic_vehicles:
            dx = enemy['x'] - car['x']
            dy = enemy['y'] - car['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < 30 and car['speed'] > 1.5:
                damage_enemy(enemy, 2) 

def update_enemy(enemy):
    if not enemy['alive']:
                       
        enemy['death_timer'] += 1
        
        if enemy['current_frame'] < ENEMY_FRAME_COUNTS['hurt'] - 1:
            enemy['frame_delay'] += 1
            if enemy['frame_delay'] >= 8:
                enemy['frame_delay'] = 0
                enemy['current_frame'] += 1
        return
    
    if check_enemy_car_collision(enemy):
        damage_enemy(enemy, 1)  
        return
    
    dx = player.x - enemy['x']
    dy = player.y - enemy['y']
    distance = (dx * dx + dy * dy) ** 0.5
    
    if distance > 0:
        dir_x = dx / distance
        dir_y = dy / distance
    else:
        dir_x, dir_y = 0, 0

    if abs(dir_x) > abs(dir_y):
        enemy['direction'] = 'right' if dir_x > 0 else 'left'
    else:
        enemy['direction'] = 'down' if dir_y > 0 else 'up'
    
                     
    if enemy['attack_cooldown'] > 0:
        enemy['attack_cooldown'] -= 1

    if distance <= enemy['attack_range']:
        if enemy['attack_cooldown'] == 0 and not enemy['attacking']:
            if enemy['type'] == 'boss':
                attack_choice = random.choice(['slash', 'spellcast', 'whip'])
                config = ENEMY_CONFIG[enemy['type']]
                config['attack_anim'] = attack_choice 
            
            enemy['state'] = ENEMY_STATE_ATTACKING
            enemy['attacking'] = True
            enemy['current_frame'] = 0
            enemy['frame_delay'] = 0
            enemy['attack_cooldown'] = 90  
    else:
        if not enemy['attacking']:
            enemy['state'] = ENEMY_STATE_WALKING
            
            speed = 1.0  
            if enemy['type'] == 'boss':
                speed = 2.0 
            
            next_x = enemy['x'] + dir_x * speed
            next_y = enemy['y'] + dir_y * speed
            
                                      
            npc_collision = False
            for npc in npcs:
                if not npc['alive']:
                    continue
                dx_npc = next_x - npc['x']
                dy_npc = next_y - npc['y']
                if (dx_npc * dx_npc + dy_npc * dy_npc) ** 0.5 < 20:
                    npc_collision = True
                    break
            
            if not check_object_collision(next_x, next_y, radius=15) and not check_enemy_collision_with_others(enemy, next_x, next_y) and not npc_collision:
                enemy['x'] = next_x
                enemy['y'] = next_y
            else:
                test_x = enemy['x'] + dir_x * speed
                test_y = enemy['y']
                
                npc_collision_x = False
                for npc in npcs:
                    if not npc['alive']:
                        continue
                    dx_npc = test_x - npc['x']
                    dy_npc = test_y - npc['y']
                    if (dx_npc * dx_npc + dy_npc * dy_npc) ** 0.5 < 20:
                        npc_collision_x = True
                        break
                
                if not check_object_collision(test_x, test_y, radius=15) and not check_enemy_collision_with_others(enemy, test_x, test_y) and not npc_collision_x:
                    enemy['x'] = test_x
                else:
                    test_x = enemy['x']
                    test_y = enemy['y'] + dir_y * speed
                    
                    npc_collision_y = False
                    for npc in npcs:
                        if not npc['alive']:
                            continue
                        dx_npc = test_x - npc['x']
                        dy_npc = test_y - npc['y']
                        if (dx_npc * dx_npc + dy_npc * dy_npc) ** 0.5 < 20:
                            npc_collision_y = True
                            break
                    
                    if not check_object_collision(test_x, test_y, radius=15) and not check_enemy_collision_with_others(enemy, test_x, test_y) and not npc_collision_y:
                        enemy['y'] = test_y
    
    if enemy['attacking']:
        enemy['frame_delay'] += 1
        
        if enemy['frame_delay'] >= 8:
            enemy['frame_delay'] = 0
            enemy['current_frame'] += 1
            
            config = ENEMY_CONFIG[enemy['type']]
            attack_anim = config['attack_anim']
            
            if enemy['type'] == 'boss':
                max_frames = BOSS_FRAME_COUNTS.get(attack_anim, 6)
            else:
                max_frames = ENEMY_FRAME_COUNTS.get(attack_anim, 6)
            
            if enemy['current_frame'] in [2, 3, 4]:  
                if enemy['current_frame'] == 2:  
                    if config['type'] in ['melee', 'boss'] and attack_anim == 'slash':
                        try:
                            sounds.katana.play() 
                        except:
                            pass
                check_enemy_attack_hit_player(enemy)
            
            if enemy['current_frame'] == 6: 
                if config['type'] == 'ranged':
                    spawn_enemy_bullet(enemy)
                elif config['type'] == 'magic':
                    spawn_enemy_magic(enemy, homing=False)
                elif config['type'] == 'boss':
                    if attack_anim == 'spellcast':
                        spawn_enemy_magic(enemy, homing=True)
                    elif attack_anim == 'whip':
                        try:
                            sounds.whip.play()  
                        except:
                            pass
                        check_boss_whip_hit_player(enemy)
                    elif attack_anim == 'slash':  
                        try:
                            sounds.katana.play()  
                        except:
                            pass

            if enemy['current_frame'] >= max_frames:
                enemy['attacking'] = False
                enemy['state'] = ENEMY_STATE_IDLE
                enemy['current_frame'] = 0

    else:
        enemy['frame_delay'] += 1
        anim_speed = 8
        
        if enemy['state'] == ENEMY_STATE_IDLE:
            anim_speed = 24
        
        if enemy['frame_delay'] >= anim_speed:
            enemy['frame_delay'] = 0
            enemy['current_frame'] += 1
            
            if enemy['state'] == ENEMY_STATE_IDLE:
                max_frames = ENEMY_FRAME_COUNTS['idle']
            else:
                max_frames = ENEMY_FRAME_COUNTS['walk']
            
            if enemy['current_frame'] >= max_frames:
                enemy['current_frame'] = 0

def check_enemy_collision_with_others(enemy, new_x, new_y):
    for other in enemies:
        if other == enemy or not other['alive']:
            continue
        
        dx = new_x - other['x']
        dy = new_y - other['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < 15:
            return True
    
    return False

def damage_player(damage):
    player_health['current'] -= damage

    sounds.hurt.play()
    
    if player_health['current'] <= 0:
        player_health['current'] = 0
        
        player_animation['state'] = 'hurt'
        player_animation['current_frame'] = 0
        player_animation['frame_delay'] = 0
        
        game_state['alive'] = False
        game_state['death_timer'] = 0
        game_state['death_cause'] = 'enemy'  
        
        print("Player died from enemy!")

def check_enemy_attack_hit_player(enemy):
    if game_state['in_car']:
        return  
    
    dx = player.x - enemy['x']
    dy = player.y - enemy['y']
    distance = (dx * dx + dy * dy) ** 0.5
    
    if distance < 40:
        direction = enemy['direction']
        in_front = False
        
        if direction == 'right' and dx > 0 and abs(dy) < 30:
            in_front = True
        elif direction == 'left' and dx < 0 and abs(dy) < 30:
            in_front = True
        elif direction == 'down' and dy > 0 and abs(dx) < 30:
            in_front = True
        elif direction == 'up' and dy < 0 and abs(dx) < 30:
            in_front = True
        
        if in_front:
            damage_player(enemy['damage'])

def check_boss_whip_hit_player(enemy):
    if game_state['in_car']:
        return
    
    dx = player.x - enemy['x']
    dy = player.y - enemy['y']
    distance = (dx * dx + dy * dy) ** 0.5
    
    if distance < 60:  
        direction = enemy['direction']
        in_front = False
        
        if direction == 'right' and dx > 0 and abs(dy) < 40:
            in_front = True
        elif direction == 'left' and dx < 0 and abs(dy) < 40:
            in_front = True
        elif direction == 'down' and dy > 0 and abs(dx) < 40:
            in_front = True
        elif direction == 'up' and dy < 0 and abs(dx) < 40:
            in_front = True
        
        if in_front:
            damage_player(enemy['damage'])


def spawn_enemy_bullet(enemy):
    try:
        sounds.rifle.play() 
    except:
        pass
    direction = enemy['direction']
    
    start_x = enemy['x']
    start_y = enemy['y']
    
                        
    if direction == 'right':
        start_x += 20
    elif direction == 'left':
        start_x -= 20
    elif direction == 'up':
        start_y -= 20
    elif direction == 'down':
        start_y += 20
    
              
    velocities = {
        'right': (BULLET_CONFIG['speed'], 0),
        'left': (-BULLET_CONFIG['speed'], 0),
        'up': (0, -BULLET_CONFIG['speed']),
        'down': (0, BULLET_CONFIG['speed'])
    }
    
    vel_x, vel_y = velocities.get(direction, (0, 0))
    
    rotation_angles = {
        'right': 0,
        'left': 180,
        'up': 90,
        'down': -90
    }
    
    bullet = {
        'x': float(start_x),
        'y': float(start_y)+3,
        'vel_x': vel_x,
        'vel_y': vel_y,
        'angle': rotation_angles.get(direction, 0),
        'lifetime': BULLET_CONFIG['lifetime'],
        'damage': enemy['damage']
    }
    
    enemy_bullets.append(bullet)

def spawn_enemy_magic(enemy, homing=False):
    direction = enemy['direction']
    
    try:
        if enemy['type'] == 'boss':
            sounds.bossmagic.play()  
        else:
            sounds.magic.play() 
    except:
        pass

    dx = player.x - enemy['x']
    dy = player.y - enemy['y']
    distance = (dx * dx + dy * dy) ** 0.5
    
    if distance > 0:
        dir_x = dx / distance
        dir_y = dy / distance
    else:
        dir_x, dir_y = 0, 1
    
    speed = BULLET_CONFIG['speed'] if not homing else BULLET_CONFIG['speed'] * 0.5
    
    magic = {
        'x': float(enemy['x']),
        'y': float(enemy['y']),
        'vel_x': dir_x * speed,
        'vel_y': dir_y * speed,
        'lifetime': 180 if not homing else 360, 
        'damage': enemy['damage'],
        'homing': homing,
        'is_boss': enemy['type'] == 'boss'
    }
    
    enemy_magic.append(magic)

def update_enemy_bullets():
    for bullet in enemy_bullets[:]:
        bullet['x'] += bullet['vel_x']
        bullet['y'] += bullet['vel_y']
        
        bullet['lifetime'] -= 1
        
        if (bullet['lifetime'] <= 0 or 
            bullet['x'] < 0 or bullet['x'] > MAP_WIDTH or
            bullet['y'] < 0 or bullet['y'] > MAP_HEIGHT):
            enemy_bullets.remove(bullet)
            continue
        
                                     
        if not game_state['in_car']:
            dx = bullet['x'] - player.x
            dy = bullet['y'] - player.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < 15:
                damage_player(bullet['damage'])
                enemy_bullets.remove(bullet)
                continue
        
                                      
        if check_object_collision(bullet['x'], bullet['y'], radius=5):
            enemy_bullets.remove(bullet)

def update_enemy_magic():
    for magic in enemy_magic[:]:
                         
        if magic['homing']:
            dx = player.x - magic['x']
            dy = player.y - magic['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance > 0:
                dir_x = dx / distance
                dir_y = dy / distance
                speed = BULLET_CONFIG['speed'] * 0.5
                magic['vel_x'] = dir_x * speed
                magic['vel_y'] = dir_y * speed
        
        magic['x'] += magic['vel_x']
        magic['y'] += magic['vel_y']
        
        magic['lifetime'] -= 1

        if magic['lifetime'] <= 0:
            enemy_magic.remove(magic)
            continue
        
                                     
        if not game_state['in_car']:
            dx = magic['x'] - player.x
            dy = magic['y'] - player.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            radius = 25 if magic['is_boss'] else 15
            
            if distance < radius:
                damage_player(magic['damage'])
                enemy_magic.remove(magic)
                continue
        
        if check_object_collision(magic['x'], magic['y'], radius=10):
            enemy_magic.remove(magic)

def update_enemies():
    for enemy in enemies[:]:
        update_enemy(enemy)
    
    update_enemy_bullets()
    update_enemy_magic()
    check_level_complete()

def damage_enemy(enemy, damage):
    if not enemy['alive']:
        return
    
    enemy['health'] -= damage
    print(f"Enemy {enemy['type']} took {damage} damage! Health: {enemy['health']}/{enemy['max_health']}")
    
    if enemy['health'] <= 0:
        enemy['health'] = 0
        enemy['alive'] = False
        enemy['state'] = ENEMY_STATE_DEAD
        enemy['current_frame'] = 0
        try:
            sounds.die.play()  
        except:
            pass
        print(f"Enemy {enemy['type']} KILLED!")

def check_bullet_hit_enemies():
    bullets_to_remove = []
    
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if not enemy['alive']:
                continue
            
            dx = bullet['x'] - enemy['x']
            dy = bullet['y'] - enemy['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < 20:
                damage_enemy(enemy, 1)  
                bullets_to_remove.append(bullet)
                break
    
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

def check_katana_hit_enemies():
    if not player_weapon['attacking']:
        return
    
    if player_animation['current_frame'] not in [2, 3, 4]:
        return
    
    katana_range = 40

    if not hasattr(check_katana_hit_enemies, 'hit_this_swing'):
        check_katana_hit_enemies.hit_this_swing = set()

    if player_animation['current_frame'] == 2:
        check_katana_hit_enemies.hit_this_swing = set()
    
    for enemy in enemies[:]:
        if not enemy['alive']:
            continue

        if id(enemy) in check_katana_hit_enemies.hit_this_swing:
            continue
        
        dx = enemy['x'] - player.x
        dy = enemy['y'] - player.y
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < katana_range:
            direction = player_animation['direction']
            
            in_front = False
            if direction == 'right' and dx > 0 and abs(dy) < 30:
                in_front = True
            elif direction == 'left' and dx < 0 and abs(dy) < 30:
                in_front = True
            elif direction == 'down' and dy > 0 and abs(dx) < 30:
                in_front = True
            elif direction == 'up' and dy < 0 and abs(dx) < 30:
                in_front = True
            
            if in_front:
                damage = 0.6  
                
                if enemy['type'] in ['enemy4', 'enemy5', 'enemy6']:
                    damage = 0.67  
                elif enemy['type'] == 'boss':
                    damage = 0.75 
                
                damage_enemy(enemy, damage)
                check_katana_hit_enemies.hit_this_swing.add(id(enemy))
                print(f"Katana hit {enemy['type']} for {damage} damage!") 

def make_npcs_flee_from_enemies():
    flee_distance = 100
    
    for npc in npcs:
        if not npc['alive']:
            continue
        
        nearest_enemy = None
        nearest_enemy_dist = float('inf')
        
        for enemy in enemies:
            if not enemy['alive']:
                continue
            
            dx = npc['x'] - enemy['x']
            dy = npc['y'] - enemy['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < nearest_enemy_dist:
                nearest_enemy_dist = distance
                nearest_enemy = enemy
        
        if nearest_enemy_dist < flee_distance and nearest_enemy:
            npc['state'] = NPC_STATE_RUNNING
            
            dx = npc['x'] - nearest_enemy['x']
            dy = npc['y'] - nearest_enemy['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance > 0:
                dir_x = dx / distance
                dir_y = dy / distance
                
                speed = NPC_CONFIG['run_speed']
                next_x = npc['x'] + dir_x * speed
                next_y = npc['y'] + dir_y * speed
                
                if abs(dir_x) > abs(dir_y):
                    npc['direction'] = 'right' if dir_x > 0 else 'left'
                else:
                    npc['direction'] = 'down' if dir_y > 0 else 'up'
                
                if (is_on_walkable_surface(next_x, next_y) and 
                    not check_object_collision(next_x, next_y, radius=12)):
                    npc['x'] = next_x
                    npc['y'] = next_y
                else:
                    alternate_dirs = [
                        (dir_x, 0),  
                        (0, dir_y),  
                        (-dir_y, dir_x), 
                        (dir_y, -dir_x)   
                    ]
                    
                    for alt_x, alt_y in alternate_dirs:
                        test_x = npc['x'] + alt_x * speed
                        test_y = npc['y'] + alt_y * speed
                        
                        if (is_on_walkable_surface(test_x, test_y) and 
                            not check_object_collision(test_x, test_y, radius=10)):
                            npc['x'] = test_x
                            npc['y'] = test_y
                            break

NPC_FRAME_COUNTS = {
    'idle': 2,
    'walk': 9,
    'run': 8,   
    'hurt': 6
}

def get_npc_frame(npc_type, state, direction, frame_index):
    if npc_type not in NPC_SPRITESHEETS:
        return None
    
    state_map = {
        NPC_STATE_IDLE: 'idle',
        NPC_STATE_WALKING: 'walk',
        NPC_STATE_RUNNING: 'run',
        NPC_STATE_HURT: 'hurt'
    }
    
    state_name = state_map.get(state, 'idle')
    
    if state_name not in NPC_SPRITESHEETS[npc_type]:
        return None
    
    spritesheet = NPC_SPRITESHEETS[npc_type][state_name]
    
    if state_name == 'hurt':
        row = 0  
    else:
        row = DIRECTION_ROWS.get(direction, 0)
    
    frame_x = frame_index * 64
    frame_y = row * 64
    
    try:
        frame = spritesheet.subsurface(pygame.Rect(frame_x, frame_y, 64, 64))
        return frame
    except:
        return None

def is_on_sidewalk(x, y):
    tile_x = int(x // TILE_SIZE)
    tile_y = int(y // TILE_SIZE)
    
    if 0 <= tile_x < MAP_TILES_WIDTH and 0 <= tile_y < MAP_TILES_HEIGHT:
        tile = map_grid[tile_y][tile_x]
        if 'sidewalk' in tile.lower():
            return True
    return False

def is_on_walkable_surface(x, y):
    tile_x = int(x // TILE_SIZE)
    tile_y = int(y // TILE_SIZE)
    
    if 0 <= tile_x < MAP_TILES_WIDTH and 0 <= tile_y < MAP_TILES_HEIGHT:
        tile = map_grid[tile_y][tile_x]
        tile_lower = tile.lower()
        if 'sidewalk' in tile_lower or 'crosswalk' in tile_lower:
            return True
    return False

def check_object_collision(x, y, radius=10):
    OBJECT_HITBOXES = {
                    
        'building1': 50,
        'building2': 50,
        'building3': 50,
        'building3.5': 50,
        'building4': 55,
        'smallhouse': 30,
        
               
        'shop1': 25,
        'shop2': 25,
        'shop3': 25,
        'supermarket': 25,
        
               
        'tree1': 15,
        'tree2': 15,
        
                       
        'bench': 10,
        'parklight': 6,
        'dustbin': 5,
        'recyclebin': 5,
        'mailboxblue': 5,
        'firehydrant': 5,
        'toilet': 8,
        'vendingmachine': 8,
        'box1': 6,
        'box2': 6,
    }
    
    for obj in map_objects:
        if obj['name'] in OBJECT_HITBOXES:
            dx = x - obj['x']
            dy = y - obj['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            obj_radius = OBJECT_HITBOXES[obj['name']]
            
            if distance < (radius + obj_radius):
                return True
    return False

def spawn_npc():
                                                 
                                                   
    for attempt in range(100):                                     
        x = random.randint(100, MAP_WIDTH - 100)
        y = random.randint(100, MAP_HEIGHT - 100)
        
                                                                     
        if is_on_sidewalk(x, y) and not check_object_collision(x, y, radius=12):
                                    
            npc_type = f'npc{random.randint(1, 9)}'
            
            npcs.append({
                'type': npc_type,
                'x': float(x),
                'y': float(y),
                'direction': random.choice(['up', 'down', 'left', 'right']),
                'state': NPC_STATE_IDLE,
                'current_frame': 0,
                'frame_delay': 0,
                'decision_timer': 0,
                'target_x': None,
                'target_y': None,
                'alive': True
            })
            return True
    return False

def initialize_npcs():
                                      
    npcs.clear()
    for i in range(NPC_CONFIG['max_population']):
        spawn_npc()
    print(f"Spawned {len(npcs)} NPCs")

def check_npc_player_collision(new_x, new_y):
                                                    
    player_radius = 8
    npc_radius = 10
    
    for npc in npcs:
        if not npc['alive']:
            continue
            
        dx = new_x - npc['x']
        dy = new_y - npc['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < (player_radius + npc_radius):
            return True                              
    
    return False                

def check_npc_car_collision(npc):
                                          
    npc_radius = 12
    car_radius = 14
    
    for car in traffic_vehicles:
        dx = npc['x'] - car['x']
        dy = npc['y'] - car['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < (npc_radius + car_radius):
            return True
    
                                            
    if game_state['in_car']:
        dx = npc['x'] - player.x
        dy = npc['y'] - player.y
        distance = (dx * dx + dy * dy) ** 0.5
        if distance < (npc_radius + car_radius):
            return True
    
    return False

def kill_npc(npc, cause='car'):
                                           
    if not npc['alive']:                
        return
    
                  
    npc['alive'] = False
    npc['state'] = NPC_STATE_HURT
    npc['current_frame'] = 0
    npc['frame_delay'] = 0
    npc['death_cause'] = cause
    
                       
    npc['decision_timer'] = 9999

    try:
        sounds.die.play()                    
    except:
        pass
    
    print(f"✗ NPC KILLED by {cause} at ({int(npc['x'])}, {int(npc['y'])})")

def keep_npc_on_sidewalk(npc):
                                                  
    if not npc['alive'] or npc['state'] == NPC_STATE_RUNNING:
        return
    
    tile_x = int(npc['x'] // TILE_SIZE)
    tile_y = int(npc['y'] // TILE_SIZE)
    
    if 0 <= tile_x < MAP_TILES_WIDTH and 0 <= tile_y < MAP_TILES_HEIGHT:
        tile = map_grid[tile_y][tile_x]
        tile_lower = tile.lower()
        
                                           
        if 'sidewalk' in tile_lower or 'crosswalk' in tile_lower:
                                                    
            tile_left = tile_x * TILE_SIZE
            tile_right = (tile_x + 1) * TILE_SIZE
            tile_top = tile_y * TILE_SIZE
            tile_bottom = (tile_y + 1) * TILE_SIZE
            
                                                    
            margin = 1
            
                                                       
            if npc['x'] < tile_left + margin:
                npc['x'] = tile_left + margin
            elif npc['x'] > tile_right - margin:
                npc['x'] = tile_right - margin
            
            if npc['y'] < tile_top + margin:
                npc['y'] = tile_top + margin
            elif npc['y'] > tile_bottom - margin:
                npc['y'] = tile_bottom - margin
        else:
                                                                    
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    check_x = tile_x + dx
                    check_y = tile_y + dy
                    
                    if 0 <= check_x < MAP_TILES_WIDTH and 0 <= check_y < MAP_TILES_HEIGHT:
                        check_tile = map_grid[check_y][check_x]
                        if 'sidewalk' in check_tile.lower():
                                                                    
                            npc['x'] = (check_x * TILE_SIZE) + (TILE_SIZE / 2)
                            npc['y'] = (check_y * TILE_SIZE) + (TILE_SIZE / 2)
                            return

def update_npc(npc):
                                    
                                                     
    if not npc['alive']:
                            
                                    
        npc['frame_delay'] += 1
        if npc['frame_delay'] >= NPC_CONFIG['animation_speed']:
            npc['frame_delay'] = 0
            
                                                          
            if npc['current_frame'] < NPC_FRAME_COUNTS['hurt'] - 1:
                npc['current_frame'] += 1
            
                   
                                                                                                   
        
        return                                        
    
                                      
    if 'direction_change_cooldown' in npc and npc['direction_change_cooldown'] > 0:
        npc['direction_change_cooldown'] -= 1

                                             
    npc['frame_delay'] += 1
    
                                                     
    anim_speed = NPC_CONFIG['animation_speed']
    if npc['state'] == NPC_STATE_IDLE:
        anim_speed = NPC_CONFIG['animation_speed'] * 3                   

    if npc['frame_delay'] >= anim_speed:
        npc['frame_delay'] = 0
        npc['current_frame'] += 1

                                          
        state_map = {
            NPC_STATE_IDLE: 'idle',
            NPC_STATE_WALKING: 'walk',
            NPC_STATE_RUNNING: 'run',
            NPC_STATE_HURT: 'hurt'
        }
        state_name = state_map.get(npc['state'], 'idle')
        max_frames = NPC_FRAME_COUNTS.get(state_name, 2)

        if npc['current_frame'] >= max_frames:
            npc['current_frame'] = 0
    
                                  
                                                                                                              
    
                                                     
    if npc['alive'] and check_npc_car_collision(npc):
        kill_npc(npc, 'car')
        spawn_npc()                     
        return
    
                                  
    if is_on_walkable_surface(npc['x'], npc['y']):
                                                  
        pass                                         
    
                             
    npc['decision_timer'] += 1
    
    if npc['decision_timer'] >= NPC_CONFIG['decision_interval']:
        npc['decision_timer'] = 0
        
                             
        behavior_choice = random.random()
        
        if behavior_choice < 0.7:                           
                                 
            npc['state'] = NPC_STATE_WALKING
            npc['direction'] = random.choice(['up', 'down', 'left', 'right'])
        else:
                             
            npc['state'] = NPC_STATE_IDLE
   
                    
    if npc['state'] == NPC_STATE_WALKING:
        speed = NPC_CONFIG['walk_speed']
        
        next_x = npc['x']
        next_y = npc['y']
        
        if npc['direction'] == 'up':
            next_y -= speed
        elif npc['direction'] == 'down':
            next_y += speed
        elif npc['direction'] == 'left':
            next_x -= speed
        elif npc['direction'] == 'right':
            next_x += speed
        
        keep_npc_on_sidewalk(npc)

                                                                    
        if is_on_walkable_surface(next_x, next_y) and not check_object_collision(next_x, next_y, radius=10):
            npc['x'] = next_x
            npc['y'] = next_y
        else:
                                                                     
            if not hasattr(npc, 'direction_change_cooldown'):
                npc['direction_change_cooldown'] = 0
            
            if npc.get('direction_change_cooldown', 0) == 0:
                                               
                possible_directions = ['up', 'down', 'left', 'right']
                random.shuffle(possible_directions)
                
                for new_dir in possible_directions:
                                         
                    test_x, test_y = npc['x'], npc['y']
                    if new_dir == 'up':
                        test_y -= speed
                    elif new_dir == 'down':
                        test_y += speed
                    elif new_dir == 'left':
                        test_x -= speed
                    elif new_dir == 'right':
                        test_x += speed
                    
                                                      
                    if is_on_walkable_surface(test_x, test_y) and not check_object_collision(test_x, test_y, radius=10):
                        npc['direction'] = new_dir
                        break
                else:
                                                           
                    npc['state'] = NPC_STATE_IDLE
                
                npc['direction_change_cooldown'] = 30                                         
                npc['decision_timer'] = NPC_CONFIG['decision_interval'] - 50
            else:
                npc['direction_change_cooldown'] -= 1

def update_npcs():
                                     
                                                      
    player_x = player.x
    player_y = player.y

    for npc in npcs[:]:
                                      
        dx = npc['x'] - player_x
        dy = npc['y'] - player_y
        distance_sq = dx * dx + dy * dy                                       
        
                                                               
        if distance_sq < 500 * 500 or not npc['alive']:
            update_npc(npc)
        else:
                                                  
            pass
    
                                                                     
    for npc in npcs[:]:
        if not npc['alive'] and npc['state'] == NPC_STATE_HURT:
                                                               
            if npc['current_frame'] >= NPC_FRAME_COUNTS['hurt'] - 1:
                                                                 
                dead_bodies.append({
                    'type': npc['type'],
                    'x': npc['x'],
                    'y': npc['y'],
                    'direction': npc['direction'],
                    'timer': 360                      
                })
                print(f"Dead body created at ({int(npc['x'])}, {int(npc['y'])})")
                npcs.remove(npc)
    
                              
    for body in dead_bodies[:]:
        body['timer'] -= 1
        if body['timer'] <= 0:
            dead_bodies.remove(body)

                                              
player_animation = {
    'current_frame': 0,
    'frame_delay': 0,
    'animation_speed': 6,                            
    'direction': 'down',                      
    'state': 'idle',                           
    'spritesheets': {},
    'current_frames': []
}

                                 
FRAME_COUNTS = {
    'idle': 2,
    'walk': 9,
    'walk_katana': 9,
    'run': 8,
    'hurt': 6,
    'slash_katana': 6,
    'shoot': 13
}

                                
FRAME_SIZES = {
    'idle': 64,
    'walk': 64,
    'walk_katana': 128,
    'run': 64,
    'hurt': 64,
    'slash_katana': 128,
    'shoot': 64
}

                          
DIRECTION_ROWS = {
    'up': 0,
    'left': 1,
    'down': 2,
    'right': 3
}

def load_player_spritesheets():
                               
    try:
        player_animation['spritesheets']['idle'] = pygame.image.load('images/idle.png')
        player_animation['spritesheets']['walk'] = pygame.image.load('images/walk.png')
        player_animation['spritesheets']['walk_katana'] = pygame.image.load('images/walk_katana.png')
        player_animation['spritesheets']['run'] = pygame.image.load('images/run.png')
        player_animation['spritesheets']['hurt'] = pygame.image.load('images/hurt.png')
        player_animation['spritesheets']['slash_katana'] = pygame.image.load('images/slash_katana.png')
        player_animation['spritesheets']['shoot'] = pygame.image.load('images/shoot.png')
        
                             
        GUN_CONFIG['image'] = pygame.image.load('images/ak47.png')
        BULLET_CONFIG['image'] = pygame.image.load('images/rifleammosmall.png')
        
        print("Player spritesheets and weapons loaded successfully!")
    except Exception as e:
        print(f"Error loading spritesheets: {e}")
    
                          
    load_npc_spritesheets()

                        
    load_enemy_spritesheets()

    load_start_menu_images()                      

    load_all_sounds()                 
    
                                          
    initialize_npcs()

def get_player_frame(state, direction, frame_index):
                                                 
    if state not in player_animation['spritesheets']:
        return None
    
    spritesheet = player_animation['spritesheets'][state]
    
                                       
    frame_size = FRAME_SIZES.get(state, 64)
    
                                                       
    if state == 'hurt':
        row = 0
    else:
        row = DIRECTION_ROWS[direction]
    
                              
    frame_x = frame_index * frame_size
    frame_y = row * frame_size
    
                       
    frame = spritesheet.subsurface(pygame.Rect(frame_x, frame_y, frame_size, frame_size))
    return frame

def get_rotated_gun(direction):
                                            
    if GUN_CONFIG['image'] is None:
        return None
    
    gun_img = GUN_CONFIG['image']
    
                                                         
    if direction == 'right':
        rotated_gun = gun_img
    elif direction == 'left':
                                                     
        rotated_gun = pygame.transform.flip(gun_img, True, False)
    elif direction == 'up':
        rotated_gun = pygame.transform.rotate(gun_img, 90)
    elif direction == 'down':
        rotated_gun = pygame.transform.rotate(gun_img, -90)
    else:
        rotated_gun = gun_img
    
    return rotated_gun

def get_gun_offset(direction):
                                                                               
                                               
                                                  
    offsets = {
        'right': (4, 5),                                                     
        'left': (-4, 5),                                                    
        'up': (-1, -3),                                                     
        'down': (1, 5)                                                       
    }
    return offsets.get(direction, (0, 0))

def spawn_bullet():
                                             
    direction = player_animation['direction']
    
    try:
        sounds.rifle.play()                    
    except:
        pass

                                                     
    start_x = player.x
    start_y = player.y
    
                                                           
    if direction == 'right':
        start_x += 20
    elif direction == 'left':
        start_x -= 20
    elif direction == 'up':
        start_y -= 20
    elif direction == 'down':
        start_y += 20
    
                                        
    velocities = {
        'right': (BULLET_CONFIG['speed'], 0),
        'left': (-BULLET_CONFIG['speed'], 0),
        'up': (0, -BULLET_CONFIG['speed']),
        'down': (0, BULLET_CONFIG['speed'])
    }
    
    vel_x, vel_y = velocities.get(direction, (0, 0))
    
                               
    rotation_angles = {
        'right': 0,
        'left': 180,
        'up': 90,
        'down': -90
    }
    
    bullet = {
        'x': float(start_x),
        'y': float(start_y)+3,
        'vel_x': vel_x,
        'vel_y': vel_y,
        'angle': rotation_angles.get(direction, 0),
        'lifetime': BULLET_CONFIG['lifetime']
    }
    
    bullets.append(bullet)
    print(f"BULLET SPAWNED! Position: ({start_x}, {start_y}), Direction: {direction}, Total: {len(bullets)}")

def check_katana_hit_npcs():
                                      
    if not player_weapon['attacking']:
        return
    
                                                      
    if player_animation['current_frame'] not in [2, 3, 4]:                       
        return
    
    katana_range = 40                            
    
    npcs_to_kill = []                      
    
    for npc in npcs[:]:
        if not npc['alive']:
            continue
        
        dx = npc['x'] - player.x
        dy = npc['y'] - player.y
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < katana_range:
                                                
            direction = player_animation['direction']
            
            in_front = False
            if direction == 'right' and dx > 0 and abs(dy) < 30:
                in_front = True
            elif direction == 'left' and dx < 0 and abs(dy) < 30:
                in_front = True
            elif direction == 'down' and dy > 0 and abs(dx) < 30:
                in_front = True
            elif direction == 'up' and dy < 0 and abs(dx) < 30:
                in_front = True
            
            if in_front:
                npcs_to_kill.append(npc)
    
                       
    for npc in npcs_to_kill:
        if npc in npcs and npc['alive']:                                           
            print(f"Katana hit NPC at ({npc['x']}, {npc['y']})")
            kill_npc(npc, 'katana')
            spawn_npc()                   
    
                        
    check_katana_hit_enemies()

def check_bullet_hit_npcs():
                                       
    bullets_to_remove = []
    npcs_to_kill = []
    
    for bullet in bullets[:]:
        for npc in npcs[:]:
            if not npc['alive']:
                continue
            
            dx = bullet['x'] - npc['x']
            dy = bullet['y'] - npc['y']
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance < 15:                        
                print(f"Bullet hit NPC at distance {distance}")
                npcs_to_kill.append(npc)
                bullets_to_remove.append(bullet)
                break                           

                    
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    
               
    for npc in npcs_to_kill:
        if npc in npcs and npc['alive']:
            kill_npc(npc, 'bullet')
            spawn_npc()                   
    
                    
    check_bullet_hit_enemies()

def check_bullet_hit_objects():
                                                       
    for bullet in bullets[:]:
        if check_object_collision(bullet['x'], bullet['y'], radius=5):
            bullets.remove(bullet)

def update_bullets():
                            
    for bullet in bullets[:]:
                     
        bullet['x'] += bullet['vel_x']
        bullet['y'] += bullet['vel_y']
        
                           
        bullet['lifetime'] -= 1
        
                                               
        if (bullet['lifetime'] <= 0 or 
            bullet['x'] < 0 or bullet['x'] > MAP_WIDTH or
            bullet['y'] < 0 or bullet['y'] > MAP_HEIGHT):
            bullets.remove(bullet)

                                 
        check_bullet_hit_npcs()
        check_bullet_hit_objects()


def update_player_animation(state, direction):
                                                                       
    player_animation['state'] = state
    player_animation['direction'] = direction
    
    if state != 'idle':                      
        player_animation['frame_delay'] += 1
        
        if player_animation['frame_delay'] >= player_animation['animation_speed']:
            player_animation['frame_delay'] = 0
            player_animation['current_frame'] += 1
            
                            
            max_frames = FRAME_COUNTS[state]
            if player_animation['current_frame'] >= max_frames:
                player_animation['current_frame'] = 0
    else:        
                             
        player_animation['frame_delay'] += 1
        
        if player_animation['frame_delay'] >= player_animation['animation_speed'] * 3:          
            player_animation['frame_delay'] = 0
            player_animation['current_frame'] += 1
            
            if player_animation['current_frame'] >= FRAME_COUNTS['idle']:
                player_animation['current_frame'] = 0

          
map_grid = []

                                 
for y in range(MAP_TILES_HEIGHT):
    row = []
    for x in range(MAP_TILES_WIDTH):
        row.append('grassfieldmiddle') 
    map_grid.append(row)

               
map_objects = []

                
traffic_vehicles = []  

                                         
TRAFFIC_CONFIG = {
    'max_cars': 80,         
    'spawn_interval': 15,                                                    
    'car_speed': 3,   
    'car_max_speed': 5,           
    'despawn_distance': 2000,
    'stop_distance': 100,                                              
    'brake_distance': 120,
    'brake_force': 0.15,
    'intersection_wait': 30,                                                
}

             
spawn_timer = 0

                                                      
INTERSECTIONS = [
                                                  
                                    
                                                  
    
                                                        

                                               
    {'x': 28 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [(28 * TILE_SIZE, 28 * TILE_SIZE)],                                     
        'down': [(28 * TILE_SIZE, 32 * TILE_SIZE)],                                   
        'right': [(30 * TILE_SIZE, 30 * TILE_SIZE)],                                       
    }},
    {'x': 53 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((53 + 2) * TILE_SIZE, 28 * TILE_SIZE)],                             
        'down': [(53 * TILE_SIZE, 32 * TILE_SIZE)],                                   
        'left': [(52 * TILE_SIZE, (30 + 5) * TILE_SIZE)],                             
        'right': [(55 * TILE_SIZE, 30 * TILE_SIZE)],                                   
    }},
    {'x': 78 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((78 + 2) * TILE_SIZE, 28 * TILE_SIZE)],                             
        'down': [(78 * TILE_SIZE, 32 * TILE_SIZE)],                                   
        'left': [(77 * TILE_SIZE, (30 + 5) * TILE_SIZE)],                             
        'right': [(80 * TILE_SIZE, 30 * TILE_SIZE)],                                   
    }},
    {'x': 106 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [((106 + 5) * TILE_SIZE, 28 * TILE_SIZE)],                                         
        'down': [(106 * TILE_SIZE, 32 * TILE_SIZE)],                                   
        'left': [(104 * TILE_SIZE, (30 + 5) * TILE_SIZE)],                            
    }},
    
                                          
    {'x': 28 * TILE_SIZE, 'y': 59 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [(28 * TILE_SIZE, 57 * TILE_SIZE)],
        'down': [(28 * TILE_SIZE, 61 * TILE_SIZE)],
        'right': [(30 * TILE_SIZE, 59 * TILE_SIZE)],
    }},
    {'x': 53 * TILE_SIZE, 'y': 59 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((53 + 2) * TILE_SIZE, 57 * TILE_SIZE)],                             
        'down': [(53 * TILE_SIZE, 61 * TILE_SIZE)],
        'left': [(52 * TILE_SIZE, (59 + 2) * TILE_SIZE)],                             
        'right': [(55 * TILE_SIZE, 59 * TILE_SIZE)],                                   
    }},
    {'x': 78 * TILE_SIZE, 'y': 59 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((78 + 2) * TILE_SIZE, 57 * TILE_SIZE)],                             
        'down': [(78 * TILE_SIZE, 61 * TILE_SIZE)],
        'left': [(77 * TILE_SIZE, (59 + 2) * TILE_SIZE)],                             
        'right': [(80 * TILE_SIZE, 59 * TILE_SIZE)],                                   
    }},
    {'x': 106 * TILE_SIZE, 'y': 59 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [((106 + 5) * TILE_SIZE, 57 * TILE_SIZE)],                             
        'down': [(106 * TILE_SIZE, 61 * TILE_SIZE)],
        'left': [(104 * TILE_SIZE, (59 + 2) * TILE_SIZE)],                            
    }},
    
                                          
    {'x': 28 * TILE_SIZE, 'y': 81 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [(28 * TILE_SIZE, 79 * TILE_SIZE)],
        'right': [(30 * TILE_SIZE, 81 * TILE_SIZE)],
    }},
    {'x': 53 * TILE_SIZE, 'y': 81 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [((53 + 2) * TILE_SIZE, 79 * TILE_SIZE)],                             
        'left': [(52 * TILE_SIZE, (81 + 2) * TILE_SIZE)],                             
        'right': [(55 * TILE_SIZE, 81 * TILE_SIZE)],                                   
    }},
    {'x': 78 * TILE_SIZE, 'y': 81 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [((78 + 2) * TILE_SIZE, 79 * TILE_SIZE)],                             
        'left': [(77 * TILE_SIZE, (81 + 2) * TILE_SIZE)],                             
        'right': [(80 * TILE_SIZE, 81 * TILE_SIZE)],                                   
    }},
    {'x': 106 * TILE_SIZE, 'y': 81 * TILE_SIZE, 'type': 'T', 'directions': {
        'up': [((106 + 5) * TILE_SIZE, 79 * TILE_SIZE)],                             
        'left': [(104 * TILE_SIZE, (81 + 2) * TILE_SIZE)],                            
    }},
                                  
    {'x': 28 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((28 + 2) * TILE_SIZE, 5 * TILE_SIZE)],                              
    }},
    {'x': 28 * TILE_SIZE, 'y': 37 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((28 + 2) * TILE_SIZE, 37 * TILE_SIZE)],                  
    }},
    {'x': 28 * TILE_SIZE, 'y': 63 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((28 + 2) * TILE_SIZE, 63 * TILE_SIZE)],                  
    }},

                                  
    {'x': 53 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((53 + 2) * TILE_SIZE, 5 * TILE_SIZE)],
    }},
    {'x': 53 * TILE_SIZE, 'y': 37 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((53 + 2) * TILE_SIZE, 37 * TILE_SIZE)],
    }},
    {'x': 53 * TILE_SIZE, 'y': 63 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((53 + 2) * TILE_SIZE, 63 * TILE_SIZE)],
    }},

                                  
    {'x': 78 * TILE_SIZE, 'y': 5 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((78 + 2) * TILE_SIZE, 5 * TILE_SIZE)],
    }},
    {'x': 78 * TILE_SIZE, 'y': 37 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((78 + 2) * TILE_SIZE, 37 * TILE_SIZE)],
    }},
    {'x': 78 * TILE_SIZE, 'y': 63 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((78 + 2) * TILE_SIZE, 63 * TILE_SIZE)],
    }},

                                                  
                                  
                                                  

                                            
    {'x': 5 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'L', 'directions': {
        'down': [(106 * TILE_SIZE, 32 * TILE_SIZE)],                                
        'right': [(7 * TILE_SIZE, 30 * TILE_SIZE)],                         
    }},
    
                                                  
                                   
                                                  
    
                                               
    {'x': 126 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 28 * TILE_SIZE)],                             
        'down': [(126 * TILE_SIZE, 32 * TILE_SIZE)],
        'left': [(125 * TILE_SIZE, (30 + 5) * TILE_SIZE)],                            
        'right': [(128 * TILE_SIZE, 30 * TILE_SIZE)],                                  
    }},
    {'x': 151 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 28 * TILE_SIZE)],                                         
        'down': [(151 * TILE_SIZE, 32 * TILE_SIZE)],
        'left': [(150 * TILE_SIZE, (30 + 5) * TILE_SIZE)],                            
        'right': [(153 * TILE_SIZE, 30 * TILE_SIZE)],                                  
    }},
    {'x': 176 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 28 * TILE_SIZE)],                             
        'down': [(176 * TILE_SIZE, 32 * TILE_SIZE)],
        'left': [(175 * TILE_SIZE, (30 + 5) * TILE_SIZE)],                            
        'right': [(178 * TILE_SIZE, 30 * TILE_SIZE)],                                  
    }},
    
                             
    {'x': 126 * TILE_SIZE, 'y': 51 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 49 * TILE_SIZE)],
        'down': [(126 * TILE_SIZE, 53 * TILE_SIZE)],
        'left': [(125 * TILE_SIZE, (51 + 2) * TILE_SIZE)],
        'right': [(128 * TILE_SIZE, 51 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 51 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 49 * TILE_SIZE)],               
        'down': [(151 * TILE_SIZE, 53 * TILE_SIZE)],
        'left': [(150 * TILE_SIZE, (51 + 2) * TILE_SIZE)],
        'right': [(153 * TILE_SIZE, 51 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 51 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 49 * TILE_SIZE)],
        'down': [(176 * TILE_SIZE, 53 * TILE_SIZE)],
        'left': [(175 * TILE_SIZE, (51 + 2) * TILE_SIZE)],
        'right': [(178 * TILE_SIZE, 51 * TILE_SIZE)],
    }},
    
                             
    {'x': 126 * TILE_SIZE, 'y': 71 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 69 * TILE_SIZE)],
        'down': [(126 * TILE_SIZE, 73 * TILE_SIZE)],
        'left': [(125 * TILE_SIZE, (71 + 2) * TILE_SIZE)],
        'right': [(128 * TILE_SIZE, 71 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 71 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 69 * TILE_SIZE)],
        'down': [(151 * TILE_SIZE, 73 * TILE_SIZE)],
        'left': [(150 * TILE_SIZE, (71 + 2) * TILE_SIZE)],
        'right': [(153 * TILE_SIZE, 71 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 71 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 69 * TILE_SIZE)],
        'down': [(176 * TILE_SIZE, 73 * TILE_SIZE)],
        'left': [(175 * TILE_SIZE, (71 + 2) * TILE_SIZE)],
        'right': [(178 * TILE_SIZE, 71 * TILE_SIZE)],
    }},
    
                             
    {'x': 126 * TILE_SIZE, 'y': 91 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 89 * TILE_SIZE)],
        'down': [(126 * TILE_SIZE, 93 * TILE_SIZE)],
        'left': [(125 * TILE_SIZE, (91 + 2) * TILE_SIZE)],
        'right': [(128 * TILE_SIZE, 91 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 91 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 89 * TILE_SIZE)],
        'down': [(151 * TILE_SIZE, 93 * TILE_SIZE)],
        'left': [(150 * TILE_SIZE, (91 + 2) * TILE_SIZE)],
        'right': [(153 * TILE_SIZE, 91 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 91 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 89 * TILE_SIZE)],
        'down': [(176 * TILE_SIZE, 93 * TILE_SIZE)],
        'left': [(175 * TILE_SIZE, (91 + 2) * TILE_SIZE)],
        'right': [(178 * TILE_SIZE, 91 * TILE_SIZE)],
    }},
    
                              
    {'x': 126 * TILE_SIZE, 'y': 111 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 109 * TILE_SIZE)],
        'down': [(126 * TILE_SIZE, 113 * TILE_SIZE)],
        'left': [(125 * TILE_SIZE, (111 + 2) * TILE_SIZE)],
        'right': [(128 * TILE_SIZE, 111 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 111 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 109 * TILE_SIZE)],
        'down': [(151 * TILE_SIZE, 113 * TILE_SIZE)],
        'left': [(150 * TILE_SIZE, (111 + 2) * TILE_SIZE)],
        'right': [(153 * TILE_SIZE, 111 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 111 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 109 * TILE_SIZE)],
        'down': [(176 * TILE_SIZE, 113 * TILE_SIZE)],
        'left': [(175 * TILE_SIZE, (111 + 2) * TILE_SIZE)],
        'right': [(178 * TILE_SIZE, 111 * TILE_SIZE)],
    }},
    
                              
    {'x': 126 * TILE_SIZE, 'y': 129 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 127 * TILE_SIZE)],
        'down': [(126 * TILE_SIZE, 131 * TILE_SIZE)],
        'left': [(125 * TILE_SIZE, (129 + 2) * TILE_SIZE)],
        'right': [(128 * TILE_SIZE, 129 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 129 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 127 * TILE_SIZE)],
        'down': [(151 * TILE_SIZE, 131 * TILE_SIZE)],
        'left': [(150 * TILE_SIZE, (129 + 2) * TILE_SIZE)],
        'right': [(153 * TILE_SIZE, 129 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 129 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 127 * TILE_SIZE)],
        'down': [(176 * TILE_SIZE, 131 * TILE_SIZE)],
        'left': [(175 * TILE_SIZE, (129 + 2) * TILE_SIZE)],
        'right': [(178 * TILE_SIZE, 129 * TILE_SIZE)],
    }},
    
                                  
    {'x': 126 * TILE_SIZE, 'y': 16 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 16 * TILE_SIZE)],
    }},
    {'x': 126 * TILE_SIZE, 'y': 37 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 37 * TILE_SIZE)],
    }},
    {'x': 126 * TILE_SIZE, 'y': 55 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 55 * TILE_SIZE)],
    }},
    {'x': 126 * TILE_SIZE, 'y': 75 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 75 * TILE_SIZE)],
    }},
    {'x': 126 * TILE_SIZE, 'y': 95 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 95 * TILE_SIZE)],
    }},
    {'x': 126 * TILE_SIZE, 'y': 115 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 115 * TILE_SIZE)],
    }},
    {'x': 126 * TILE_SIZE, 'y': 133 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((126 + 2) * TILE_SIZE, 133 * TILE_SIZE)],
    }},

                                                              
    {'x': 151 * TILE_SIZE, 'y': 16 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 16 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 37 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 37 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 55 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 55 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 75 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 75 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 95 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 95 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 115 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 115 * TILE_SIZE)],
    }},
    {'x': 151 * TILE_SIZE, 'y': 133 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((151 + 5) * TILE_SIZE, 133 * TILE_SIZE)],
    }},

                                  
    {'x': 176 * TILE_SIZE, 'y': 16 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 16 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 37 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 37 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 55 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 55 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 75 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 75 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 95 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 95 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 115 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 115 * TILE_SIZE)],
    }},
    {'x': 176 * TILE_SIZE, 'y': 133 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((176 + 2) * TILE_SIZE, 133 * TILE_SIZE)],
    }},

                                                      
    {'x': 113 * TILE_SIZE, 'y': 9 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'left': [(113 * TILE_SIZE, (9 + 5) * TILE_SIZE)],                             
    }},
    {'x': 190 * TILE_SIZE, 'y': 9 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'right': [(190 * TILE_SIZE, 9 * TILE_SIZE)],                                   
    }},
                                                  
                                 
                                                  
    
                            
    {'x': 11 * TILE_SIZE, 'y': 105 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((11 + 2) * TILE_SIZE, 103 * TILE_SIZE)],                            
        'down': [(11 * TILE_SIZE, 107 * TILE_SIZE)],
        'left': [(10 * TILE_SIZE, (105 + 5) * TILE_SIZE)],                             
        'right': [(13 * TILE_SIZE, 105 * TILE_SIZE)],                                   
    }},
    {'x': 36 * TILE_SIZE, 'y': 105 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((36 + 2) * TILE_SIZE, 103 * TILE_SIZE)],
        'down': [(36 * TILE_SIZE, 107 * TILE_SIZE)],
        'left': [(35 * TILE_SIZE, (105 + 5) * TILE_SIZE)],
        'right': [(38 * TILE_SIZE, 105 * TILE_SIZE)],
    }},
    {'x': 61 * TILE_SIZE, 'y': 105 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((61 + 2) * TILE_SIZE, 103 * TILE_SIZE)],
        'down': [(61 * TILE_SIZE, 107 * TILE_SIZE)],
        'left': [(60 * TILE_SIZE, (105 + 5) * TILE_SIZE)],
        'right': [(63 * TILE_SIZE, 105 * TILE_SIZE)],
    }},
    {'x': 86 * TILE_SIZE, 'y': 105 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((86 + 2) * TILE_SIZE, 103 * TILE_SIZE)],
        'down': [(86 * TILE_SIZE, 107 * TILE_SIZE)],
        'left': [(85 * TILE_SIZE, (105 + 5) * TILE_SIZE)],
        'right': [(88 * TILE_SIZE, 105 * TILE_SIZE)],
    }},
    
                                             
    {'x': 11 * TILE_SIZE, 'y': 125 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((11 + 2) * TILE_SIZE, 123 * TILE_SIZE)],
        'down': [(11 * TILE_SIZE, 134 * TILE_SIZE)],
        'left': [(10 * TILE_SIZE, (125 + 5) * TILE_SIZE)],
        'right': [(13 * TILE_SIZE, 125 * TILE_SIZE)],
    }},
    {'x': 36 * TILE_SIZE, 'y': 125 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((36 + 2) * TILE_SIZE, 123 * TILE_SIZE)],
        'down': [(36 * TILE_SIZE, 134 * TILE_SIZE)],
        'left': [(35 * TILE_SIZE, (125 + 5) * TILE_SIZE)],
        'right': [(38 * TILE_SIZE, 125 * TILE_SIZE)],
    }},
    {'x': 61 * TILE_SIZE, 'y': 125 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((61 + 2) * TILE_SIZE, 123 * TILE_SIZE)],
        'down': [(61 * TILE_SIZE, 134 * TILE_SIZE)],
        'left': [(60 * TILE_SIZE, (125 + 5) * TILE_SIZE)],
        'right': [(63 * TILE_SIZE, 125 * TILE_SIZE)],
    }},
    {'x': 86 * TILE_SIZE, 'y': 125 * TILE_SIZE, 'type': 'cross', 'directions': {
        'up': [((86 + 2) * TILE_SIZE, 123 * TILE_SIZE)],
        'down': [(86 * TILE_SIZE, 134 * TILE_SIZE)],
        'left': [(85 * TILE_SIZE, (125 + 5) * TILE_SIZE)],
        'right': [(88 * TILE_SIZE, 125 * TILE_SIZE)],
    }},
                                                  
                                                   
                                                  

                                 
    {'x': 11 * TILE_SIZE, 'y': 114 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((11 + 2) * TILE_SIZE, 114 * TILE_SIZE)],
    }},
    {'x': 11 * TILE_SIZE, 'y': 151 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((11 + 2) * TILE_SIZE, 151 * TILE_SIZE)],
    }},

                                 
    {'x': 36 * TILE_SIZE, 'y': 114 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((36 + 2) * TILE_SIZE, 114 * TILE_SIZE)],
    }},
    {'x': 36 * TILE_SIZE, 'y': 151 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((36 + 2) * TILE_SIZE, 151 * TILE_SIZE)],
    }},

                                 
    {'x': 61 * TILE_SIZE, 'y': 114 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((61 + 2) * TILE_SIZE, 114 * TILE_SIZE)],
    }},
    {'x': 61 * TILE_SIZE, 'y': 151 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((61 + 2) * TILE_SIZE, 151 * TILE_SIZE)],
    }},

                                 
    {'x': 86 * TILE_SIZE, 'y': 114 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((86 + 2) * TILE_SIZE, 114 * TILE_SIZE)],
    }},
    {'x': 86 * TILE_SIZE, 'y': 151 * TILE_SIZE, 'type': 'dead_end', 'directions': {
        'up': [((86 + 2) * TILE_SIZE, 151 * TILE_SIZE)],
    }},

]

               
rotated_images = {}

def get_rotated_image(image_name, angle):
                                    
    cache_key = f"{image_name}_{angle}"
    if cache_key not in rotated_images:
        try:
            img = pygame.image.load(f'images/{image_name}.png')
            if angle != 0:
                rotated_images[cache_key] = pygame.transform.rotate(img, angle)
            else:
                rotated_images[cache_key] = img
        except:
            rotated_images[cache_key] = None
    return rotated_images[cache_key]

def place_tile(tile_name, tile_x, tile_y, rotation=0):
    if 0 <= tile_x < MAP_TILES_WIDTH and 0 <= tile_y < MAP_TILES_HEIGHT:
        if rotation == 0:
            map_grid[tile_y][tile_x] = tile_name
        else:
            map_grid[tile_y][tile_x] = f"{tile_name}|rot{rotation}"

def place_object(obj_name, pixel_x, pixel_y):
    map_objects.append({'name': obj_name, 'x': pixel_x, 'y': pixel_y})

def place_horizontal_road_normal(start_x, start_y, length):
    for i in range(length):
        x = start_x + i
        place_tile('sidewalkmiddle', x, start_y - 2)
        place_tile('sidewalkmiddle', x, start_y - 1)
        place_tile('road', x, start_y)
        place_tile('road', x, start_y + 1)
        place_tile('roadhorizontal', x, start_y + 2, rotation=90)
        place_tile('road', x, start_y + 3)
        place_tile('road', x, start_y + 4)
        place_tile('sidewalkmiddle', x, start_y + 5)
        place_tile('sidewalkmiddle', x, start_y + 6)

def place_horizontal_road_main(start_x, start_y, length):
    for i in range(length):
        x = start_x + i
        place_tile('sidewalkmiddle', x, start_y - 2)
        place_tile('sidewalkmiddle', x, start_y - 1)
        place_tile('road', x, start_y)
        place_tile('road', x, start_y + 1)
        place_tile('road', x, start_y + 2)
        place_tile('road', x, start_y + 3)
        place_tile('roadhorizontaldoubleline', x, start_y + 4, rotation=90)
        place_tile('road', x, start_y + 5)
        place_tile('road', x, start_y + 6)
        place_tile('road', x, start_y + 7)
        place_tile('road', x, start_y + 8)
        place_tile('sidewalkmiddle', x, start_y + 9)
        place_tile('sidewalkmiddle', x, start_y + 10)

def place_vertical_road_normal(start_x, start_y, length):
    for i in range(length):
        y = start_y + i
        place_tile('sidewalkmiddle', start_x - 2, y, rotation=90)
        place_tile('sidewalkmiddle', start_x - 1, y, rotation=90)
        place_tile('road', start_x, y, rotation=90)
        place_tile('road', start_x + 1, y, rotation=90)
        place_tile('roadhorizontal', start_x + 2, y)
        place_tile('road', start_x + 3, y, rotation=90)
        place_tile('road', start_x + 4, y, rotation=90)
        place_tile('sidewalkmiddle', start_x + 5, y, rotation=90)
        place_tile('sidewalkmiddle', start_x + 6, y, rotation=90)

def place_vertical_road_main(start_x, start_y, length):
    for i in range(length):
        y = start_y + i
        place_tile('sidewalkmiddle', start_x - 2, y, rotation=90)
        place_tile('sidewalkmiddle', start_x - 1, y, rotation=90)
        place_tile('road', start_x, y, rotation=90)
        place_tile('road', start_x + 1, y, rotation=90)
        place_tile('road', start_x + 2, y, rotation=90)
        place_tile('road', start_x + 3, y, rotation=90)
        place_tile('roadhorizontaldoubleline', start_x + 4, y)
        place_tile('road', start_x + 5, y, rotation=90)
        place_tile('road', start_x + 6, y, rotation=90)
        place_tile('road', start_x + 7, y, rotation=90)
        place_tile('road', start_x + 8, y, rotation=90)
        place_tile('sidewalkmiddle', start_x + 9, y, rotation=90)
        place_tile('sidewalkmiddle', start_x + 10, y, rotation=90)

def place_crosswalk_horizontal(center_x, center_y, road_width):
    for offset in range(-3, road_width - 1):
        place_tile('crosswalk', center_x, center_y + offset, rotation=90)

def place_crosswalk_vertical(center_x, center_y, road_width):
    for offset in range(-3, road_width - 1):
        place_tile('crosswalk', center_x + offset, center_y)

def fill_grass_area(start_x, start_y, width, height):
    for dy in range(height):
        for dx in range(width):
            x = start_x + dx
            y = start_y + dy
            if dy == 0 and dx == 0:
                tile = 'grassfieldtopleftcorner'
            elif dy == 0 and dx == width - 1:
                tile = 'grassfieldtoprightcorner'
            elif dy == height - 1 and dx == 0:
                tile = 'grassfieldbottomleftcorner'
            elif dy == height - 1 and dx == width - 1:
                tile = 'grassfieldbottomrightcorner'
            elif dy == 0:
                tile = 'grassfieldtopmiddle'
            elif dy == height - 1:
                tile = 'grassfieldbottommiddle'
            elif dx == 0:
                tile = 'grassfieldleftmiddle'
            elif dx == width - 1:
                tile = 'grassfieldrightmiddle'
            else:
                tile = 'grassfieldmiddle'
            place_tile(tile, x, y)

                                              
                  
                                              

place_vertical_road_main(104, 5, 145)
place_horizontal_road_main(5, 28, 99)

place_horizontal_road_normal(5, 58, 99)
place_horizontal_road_normal(5, 82, 99)

place_vertical_road_normal(27, 5, 23)
place_vertical_road_normal(27, 37, 21)
place_vertical_road_normal(27, 63, 19)

place_vertical_road_normal(52, 5, 23)
place_vertical_road_normal(52, 37, 21)
place_vertical_road_normal(52, 63, 19)

place_vertical_road_normal(77, 5, 23)
place_vertical_road_normal(77, 37, 21)
place_vertical_road_normal(77, 63, 19)

            
place_crosswalk_vertical(30, 27, 3)
place_crosswalk_vertical(30, 26, 3)
place_crosswalk_vertical(30, 37, 3)
place_crosswalk_vertical(30, 38, 3)
place_crosswalk_vertical(55, 26, 3)
place_crosswalk_vertical(55, 27, 3)
place_crosswalk_vertical(55, 37, 3)
place_crosswalk_vertical(55, 38, 3)
place_crosswalk_vertical(80, 26, 3)
place_crosswalk_vertical(80, 27, 3)
place_crosswalk_vertical(80, 37, 3)
place_crosswalk_vertical(80, 38, 3)

place_crosswalk_vertical(30, 56, 3)
place_crosswalk_vertical(30, 57, 3)
place_crosswalk_vertical(30, 63, 3)
place_crosswalk_vertical(30, 64, 3)
place_crosswalk_vertical(55, 56, 3)
place_crosswalk_vertical(55, 57, 3)
place_crosswalk_vertical(55, 63, 3)
place_crosswalk_vertical(55, 64, 3)
place_crosswalk_vertical(80, 56, 3)
place_crosswalk_vertical(80, 57, 3)
place_crosswalk_vertical(80, 63, 3)
place_crosswalk_vertical(80, 64, 3)

place_crosswalk_vertical(30, 80, 3)
place_crosswalk_vertical(30, 81, 3)
place_crosswalk_vertical(55, 80, 3)
place_crosswalk_vertical(55, 81, 3)
place_crosswalk_vertical(80, 80, 3)
place_crosswalk_vertical(80, 81, 3)

place_crosswalk_horizontal(25, 31, 7)
place_crosswalk_horizontal(26, 31, 7)
place_crosswalk_horizontal(32, 31, 7)
place_crosswalk_horizontal(33, 31, 7)
place_crosswalk_horizontal(50, 31, 7)
place_crosswalk_horizontal(51, 31, 7)
place_crosswalk_horizontal(57, 31, 7)
place_crosswalk_horizontal(58, 31, 7)
place_crosswalk_horizontal(75, 31, 7)
place_crosswalk_horizontal(76, 31, 7)
place_crosswalk_horizontal(82, 31, 7)
place_crosswalk_horizontal(83, 31, 7)
place_crosswalk_horizontal(102, 31, 7)
place_crosswalk_horizontal(103, 31, 7)

place_crosswalk_horizontal(25, 61, 3)
place_crosswalk_horizontal(26, 61, 3)
place_crosswalk_horizontal(32, 61, 3)
place_crosswalk_horizontal(33, 61, 3)
place_crosswalk_horizontal(50, 61, 3)
place_crosswalk_horizontal(51, 61, 3)
place_crosswalk_horizontal(57, 61, 3)
place_crosswalk_horizontal(58, 61, 3)
place_crosswalk_horizontal(75, 61, 3)
place_crosswalk_horizontal(76, 61, 3)
place_crosswalk_horizontal(82, 61, 3)
place_crosswalk_horizontal(83, 61, 3)
place_crosswalk_horizontal(102, 61, 3)
place_crosswalk_horizontal(103, 61, 3)

place_crosswalk_horizontal(25, 85, 3)
place_crosswalk_horizontal(26, 85, 3)
place_crosswalk_horizontal(32, 85, 3)
place_crosswalk_horizontal(33, 85, 3)
place_crosswalk_horizontal(50, 85, 3)
place_crosswalk_horizontal(51, 85, 3)
place_crosswalk_horizontal(57, 85, 3)
place_crosswalk_horizontal(58, 85, 3)
place_crosswalk_horizontal(75, 85, 3)
place_crosswalk_horizontal(76, 85, 3)
place_crosswalk_horizontal(82, 85, 3)
place_crosswalk_horizontal(83, 85, 3)
place_crosswalk_horizontal(102, 85, 3)
place_crosswalk_horizontal(103, 85, 3)

                         
fill_grass_area(5, 5, 20, 20)
fill_grass_area(34, 5, 16, 20)
fill_grass_area(59, 5, 16, 20)
fill_grass_area(84, 5, 16, 20)

fill_grass_area(5, 43, 20, 12)
fill_grass_area(34, 43, 16, 12)
fill_grass_area(59, 43, 16, 12)
fill_grass_area(84, 43, 16, 12)

fill_grass_area(5, 67, 20, 12)
fill_grass_area(34, 67, 16, 12)
fill_grass_area(59, 67, 16, 12)
fill_grass_area(84, 67, 16, 12)

fill_grass_area(5, 90, 97, 7)

                    
x_positions = [7, 11, 15, 19, 23, 36, 40, 44, 48, 61, 65, 69, 73, 86, 90, 94, 98]
y_positions = [7, 9.67, 12.3, 15.01, 17.68, 20.35, 23]
for x in x_positions:
    for y in y_positions:
        place_object('smallhouse', x * TILE_SIZE, y * TILE_SIZE)

x_positions = [7, 11, 15, 19, 23, 36, 40, 44, 48, 61, 65, 69, 73, 86, 90, 94, 98]
y_positions = [45, 47.67, 50.34, 53.01]
for x in x_positions:
    for y in y_positions:
        place_object('smallhouse', x * TILE_SIZE, y * TILE_SIZE)

x_positions = [7, 11, 15, 19, 23, 36, 40, 44, 48, 61, 65, 69, 73, 86, 90, 94, 98]
y_positions = [69, 71.67, 74.34, 77.01]
for x in x_positions:
    for y in y_positions:
        place_object('smallhouse', x * TILE_SIZE, y * TILE_SIZE)

x_positions = []
x = 7
while x <= 100:
    x_positions.append(x)
    x += 4
y_positions = [92, 94.67]
for x in x_positions:
    for y in y_positions:
        place_object('smallhouse', x * TILE_SIZE, y * TILE_SIZE)

                   
place_object('shop1', 38 * TILE_SIZE, 26 * TILE_SIZE)
place_object('shop2', 70 * TILE_SIZE, 26 * TILE_SIZE)
place_object('shop3', 100 * TILE_SIZE, 26 * TILE_SIZE)

place_object('shop1', 7 * TILE_SIZE, 101 * TILE_SIZE)
place_object('shop2', 14 * TILE_SIZE, 101 * TILE_SIZE)
place_object('shop3', 21 * TILE_SIZE, 101 * TILE_SIZE)
place_object('supermarket', 28 * TILE_SIZE, 101 * TILE_SIZE)
place_object('vendingMachine', 34 * TILE_SIZE, 103 * TILE_SIZE)
place_object('vendingMachine', 36 * TILE_SIZE, 103 * TILE_SIZE)
place_object('shop1', 42 * TILE_SIZE, 101 * TILE_SIZE)
place_object('shop2', 49 * TILE_SIZE, 101 * TILE_SIZE)
place_object('shop3', 56 * TILE_SIZE, 101 * TILE_SIZE)
place_object('supermarket', 63 * TILE_SIZE, 101 * TILE_SIZE)
place_object('vendingMachine', 69 * TILE_SIZE, 103 * TILE_SIZE)
place_object('vendingMachine', 71 * TILE_SIZE, 103 * TILE_SIZE)
place_object('shop1', 77 * TILE_SIZE, 101 * TILE_SIZE)
place_object('shop2', 84 * TILE_SIZE, 101 * TILE_SIZE)
place_object('shop3', 91 * TILE_SIZE, 101 * TILE_SIZE)
place_object('supermarket', 98 * TILE_SIZE, 101 * TILE_SIZE)

                   
place_object('tree1', 7 * TILE_SIZE, 8 * TILE_SIZE)
place_object('tree2', 20 * TILE_SIZE, 10 * TILE_SIZE)
place_object('tree1', 51 * TILE_SIZE, 8 * TILE_SIZE)
place_object('tree2', 76 * TILE_SIZE, 9 * TILE_SIZE)
place_object('tree1', 7 * TILE_SIZE, 45 * TILE_SIZE)
place_object('tree2', 51 * TILE_SIZE, 46 * TILE_SIZE)
place_object('tree1', 76 * TILE_SIZE, 45 * TILE_SIZE)
place_object('tree1', 15 * TILE_SIZE, 95 * TILE_SIZE)
place_object('tree2', 70 * TILE_SIZE, 96 * TILE_SIZE)

place_object('bench', 23 * TILE_SIZE, 26 * TILE_SIZE)
place_object('bench', 62 * TILE_SIZE, 26 * TILE_SIZE)
place_object('parklight', 26 * TILE_SIZE, 24 * TILE_SIZE)
place_object('parklight', 33 * TILE_SIZE, 24 * TILE_SIZE)
place_object('parklight', 58 * TILE_SIZE, 24 * TILE_SIZE)
place_object('dustbin', 23 * TILE_SIZE, 38 * TILE_SIZE)
place_object('recyclebin', 61 * TILE_SIZE, 38 * TILE_SIZE)
place_object('mailboxblue', 26 * TILE_SIZE, 66 * TILE_SIZE)

place_object('tree1', 5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 6.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 7.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 9 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 10 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 11.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 13 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 15 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 16.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 17.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 19 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 20 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 21.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 23 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 25 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 26.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 27.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 29 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 30 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 31.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 33 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 35 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 36.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 37.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 39 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 40 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 41.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 43 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 45 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 46.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 47.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 49 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 50 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 51.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 53 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 55 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 56.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 57.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 59 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 60 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 61.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 63 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 65 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 66.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 67.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 69 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 70 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 71.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 73 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 75 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 76.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 77.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 79 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 80 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 81.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 83 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 85 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 86.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 87.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 89 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 90 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 91.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 93 * TILE_SIZE, 98 * TILE_SIZE)

place_object('tree1', 95 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree2', 96.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 97.6 * TILE_SIZE, 98 * TILE_SIZE)
place_object('bench', 99 * TILE_SIZE, 98 * TILE_SIZE)
place_object('parklight', 100 * TILE_SIZE, 98 * TILE_SIZE)
place_object('tree1', 101 * TILE_SIZE, 98 * TILE_SIZE)

                                              
                 
                                              

                 
place_horizontal_road_main(113, 28, 77)
place_horizontal_road_main(113, 7, 77)

                               
place_horizontal_road_normal(113, 50, 77)
place_horizontal_road_normal(113, 70, 77)
place_horizontal_road_normal(113, 90, 77)
place_horizontal_road_normal(113, 110, 77)
place_horizontal_road_normal(113, 128, 77)


place_vertical_road_main(150, 16, 12)
place_vertical_road_main(150, 37, 13)
place_vertical_road_main(150, 55, 15)
place_vertical_road_main(150, 75, 15)
place_vertical_road_main(150, 95, 15)
place_vertical_road_main(150, 115, 13)
place_vertical_road_main(150, 133, 12)

                             
place_vertical_road_normal(125, 16, 12)
place_vertical_road_normal(125, 37, 12)
place_vertical_road_normal(125, 55, 14)
place_vertical_road_normal(125, 75, 14)
place_vertical_road_normal(125, 95, 14)
place_vertical_road_normal(125, 115, 13)
place_vertical_road_normal(125, 133, 12)

place_vertical_road_normal(175, 16, 12)
place_vertical_road_normal(175, 37, 13)
place_vertical_road_normal(175, 55, 14)
place_vertical_road_normal(175, 75, 14)
place_vertical_road_normal(175, 95, 14)
place_vertical_road_normal(175, 115, 13)
place_vertical_road_normal(175, 133, 12)

                       
place_crosswalk_vertical(128, 26, 3)
place_crosswalk_vertical(128, 27, 3)
place_crosswalk_vertical(128, 16, 3)
place_crosswalk_vertical(128, 17, 3)
place_crosswalk_vertical(153, 26, 3)
place_crosswalk_vertical(153, 27, 3)
place_crosswalk_vertical(153, 16, 3)
place_crosswalk_vertical(153, 17, 3)
place_crosswalk_vertical(157, 26, 3)
place_crosswalk_vertical(157, 27, 3)
place_crosswalk_vertical(157, 16, 3)
place_crosswalk_vertical(157, 17, 3)
place_crosswalk_vertical(178, 26, 3)
place_crosswalk_vertical(178, 27, 3)
place_crosswalk_vertical(178, 16, 3)
place_crosswalk_vertical(178, 17, 3)

place_crosswalk_vertical(128, 48, 3)
place_crosswalk_vertical(128, 49, 3)
place_crosswalk_vertical(128, 37, 3)
place_crosswalk_vertical(128, 38, 3)
place_crosswalk_vertical(153, 48, 3)
place_crosswalk_vertical(153, 49, 3)
place_crosswalk_vertical(153, 37, 3)
place_crosswalk_vertical(153, 38, 3)
place_crosswalk_vertical(157, 48, 3)
place_crosswalk_vertical(157, 49, 3)
place_crosswalk_vertical(157, 37, 3)
place_crosswalk_vertical(157, 38, 3)
place_crosswalk_vertical(178, 48, 3)
place_crosswalk_vertical(178, 49, 3)
place_crosswalk_vertical(178, 37, 3)
place_crosswalk_vertical(178, 38, 3)

place_crosswalk_vertical(128, 68, 3)
place_crosswalk_vertical(128, 69, 3)
place_crosswalk_vertical(128, 55, 3)
place_crosswalk_vertical(128, 56, 3)
place_crosswalk_vertical(153, 68, 3)
place_crosswalk_vertical(153, 69, 3)
place_crosswalk_vertical(153, 55, 3)
place_crosswalk_vertical(153, 56, 3)
place_crosswalk_vertical(157, 68, 3)
place_crosswalk_vertical(157, 69, 3)
place_crosswalk_vertical(157, 55, 3)
place_crosswalk_vertical(157, 56, 3)
place_crosswalk_vertical(178, 68, 3)
place_crosswalk_vertical(178, 69, 3)
place_crosswalk_vertical(178, 55, 3)
place_crosswalk_vertical(178, 56, 3)

place_crosswalk_vertical(128, 88, 3)
place_crosswalk_vertical(128, 89, 3)
place_crosswalk_vertical(128, 75, 3)
place_crosswalk_vertical(128, 76, 3)
place_crosswalk_vertical(153, 88, 3)
place_crosswalk_vertical(153, 89, 3)
place_crosswalk_vertical(153, 75, 3)
place_crosswalk_vertical(153, 76, 3)
place_crosswalk_vertical(157, 88, 3)
place_crosswalk_vertical(157, 89, 3)
place_crosswalk_vertical(157, 75, 3)
place_crosswalk_vertical(157, 76, 3)
place_crosswalk_vertical(178, 88, 3)
place_crosswalk_vertical(178, 89, 3)
place_crosswalk_vertical(178, 75, 3)
place_crosswalk_vertical(178, 76, 3)

place_crosswalk_vertical(128, 108, 3)
place_crosswalk_vertical(128, 109, 3)
place_crosswalk_vertical(128, 95, 3)
place_crosswalk_vertical(128, 96, 3)
place_crosswalk_vertical(153, 108, 3)
place_crosswalk_vertical(153, 109, 3)
place_crosswalk_vertical(153, 95, 3)
place_crosswalk_vertical(153, 96, 3)
place_crosswalk_vertical(157, 108, 3)
place_crosswalk_vertical(157, 109, 3)
place_crosswalk_vertical(157, 95, 3)
place_crosswalk_vertical(157, 96, 3)
place_crosswalk_vertical(178, 108, 3)
place_crosswalk_vertical(178, 109, 3)
place_crosswalk_vertical(178, 95, 3)
place_crosswalk_vertical(178, 96, 3)

place_crosswalk_vertical(128, 126, 3)
place_crosswalk_vertical(128, 127, 3)
place_crosswalk_vertical(128, 115, 3)
place_crosswalk_vertical(128, 116, 3)
place_crosswalk_vertical(153, 126, 3)
place_crosswalk_vertical(153, 127, 3)
place_crosswalk_vertical(153, 115, 3)
place_crosswalk_vertical(153, 116, 3)
place_crosswalk_vertical(157, 126, 3)
place_crosswalk_vertical(157, 127, 3)
place_crosswalk_vertical(157, 115, 3)
place_crosswalk_vertical(157, 116, 3)
place_crosswalk_vertical(178, 126, 3)
place_crosswalk_vertical(178, 127, 3)
place_crosswalk_vertical(178, 115, 3)
place_crosswalk_vertical(178, 116, 3)

place_crosswalk_vertical(128, 133, 3)
place_crosswalk_vertical(128, 134, 3)
place_crosswalk_vertical(153, 133, 3)
place_crosswalk_vertical(153, 134, 3)
place_crosswalk_vertical(157, 133, 3)
place_crosswalk_vertical(157, 134, 3)
place_crosswalk_vertical(178, 133, 3)
place_crosswalk_vertical(178, 134, 3)

place_crosswalk_horizontal(113, 10, 7)
place_crosswalk_horizontal(114, 10, 7)
place_crosswalk_horizontal(123, 10, 7)
place_crosswalk_horizontal(124, 10, 7)
place_crosswalk_horizontal(130, 10, 7)
place_crosswalk_horizontal(131, 10, 7)
place_crosswalk_horizontal(148, 10, 7)
place_crosswalk_horizontal(149, 10, 7)
place_crosswalk_horizontal(159, 10, 7)
place_crosswalk_horizontal(160, 10, 7)
place_crosswalk_horizontal(173, 10, 7)
place_crosswalk_horizontal(174, 10, 7)
place_crosswalk_horizontal(180, 10, 7)
place_crosswalk_horizontal(181, 10, 7)

place_crosswalk_horizontal(113, 31, 7)
place_crosswalk_horizontal(114, 31, 7)
place_crosswalk_horizontal(123, 31, 7)
place_crosswalk_horizontal(124, 31, 7)
place_crosswalk_horizontal(130, 31, 7)
place_crosswalk_horizontal(131, 31, 7)
place_crosswalk_horizontal(148, 31, 7)
place_crosswalk_horizontal(149, 31, 7)
place_crosswalk_horizontal(159, 31, 7)
place_crosswalk_horizontal(160, 31, 7)
place_crosswalk_horizontal(173, 31, 7)
place_crosswalk_horizontal(174, 31, 7)
place_crosswalk_horizontal(180, 31, 7)
place_crosswalk_horizontal(181, 31, 7)

place_crosswalk_horizontal(113, 53, 3)
place_crosswalk_horizontal(114, 53, 3)
place_crosswalk_horizontal(123, 53, 3)
place_crosswalk_horizontal(124, 53, 3)
place_crosswalk_horizontal(130, 53, 3)
place_crosswalk_horizontal(131, 53, 3)
place_crosswalk_horizontal(148, 53, 3)
place_crosswalk_horizontal(149, 53, 3)
place_crosswalk_horizontal(159, 53, 3)
place_crosswalk_horizontal(160, 53, 3)
place_crosswalk_horizontal(173, 53, 3)
place_crosswalk_horizontal(174, 53, 3)
place_crosswalk_horizontal(180, 53, 3)
place_crosswalk_horizontal(181, 53, 3)

place_crosswalk_horizontal(113, 73, 3)
place_crosswalk_horizontal(114, 73, 3)
place_crosswalk_horizontal(123, 73, 3)
place_crosswalk_horizontal(124, 73, 3)
place_crosswalk_horizontal(130, 73, 3)
place_crosswalk_horizontal(131, 73, 3)
place_crosswalk_horizontal(148, 73, 3)
place_crosswalk_horizontal(149, 73, 3)
place_crosswalk_horizontal(159, 73, 3)
place_crosswalk_horizontal(160, 73, 3)
place_crosswalk_horizontal(173, 73, 3)
place_crosswalk_horizontal(174, 73, 3)
place_crosswalk_horizontal(180, 73, 3)
place_crosswalk_horizontal(181, 73, 3)

place_crosswalk_horizontal(113, 93, 3)
place_crosswalk_horizontal(114, 93, 3)
place_crosswalk_horizontal(123, 93, 3)
place_crosswalk_horizontal(124, 93, 3)
place_crosswalk_horizontal(130, 93, 3)
place_crosswalk_horizontal(131, 93, 3)
place_crosswalk_horizontal(148, 93, 3)
place_crosswalk_horizontal(149, 93, 3)
place_crosswalk_horizontal(159, 93, 3)
place_crosswalk_horizontal(160, 93, 3)
place_crosswalk_horizontal(173, 93, 3)
place_crosswalk_horizontal(174, 93, 3)
place_crosswalk_horizontal(180, 93, 3)
place_crosswalk_horizontal(181, 93, 3)

place_crosswalk_horizontal(113, 113, 3)
place_crosswalk_horizontal(114, 113, 3)
place_crosswalk_horizontal(123, 113, 3)
place_crosswalk_horizontal(124, 113, 3)
place_crosswalk_horizontal(130, 113, 3)
place_crosswalk_horizontal(131, 113, 3)
place_crosswalk_horizontal(148, 113, 3)
place_crosswalk_horizontal(149, 113, 3)
place_crosswalk_horizontal(159, 113, 3)
place_crosswalk_horizontal(160, 113, 3)
place_crosswalk_horizontal(173, 113, 3)
place_crosswalk_horizontal(174, 113, 3)
place_crosswalk_horizontal(180, 113, 3)
place_crosswalk_horizontal(181, 113, 3)

place_crosswalk_horizontal(113, 131, 3)
place_crosswalk_horizontal(114, 131, 3)
place_crosswalk_horizontal(123, 131, 3)
place_crosswalk_horizontal(124, 131, 3)
place_crosswalk_horizontal(130, 131, 3)
place_crosswalk_horizontal(131, 131, 3)
place_crosswalk_horizontal(148, 131, 3)
place_crosswalk_horizontal(149, 131, 3)
place_crosswalk_horizontal(159, 131, 3)
place_crosswalk_horizontal(160, 131, 3)
place_crosswalk_horizontal(173, 131, 3)
place_crosswalk_horizontal(174, 131, 3)
place_crosswalk_horizontal(180, 131, 3)
place_crosswalk_horizontal(181, 131, 3)



             
place_object('building1', 117 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building2', 121 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building4', 119 * TILE_SIZE, 23 * TILE_SIZE)

place_object('building1', 134 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building3.5', 137.5 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building4', 142 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building3.5', 146 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building2', 134 * TILE_SIZE, 23 * TILE_SIZE)
place_object('building4', 138 * TILE_SIZE, 23 * TILE_SIZE)
place_object('building3', 142 * TILE_SIZE, 23 * TILE_SIZE)
place_object('building3.5', 146 * TILE_SIZE, 23 * TILE_SIZE)


place_object('building1', 163 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building3', 167 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building2', 171 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building3.5', 163 * TILE_SIZE, 23 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 23 * TILE_SIZE)
place_object('building3', 171 * TILE_SIZE, 23 * TILE_SIZE)

place_object('building1', 184 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building3', 188 * TILE_SIZE, 19 * TILE_SIZE)
place_object('building2', 184 * TILE_SIZE, 23 * TILE_SIZE)
place_object('building3.5', 188 * TILE_SIZE, 23 * TILE_SIZE)



         
place_object('building4', 119 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building4', 119 * TILE_SIZE, 44 * TILE_SIZE)

place_object('building4', 135 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building3', 139 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building1', 142 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building2', 146 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building3.5', 134 * TILE_SIZE, 44 * TILE_SIZE)
place_object('building2', 137.5 * TILE_SIZE, 44 * TILE_SIZE)
place_object('building4', 142 * TILE_SIZE, 44 * TILE_SIZE)
place_object('building3', 146 * TILE_SIZE, 44 * TILE_SIZE)


place_object('building2', 163 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building3.5', 171 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building1', 163 * TILE_SIZE, 44 * TILE_SIZE)
place_object('building3', 166 * TILE_SIZE, 44 * TILE_SIZE)
place_object('building4', 170 * TILE_SIZE, 44 * TILE_SIZE)

place_object('building4', 184.5 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building2', 188 * TILE_SIZE, 40 * TILE_SIZE)
place_object('building4', 184.5 * TILE_SIZE, 44 * TILE_SIZE)
place_object('building1', 188 * TILE_SIZE, 44 * TILE_SIZE)


         
place_object('building4', 119 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building1', 117 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building2', 121 * TILE_SIZE, 64 * TILE_SIZE)


place_object('building3.5', 134 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building2', 138 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building3', 142 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building1', 146 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building3', 134 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building1', 137.5 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building2', 141.3 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building4', 145.6 * TILE_SIZE, 64 * TILE_SIZE)


place_object('building3.5', 163 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building3', 167 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building2', 171 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building1', 163 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building3', 171 * TILE_SIZE, 64 * TILE_SIZE)

place_object('building2', 184.5 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building1', 189 * TILE_SIZE, 58 * TILE_SIZE)
place_object('building3', 184.5 * TILE_SIZE, 64 * TILE_SIZE)
place_object('building3.5', 189 * TILE_SIZE, 64 * TILE_SIZE)

         
place_object('building1', 117 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building2', 121 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building4', 119 * TILE_SIZE, 84 * TILE_SIZE)

place_object('building1', 134 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building3.5', 137.5 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building4', 142 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building3.5', 146 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building2', 134 * TILE_SIZE, 84 * TILE_SIZE)
place_object('building4', 138 * TILE_SIZE, 84 * TILE_SIZE)
place_object('building3', 142 * TILE_SIZE, 84 * TILE_SIZE)
place_object('building3.5', 146 * TILE_SIZE, 84 * TILE_SIZE)


place_object('building1', 163 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building3', 167 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building2', 171 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building3.5', 163 * TILE_SIZE, 84 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 84 * TILE_SIZE)
place_object('building3', 171 * TILE_SIZE, 84 * TILE_SIZE)

place_object('building1', 184 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building3', 188 * TILE_SIZE, 78 * TILE_SIZE)
place_object('building2', 184 * TILE_SIZE, 84 * TILE_SIZE)
place_object('building3.5', 188 * TILE_SIZE, 84 * TILE_SIZE)

         
place_object('building4', 119 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building4', 119 * TILE_SIZE, 104 * TILE_SIZE)

place_object('building4', 135 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building3', 139 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building1', 142 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building2', 146 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building3.5', 134 * TILE_SIZE, 104 * TILE_SIZE)
place_object('building2', 137.5 * TILE_SIZE, 104 * TILE_SIZE)
place_object('building4', 142 * TILE_SIZE, 104 * TILE_SIZE)
place_object('building3', 146 * TILE_SIZE, 104 * TILE_SIZE)


place_object('building2', 163 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building3.5', 171 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building1', 163 * TILE_SIZE, 104 * TILE_SIZE)
place_object('building3', 166 * TILE_SIZE, 104 * TILE_SIZE)
place_object('building4', 170 * TILE_SIZE, 104 * TILE_SIZE)

place_object('building4', 184.5 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building2', 189 * TILE_SIZE, 98 * TILE_SIZE)
place_object('building4', 184.5 * TILE_SIZE, 104 * TILE_SIZE)
place_object('building1', 189 * TILE_SIZE,104 * TILE_SIZE)

         
place_object('building4', 119 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building1', 117 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building2', 121 * TILE_SIZE, 122 * TILE_SIZE)


place_object('building3.5', 134 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building2', 138 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building3', 142 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building1', 146 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building3', 134 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building1', 137.5 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building2', 141.3 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building4', 145.6 * TILE_SIZE, 122 * TILE_SIZE)


place_object('building3.5', 163 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building3', 167 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building2', 171 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building1', 163 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building3', 171 * TILE_SIZE, 122 * TILE_SIZE)

place_object('building2', 184.5 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building1', 189 * TILE_SIZE, 118 * TILE_SIZE)
place_object('building3', 184.5 * TILE_SIZE, 122 * TILE_SIZE)
place_object('building3.5', 189 * TILE_SIZE, 122 * TILE_SIZE)

         
place_object('building1', 117 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building2', 121 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building4', 119 * TILE_SIZE, 140 * TILE_SIZE)

place_object('building1', 134 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building3.5', 137.5 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building4', 142 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building3.5', 146 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building2', 134 * TILE_SIZE, 140 * TILE_SIZE)
place_object('building4', 138 * TILE_SIZE, 140 * TILE_SIZE)
place_object('building3', 142 * TILE_SIZE, 140 * TILE_SIZE)
place_object('building3.5', 146 * TILE_SIZE, 140 * TILE_SIZE)


place_object('building1', 163 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building3', 167 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building2', 171 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building3.5', 163 * TILE_SIZE, 140 * TILE_SIZE)
place_object('building4', 167 * TILE_SIZE, 140 * TILE_SIZE)
place_object('building3', 171 * TILE_SIZE, 140 * TILE_SIZE)

place_object('building1', 184 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building3', 188 * TILE_SIZE, 136 * TILE_SIZE)
place_object('building2', 184 * TILE_SIZE, 140 * TILE_SIZE)
place_object('building3.5', 188 * TILE_SIZE, 140 * TILE_SIZE)

                                              
                  
                                              

                      
place_object('parklight', 124 * TILE_SIZE, 19 * TILE_SIZE)
place_object('parklight', 124 * TILE_SIZE, 40 * TILE_SIZE)
place_object('parklight', 124 * TILE_SIZE, 60 * TILE_SIZE)
place_object('parklight', 124 * TILE_SIZE, 80 * TILE_SIZE)
place_object('parklight', 124 * TILE_SIZE, 100 * TILE_SIZE)
place_object('parklight', 124 * TILE_SIZE, 120 * TILE_SIZE)

place_object('parklight', 181 * TILE_SIZE, 15 * TILE_SIZE)
place_object('parklight', 181 * TILE_SIZE, 40 * TILE_SIZE)
place_object('parklight', 181 * TILE_SIZE, 60 * TILE_SIZE)
place_object('parklight', 181 * TILE_SIZE, 80 * TILE_SIZE)
place_object('parklight', 181 * TILE_SIZE, 100 * TILE_SIZE)
place_object('parklight', 181 * TILE_SIZE, 120 * TILE_SIZE)

               
place_object('dustbin', 149 * TILE_SIZE, 48 * TILE_SIZE)
place_object('recyclebin', 149 * TILE_SIZE, 88 * TILE_SIZE)
place_object('firehydrant', 149 * TILE_SIZE, 127 * TILE_SIZE)

                     
place_object('box1', 192 * TILE_SIZE, 58 * TILE_SIZE)
place_object('box2', 191 * TILE_SIZE, 58 * TILE_SIZE)
place_object('box1', 192 * TILE_SIZE, 98 * TILE_SIZE)
place_object('box2', 191 * TILE_SIZE, 98 * TILE_SIZE)

            
place_object('toilet', 149 * TILE_SIZE, 138 * TILE_SIZE)
place_object('vendingmachine', 174 * TILE_SIZE, 138 * TILE_SIZE)


                                              
                                                                            
                                              
                     
place_horizontal_road_main(5, 105, 99)                                                                         
place_horizontal_road_main(5, 125, 99)                         

                                                    
                       
place_vertical_road_normal(10, 114, 11)
place_vertical_road_normal(10, 134, 17)
place_vertical_road_normal(35, 114, 11)                
place_vertical_road_normal(35, 134, 17)
place_vertical_road_normal(60, 114, 11)                
place_vertical_road_normal(60, 134, 17)
place_vertical_road_normal(85, 114, 11)                                                     
place_vertical_road_normal(85, 134, 17)


                                   
                                                   
crosswalk_x_positions = [13, 38, 63, 88]                  
for x in crosswalk_x_positions:
    place_crosswalk_vertical(x, 114, 3)                       
    place_crosswalk_vertical(x, 115, 3)
    place_crosswalk_vertical(x, 123, 3)                       
    place_crosswalk_vertical(x, 124, 3)
    place_crosswalk_vertical(x, 134, 3)                       
    place_crosswalk_vertical(x, 135, 3)

                                                   
crosswalk_y_positions = [108, 128]
for y in crosswalk_y_positions:
    for x_pos in [8, 9, 15, 16, 33, 34, 40, 41, 58, 59, 65, 66, 83, 84, 90, 91, 102, 103]:                  
        place_crosswalk_horizontal(x_pos, y, 7)

                                 
                                                   
                                                

def place_downtown_block(start_x, start_y, pattern='dense'):
    
    if pattern == 'dense':
                                             
        place_object('building3', start_x * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building4', (start_x + 4) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building1', start_x * TILE_SIZE, (start_y + 4) * TILE_SIZE)
        place_object('building2', (start_x + 4) * TILE_SIZE, (start_y + 4) * TILE_SIZE)
        place_object('building2', (start_x + 8) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building1', (start_x + 12) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building4', (start_x + 8) * TILE_SIZE, (start_y + 4) * TILE_SIZE)
        place_object('building3', (start_x + 12) * TILE_SIZE, (start_y + 4) * TILE_SIZE)
    
    elif pattern == 'towers':
                                             
        place_object('building4', start_x * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building4', start_x * TILE_SIZE, (start_y + 4) * TILE_SIZE)
        place_object('building2', (start_x + 5) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building3.5', (start_x + 5) * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)
        place_object('building4', (start_x + 10)  * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building4', (start_x + 10) * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)

    elif pattern == 'smalltowers':
                                         
        place_object('building4', start_x * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building4', start_x * TILE_SIZE, (start_y + 4) * TILE_SIZE)
        place_object('building2', (start_x + 5) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building3.5', (start_x + 5) * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)
    
    elif pattern == 'mixed':
                                   
        place_object('building1', start_x * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building3.5', (start_x + 3.5) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building2', start_x * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)
        place_object('building3', (start_x + 3.5) * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)
        place_object('building3', (start_x + 7) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building2', (start_x + 10.5) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building3.5', (start_x + 7) * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)
        place_object('building1', (start_x + 10.5) * TILE_SIZE, (start_y + 3.5) * TILE_SIZE)
        place_object('building4', (start_x + 2) * TILE_SIZE, (start_y + 7) * TILE_SIZE)
        place_object('building4', (start_x + 9) * TILE_SIZE, (start_y + 7) * TILE_SIZE)
    
    elif pattern == 'plaza':
                                             
        place_object('building3', start_x * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building2', (start_x + 6) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building1', start_x * TILE_SIZE, (start_y + 6) * TILE_SIZE)
        place_object('building4', (start_x + 6) * TILE_SIZE, (start_y + 6) * TILE_SIZE)
        place_object('building2', (start_x + 11) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building1', (start_x + 11) * TILE_SIZE, (start_y + 6) * TILE_SIZE)
        
                             
        place_object('bench', (start_x ) * TILE_SIZE, (start_y + 3) * TILE_SIZE)
        place_object('tree1', (start_x ) * TILE_SIZE, (start_y + 4) * TILE_SIZE)

    elif pattern == 'smallplaza':
                                             
        place_object('building3', start_x * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building2', (start_x + 6) * TILE_SIZE, start_y * TILE_SIZE)
        place_object('building1', start_x * TILE_SIZE, (start_y + 6) * TILE_SIZE)
        place_object('building4', (start_x + 6) * TILE_SIZE, (start_y + 6) * TILE_SIZE)

                                                           
place_downtown_block(19, 116, 'dense')                 
place_downtown_block(45, 116, 'towers')                
place_downtown_block(69, 116, 'dense')                 
place_downtown_block(95, 116, 'smalltowers') 

                                                           
place_downtown_block(19, 137, 'mixed')                 
place_downtown_block(44, 137, 'plaza')                                 
place_downtown_block(69.5, 137, 'mixed')                
place_downtown_block(94, 137, 'smallplaza')

                                   
                                                
for x in [18, 43, 66, 91]:
    place_object('parklight', x * TILE_SIZE, 103 * TILE_SIZE)                    
    place_object('parklight', x * TILE_SIZE, 123 * TILE_SIZE)                    
    place_object('parklight', x * TILE_SIZE, 143 * TILE_SIZE)                    

                                       
place_object('bench', 20 * TILE_SIZE, 103 * TILE_SIZE)
place_object('bench', 75 * TILE_SIZE, 103 * TILE_SIZE)

place_object('dustbin', 45 * TILE_SIZE, 123 * TILE_SIZE)
place_object('recyclebin', 45 * TILE_SIZE, 123 * TILE_SIZE)

           
place_object('vendingmachine', 30 * TILE_SIZE, 103 * TILE_SIZE)
place_object('toilet', 80 * TILE_SIZE, 123 * TILE_SIZE)
place_object('mailboxblue', 55 * TILE_SIZE, 103 * TILE_SIZE)
place_object('firehydrant', 80 * TILE_SIZE, 103 * TILE_SIZE)

                                   
place_object('tree1', 50 * TILE_SIZE, 103 * TILE_SIZE)
place_object('tree2', 25 * TILE_SIZE, 123 * TILE_SIZE)
place_object('tree1', 75 * TILE_SIZE, 123 * TILE_SIZE)

load_player_spritesheets()

              
map_objects.sort(key=lambda obj: obj['y'])

                                              
                
                                              

                 
CAR_STATE_DRIVING = 0
CAR_STATE_WAITING = 1
CAR_STATE_TURNING = 2
CAR_STATE_BRAKING = 3

def spawn_traffic_car():
                                           
    global spawn_timer
    
    if len(traffic_vehicles) >= TRAFFIC_CONFIG['max_cars']:
        return
    
    spawn_timer += 1
    if spawn_timer < TRAFFIC_CONFIG['spawn_interval']:
        return
    spawn_timer = 0
    
                                                    
    spawn_points = [
                                                      
                                 
                                                      
        
                                                                     
        {'x': 8 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'direction': 'right'},
                                                                    
        {'x': 110 * TILE_SIZE, 'y': (30 + 5) * TILE_SIZE, 'direction': 'left'},
        
                                                  
        {'x': 8 * TILE_SIZE, 'y': 59 * TILE_SIZE, 'direction': 'right'},
                                                 
        {'x': 110 * TILE_SIZE, 'y': (59 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                                  
        {'x': 8 * TILE_SIZE, 'y': 81 * TILE_SIZE, 'direction': 'right'},
                                                 
        {'x': 110 * TILE_SIZE, 'y': (81 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                               
        {'x': 28 * TILE_SIZE, 'y': 8 * TILE_SIZE, 'direction': 'down'},
                                             
        {'x': (28 + 2) * TILE_SIZE, 'y': 95 * TILE_SIZE, 'direction': 'up'},
        
                                               
        {'x': 53 * TILE_SIZE, 'y': 8 * TILE_SIZE, 'direction': 'down'},
                                             
        {'x': (53 + 2) * TILE_SIZE, 'y': 95 * TILE_SIZE, 'direction': 'up'},
        
                                               
        {'x': 78 * TILE_SIZE, 'y': 8 * TILE_SIZE, 'direction': 'down'},
                                             
        {'x': (78 + 2) * TILE_SIZE, 'y': 95 * TILE_SIZE, 'direction': 'up'},
        
                                                          
        {'x': 106 * TILE_SIZE, 'y': 8 * TILE_SIZE, 'direction': 'down'},
                                                        
        {'x': (106 + 5) * TILE_SIZE, 'y': 148 * TILE_SIZE, 'direction': 'up'},
        
                                                      
                                
                                                      
        
                                                                  
        {'x': 115 * TILE_SIZE, 'y': 30 * TILE_SIZE, 'direction': 'right'},
                                                                 
        {'x': 188 * TILE_SIZE, 'y': (30 + 5) * TILE_SIZE, 'direction': 'left'},
        
                                                             
        {'x': 115 * TILE_SIZE, 'y': 51 * TILE_SIZE, 'direction': 'right'},
                                                            
        {'x': 188 * TILE_SIZE, 'y': (51 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                                             
        {'x': 115 * TILE_SIZE, 'y': 71 * TILE_SIZE, 'direction': 'right'},
                                                            
        {'x': 188 * TILE_SIZE, 'y': (71 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                                             
        {'x': 115 * TILE_SIZE, 'y': 9 * TILE_SIZE, 'direction': 'right'},
                                                            
        {'x': 188 * TILE_SIZE, 'y': (91 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                                              
        {'x': 115 * TILE_SIZE, 'y': 111 * TILE_SIZE, 'direction': 'right'},
                                                             
        {'x': 188 * TILE_SIZE, 'y': (111 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                                              
        {'x': 115 * TILE_SIZE, 'y': 129 * TILE_SIZE, 'direction': 'right'},
                                                             
        {'x': 188 * TILE_SIZE, 'y': (129 + 2) * TILE_SIZE, 'direction': 'left'},
        
                                                           
        {'x': 127 * TILE_SIZE, 'y': 10 * TILE_SIZE, 'direction': 'down'},
                                                         
        {'x': (127 + 3) * TILE_SIZE, 'y': 145 * TILE_SIZE, 'direction': 'up'},
        
                                                           
        {'x': 152 * TILE_SIZE, 'y': 10 * TILE_SIZE, 'direction': 'down'},
                                                         
        {'x': (152 + 5) * TILE_SIZE, 'y': 145 * TILE_SIZE, 'direction': 'up'},
        
                                                           
        {'x': 176 * TILE_SIZE, 'y': 10 * TILE_SIZE, 'direction': 'down'},
                                                         
        {'x': (176 + 2) * TILE_SIZE, 'y': 145 * TILE_SIZE, 'direction': 'up'},
        
                                                      
                              
                                                      
        
                                                            
        {'x': 8 * TILE_SIZE, 'y': 105 * TILE_SIZE, 'direction': 'right'},
                                                           
        {'x': 110 * TILE_SIZE, 'y': (105 + 5) * TILE_SIZE, 'direction': 'left'},
        
                                                            
        {'x': 8 * TILE_SIZE, 'y': 125 * TILE_SIZE, 'direction': 'right'},
                                                           
        {'x': 110 * TILE_SIZE, 'y': (125 + 5) * TILE_SIZE, 'direction': 'left'},
        
                                                   
        {'x': 11 * TILE_SIZE, 'y': 98 * TILE_SIZE, 'direction': 'down'},
                                                 
        {'x': (11 + 2) * TILE_SIZE, 'y': 148 * TILE_SIZE, 'direction': 'up'},
        
                                                   
        {'x': 36 * TILE_SIZE, 'y': 98 * TILE_SIZE, 'direction': 'down'},
                                                 
        {'x': (36 + 2) * TILE_SIZE, 'y': 148 * TILE_SIZE, 'direction': 'up'},
        
                                                   
        {'x': 61 * TILE_SIZE, 'y': 98 * TILE_SIZE, 'direction': 'down'},
                                                 
        {'x': (61 + 2) * TILE_SIZE, 'y': 148 * TILE_SIZE, 'direction': 'up'},
        
                                                   
        {'x': 86 * TILE_SIZE, 'y': 98 * TILE_SIZE, 'direction': 'down'},
                                                 
        {'x': (86 + 2) * TILE_SIZE, 'y': 148 * TILE_SIZE, 'direction': 'up'},
    ]
    
    for _ in range(10):
        spawn = random.choice(spawn_points)
        
        if not is_position_blocked(spawn['x'], spawn['y'], 80):
            car_type = random.choice(['ambulanceup', 'truckup', 'carup1'])
            
            traffic_vehicles.append({
                'name': car_type,
                'x': float(spawn['x']),
                'y': float(spawn['y']),
                'direction': spawn['direction'],
                'speed': TRAFFIC_CONFIG['car_speed'],
                'target_speed': TRAFFIC_CONFIG['car_max_speed'],
                'angle': get_angle_for_direction(spawn['direction']),
                'state': CAR_STATE_DRIVING,
                'wait_timer': 0,
                'target_lane': None,
                'last_intersection': None,
                'frames_since_turn': 999,
                'lane_y': spawn['y'] if spawn['direction'] in ['right', 'left'] else None,
                'lane_x': spawn['x'] if spawn['direction'] in ['up', 'down'] else None,
            })
            return

def is_position_blocked(x, y, min_dist):
    for car in traffic_vehicles:
        dx = abs(car['x'] - x)
        dy = abs(car['y'] - y)
        if (dx * dx + dy * dy) ** 0.5 < min_dist:
            return True
    return False

def get_angle_for_direction(direction):
    return {'up': 180, 'down': 0, 'left': 270, 'right': 90}.get(direction, 0)

def is_on_road(x, y):
                                                 
    tile_x = int(x // TILE_SIZE)
    tile_y = int(y // TILE_SIZE)
    
    if 0 <= tile_x < MAP_TILES_WIDTH and 0 <= tile_y < MAP_TILES_HEIGHT:
        tile = map_grid[tile_y][tile_x]
        tile_lower = tile.lower()
        
        if ('road' in tile_lower or 'crosswalk' in tile_lower) and 'sidewalk' not in tile_lower:
            return True
    return False

def is_at_intersection(x, y):
                                  
    threshold = 12
    
    for intersection in INTERSECTIONS:
        dx = abs(x - intersection['x'])
        dy = abs(y - intersection['y'])
        
        if dx < threshold and dy < threshold:
            return intersection
    return None

def get_opposite_direction(direction):
    return {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}.get(direction, direction)

def choose_new_direction(car, intersection):
                                            
    current_dir = car['direction']
    opposite_dir = get_opposite_direction(current_dir)
    
    available_dirs = [d for d in intersection['directions'].keys() if d != opposite_dir]
    
    if not available_dirs:
        return current_dir, None
    
                                     
    if current_dir in available_dirs and random.random() < 0.65:
        new_dir = current_dir
    else:
        new_dir = random.choice(available_dirs)
    
                     
    target_positions = intersection['directions'][new_dir]
    target_lane = target_positions[0] if target_positions else None
    
                          
    if new_dir in ['right', 'left']:
        car['lane_y'] = target_lane[1] if target_lane else car['y']
        car['lane_x'] = None
    else:
        car['lane_x'] = target_lane[0] if target_lane else car['x']
        car['lane_y'] = None

    
    return new_dir, target_lane

def check_obstacle_ahead(car, check_distance):
                                         
    min_distance = check_distance
    found_obstacle = False
    
                                             
    for other_car in traffic_vehicles:
        if other_car == car:
            continue
        
        same_lane = False
        is_ahead = False
        dist = 0
        
        if car['direction'] == 'right':
                                                           
            same_lane = abs(car['y'] - other_car['y']) < 10
            if same_lane and other_car['x'] > car['x']:
                is_ahead = True
                dist = other_car['x'] - car['x']
                
        elif car['direction'] == 'left':
            same_lane = abs(car['y'] - other_car['y']) < 10
            if same_lane and other_car['x'] < car['x']:
                is_ahead = True
                dist = car['x'] - other_car['x']
                
        elif car['direction'] == 'down':
            same_lane = abs(car['x'] - other_car['x']) < 10
            if same_lane and other_car['y'] > car['y']:
                is_ahead = True
                dist = other_car['y'] - car['y']
                
        elif car['direction'] == 'up':
            same_lane = abs(car['x'] - other_car['x']) < 10
            if same_lane and other_car['y'] < car['y']:
                is_ahead = True
                dist = car['y'] - other_car['y']
        
        if is_ahead and 0 < dist < min_distance:
            min_distance = dist
            found_obstacle = True
    
                                          
    for npc in npcs:
        if not npc['alive']:
            continue
        
        npc_ahead = False
        npc_dist = 0
        
        if car['direction'] == 'right':
            if abs(car['y'] - npc['y']) < 25 and npc['x'] > car['x']:
                npc_dist = npc['x'] - car['x']
                npc_ahead = True
        elif car['direction'] == 'left':
            if abs(car['y'] - npc['y']) < 25 and npc['x'] < car['x']:
                npc_dist = car['x'] - npc['x']
                npc_ahead = True
        elif car['direction'] == 'down':
            if abs(car['x'] - npc['x']) < 25 and npc['y'] > car['y']:
                npc_dist = npc['y'] - car['y']
                npc_ahead = True
        elif car['direction'] == 'up':
            if abs(car['x'] - npc['x']) < 25 and npc['y'] < car['y']:
                npc_dist = car['y'] - npc['y']
                npc_ahead = True
        
        if npc_ahead and 0 < npc_dist < min_distance:
            min_distance = npc_dist
            found_obstacle = True

                  
    player_ahead = False
    player_dist = 0
    
    if car['direction'] == 'right':
        if abs(car['y'] - player.y) < 25 and player.x > car['x']:
            player_dist = player.x - car['x']
            player_ahead = True
    elif car['direction'] == 'left':
        if abs(car['y'] - player.y) < 25 and player.x < car['x']:
            player_dist = car['x'] - player.x
            player_ahead = True
    elif car['direction'] == 'down':
        if abs(car['x'] - player.x) < 25 and player.y > car['y']:
            player_dist = player.y - car['y']
            player_ahead = True
    elif car['direction'] == 'up':
        if abs(car['x'] - player.x) < 25 and player.y < car['y']:
            player_dist = car['y'] - player.y
            player_ahead = True
    
    if player_ahead and player_dist < min_distance:
        min_distance = player_dist
        found_obstacle = True
    
    return found_obstacle, min_distance

def update_traffic():
                                                 
    spawn_traffic_car()
    
    for car in traffic_vehicles[:]:
        if 'frames_since_turn' not in car:
            car['frames_since_turn'] = 999
        car['frames_since_turn'] += 1
        
                                                            
        if car['state'] == CAR_STATE_DRIVING and car['frames_since_turn'] > 30:
            if car['direction'] in ['right', 'left'] and car['lane_y'] is not None:
                                               
                if abs(car['y'] - car['lane_y']) > 2:
                    car['y'] += (car['lane_y'] - car['y']) * 0.08
            elif car['direction'] in ['up', 'down'] and car['lane_x'] is not None:
                                               
                if abs(car['x'] - car['lane_x']) > 3:
                    car['x'] += (car['lane_x'] - car['x']) * 0.08
        
                         
        has_obstacle, obstacle_dist = check_obstacle_ahead(car, TRAFFIC_CONFIG['brake_distance'])
        
                        
        if has_obstacle:
            if obstacle_dist < TRAFFIC_CONFIG['stop_distance']:
                car['state'] = CAR_STATE_WAITING
                car['speed'] = max(0, car['speed'] - TRAFFIC_CONFIG['brake_force'] * 3)
                car['wait_timer'] += 1
                
                if car['wait_timer'] > 500:
                    traffic_vehicles.remove(car)
                continue
            elif obstacle_dist < TRAFFIC_CONFIG['brake_distance']:
                car['state'] = CAR_STATE_BRAKING
                car['speed'] = max(1.0, car['speed'] - TRAFFIC_CONFIG['brake_force'])
            else:
                car['state'] = CAR_STATE_DRIVING
                car['speed'] = min(car['target_speed'], car['speed'] + 0.06)
        else:
            car['state'] = CAR_STATE_DRIVING
            car['speed'] = min(car['target_speed'], car['speed'] + 0.06)
            car['wait_timer'] = 0
        
                               
        intersection = None
        if car['frames_since_turn'] > 30:
            intersection = is_at_intersection(car['x'], car['y'])
        
        if intersection and car['state'] in [CAR_STATE_DRIVING, CAR_STATE_BRAKING]:
            if car.get('last_intersection') != intersection:
                new_direction, target_lane = choose_new_direction(car, intersection)
                
                if new_direction != car['direction']:
                    car['direction'] = new_direction
                    car['angle'] = get_angle_for_direction(new_direction)
                    car['target_lane'] = target_lane
                    car['state'] = CAR_STATE_TURNING
                    car['frames_since_turn'] = 0
                    
                    car['x'] = float(intersection['x'])
                    car['y'] = float(intersection['y'])
                
                car['last_intersection'] = intersection
        
                         
        if car['state'] == CAR_STATE_TURNING and car['target_lane']:
            target_x, target_y = car['target_lane']
            
            dx = target_x - car['x']
            dy = target_y - car['y']
            dist = (dx * dx + dy * dy) ** 0.5
            
            if dist < 10:
                car['state'] = CAR_STATE_DRIVING
                car['target_lane'] = None
            else:
                car['x'] += dx * 0.08
                car['y'] += dy * 0.08
        
                  
        if car['state'] in [CAR_STATE_DRIVING, CAR_STATE_BRAKING]:
            next_x, next_y = car['x'], car['y']
            
            if car['direction'] == 'right':
                next_x += car['speed']
            elif car['direction'] == 'left':
                next_x -= car['speed']
            elif car['direction'] == 'down':
                next_y += car['speed']
            elif car['direction'] == 'up':
                next_y -= car['speed']
            
                                             
            if is_on_road(next_x, next_y) and not check_object_collision(next_x, next_y, radius=14):
                car['x'], car['y'] = next_x, next_y
                
                if intersection is None:
                    car['last_intersection'] = None
            else:
                traffic_vehicles.remove(car)
                continue
        
                 
        dist = ((car['x'] - player.x)**2 + (car['y'] - player.y)**2)**0.5
        if dist > TRAFFIC_CONFIG['despawn_distance']:
            traffic_vehicles.remove(car)


                                              
                                            
                                              
def play_hurt_animation():
                                  
    player_animation['state'] = 'hurt'
    player_animation['current_frame'] = 0
    player_animation['frame_delay'] = 0

def get_car_hitbox(car):
                                                                    
                        
    if car['name'] in ['truckup']:
        width, height = 32, 51                   
    else:
        width, height = 27, 46                
    
                                      
    if car['direction'] in ['up', 'down']:
                                          
        half_w = width / 2
        half_h = height / 2
    else:               
                                           
        half_w = height / 2
        half_h = width / 2
    
    return {
        'left': car['x'] - half_w,
        'right': car['x'] + half_w,
        'top': car['y'] - half_h,
        'bottom': car['y'] + half_h
    }

def check_rect_collision(x, y, hitbox, padding=0):
                                                                
    player_size = 6 + padding                         
    
    return (x + player_size > hitbox['left'] and 
            x - player_size < hitbox['right'] and
            y + player_size > hitbox['top'] and 
            y - player_size < hitbox['bottom'])

def check_player_car_collision(new_x, new_y):
                                                                                  
    for car in traffic_vehicles:
        hitbox = get_car_hitbox(car)
        
        if check_rect_collision(new_x, new_y, hitbox, padding=5):
            return True                              
    
    return False                                 

def find_nearest_car():
                                                   
    nearest_car = None
    min_distance = 50                     
    
    for car in traffic_vehicles:
        dx = player.x - car['x']
        dy = player.y - car['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < min_distance:
            min_distance = distance
            nearest_car = car
    
    return nearest_car

def enter_car(car):
                             
                                       
    player.x = car['x']
    player.y = car['y']
    
    game_state['in_car'] = True
    game_state['car_type'] = car['name']
    game_state['car_angle'] = car['angle']
    game_state['car_speed'] = TRAFFIC_CONFIG['car_max_speed']
    
                                    
    if car in traffic_vehicles:
        traffic_vehicles.remove(car)

    try:
        sounds.carstart.play()                        
        music_system['carstart_playing'] = True
        
                                                            
                                        
        carstart_duration = sounds.carstart.get_length()
        music_system['carstart_start_time'] = pygame.time.get_ticks()
        music_system['carstart_duration'] = carstart_duration * 1000                           
    except:
        pass
    
    print(f"Player entered car at ({player.x}, {player.y})")

def exit_car():
                              
    game_state['in_car'] = False
    game_state['car_type'] = None
    game_state['car_angle'] = 0
    game_state['car_speed'] = 0

    try:
        if music_system['drive_channel']:
            music_system['drive_channel'].fadeout(500)                  
            music_system['drive_channel'] = None
        music_system['carstart_playing'] = False
    except:
        pass


def check_player_car_traffic_collision():
                                                               
    if not game_state['in_car']:
        return False
    
    car_radius = 40
    
    for car in traffic_vehicles:
        dx = player.x - car['x']
        dy = player.y - car['y']
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance < car_radius:
            return True
    
    return False

def check_collision_with_cars():
                                                                               
    for car in traffic_vehicles:
        hitbox = get_car_hitbox(car)
        
                                              
        if check_rect_collision(player.x, player.y, hitbox, padding=0):
                                                    
            if car['speed'] < 1.8:
                continue                               
            
                                                                             
            dx = player.x - car['x']
            dy = player.y - car['y']
            
                                                      
            if car['direction'] == 'right':
                if dx > -20:                         
                                        
                    player_animation['state'] = 'hurt'
                    player_animation['current_frame'] = 0
                    player_animation['frame_delay'] = 0
                    
                                       
                    game_state['alive'] = False
                    game_state['death_timer'] = 0
                    game_state['death_cause'] = 'car'
                    return True
            elif car['direction'] == 'left':
                if dx < 20:
                    player_animation['state'] = 'hurt'
                    player_animation['current_frame'] = 0
                    player_animation['frame_delay'] = 0
                    game_state['alive'] = False
                    game_state['death_timer'] = 0
                    game_state['death_cause'] = 'car'
                    return True
            elif car['direction'] == 'down':
                if dy > -20:
                    player_animation['state'] = 'hurt'
                    player_animation['current_frame'] = 0
                    player_animation['frame_delay'] = 0
                    game_state['alive'] = False
                    game_state['death_timer'] = 0
                    game_state['death_cause'] = 'car'
                    return True
            elif car['direction'] == 'up':
                if dy < 20:
                    player_animation['state'] = 'hurt'
                    player_animation['current_frame'] = 0
                    player_animation['frame_delay'] = 0
                    game_state['alive'] = False
                    game_state['death_timer'] = 0
                    game_state['death_cause'] = 'car'
                    return True
    
    return False

def restart_game():
                                                        
    global player, traffic_vehicles, game_state, bullets, enemies, enemy_bullets, enemy_magic, player_animation
    
                           
    player.x = 500
    player.y = 500
    
                                                       
    player_animation['direction'] = 'down'
    player_animation['current_frame'] = 0
    player_animation['frame_delay'] = 0
    player_animation['state'] = 'idle'                          
    
                        
    player_weapon['type'] = 'none'
    player_weapon['attacking'] = False
    player_weapon['shoot_animation_done'] = False
    
                       
    traffic_vehicles.clear()
    
                       
    bullets.clear()
    enemy_bullets.clear()
    enemy_magic.clear()
    
                                       
    if level_system['active']:
        current_level = level_system['current_level']
        level_system['active'] = False
        enemies.clear()
        
                                     
        player_health['current'] = player_health['max']
        
                           
        start_level(current_level)
    
                           
    game_state['alive'] = True
    game_state['death_timer'] = 0
    game_state['in_car'] = False                        
    game_state['car_type'] = None
    game_state['car_angle'] = 0
    game_state['car_speed'] = 0
    play_bgmusic()
    print("Game restarted successfully!")

                                              
                
                                              

def draw():

    import time
    
                 
    if not hasattr(draw, 'frame_times'):
        draw.frame_times = []
        draw.last_time = time.time()
    
    current_time = time.time()
    frame_time = current_time - draw.last_time
    draw.last_time = current_time
    
    draw.frame_times.append(frame_time)
    if len(draw.frame_times) > 60:
        draw.frame_times.pop(0)
    
    avg_frame_time = sum(draw.frame_times) / len(draw.frame_times)
    fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
    
                      
    screen.draw.text(f"FPS: {int(fps)}", (WIDTH - 100, 10), color="yellow", fontsize=24)



    screen.clear()

                                                       
    if game_state['show_start_menu']:
        draw_start_menu()
        return                            
    
    global camera_x, camera_y
    
    view_width = WIDTH / CAMERA_ZOOM
    view_height = HEIGHT / CAMERA_ZOOM
    
    camera_x = player.x - view_width / 2
    camera_y = player.y - view_height / 2
    
    camera_x = max(0, min(camera_x, MAP_WIDTH - view_width))
    camera_y = max(0, min(camera_y, MAP_HEIGHT - view_height))
    
    start_tile_x = max(0, int(camera_x // TILE_SIZE) - 1)
    end_tile_x = min(MAP_TILES_WIDTH, int((camera_x + view_width) // TILE_SIZE) + 2)
    start_tile_y = max(0, int(camera_y // TILE_SIZE) - 1)
    end_tile_y = min(MAP_TILES_HEIGHT, int((camera_y + view_height) // TILE_SIZE) + 2)
    
                
    for tile_y in range(start_tile_y, end_tile_y):
        for tile_x in range(start_tile_x, end_tile_x):
            tile_data = map_grid[tile_y][tile_x]
            
            world_x = tile_x * TILE_SIZE
            world_y = tile_y * TILE_SIZE
            screen_x = (world_x - camera_x) * CAMERA_ZOOM
            screen_y = (world_y - camera_y) * CAMERA_ZOOM
            
            if '|rot' in tile_data:
                parts = tile_data.split('|rot')
                tile_name = parts[0]
                rotation = int(parts[1])
            else:
                tile_name = tile_data
                rotation = 0
            
            try:
                img = get_rotated_image(tile_name, rotation)
                if img:
                    scaled_img = pygame.transform.scale(img, 
                        (int(img.get_width() * CAMERA_ZOOM) + 1, int(img.get_height() * CAMERA_ZOOM) + 1))
                    screen.blit(scaled_img, (int(screen_x), int(screen_y)))
            except:
                if 'road' in tile_name:
                    screen.draw.filled_rect(Rect(int(screen_x), int(screen_y), int(TILE_SIZE * CAMERA_ZOOM) + 1, int(TILE_SIZE * CAMERA_ZOOM) + 1), (60, 60, 60))
                elif 'sidewalk' in tile_name:
                    screen.draw.filled_rect(Rect(int(screen_x), int(screen_y), int(TILE_SIZE * CAMERA_ZOOM) + 1, int(TILE_SIZE * CAMERA_ZOOM) + 1), (100, 100, 110))
                elif 'grass' in tile_name:
                    screen.draw.filled_rect(Rect(int(screen_x), int(screen_y), int(TILE_SIZE * CAMERA_ZOOM) + 1, int(TILE_SIZE * CAMERA_ZOOM) + 1), (60, 140, 60))
    
                  
    for obj in map_objects:
        world_x = obj['x']
        world_y = obj['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
        if -200 < screen_x < WIDTH + 200 and -200 < screen_y < HEIGHT + 200:
            try:
                img = pygame.image.load(f'images/{obj["name"]}.png')
                scaled_img = pygame.transform.scale(img,
                    (int(img.get_width() * CAMERA_ZOOM), int(img.get_height() * CAMERA_ZOOM)))
                screen.blit(scaled_img, (screen_x - scaled_img.get_width()//2, screen_y - scaled_img.get_height()//2))
            except:
                if 'building' in obj['name'] or 'house' in obj['name'] or 'shop' in obj['name']:
                    screen.draw.filled_rect(Rect(screen_x-25*CAMERA_ZOOM, screen_y-40*CAMERA_ZOOM, 50*CAMERA_ZOOM, 80*CAMERA_ZOOM), (120, 100, 100))
                elif 'tree' in obj['name']:
                    screen.draw.filled_circle((int(screen_x), int(screen_y)), int(8*CAMERA_ZOOM), (50, 150, 50))
                else:
                    screen.draw.filled_rect(Rect(screen_x-5*CAMERA_ZOOM, screen_y-5*CAMERA_ZOOM, 10*CAMERA_ZOOM, 10*CAMERA_ZOOM), (150, 150, 150))
    
                                         
    for light in level_system['red_lights']:
        if light['active']:
            world_x = light['x']
            world_y = light['y']
            screen_x = (world_x - camera_x) * CAMERA_ZOOM
            screen_y = (world_y - camera_y) * CAMERA_ZOOM
            
            if -100 < screen_x < WIDTH + 100 and -100 < screen_y < HEIGHT + 100:
                                          
                import time
                pulse = abs(math.sin(time.time() * 3))
                radius = int((15 + pulse * 5) * CAMERA_ZOOM)
                screen.draw.filled_circle((int(screen_x), int(screen_y)), radius, (255, 0, 0))
                screen.draw.circle((int(screen_x), int(screen_y)), radius + 5, (255, 100, 100))

                       
    for car in traffic_vehicles:
        world_x = car['x']
        world_y = car['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
        if -200 < screen_x < WIDTH + 200 and -200 < screen_y < HEIGHT + 200:
            try:
                img = pygame.image.load(f'images/{car["name"]}.png')
                scaled_img = pygame.transform.scale(img,
                    (int(img.get_width() * CAMERA_ZOOM), int(img.get_height() * CAMERA_ZOOM)))
                rotated_car = pygame.transform.rotate(scaled_img, car['angle'])
                car_rect = rotated_car.get_rect(center=(int(screen_x), int(screen_y)))
                screen.blit(rotated_car, car_rect)
            except:
                 screen.draw.filled_rect(Rect(screen_x-10*CAMERA_ZOOM, screen_y-10*CAMERA_ZOOM, 20*CAMERA_ZOOM, 20*CAMERA_ZOOM), (200, 50, 50))

                                     
    try:
        if game_state['in_car']:
                      
            car_img = pygame.image.load(f'images/{game_state["car_type"]}.png')
            car_scale = 1.0
            scaled_car = pygame.transform.scale(car_img,
                (int(car_img.get_width() * CAMERA_ZOOM * car_scale), 
                 int(car_img.get_height() * CAMERA_ZOOM * car_scale)))
            rotated_car = pygame.transform.rotate(scaled_car, game_state['car_angle'])
            car_rect = rotated_car.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(rotated_car, car_rect)
        else:
                                
            state = player_animation['state']
            direction = player_animation['direction']
            frame = player_animation['current_frame']
            
            player_img = get_player_frame(state, direction, frame)
            
            if player_img:
                frame_size = FRAME_SIZES.get(state, 64)
                player_scale = 0.6
                
                scaled_player = pygame.transform.scale(player_img,
                    (int(frame_size * CAMERA_ZOOM * player_scale), int(frame_size * CAMERA_ZOOM * player_scale)))
                player_rect = scaled_player.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(scaled_player, player_rect)
            else:
                screen.draw.filled_circle((WIDTH // 2, HEIGHT // 2), int(10*CAMERA_ZOOM), (255, 255, 0))
    except Exception as e:
        screen.draw.filled_circle((WIDTH // 2, HEIGHT // 2), int(10*CAMERA_ZOOM), (255, 255, 0))
    
                                                 
    if player_weapon['type'] == 'gun' and GUN_CONFIG['image']:
        try:
            direction = player_animation['direction']
            gun_img = get_rotated_gun(direction)
            
            if gun_img:
                           
                gun_width = int(gun_img.get_width() * CAMERA_ZOOM * GUN_CONFIG['scale'])
                gun_height = int(gun_img.get_height() * CAMERA_ZOOM * GUN_CONFIG['scale'])
                scaled_gun = pygame.transform.scale(gun_img, (gun_width, gun_height))
                
                                     
                offset_x, offset_y = get_gun_offset(direction)
                
                                                                      
                gun_x = WIDTH // 2 + (offset_x * CAMERA_ZOOM)
                gun_y = HEIGHT // 2 + (offset_y * CAMERA_ZOOM)
                
                gun_rect = scaled_gun.get_rect(center=(gun_x, gun_y))
                screen.blit(scaled_gun, gun_rect)
        except Exception as e:
            pass

                                 
    for bullet in bullets:
        world_x = bullet['x']
        world_y = bullet['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
                                
        if -100 < screen_x < WIDTH + 100 and -100 < screen_y < HEIGHT + 100:
            try:
                if BULLET_CONFIG['image']:
                                  
                    bullet_width = int(BULLET_CONFIG['image'].get_width() * CAMERA_ZOOM * BULLET_CONFIG['scale']* 0.6)
                    bullet_height = int(BULLET_CONFIG['image'].get_height() * CAMERA_ZOOM * BULLET_CONFIG['scale']* 0.6)
                    scaled_bullet = pygame.transform.scale(BULLET_CONFIG['image'], (bullet_width, bullet_height))
                    
                                                  
                    rotated_bullet = pygame.transform.rotate(scaled_bullet, bullet['angle'])
                    bullet_rect = rotated_bullet.get_rect(center=(int(screen_x), int(screen_y)))
                    screen.blit(rotated_bullet, bullet_rect)
                else:
                                               
                    screen.draw.filled_circle((int(screen_x), int(screen_y)), 8, (255, 255, 0))
            except:
                                           
                screen.draw.filled_circle((int(screen_x), int(screen_y)), 8, (255, 255, 0))


                                                              
    visible_npcs = 0
    for npc in npcs:
        world_x = npc['x']
        world_y = npc['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
                                
        if -200 < screen_x < WIDTH + 200 and -200 < screen_y < HEIGHT + 200:
            visible_npcs += 1
            try:
                npc_img = get_npc_frame(npc['type'], npc['state'], npc['direction'], npc['current_frame'])
                
                if npc_img:
                    npc_scale = 0.5                                     
                    scaled_npc = pygame.transform.scale(npc_img,
                        (int(64 * CAMERA_ZOOM * npc_scale), int(64 * CAMERA_ZOOM * npc_scale)))
                    npc_rect = scaled_npc.get_rect(center=(int(screen_x), int(screen_y)))
                    screen.blit(scaled_npc, npc_rect)
            except:
                                        
                screen.draw.filled_circle((int(screen_x), int(screen_y)), int(8*CAMERA_ZOOM), (100, 200, 100))

                      
    for body in dead_bodies:
        world_x = body['x']
        world_y = body['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
        if -200 < screen_x < WIDTH + 200 and -200 < screen_y < HEIGHT + 200:
            try:
                                                   
                body_img = get_npc_frame(body['type'], NPC_STATE_HURT, body['direction'], NPC_FRAME_COUNTS['hurt'] - 1)
                
                if body_img:
                    npc_scale = 0.5
                    scaled_body = pygame.transform.scale(body_img,
                        (int(64 * CAMERA_ZOOM * npc_scale), int(64 * CAMERA_ZOOM * npc_scale)))
                    body_rect = scaled_body.get_rect(center=(int(screen_x), int(screen_y)))
                    screen.blit(scaled_body, body_rect)
            except:
                pass

                                           
    for enemy in enemies:
        world_x = enemy['x']
        world_y = enemy['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
        if -200 < screen_x < WIDTH + 200 and -200 < screen_y < HEIGHT + 200:
            try:
                enemy_img = get_enemy_frame(enemy['type'], enemy['state'], enemy['direction'], enemy['current_frame'])
                
                if enemy_img:
                                                   
                    config = ENEMY_CONFIG[enemy['type']]
                    if enemy['state'] == ENEMY_STATE_ATTACKING:
                        anim_name = config['attack_anim']
                    elif enemy['state'] in [ENEMY_STATE_HURT, ENEMY_STATE_DEAD]:
                        anim_name = 'hurt'
                    elif enemy['state'] == ENEMY_STATE_WALKING:
                        anim_name = 'walk'
                    else:
                        anim_name = 'idle'
                    
                    frame_size = ENEMY_FRAME_SIZES[enemy['type']].get(anim_name, 64)
                    
                    enemy_scale = 0.6 if enemy['type'] != 'boss' else 0.8
                    scaled_enemy = pygame.transform.scale(enemy_img,
                        (int(frame_size * CAMERA_ZOOM * enemy_scale), int(frame_size * CAMERA_ZOOM * enemy_scale)))
                    enemy_rect = scaled_enemy.get_rect(center=(int(screen_x), int(screen_y)))
                    screen.blit(scaled_enemy, enemy_rect)
                    
                                           
                    if enemy['type'] == 'enemy3' and GUN_CONFIG['image']:
                        direction = enemy['direction']
                        gun_img = get_rotated_gun(direction)
                        
                        if gun_img:
                            gun_scale = 0.6                     
                            gun_width = int(gun_img.get_width() * CAMERA_ZOOM * gun_scale)
                            gun_height = int(gun_img.get_height() * CAMERA_ZOOM * gun_scale)
                            scaled_gun = pygame.transform.scale(gun_img, (gun_width, gun_height))
                            
                                                  
                            offset_x, offset_y = get_gun_offset(direction)
                            gun_x = screen_x + (offset_x * CAMERA_ZOOM * 0.8)
                            gun_y = screen_y + (offset_y * CAMERA_ZOOM * 0.8)
                            
                            gun_rect = scaled_gun.get_rect(center=(gun_x, gun_y))
                            screen.blit(scaled_gun, gun_rect)
                    
                                     
                    if enemy['alive']:
                        bar_width = 40
                        bar_height = 4
                        bar_x = screen_x - bar_width // 2
                        bar_y = screen_y - 30
                        
                                          
                        screen.draw.filled_rect(Rect(bar_x, bar_y, bar_width, bar_height), (200, 0, 0))
                        
                                        
                        health_width = (enemy['health'] / enemy['max_health']) * bar_width
                        screen.draw.filled_rect(Rect(bar_x, bar_y, health_width, bar_height), (0, 200, 0))
            except Exception as e:
                          
                color = (255, 0, 0) if enemy['type'] == 'boss' else (200, 100, 0)
                screen.draw.filled_circle((int(screen_x), int(screen_y)), int(12*CAMERA_ZOOM), color)
    
                        
    for bullet in enemy_bullets:
        world_x = bullet['x']
        world_y = bullet['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
        if -100 < screen_x < WIDTH + 100 and -100 < screen_y < HEIGHT + 100:
            try:
                if BULLET_CONFIG['image']:
                                                                 
                    bullet_width = int(BULLET_CONFIG['image'].get_width() * CAMERA_ZOOM * BULLET_CONFIG['scale'] * 0.6)
                    bullet_height = int(BULLET_CONFIG['image'].get_height() * CAMERA_ZOOM * BULLET_CONFIG['scale'] * 0.6)
                    scaled_bullet = pygame.transform.scale(BULLET_CONFIG['image'], (bullet_width, bullet_height))
                    
                                                  
                    rotated_bullet = pygame.transform.rotate(scaled_bullet, bullet['angle'])
                    bullet_rect = rotated_bullet.get_rect(center=(int(screen_x), int(screen_y)))
                    screen.blit(rotated_bullet, bullet_rect)
                else:
                                               
                    screen.draw.filled_circle((int(screen_x), int(screen_y)), 8, (255, 100, 0))
            except:
                                           
                screen.draw.filled_circle((int(screen_x), int(screen_y)), 8, (255, 100, 0))
    
                      
    for magic in enemy_magic:
        world_x = magic['x']
        world_y = magic['y']
        screen_x = (world_x - camera_x) * CAMERA_ZOOM
        screen_y = (world_y - camera_y) * CAMERA_ZOOM
        
        if -100 < screen_x < WIDTH + 100 and -100 < screen_y < HEIGHT + 100:
            if magic['is_boss']:
                                                                      
                for i in range(3):
                    radius = 25 - i * 5
                    alpha_color = (150 + i * 30, 0, 150 - i * 30)
                    screen.draw.filled_circle((int(screen_x), int(screen_y)), radius, alpha_color)
            else:
                                
                screen.draw.filled_circle((int(screen_x), int(screen_y)), 15, (139, 0, 0))
    
        
    screen.draw.text(f"Traffic: {len(traffic_vehicles)}/{TRAFFIC_CONFIG['max_cars']}", (10, 10), color="cyan", fontsize=20)
    screen.draw.text(f"NPCs: {len(npcs)}/{NPC_CONFIG['max_population']}", (10, 35), color="green", fontsize=20)
                                    
    health_bar_x = WIDTH - 220
    health_bar_y = 20
    health_bar_width = 200
    health_bar_height = 30
    
                
    screen.draw.filled_rect(Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height), (60, 60, 60))
    
            
    health_percent = player_health['current'] / player_health['max']
    health_fill_width = health_bar_width * health_percent
    health_color = (0, 200, 0) if health_percent > 0.5 else (200, 200, 0) if health_percent > 0.25 else (200, 0, 0)
    screen.draw.filled_rect(Rect(health_bar_x, health_bar_y, health_fill_width, health_bar_height), health_color)
    
            
    screen.draw.rect(Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height), (255, 255, 255))
    
          
    screen.draw.text(f"HP: {int(player_health['current'])}/{player_health['max']}", 
                     (health_bar_x + 10, health_bar_y + 7), color="white", fontsize=20)
    
                     
    if level_system['active']:
        screen.draw.text(f"LEVEL {level_system['current_level']} ACTIVE", 
                        (WIDTH // 2 - 100, 20), color="red", fontsize=30)
        screen.draw.text(f"Enemies: {len([e for e in enemies if e['alive']])}", 
                        (WIDTH // 2 - 80, 55), color="yellow", fontsize=24)
    
                                           
    minimap_scale = 0.05
    minimap_offset_x = WIDTH - 210
    minimap_offset_y = HEIGHT - 210
    minimap_width = 200
    minimap_height = 200
    
                        
    screen.draw.filled_rect(Rect(minimap_offset_x, minimap_offset_y, minimap_width, minimap_height), (40, 40, 40))
    
                                    
                                                        
    for tile_y in range(0, MAP_TILES_HEIGHT, 5):
        for tile_x in range(0, MAP_TILES_WIDTH, 5):
            tile = map_grid[tile_y][tile_x]
            tile_lower = tile.lower()
            
                                        
            map_x = minimap_offset_x + (tile_x * TILE_SIZE * minimap_scale)
            map_y = minimap_offset_y + (tile_y * TILE_SIZE * minimap_scale)
            
                                                            
            if 'road' in tile_lower and 'sidewalk' not in tile_lower:
                                   
                screen.draw.filled_rect(Rect(map_x, map_y, 2, 2), (80, 80, 80))
            elif 'sidewalk' in tile_lower:
                                        
                screen.draw.filled_rect(Rect(map_x, map_y, 2, 2), (120, 120, 120))
    
                               
    for obj in map_objects:
        if 'building' in obj['name'] or 'house' in obj['name'] or 'shop' in obj['name'] or 'supermarket' in obj['name']:
            obj_minimap_x = minimap_offset_x + obj['x'] * minimap_scale
            obj_minimap_y = minimap_offset_y + obj['y'] * minimap_scale
                               
            screen.draw.filled_rect(Rect(obj_minimap_x - 1, obj_minimap_y - 1, 3, 3), (139, 90, 60))
    
                 
    screen.draw.rect(Rect(minimap_offset_x, minimap_offset_y, minimap_width, minimap_height), (255, 255, 255))
    
                                                  
    player_minimap_x = minimap_offset_x + player.x * minimap_scale
    player_minimap_y = minimap_offset_y + player.y * minimap_scale
    screen.draw.filled_circle((int(player_minimap_x), int(player_minimap_y)), 5, (0, 255, 0))
    screen.draw.circle((int(player_minimap_x), int(player_minimap_y)), 6, (255, 255, 255))
    
                                          
    import time
    pulse = abs(math.sin(time.time() * 3))
    for light in level_system['red_lights']:
        if light['active']:
            light_minimap_x = minimap_offset_x + light['x'] * minimap_scale
            light_minimap_y = minimap_offset_y + light['y'] * minimap_scale
            
                               
            light_size = int(6 + pulse * 2)
            screen.draw.filled_circle((int(light_minimap_x), int(light_minimap_y)), light_size, (255, 0, 0))
            screen.draw.circle((int(light_minimap_x), int(light_minimap_y)), light_size + 1, (255, 100, 100))
            
                                                             
            dx = light['x'] - player.x
            dy = light['y'] - player.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance > 200:                               
                                           
                angle = math.atan2(dy, dx)
                arrow_length = 15
                arrow_end_x = player_minimap_x + math.cos(angle) * arrow_length
                arrow_end_y = player_minimap_y + math.sin(angle) * arrow_length
                
                                 
                screen.draw.line((player_minimap_x, player_minimap_y), (arrow_end_x, arrow_end_y), (255, 255, 0))
                
                                 
                arrow_head_angle1 = angle + 2.8
                arrow_head_angle2 = angle - 2.8
                head_x1 = arrow_end_x + math.cos(arrow_head_angle1) * 5
                head_y1 = arrow_end_y + math.sin(arrow_head_angle1) * 5
                head_x2 = arrow_end_x + math.cos(arrow_head_angle2) * 5
                head_y2 = arrow_end_y + math.sin(arrow_head_angle2) * 5
                
                screen.draw.line((arrow_end_x, arrow_end_y), (head_x1, head_y1), (255, 255, 0))
                screen.draw.line((arrow_end_x, arrow_end_y), (head_x2, head_y2), (255, 255, 0))
    
                            
    player_minimap_x = minimap_offset_x + player.x * minimap_scale
    player_minimap_y = minimap_offset_y + player.y * minimap_scale
    screen.draw.filled_circle((int(player_minimap_x), int(player_minimap_y)), 4, (0, 255, 0))
    
                                
    for light in level_system['red_lights']:
        if light['active']:
            light_minimap_x = minimap_offset_x + light['x'] * minimap_scale
            light_minimap_y = minimap_offset_y + light['y'] * minimap_scale
            screen.draw.filled_circle((int(light_minimap_x), int(light_minimap_y)), 6, (255, 0, 0))
            
                                                 
            dx = light['x'] - player.x
            dy = light['y'] - player.y
            distance = (dx * dx + dy * dy) ** 0.5
            
            if distance > 100:                               
                                                                                 
                angle = math.atan2(dy, dx)
                arrow_x = light_minimap_x
                arrow_y = light_minimap_y
                
                                        
                screen.draw.line((player_minimap_x, player_minimap_y), (arrow_x, arrow_y), (255, 255, 0))

                          
    if not game_state['alive']:
                     
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)                    
        overlay.fill((255, 0, 0))       
        screen.blit(overlay, (0, 0))
        
                    
        screen.draw.text("YOU DIED!", center=(WIDTH // 2, HEIGHT // 2 - 50), 
                        color="white", fontsize=80)
        
                               
        death_message = "Hit by a car!"           
        if 'death_cause' in game_state:
            if game_state['death_cause'] == 'enemy':
                death_message = "Killed by enemy!"
            elif game_state['death_cause'] == 'car':
                death_message = "Hit by a car!"
        
        screen.draw.text(death_message, center=(WIDTH // 2, HEIGHT // 2 + 20), 
                        color="white", fontsize=40)
        screen.draw.text("Restarting...", center=(WIDTH // 2, HEIGHT // 2 + 80), 
                        color="yellow", fontsize=30)


def draw_start_menu():
                             
                     
    if 'background' in start_menu_images:
        bg = start_menu_images['background']
        scaled_bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))
    else:
        screen.fill((0, 0, 0))                  
    
                                         
    start_button_x = WIDTH // 2
    start_button_y = HEIGHT // 2 - 60
    exit_button_x = WIDTH // 2
    exit_button_y = HEIGHT // 2 + 60
    
                                             
    BUTTON_SCALE = 2                                                         

                       
    if menu_state['start_hover']:
        start_img = start_menu_images.get('start_hover', start_menu_images.get('start_normal'))
    else:
        start_img = start_menu_images.get('start_normal')

    if start_img:
                          
        scaled_width = int(start_img.get_width() * BUTTON_SCALE)
        scaled_height = int(start_img.get_height() * BUTTON_SCALE)
        start_img = pygame.transform.scale(start_img, (scaled_width, scaled_height))

        start_rect = start_img.get_rect(center=(start_button_x, start_button_y))
        screen.blit(start_img, start_rect)
                                               
        button_rects['start'] = start_rect

                      
    if menu_state['exit_hover']:
        exit_img = start_menu_images.get('exit_hover', start_menu_images.get('exit_normal'))
    else:
        exit_img = start_menu_images.get('exit_normal')

    if exit_img:
                          
        scaled_width = int(exit_img.get_width() * BUTTON_SCALE)
        scaled_height = int(exit_img.get_height() * BUTTON_SCALE)
        exit_img = pygame.transform.scale(exit_img, (scaled_width, scaled_height))

        exit_rect = exit_img.get_rect(center=(exit_button_x, exit_button_y))
        screen.blit(exit_img, exit_rect)
                                               
        button_rects['exit'] = exit_rect

def start_game():
                               
    game_state['show_start_menu'] = False
    game_state['game_started'] = True
    play_bgmusic()
    print("Game started!")

def update_car_sounds():
                                      
    if game_state['in_car']:
                                                              
        if music_system['carstart_playing']:
            current_time = pygame.time.get_ticks()
            if current_time - music_system['carstart_start_time'] >= music_system['carstart_duration']:
                                                     
                try:
                    music_system['drive_channel'] = sounds.drive.play(loops=-1)                
                    music_system['carstart_playing'] = False
                except:
                    pass

def update():
    global player

                                                       
    if game_state['show_start_menu']:
        return
    
    update_car_sounds() 
    
                                                     
    if player_animation['state'] == 'hurt':
        player_animation['frame_delay'] += 1
        
        if player_animation['frame_delay'] >= player_animation['animation_speed']:
            player_animation['frame_delay'] = 0
            player_animation['current_frame'] += 1
            
                                                                       
            if player_animation['current_frame'] >= FRAME_COUNTS['hurt']:
                if not game_state['alive']:
                                                      
                    player_animation['current_frame'] = FRAME_COUNTS['hurt'] - 1                      
                else:
                                             
                    player_animation['current_frame'] = 0
                    player_animation['state'] = 'idle'
    
                              
    if not game_state['alive']:
        game_state['death_timer'] += 1
        if game_state['death_timer'] == 1:                                          
            stop_all_sounds()                   
            try:
                sounds.gameover.play()                        
            except:
                pass
        if game_state['death_timer'] >= game_state['death_delay']:
            restart_game()
        return                                        
    
                    
    update_traffic()

                                 
    update_npcs()

                          
    update_enemies()
    check_enemy_traffic_collision()                 
    make_npcs_flee_from_enemies()
    check_player_red_light_collision()
    
                                                    
    if not game_state['in_car']:
        if check_collision_with_cars():
            game_state['alive'] = False
            game_state['death_timer'] = 0
            return
    
                          
    if keyboard.k_1:
        player_weapon['type'] = 'none'
        player_weapon['shoot_animation_done'] = False
    if keyboard.k_2:
        player_weapon['type'] = 'katana'
        player_weapon['shoot_animation_done'] = False
    if keyboard.k_3:
        player_weapon['type'] = 'gun'
        player_weapon['shoot_animation_done'] = False
                               
        player_animation['state'] = 'shoot'
        player_animation['current_frame'] = 0
        player_animation['frame_delay'] = 0

        
                                                       
    if player_weapon['type'] == 'katana' and player_weapon['attacking']:
                                   
        player_animation['frame_delay'] += 1
        
        if player_animation['frame_delay'] >= player_animation['animation_speed']:
            player_animation['frame_delay'] = 0
            player_animation['current_frame'] += 1
            
                                                  
            if player_animation['current_frame'] in [2, 3, 4]:
                check_katana_hit_npcs()                    
                check_katana_hit_enemies()                       
            
                                       
            if player_animation['current_frame'] >= FRAME_COUNTS['slash_katana']:
                player_weapon['attacking'] = False
                player_animation['current_frame'] = 0
        
        return                                                

                     
    if 'e_pressed' not in game_state:
        game_state['e_pressed'] = False
        game_state['e_cooldown'] = 0
    
    if game_state['e_cooldown'] > 0:
        game_state['e_cooldown'] -= 1
    
    if keyboard.e and game_state['e_cooldown'] == 0:
        if not game_state['in_car']:
                                      
            nearest_car = find_nearest_car()
            if nearest_car:
                enter_car(nearest_car)
                game_state['e_cooldown'] = 30                
                print(f"ENTERED CAR: {game_state['car_type']}")
        else:
                      
            exit_car()
            game_state['e_cooldown'] = 30
            print("EXITED CAR")
    
                                                                     
    if player_weapon['type'] == 'gun' and player_animation['state'] == 'shoot' and not player_weapon['shoot_animation_done']:
        player_animation['frame_delay'] += 1
        
        if player_animation['frame_delay'] >= player_animation['animation_speed']:
            player_animation['frame_delay'] = 0
            player_animation['current_frame'] += 1
            
                                         
            if player_animation['current_frame'] >= FRAME_COUNTS['shoot']:
                                    
                player_animation['current_frame'] = FRAME_COUNTS['shoot'] - 1
                player_weapon['shoot_animation_done'] = True
    
                    
    update_bullets()

                        
    if game_state['in_car']:
        moving = False
        
                                    
        if keyboard.a:
            game_state['car_angle'] += 3
            moving = True
        if keyboard.d:
            game_state['car_angle'] -= 3
            moving = True
        
                      
        if keyboard.s:
            moving = True
                                               
            angle_rad = math.radians(game_state['car_angle'])
            dx = -math.sin(angle_rad) * game_state['car_speed']
            dy = -math.cos(angle_rad) * game_state['car_speed']
            
            new_x = player.x + dx
            new_y = player.y + dy
            
                                                                 
            old_x, old_y = player.x, player.y
            player.x, player.y = new_x, new_y
            
                                      
            if not check_object_collision(new_x, new_y, radius=15) and not check_player_car_traffic_collision():
                                   
                if 0 < new_x < MAP_WIDTH and 0 < new_y < MAP_HEIGHT:
                    pass                 
                else:
                    player.x, player.y = old_x, old_y                            
            else:
                                                            
                player.x, player.y = old_x, old_y
        
        if keyboard.w:
            moving = True
                     
            angle_rad = math.radians(game_state['car_angle'])
            dx = math.sin(angle_rad) * (game_state['car_speed'] * 0.5)
            dy = math.cos(angle_rad) * (game_state['car_speed'] * 0.5)
            
            new_x = player.x + dx
            new_y = player.y + dy
            
                                                                 
            old_x, old_y = player.x, player.y
            player.x, player.y = new_x, new_y
            
            if not check_object_collision(new_x, new_y, radius=15) and not check_player_car_traffic_collision():
                if 0 < new_x < MAP_WIDTH and 0 < new_y < MAP_HEIGHT:
                    pass                 
                else:
                    player.x, player.y = old_x, old_y
            else:
                player.x, player.y = old_x, old_y
        
        return                                           
    
    else:
                                                   
        moving = False
        dx, dy = 0, 0
        
                                               
        is_running = keyboard.lshift or keyboard.rshift
        current_speed = player_run_speed if is_running else player_walk_speed
        
        if keyboard.w:
            dy = -current_speed
            player_animation['direction'] = 'up'
            moving = True
        if keyboard.s:
            dy = current_speed
            player_animation['direction'] = 'down'
            moving = True
        if keyboard.a:
            dx = -current_speed
            player_animation['direction'] = 'left'
            moving = True
        if keyboard.d:
            dx = current_speed
            player_animation['direction'] = 'right'
            moving = True
        
                                             
        if player_weapon['attacking']:
            return                                                 
        
                                   
        if moving:
                                                                    
            if is_running:
                update_player_animation('run', player_animation['direction'])
            else:
                                                                           
                if player_weapon['type'] == 'katana':
                    update_player_animation('walk_katana', player_animation['direction'])
                else:
                    update_player_animation('walk', player_animation['direction'])
            
                                                                                         
            if player_weapon['type'] == 'gun':
                player_weapon['shoot_animation_done'] = False
        else:
                                   
            if player_weapon['type'] == 'gun':
                                                                    
                if not player_weapon['shoot_animation_done']:
                    player_animation['state'] = 'shoot'
                                                                                    
            else:
                update_player_animation('idle', player_animation['direction'])

                        
        if moving:
            new_x = player.x + dx
            new_y = player.y + dy

                        
            if dx != 0:
                test_x = player.x + dx
                test_y = player.y
                
                collision_checks_x = (
                    not check_player_car_collision(test_x, test_y) and
                    not check_npc_player_collision(test_x, test_y) and
                    not check_object_collision(test_x, test_y, radius=8)
                )
                
                if collision_checks_x and 0 < test_x < MAP_WIDTH:
                    player.x = test_x
            
                         
            if dy != 0:
                test_x = player.x
                test_y = player.y + dy
                
                collision_checks_y = (
                    not check_player_car_collision(test_x, test_y) and
                    not check_npc_player_collision(test_x, test_y) and
                    not check_object_collision(test_x, test_y, radius=8)
                )
                
                if collision_checks_y and 0 < test_y < MAP_HEIGHT:
                    player.y = test_y

def on_mouse_move(pos):
                                                
    if not game_state['show_start_menu']:
        return
    
    mouse_x, mouse_y = pos
    
                                         
    if 'start' in button_rects:
        menu_state['start_hover'] = button_rects['start'].collidepoint(mouse_x, mouse_y)
    
                                        
    if 'exit' in button_rects:
        menu_state['exit_hover'] = button_rects['exit'].collidepoint(mouse_x, mouse_y)

def on_mouse_down(pos, button):
                             

                              
    if game_state['show_start_menu']:
        mouse_x, mouse_y = pos
        
        if button == mouse.LEFT:
                                
            if 'start' in button_rects and button_rects['start'].collidepoint(mouse_x, mouse_y):
                start_game()
                return
            
                               
            if 'exit' in button_rects and button_rects['exit'].collidepoint(mouse_x, mouse_y):
                import sys
                sys.exit()
                return
        
        return                                            
                        
    if not game_state['alive'] or game_state['in_car']:
        return
    
    if button == mouse.LEFT:
        if player_weapon['type'] == 'katana' and not player_weapon['attacking']:
                                 
            try:
                sounds.katana.play()                     
            except:
                pass
            player_weapon['attacking'] = True
            player_animation['state'] = 'slash_katana'
            player_animation['current_frame'] = 0
            player_animation['frame_delay'] = 0
        
        elif player_weapon['type'] == 'gun':
                          
            spawn_bullet()
                                                 
            player_weapon['shoot_animation_done'] = False
            player_animation['state'] = 'shoot'
            player_animation['current_frame'] = 0
            player_animation['frame_delay'] = 0


pgzrun.go()
