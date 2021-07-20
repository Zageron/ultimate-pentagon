#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

import random
import math
import pygame as pg

# constants
WINSIZE = [640, 640]
WINCENTER = [320, 320]
NUMSTARS = 10


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


def update_fps(clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pg.Color("coral"))
    return fps_text


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
    green = (0, 255, 0)
    screen.fill(black)

    clock = pg.time.Clock()
    font = pg.font.SysFont("Arial", 18)

    # main game loop
    done = 0
    while not done:
        dt = clock.tick(120)
        screen.fill(black)
        offset = 40

        # Generate points
        length_of_side_point = math.sqrt(2) / 2

        original_points = [
            (0, 1),
            (length_of_side_point, length_of_side_point),
            (1, 0),
            (length_of_side_point, -length_of_side_point),
            (0, -1),
            (-length_of_side_point, -length_of_side_point),
            (-1, 0),
            (-length_of_side_point, length_of_side_point),
        ]
        translated_points = list()
        for point in original_points:
            translated_points.append(
                (point[0] * offset + WINCENTER[0], point[1] * offset + WINCENTER[1])
            )

        pg.draw.polygon(screen, green, translated_points, 1)

        x, y = field.get_position(character)
        draw_circle(screen, red, x, y)
        screen.blit(update_fps(clock, font), (10, 0))

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
