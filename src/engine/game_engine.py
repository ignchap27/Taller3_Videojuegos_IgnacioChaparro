import json
import pygame
import esper

from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_input import system_input
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.create.prefab_creator import (
    create_enemy_spawner,
    create_input_player,
    create_player_square,
    create_bullet,
)


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), pygame.SCALED
        )

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(
            self.window_cfg["bg_color"]["r"],
            self.window_cfg["bg_color"]["g"],
            self.window_cfg["bg_color"]["b"],
        )
        self.ecs_world = esper.World()

        self.num_bullets = 0

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(
            self.ecs_world, self.player_cfg, self.level_01_cfg["player_spawn"]
        )
        self._player_c_v = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity
        )
        self._player_c_t = self.ecs_world.component_for_entity(
            self._player_entity, CTransform
        )
        self._player_c_s = self.ecs_world.component_for_entity(
            self._player_entity, CSurface
        )
        self._player_tag = self.ecs_world.component_for_entity(
            self._player_entity, CTagPlayer
        )

        create_enemy_spawner(self.ecs_world, self.level_01_cfg)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0
        if self.delta_time > 1 / 30:
            self.delta_time = 1 / 30

    def _process_events(self):
        for event in pygame.event.get():
            system_input(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.enemies_cfg, self.delta_time)
        system_movement(self.ecs_world, self.delta_time)

        system_screen_bounce(self.ecs_world, self.screen)
        system_screen_player(
            self.ecs_world, self.player_cfg["input_velocity"], self.screen
        )
        system_screen_bullet(self.ecs_world, self.screen)

        system_collision_enemy_bullet(self.ecs_world)
        system_collision_player_enemy(
            self.ecs_world, self._player_entity, self.level_01_cfg
        )

        self.ecs_world._clear_dead_entities()
        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            self._player_tag.left = c_input.phase == CommandPhase.START
        if c_input.name == "PLAYER_RIGHT":
            self._player_tag.right = c_input.phase == CommandPhase.START
        if c_input.name == "PLAYER_UP":
            self._player_tag.up = c_input.phase == CommandPhase.START
        if c_input.name == "PLAYER_DOWN":
            self._player_tag.down = c_input.phase == CommandPhase.START

        if (
            c_input.name == "PLAYER_FIRE"
            and self.num_bullets < self.level_01_cfg["player_spawn"]["max_bullets"]
            and c_input.phase == CommandPhase.START
        ):
            create_bullet(
                self.ecs_world,
                c_input.mouse_pos,
                self._player_c_t.pos,
                self._player_c_s.surf.get_size(),
                self.bullet_cfg,
            )
