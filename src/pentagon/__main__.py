#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""

import random
import math
import numpy as np
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


def create_obstacle(obstacle_positions: list[int], obstacle_segments: list[int]):
    index = 0
    for obstacle in obstacle_positions:
        index += 1
        if obstacle == -1:
            obstacle = 1

    # Match the index of the new obstacle position so that we're using the same index.
    # Use this for positioning around the octagon.
    obstacle_segments[index]


def update_obstacle_progress(obstacle_positions, amount: int):
    for obstacle in obstacle_positions:
        obstacle += amount


def draw_circle(surface, color, x, y):
    """ Draws a simple circle representing the character. """
    pg.draw.circle(surface, color, (WINCENTER[0] + x, WINCENTER[1] + y), 10)


def update_fps(clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pg.Color("coral"))
    return fps_text


def generate_octagon_unit_verticies(num_sides: int) -> list[tuple[int, int]]:
    step = 2 * math.pi / num_sides
    shift = (math.pi / 180.0) * 45 * 0.5

    points: tuple[int, int] = list()
    for i in range(0, num_sides):
        segment = i * step + shift
        points.append((math.cos(segment), math.sin(segment)))

    return points


def translate_octagon_vertices_to_screen_space(
    unit_space_points: list[tuple[int, int]], offset: int
) -> list[tuple[int, int]]:
    translated_points: tuple[int, int] = list()
    for point in unit_space_points:
        translated_points.append(
            (point[0] * offset + WINCENTER[0], point[1] * offset + WINCENTER[1])
        )

    return translated_points


def draw_octagon_in_center(screen, color, offset: int, segment_count: int):
    points: tuple[int, int] = generate_octagon_unit_verticies(segment_count)

    translated_points: tuple[int, int] = translate_octagon_vertices_to_screen_space(
        points, offset
    )

    pg.draw.polygon(screen, color, translated_points, 1)


def calculate_segments(
    screen, offset: int, segment_count: int, colors: list[pg.Color],
):
    points: tuple[int, int] = generate_octagon_unit_verticies(segment_count)

    length = 10

    index: int = 0
    for point in points:
        pg.draw.line(
            screen,
            colors[index],
            (point[0] * offset + WINCENTER[0], point[1] * offset + WINCENTER[1]),
            (
                point[0] * offset * length + WINCENTER[0],
                point[1] * offset * length + WINCENTER[1],
            ),
            1,
        )

        index += 1


def lerp(norm: int, min: int, max: int):
    return max - min * norm + min


def main():
    "This is the starfield code"

    # Create our field and character
    character: Character = Character()
    field: Field = Field()

    # create our starfield
    random.seed()
    clock = pg.time.Clock()

    # initialize and prepare screen
    pg.init()
    screen = pg.display.set_mode(WINSIZE)
    pg.display.set_caption("Ultimate Pentagon")

    # Colors
    # white: tuple[int, int, int] = (255, 240, 200)
    black: tuple[int, int, int] = (20, 20, 40)
    red: tuple[int, int, int] = (255, 0, 0)
    green: tuple[int, int, int] = (0, 255, 0)

    screen.fill(black)

    clock = pg.time.Clock()
    font = pg.font.SysFont("Arial", 18)

    # Where 1 is outside of the screen, and 0 is at the center of the screen.
    # obstacle_positions: list[int] = [-1]

    # Where 0 through 7 are the segments of an octagon.
    # obstacle_sections: list[int] = [-1]

    accumulated_time = 0
    # total_spawned_obstacles = 0
    segment_count = 8

    colors: list[pg.Color] = list()
    for _ in range(segment_count):
        colors.append(pg.Color(np.random.choice(range(256), size=3)))

    # main game loop
    done = 0
    while not done:
        dt = clock.tick(120)
        accumulated_time += dt

        screen.fill(black)
        offset = 40

        # if accumulated_time > (total_spawned_obstacles * 2000) + 2000:
        # create_obstacle(obstacle_positions, obstacle_sections)

        draw_octagon_in_center(screen, green, offset, segment_count)

        calculate_segments(screen, offset, segment_count, colors)

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
