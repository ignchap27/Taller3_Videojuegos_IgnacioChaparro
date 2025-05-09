import math
import random
import pygame
import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity

def create_sprite(world:esper.World, pos:pygame.Vector2, vel:pygame.Vector2, surface:pygame.Surface):
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    
    return sprite_entity

def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    if enemy_info["image"] == 'assets/img/enemy.png':
        # Create Hunter enemy
        enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
        # Calculate the width of a single frame
        frame_width = enemy_surface.get_width() / enemy_info["animations"]["number_frames"]
        frame_height = enemy_surface.get_height()
        
        # Adjust position to center the enemy
        adjusted_pos = pygame.Vector2(
            pos.x - frame_width / 2,
            pos.y - frame_height / 2
        )
        
        enemy_entity = create_sprite(world, adjusted_pos, pygame.Vector2(0, 0), enemy_surface)
        
        
        world.add_component(enemy_entity, CTagEnemy())
        world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
        world.add_component(enemy_entity, 
                            CEnemyHunterState(
                                pos,
                                enemy_info["distance_start_chase"],
                                enemy_info["distance_start_return"],
                                enemy_info["velocity_chase"],
                                enemy_info["velocity_return"]
                            ))
    else:
        # Create regular enemy (asteroid)
        enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
        ServiceLocator.sounds_service.play(enemy_info["sound"])
        vel_max = enemy_info["velocity_max"]
        vel_min = enemy_info["velocity_min"]
        vel_range = random.randrange(vel_min, vel_max)
        velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
        enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
        world.add_component(enemy_entity, CTagEnemy())


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0] / 2),
                         player_lvl_info["position"]["y"] - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity,
                        CAnimation(player_info["animations"]))
    world.add_component(player_entity,
                        CPlayerState())
    
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", [pygame.K_a, pygame.K_LEFT]))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", [pygame.K_d, pygame.K_RIGHT]))
    world.add_component(input_up,
                        CInputCommand("PLAYER_UP", [pygame.K_w, pygame.K_UP]))
    world.add_component(input_down,
                        CInputCommand("PLAYER_DOWN", [pygame.K_s, pygame.K_DOWN]))

    input_fire = world.create_entity()
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", [pygame.BUTTON_LEFT]))
    
    input_pause = world.create_entity()
    world.add_component(input_pause,
                        CInputCommand("PAUSE_GAME", [pygame.K_p]))

def create_bullet(world: esper.World,
                  mouse_pos: pygame.Vector2,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size

    pos = pygame.Vector2((player_pos.x + player_size[0] / 2) - (bullet_size[0] / 2), 
                         (player_pos.y + player_size[1] / 2) - (bullet_size[1] / 2))
    
    direccion = (mouse_pos - player_pos)
    direccion = direccion.normalize()
    vel = direccion * bullet_info["velocity"]

    bullet_entity = create_sprite(world,pos, vel, bullet_surface)
    ServiceLocator.sounds_service.play(bullet_info["sound"])
    world.add_component(bullet_entity, CTagBullet())
    
def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_cfg: dict):
    explosion_surface = ServiceLocator.images_service.get(explosion_cfg["image"])
    explosion_entity = create_sprite(world, pos, pygame.Vector2(0, 0), explosion_surface)
    world.add_component(explosion_entity, CAnimation(explosion_cfg["animations"]))
    world.add_component(explosion_entity, CTagExplosion())
    ServiceLocator.sounds_service.play(explosion_cfg["sound"])
    # Start the explosion animation
    c_anim = world.component_for_entity(explosion_entity, CAnimation)
    c_anim.curr_frame = c_anim.animations_list[0].start
    c_anim.curr_anim_time = 0
    return explosion_entity
