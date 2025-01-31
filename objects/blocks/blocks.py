import pygame

from objects.blocks._block import Block


class BlockBlue(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "blue", x, y, 2)


class BlockCyan(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "cyan", x, y, 2)


class BlockGold(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "gold", x, y, 4)


class BlockGreen(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "green", x, y)


class BlockOrange(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "orange", x, y)


class BlockPink(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "pink", x, y)


class BlockRed(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "red", x, y)


class BlockSilver(Block):
    def __init__(self, screen: pygame.surface.Surface, x: float, y: float):
        super().__init__(screen, "silver", x, y, 3)
