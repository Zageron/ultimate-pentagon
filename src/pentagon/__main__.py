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


def generate_octagon_unit_verticies() -> list[tuple[int, int]]:
    num_sides = 8
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


def draw_octagon_in_center(screen, color, offset: int):
    points: tuple[int, int] = generate_octagon_unit_verticies()

    translated_points: tuple[int, int] = translate_octagon_vertices_to_screen_space(
        points, offset
    )

    pg.draw.polygon(screen, color, translated_points, 1)


def calculate_segments(screen, offset: int):
    points: tuple[int, int] = generate_octagon_unit_verticies()

    translated_points: tuple[int, int] = translate_octagon_vertices_to_screen_space(
        points, offset
    )

    # Middle bottom right line
    line0 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[0]),
        (translated_points[0][0] + 0.1 * 40, translated_points[0][1] + .1 * 100),
        1,
    )

    # Bottom right line
    line1 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[1]),
        (translated_points[0][0] + 1500, translated_points[0][1] + 2000),
        1,
    )

    segment1 = [line0, line1]

    # Bottom left line
    line2 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[2]),
        (translated_points[0][0] + -300, translated_points[0][1] + 1000),
        1,
    )

    # Middle bottom left line
    line3 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[3]),
        (translated_points[0][0] + -1500, translated_points[0][1] + 1500),
        1,
    )

    segment2 = [line2, line3]

    # Middle top left line
    line4 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[4]),
        (translated_points[0][0] + -9500, translated_points[0][1] + -3000),
        1,
    )

    # Top left line
    line5 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[5]),
        (translated_points[0][0] + -9500, translated_points[0][1] + -9500),
        1,
    )

    segment3 = [line4, line5]

    # Top right line
    line6 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[6]),
        (translated_points[0][0] + 400, translated_points[0][1] + -1000),
        1,
    )

    # Middle top right line
    line7 = pg.draw.line(
        screen,
        (100, 0, 0),
        (translated_points[7]),
        (translated_points[0][0] + 9500, translated_points[0][1] + -1000),
        1,
    )

    segment4 = [line6, line7]


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
    white: tuple[int, int, int] = (255, 240, 200)
    black: tuple[int, int, int] = (20, 20, 40)
    red: tuple[int, int, int] = (255, 0, 0)
    green: tuple[int, int, int] = (0, 255, 0)

    screen.fill(black)

    clock = pg.time.Clock()
    font = pg.font.SysFont("Arial", 18)

    # Where 1 is outside of the screen, and 0 is at the center of the screen.
    obstacle_positions: list[int] = [-1]

    # Where 0 through 7 are the segments of an octagon.
    obstacle_sections: list[int] = [-1]

    accumulated_time = 0
    total_spawned_obstacles = 0

    # main game loop
    done = 0
    while not done:
        dt = clock.tick(120)
        accumulated_time += dt

        screen.fill(black)
        offset = 40

        # if accumulated_time > (total_spawned_obstacles * 2000) + 2000:
        # create_obstacle(obstacle_positions, obstacle_sections)

        draw_octagon_in_center(screen, green, offset)

        calculate_segments(screen, offset)

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
