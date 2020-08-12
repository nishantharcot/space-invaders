# All Parameters
import os
import pygame

pygame.init()

# Game
HEIGHT = 720
WIDTH = 720
BLOCK_SIZE = 10  # pixels
SHOW_GRID = False
BACKGROUND_COLOR = (255, 255, 255)  # white
FPS = 60
basicfont = pygame.font.SysFont(None, 48)
SCREEN_PAUSE = pygame.image.load("assets/pause.jpg")
ALIENS_TO_KILL_BEFORE_BOSS = 10

# Aliens
MAX_HEALTH_ALIEN = 1000
RESPAWN_TIME_ALIEN = 3000  # milli seconds

# Missiles
DAMAGE_NORMAL = 100
DAMAGE_POWERFUL = MAX_HEALTH_ALIEN
DAMAGE_ALIEN = 10

# Explosions
battle_field = pygame.display.set_mode((WIDTH, HEIGHT))
IMGS_EXPLOSION = [pygame.image.load(os.path.join('assets/explosions', img))
                  .convert_alpha()
                  for img in os.listdir('assets/explosions')]

# Spaceship
HERO_MAX_LIFE = 1000
AMMO_NORMAL = float("inf")
AMMO_POWERFUL = 10

# Sounds
pygame.mixer.init()
sound_shoot = pygame.mixer.Sound("assets/shoot.ogg")
sound_explosion = pygame.mixer.Sound("assets/explosion.ogg")
sound_hero_hit = pygame.mixer.Sound("assets/hero_hit.ogg")
music_normal_mode = pygame.mixer.Sound('assets/offlimits.ogg')
music_boss_mode = pygame.mixer.Sound('assets/boss.ogg')

# The default number of channels is 8.
# So if you need to go higher set it below.
pygame.mixer.set_num_channels(16)
channel_music = pygame.mixer.Channel(0)
channel_hero_bullets = pygame.mixer.Channel(1)
channel_hero_hit = pygame.mixer.Channel(2)
channels_explosion = [pygame.mixer.Channel(i) for i in range(3, 11)]
