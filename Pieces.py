# Pieces.py
# Different kinds of game pieces
# Copyright 2020 David Kopec
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>
from __future__ import annotations
import arcade
import arcade.color
from Util import Cell, Location
import random

# Aliases to make the rest of this file more readable
Position = list[list[Cell]]
E = Cell.EMPTY
B = Cell.BLOCK


class Piece:
    def __init__(self, positions: list[Position], color: tuple[int, int, int], location: Location):
        self._positions: list[Position] = positions
        self._color = color
        self._position_index = 0
        self._location = location

    def rotate_right(self) -> None:
        self._position_index = (self._position_index + 1) % len(self._positions)

    def rotate_left(self) -> None:
        self._position_index = (self._position_index - 1) % len(self._positions)

    def move_right(self):
        self._location.column += 1

    def move_left(self):
        self._location.column -= 1

    def move_down(self):
        self._location.row -= 1

    def move_up(self):
        self._location.row += 1

    @property
    def color(self) -> tuple[int, int, int]:
        return self._color

    @property
    def position(self) -> Position:
        return self._positions[self._position_index]

    @property
    def grid_locations(self) -> list[Location]:
        locations = []
        for row in range(len(self.position)):
            for col in range(len(self.position[0])):
                cell = self.position[row][col]
                if cell is Cell.BLOCK:
                    locations.append(Location(row + self._location.row,
                                              col + self._location.column))
        return locations

    @staticmethod
    def random(location: Location) -> Piece:
        """Get a random piece."""
        possible_pieces = (I, O, J, L, S, T, Z)
        return random.choice(possible_pieces)(location)


class I(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E, E],
                     [E, E, E, E],
                     [B, B, B, B],
                     [E, E, E, E]]

        position1 = [[E, E, B, E],
                     [E, E, B, E],
                     [E, E, B, E],
                     [E, E, B, E]]

        positions = [position0, position1]

        super().__init__(positions, arcade.color.AMBER, location)


class O(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E, E],
                     [E, B, B, E],
                     [E, B, B, E],
                     [E, E, E, E]]

        positions = [position0]

        super().__init__(positions, arcade.color.RED, location)


class J(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E],
                     [B, B, B],
                     [E, E, B]]

        position1 = [[E, B, E],
                     [E, B, E],
                     [B, B, E]]

        position2 = [[B, E, E],
                     [B, B, B],
                     [E, E, E]]

        position3 = [[E, B, B],
                     [E, B, E],
                     [E, B, E]]

        positions = [position0, position1, position2, position3]

        super().__init__(positions, arcade.color.ALMOND, location)


class L(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E],
                     [B, B, B],
                     [B, E, E]]

        position1 = [[B, B, E],
                     [E, B, E],
                     [E, B, E]]

        position2 = [[E, E, B],
                     [B, B, B],
                     [E, E, E]]

        position3 = [[E, B, E],
                     [E, B, E],
                     [E, B, B]]

        positions = [position0, position1, position2, position3]

        super().__init__(positions, arcade.color.INDIGO, location)


class S(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E],
                     [E, B, B],
                     [B, B, E]]

        position1 = [[E, B, E],
                     [E, B, B],
                     [E, E, B]]

        positions = [position0, position1]

        super().__init__(positions, arcade.color.AQUA, location)


class T(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E],
                     [B, B, B],
                     [E, B, E]]

        position1 = [[E, B, E],
                     [B, B, E],
                     [E, B, E]]

        position2 = [[E, B, E],
                     [B, B, B],
                     [E, E, E]]

        position3 = [[E, B, E],
                     [E, B, B],
                     [E, B, E]]

        positions = [position0, position1, position2, position3]

        super().__init__(positions, arcade.color.EUCALYPTUS, location)


class Z(Piece):
    def __init__(self, location: Location):
        position0 = [[E, E, E],
                     [B, B, E],
                     [E, B, B]]

        position1 = [[E, E, B],
                     [E, B, B],
                     [E, B, E]]

        positions = [position0, position1]

        super().__init__(positions, arcade.color.GRAY, location)
