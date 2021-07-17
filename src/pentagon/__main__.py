#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The entrypoint for both poetry and Nuitka
"""


def talk(message):
    return "Talk " + message


def main():
    print(talk("Hello World"))


if __name__ == "__main__":
    main()
