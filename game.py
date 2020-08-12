"""
Game Driver for the space invaders game
"""

# Pygame and Game objects
import random
import pygame
from aliens import NormalAlien, BossAlien
from config import HEIGHT, WIDTH, FPS, SCREEN_PAUSE, ALIENS_TO_KILL_BEFORE_BOSS
from config import battle_field, RESPAWN_TIME_ALIEN
from config import channel_music, music_normal_mode, music_boss_mode
from explosions import Explosion
from missiles import NormalMissile, PowerfulMissile, AlienMissile, BossMissile, GuidedMissile
from score import Score
from spaceship import SpaceShip


# ###################################################################################
# Helper Functions
# ###################################################################################
def spawn_missile(spaceship_position, missile_type):
    """
    Add a missile to the missiles group based on spaceship_position
    Input: (spaceship_position:<pygame rect object>, missile_type:<str>)
    Output: Boolean, whether the missile was added or not
    """
    if missile_type in (BossMissile, GuidedMissile):
        missile = missile_type(spaceship_position, hero.rect)
    else:
        missile = missile_type(spaceship_position)
    # prevent missiles collision
    colliding_with_missiles = pygame.sprite.spritecollideany(missile, missiles)
    if colliding_with_missiles:
        missile.kill()
        return False
    else:
        if (isinstance(missile, AlienMissile) or 
            isinstance(missile, BossMissile) or
            isinstance(missile, GuidedMissile)):
            missiles_alien.add(missile)
        else:
            missiles.add(missile)
        return True


def spawn_alien(time_elapsed):
    """
    Add an alien to the battle_field in the top two rows.
    """
    dt = clock_alien.tick()
    time_elapsed += dt
    if time_elapsed > RESPAWN_TIME_ALIEN:
        time_elapsed = 0
        alien = NormalAlien(100, 100)  # Dummy alien
        collisions = True
        while collisions:  # TODO: this is just a hack, need changes
            alien.kill()
            x = random.randint(0, WIDTH - 50)
            y = random.randint(0, 100)
            alien = NormalAlien(x, y)
            collisions = pygame.sprite.spritecollideany(alien, aliens)
        aliens.add(alien)

    return time_elapsed


def scroll_background(position):
    """
    Scroll Background for movement effect
    """
    position_relative = position % background.get_rect().height
    battle_field.blit(background, (0, position_relative -
                      background.get_rect().height))
    if position_relative < HEIGHT:
        battle_field.blit(background, (0, position_relative))

    return position + 1


def update_sprites(sprite_groups):
    """
    Call the update functions on the sprite groups and draw them on battlefield
    """
    health.score = hero.health
    ammo_left.score = hero.ammo_powerful
    for sprite_group in sprite_groups:
        sprite_group.update()
        sprite_group.draw(battle_field)


def resolve_alien_missile_collisions():
    """
    Game logic for alien and missiles collision
    """
    for alien in aliens:
        collisions = pygame.sprite.spritecollide(alien, missiles, False)
        if collisions:
            for missile in collisions:
                alien.hit(missile.damage)
                missile.kill()
                if alien.health <= 0:
                    explosion = Explosion(alien.rect.center)
                    explosions.add(explosion)
                    alien.kill()
                    score.score += 1


def resolve_spaceship_missile_collisions():
    """
    Game logic for spaceship and alien missiles collision
    """
    collisions = pygame.sprite.spritecollide(hero, missiles_alien, False)
    for missile in collisions:
        hero.hit(missile.damage)
        if isinstance(missile, BossMissile) or isinstance(missile, GuidedMissile):
            explosion = Explosion(missile.rect.center)
            explosions.add(explosion)
        missile.kill()
    game_over = True if hero.health <= 0 else False
    return game_over


def resolve_missile_missile_collisions():
    """
    Game logic for collisions between spaceship missiles and alien missiles
    """
    # missile missile collisions
    for missile in missiles:
        collisions = pygame.sprite.spritecollide(missile, missiles_alien, True)
        if collisions:
            missile.kill()


def pause_screen(pause):
    """
    Pause the screen until "P" is pressed.
    """
    while pause:
        battle_field.blit(SCREEN_PAUSE, (0, 0))
        pygame.display.flip()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_q:
                    pygame.quit()

    return pause


def play_music(music):
    """
    Play given music in the music channel indefinitely
    """
    channel_music.stop()  # stop if any music is already playing
    channel_music.play(music, loops = -1)


def boss_battle():
    channel_music.stop()
    channel_music.play(music_boss_mode, loops=-1)
    aliens.empty()
    boss = BossAlien(WIDTH//2, 20)
    aliens.add(boss)

# ###################################################################################
# Helper Functions End
# ###################################################################################

# ###################################################################################
# Game initialization
# ###################################################################################
pygame.init()
# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()
# area which displays game and score

background = pygame.image.load("assets/background.jpg").convert()
position = HEIGHT

hero = SpaceShip()
spaceships = pygame.sprite.Group()  # For multiplayer support
spaceships.add(hero)  # single player for now

missiles = pygame.sprite.Group()
missiles_alien = pygame.sprite.Group()

aliens = pygame.sprite.Group()
clock_alien = pygame.time.Clock()  # used to keep track of alien respawn
time_elapsed = spawn_alien(RESPAWN_TIME_ALIEN)  # start game with one alien


explosions = pygame.sprite.Group()

scores = pygame.sprite.Group()  # For multiplayer support
score = Score("Score", 0, HEIGHT - 30)
scores.add(score)
health = Score("Health", WIDTH - 200, HEIGHT - 30)
scores.add(health)
ammo_left = Score("Heavy Ammo", WIDTH//2 - 150, HEIGHT - 30)
scores.add(ammo_left)

game_over = False
pause = True
game_mode = "normal"
kill_counter = ALIENS_TO_KILL_BEFORE_BOSS
# cue the music!
play_music(music_normal_mode)

# ###################################################################################
# Game initialization End
# ###################################################################################

# ###################################################################################
# Game Loop
# ###################################################################################
def game_loop(mode):

    # resolve all collisions
    resolve_alien_missile_collisions()
    game_over = resolve_spaceship_missile_collisions()
    resolve_missile_missile_collisions()

    # finally update all sprites and draw them
    update_sprites([
        spaceships,
        aliens,
        missiles,
        missiles_alien,
        explosions,
        scores
    ])

    pygame.display.flip()  # Just do one thing, update/flip.
    clock.tick(FPS)  # to control FPS
    return game_over

# game logic
while not game_over:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
            pause = not pause
        elif event.key == pygame.K_q:
            pygame.quit()

    # check if player wants to pause and set pause accordingly
    pause = pause_screen(pause)

    # update position and scroll background
    position = scroll_background(position)

    # update time for spawning alien and spawn an alien
    if game_mode == "normal":
        time_elapsed = spawn_alien(time_elapsed)
    if game_mode == "boss" and not aliens:
        game_mode = "normal"
        kill_counter += ALIENS_TO_KILL_BEFORE_BOSS

    if score.score / kill_counter > 1 and game_mode == "normal":
        game_mode = "boss"
        boss_battle()

    game_over = game_loop(game_mode)
    
# ###################################################################################
# Game loop End
# ###################################################################################

# ###################################################################################
# Game Cleanup
# TODO: Maintain a record of high scores
# ###################################################################################
pygame.quit()
# ###################################################################################
# Game Cleanup End
# ###################################################################################
