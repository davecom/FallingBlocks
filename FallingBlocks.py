# FallingBlocks.py
# A simple puzzle game implemented using the Arcade library in Python.
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
import arcade
import arcade.color
import arcade.key
from copy import deepcopy
from Pieces import Piece
from Util import Location, Cell


class FallingBlocks(arcade.Window):
    # CONSTANTS
    # Window Setup
    WIDTH = 600
    HEIGHT = 600
    TITLE = "Falling Blocks"
    BACKGROUND_COLOR = arcade.color.BLACK
    # Cell Setup
    COLUMNS = 10
    ROWS = 20
    CELL_WIDTH = WIDTH / 2 / COLUMNS
    CELL_HEIGHT = HEIGHT / ROWS
    EMPTY_CELL_COLOR = arcade.color.BEIGE
    BLOCKED_CELL_COLOR = arcade.color.BLUE
    # Piece Setup
    START_LOCATION = Location(ROWS - 2, COLUMNS // 2 - 2)
    # Scoring by number of lines
    SCORING = [0, 10, 25, 75, 300]
    LINES_PER_LEVEL = 10

    def __init__(self):
        super().__init__(self.WIDTH, self.HEIGHT, self.TITLE)
        arcade.set_background_color(self.BACKGROUND_COLOR)
        # Fill with a grid of empty cells
        self._grid: list[list[Cell]] = [[Cell.EMPTY for _ in range(self.COLUMNS)]
                                        for _ in range(self.ROWS)]
        # Generate pieces
        self._next_piece = Piece.random(deepcopy(self.START_LOCATION))
        self._generate_pieces()
        # Setup statistics
        self._level = 1
        self._lines = 0
        self._score = 0
        self._gameover = False
        # Schedule game play update interval, no smaller than 0.1 seconds
        arcade.schedule(self._down, max(1 - self._level * .1, 0.1))

    def _generate_pieces(self) -> None:
        self._piece = self._next_piece
        self._next_piece = Piece.random(deepcopy(self.START_LOCATION))

    def on_draw(self):
        # Must be called before drawing anything
        arcade.start_render()
        # Draw grid
        # Play area rectangle
        arcade.draw_xywh_rectangle_filled(0, 0, self.WIDTH / 2, self.HEIGHT, self.EMPTY_CELL_COLOR)
        # Rectangles for each blocked cell
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                if self._grid[row][col] is Cell.BLOCK:
                    arcade.draw_xywh_rectangle_filled(col * self.CELL_WIDTH, row * self.CELL_HEIGHT,
                                                      self.CELL_WIDTH, self.CELL_HEIGHT, self.BLOCKED_CELL_COLOR)
        # Draw piece
        for location in self._piece.grid_locations:
            arcade.draw_xywh_rectangle_filled(location.column * self.CELL_WIDTH, location.row * self.CELL_HEIGHT,
                                              self.CELL_WIDTH, self.CELL_HEIGHT, self._piece.color)
        # Draw next piece and score
        self._draw_info()

    def _draw_info(self) -> None:
        # Draw Next Piece
        arcade.draw_text("Next Piece", self.WIDTH / 2, self.HEIGHT - self.HEIGHT / 8, arcade.color.WHITE, 18,
                         self.WIDTH // 2, "center")
        for row in range(len(self._next_piece.position)):
            for col in range(len(self._next_piece.position[0])):
                cell = self._next_piece.position[row][col]
                if cell is Cell.BLOCK:
                    arcade.draw_xywh_rectangle_filled(col * self.CELL_WIDTH + self.WIDTH / 2 + self.WIDTH / 6,
                                                      row * self.CELL_HEIGHT + self.HEIGHT / 8 * 5,
                                                      self.CELL_WIDTH, self.CELL_HEIGHT, self._next_piece.color)
        # Draw stats
        arcade.draw_text("Level\n" + str(self._level), self.WIDTH / 2, self.HEIGHT / 8 * 4,
                         arcade.color.WHITE, 18,
                         self.WIDTH // 2, "center")
        arcade.draw_text("Lines\n" + str(self._lines), self.WIDTH / 2, self.HEIGHT / 8 * 3,
                         arcade.color.WHITE, 18,
                         self.WIDTH // 2, "center")
        arcade.draw_text("Score\n" + str(self._score), self.WIDTH / 2, self.HEIGHT / 8 * 2,
                         arcade.color.WHITE, 18,
                         self.WIDTH // 2, "center")
        if self._gameover:
            arcade.draw_text("Game Over", 0, self.HEIGHT / 2,
                             arcade.color.WHITE, 32,
                             self.WIDTH // 2, "center")

    def _invalid(self) -> bool:
        """Is this an invalid game state?"""
        # Check if the piece overlaps any of the blocked cells
        for location in self._piece.grid_locations:
            if location.row < 0:
                return True
            if location.column < 0:
                return True
            if location.column >= self.COLUMNS:
                return True
            # Order matters, we must not go "off the grid" so we check too far left, right or down first
            try:
                if self._grid[location.row][location.column] is Cell.BLOCK:
                    return True
            except IndexError:  # Ignore if we're off grid too high up
                continue
        return False

    def _down(self, dt: float) -> None:
        self._piece.move_down()
        # If we hit the bottom, undo and go to next piece
        if self._invalid():
            self._piece.move_up()  # Undo
            # Transfer pieces to grid
            for location in self._piece.grid_locations:
                try:
                    self._grid[location.row][location.column] = Cell.BLOCK
                except IndexError:  # Ignore if we're off grid too high up
                    continue
            # Change over to next piece
            self._generate_pieces()
            # If immediately after we generate the piece we are invalid, then we lost
            if self._invalid():
                arcade.unschedule(self._down)
                self._gameover = True
            # Check for newly completed lines
            self._check_lines()

    def _check_lines(self) -> None:
        """Remove completed lines."""
        # Go from bottom up, finding lines that are full or should be removed
        indices_for_removal: list[int] = []
        for index, row in enumerate(self._grid):
            if all(cell is Cell.BLOCK for cell in row):
                indices_for_removal.append(index)
        # Remove each line that should be removed and add a blank line to top of grid
        # Must remove from the top down so subsequent indices are still correct
        for index in reversed(indices_for_removal):
            del self._grid[index]
            self._grid.append([Cell.EMPTY] * self.COLUMNS)
        # Update statistics
        lines_cleared = len(indices_for_removal)
        if lines_cleared > 0:
            self._lines += lines_cleared
            self._score += self.SCORING[lines_cleared] * self._level
            old_level = self._level
            self._level = (self._lines // self.LINES_PER_LEVEL) + 1
            if old_level != self._level:  # reschedule if level changed
                arcade.unschedule(self._down)
                arcade.schedule(self._down, max(1 - self._level * .1, 0.1))

    def on_key_press(self, symbol: int, modifiers: int):
        # Try to do what the user asks, but if it puts us in an
        # invalid state, then undo it
        if symbol == arcade.key.A or symbol == arcade.key.LEFT:  # move left
            self._piece.move_left()
            if self._invalid():
                self._piece.move_right()
        elif symbol == arcade.key.D or symbol == arcade.key.RIGHT:  # move right
            self._piece.move_right()
            if self._invalid():
                self._piece.move_left()
        elif symbol == arcade.key.S or symbol == arcade.key.DOWN:  # rotate right
            self._piece.rotate_right()
            if self._invalid():
                self._piece.rotate_left()
        elif symbol == arcade.key.W or symbol == arcade.key.UP:  # rotate left
            self._piece.rotate_left()
            if self._invalid():
                self._piece.rotate_right()
        elif symbol == arcade.key.SPACE:  # straight down
            while True:
                self._piece.move_down()
                if self._invalid():
                    self._piece.move_up()
                    break


if __name__ == "__main__":
    fb = FallingBlocks()
    arcade.run()
