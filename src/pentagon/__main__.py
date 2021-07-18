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


class Field:
    """Defines the limitations of the play field."""

    MIN_POSITION: int = 0
    MAX_POSITION: int = 360


class Character:
    """Holds position data."""

    position: int = 0


def position_character():
    """Positions the character in an arc around a set point."""
    pass


def move_character():
    """Move the character along a virtual 1D line."""
    pass


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
    screen.fill(black)

    # main game loop
    done = 0
    while not done:
        draw_stars(screen, stars, black)
        move_stars(stars)
        draw_stars(screen, stars, white)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                WINCENTER[:] = list(e.pos)

        # Move the center of the screen around, yay.
        pressed_keys: list[bool] = pg.key.get_pressed()
        if pressed_keys[pg.K_LEFT]:
            WINCENTER[0] -= 1
        if pressed_keys[pg.K_RIGHT]:
            WINCENTER[0] += 1
        if pressed_keys[pg.K_UP]:
            WINCENTER[1] -= 1
        if pressed_keys[pg.K_DOWN]:
            WINCENTER[1] += 1

        clock.tick(50)
    pg.quit()


if __name__ == "__main__":
    main()
