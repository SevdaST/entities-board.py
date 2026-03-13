"""
Reusable board system for a memory matching game.

This class is responsible for:
- validating board dimensions
- calculating a centered grid
- generating card positions
- creating shuffled matching pairs
- creating Card objects
"""

import random
import pygame

from entities.card import Card


class Board:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        rows: int,
        cols: int,
        margin: int = 40,
        spacing: int = 10,
    ):
        """
        Create a new board.

        screen_width  -> width of the game window
        screen_height -> height of the game window
        rows          -> number of rows
        cols          -> number of columns
        margin        -> distance from screen edges
        spacing       -> distance between cards
        """

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rows = rows
        self.cols = cols

        self.margin = margin
        self.spacing = spacing

        # Validate board size
        self._validate_dimensions()

        # Layout values
        self.cell_size = 0
        self.start_x = 0
        self.start_y = 0

        # Containers
        self.cells = []
        self.cards = []

        # Build the board
        self._calculate_layout()
        self._create_cells()
        self._create_cards()

    def _validate_dimensions(self) -> None:
        """
        Ensure the board can be used in a memory game.

        A memory game must contain an even number of cells
        because cards are created in matching pairs.
        """

        total_cells = self.rows * self.cols

        if total_cells <= 0:
            raise ValueError("Board dimensions must be positive.")

        if total_cells % 2 != 0:
            raise ValueError(
                "Board must contain an even number of cells for matching pairs."
            )

    def _calculate_layout(self) -> None:
        """
        Calculate cell size and the starting position of the centered grid.
        """

        usable_width = self.screen_width - (2 * self.margin)
        usable_height = self.screen_height - (2 * self.margin)

        max_cell_width = (
            usable_width - (self.cols - 1) * self.spacing
        ) // self.cols

        max_cell_height = (
            usable_height - (self.rows - 1) * self.spacing
        ) // self.rows

        # Keep each card square
        self.cell_size = min(max_cell_width, max_cell_height)

        grid_width = self.cols * self.cell_size + (self.cols - 1) * self.spacing
        grid_height = self.rows * self.cell_size + (self.rows - 1) * self.spacing

        # Center the grid on the screen
        self.start_x = (self.screen_width - grid_width) // 2
        self.start_y = (self.screen_height - grid_height) // 2

    def _create_cells(self) -> None:
        """
        Create pygame.Rect objects for every board cell.
        """

        self.cells.clear()

        for row in range(self.rows):
            for col in range(self.cols):
                x = self.start_x + col * (self.cell_size + self.spacing)
                y = self.start_y + row * (self.cell_size + self.spacing)

                rect = pygame.Rect(
                    x,
                    y,
                    self.cell_size,
                    self.cell_size,
                )

                self.cells.append(rect)

    def _generate_card_values(self) -> list[int]:
        """
        Generate shuffled matching pairs.

        Example:
        [1, 1, 2, 2, 3, 3, 4, 4]
        """

        total_cards = self.rows * self.cols
        pair_count = total_cards // 2

        values = []

        for value in range(1, pair_count + 1):
            values.append(value)
            values.append(value)

        random.shuffle(values)
        return values

    def _create_cards(self) -> None:
        """
        Create Card objects using generated values and cell positions.
        """

        self.cards.clear()

        values = self._generate_card_values()

        for rect, value in zip(self.cells, values):
            card = Card(value=value, rect=rect)
            self.cards.append(card)

    def rebuild(self) -> None:
        """
        Rebuild the board with the current dimensions.

        Useful for restarting the current level.
        """

        self._calculate_layout()
        self._create_cells()
        self._create_cards()

    def resize(self, rows: int, cols: int) -> None:
        """
        Change board size and rebuild the board.
        """

        self.rows = rows
        self.cols = cols

        self._validate_dimensions()
        self.rebuild()

    def draw_cards(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """
        Draw all cards on the board.
        """

        for card in self.cards:
            card.draw(screen, font)

    def draw_debug(self, screen: pygame.Surface) -> None:
        """
        Draw the grid rectangles for debugging layout.
        """

        for rect in self.cells:
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)

    def get_card_at_pos(self, pos: tuple[int, int]):
        """
        Return the clicked card if the mouse position is inside a card.
        Otherwise return None.
        """

        for card in self.cards:
            if card.contains_point(pos):
                return card

        return None

    def all_cards_matched(self) -> bool:
        """
        Return True if every card is matched.
        """

        for card in self.cards:
            if not card.is_matched:
                return False

        return True

    def get_dimensions(self) -> tuple[int, int]:
        """
        Return board size as (rows, cols).
        """

        return self.rows, self.cols
