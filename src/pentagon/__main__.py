#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

import random
import math
import pygame as pg

# constants
WINSIZE = [640, 480]
WINCENTER = [320, 240]
NUMSTARS = 150


class Character:
    """Holds position data."""

    position: int = 0
    MIN_POSITION: int = 0
    MAX_POSITION: int = 360
    RANGE: int = MAX_POSITION - MIN_POSITION
    INV_RANGE: int = 1 / RANGE

    def __init__(self, new_position=0) -> None:
        """ Initialize a character at the initial position. """
        self.position = new_position

    def move(self, distance: int) -> None:
        """Move the character along a virtual 1D line."""
        self.position += distance
        self.position = self.position - (
            self.RANGE * math.floor(distance * self.INV_RANGE)
        )


class Field:
    """Defines the limitations of the play field."""

    RADIUS: int = 60

    def get_position(self, character: Character) -> tuple[int, int]:
        """Positions the character in an arc around a set point."""
        x = self.RADIUS * math.sin(math.radians(character.position))
        y = self.RADIUS * math.cos(math.radians(character.position))

        return x, y


def init_star():
    "creates new star values"
    dir = random.randrange(100000)
    velmult = random.random() * 0.6 + 0.4
    vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]
    return vel, WINCENTER[:]


def initialize_stars():
    "creates a new starfield"
    stars = []
    for x in range(NUMSTARS):
        star = init_star()
        vel, pos = star
        steps = random.randint(0, WINCENTER[0])
        pos[0] = pos[0] + (vel[0] * steps)
        pos[1] = pos[1] + (vel[1] * steps)
        vel[0] = vel[0] * (steps * 0.09)
        vel[1] = vel[1] * (steps * 0.09)
        stars.append(star)
    move_stars(stars)
    return stars


def draw_stars(surface, stars, color):
    "used to draw (and clear) the stars"
    for vel, pos in stars:
        pos = (int(pos[0]), int(pos[1]))
        surface.set_at(pos, color)


def draw_circle(surface, color, x, y):
    """ Draws a simple circle representing the character. """
    pg.draw.circle(surface, color, (WINCENTER[0] + x, WINCENTER[1] + y), 10)


def move_stars(stars):
    "animate the star values"
    for vel, pos in stars:
        pos[0] = pos[0] + vel[0]
        pos[1] = pos[1] + vel[1]
        if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
            vel[:], pos[:] = init_star()
        else:
            vel[0] = vel[0] * 1.05
            vel[1] = vel[1] * 1.05


def main():
    "This is the starfield code"

    # Create our field and character
    character: Character = Character()
    field: Field = Field()

    # create our starfield
    random.seed()
    stars = initialize_stars()
    clock = pg.time.Clock()
    # initialize and prepare screen
    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("pygame Stars Example")
    white = 255, 240, 200
    black = 20, 20, 40
    red = 255, 0, 0
    screen.fill(black)

    # main game loop
    done = 0
    while not done:
        dt = clock.tick(60)

        screen.fill(black)
        draw_stars(screen, stars, black)
        move_stars(stars)
        draw_stars(screen, stars, white)

        x, y = field.get_position(character)
        draw_circle(screen, red, x, y)

        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break

        # Move the center of the screen around, yay.
        pressed_keys: list[bool] = pg.key.get_pressed()
        if pressed_keys[pg.K_LEFT]:
            character.move(0.25 * dt)
        if pressed_keys[pg.K_RIGHT]:
            character.move(-0.25 * dt)
    pg.quit()


if __name__ == "__main__":
    main()
