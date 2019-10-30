import json

from pygame.sprite import Group

from library.collidables.brick import Brick
from library.collidables.dead_block import DeadBlock
from library.collidables.item_block import ItemBlock
from library.collidables.terrain import Terrain
from library.collidables.stairs import Stairs
from library.entities.enemies.koopa import Koopa
from library.entities.enemies.goomba import Goomba
from library.background import Background


class Level:
    """Handles the images and positions of assets."""

    def __init__(self, settings, screen, data):
        self.settings = settings
        self.screen = screen

        # Load data
        with open(data) as data_f:
            self.data = json.load(data_f)

        # Load sprite groups
        self.blocks = self.load_blocks()
        self.terrain = self.load_terrain()
        self.terrain.add(self.blocks)
        self.enemies = self.load_enemies()

        self.background = Background(settings, screen, self.data["background"])

    def load_terrain(self):
        """Loads terrain sprites."""
        terrain = Group()
        # Pipes
        for i in range(self.data["pipe"]["count"]):
            position = self.data["pipe"]["position"][i]
            pipe = Terrain(self.settings, self.screen, self.data["pipe"]["image"], position)
            terrain.add(pipe)
        # Down stairs; L shape
        stairs = Stairs(self.settings, self.screen, self.data["down_stairs"], 1)
        terrain.add(stairs.blocks)
        # Up stairs; flipped L shape
        stairs = Stairs(self.settings, self.screen, self.data["up_stairs"], -1)
        terrain.add(stairs.blocks)
        # Castle
        position = self.data["castle"]
        castle = Terrain(self.settings, self.screen, "resources/images/castle.png", position)
        terrain.add(castle)
        # TODO: maybe combine flag and flag_pole
        # Flag pole
        position = self.data["flag_pole"]
        pole = Terrain(self.settings, self.screen, "resources/images/flag_pole.png", position)
        terrain.add(pole)
        # Flag
        position = self.data["flag"]
        flag = Terrain(self.settings, self.screen, "resources/images/flag.png", position)
        terrain.add(flag)
        # Ground
        for i in range(self.data["ground"]["count"]):
            image_name = self.data["ground"]["image"][i]
            position = self.data["ground"]["position"][i]
            ground = Terrain(self.settings, self.screen, image_name, position)
            terrain.add(ground)
        return terrain

    def load_enemies(self):
        """Loads enemy sprites."""
        enemies = Group()
        # Goomba's
        for i in range(self.data["goomba"]["count"]):
            position = self.data["goomba"]["position"][i]
            goomba = Goomba(self.settings, self.screen, position)
            enemies.add(goomba)
        # Koopa's
        for i in range(self.data["koopa"]["count"]):
            position = self.data["koopa"]["position"][i]
            koopa = Koopa(self.settings, self.screen, position)
            enemies.add(koopa)
        return enemies

    def load_blocks(self):
        """Loads block sprites."""
        blocks = Group()
        # Yellow ? blocks
        for i in range(self.data["yellow"]["count"]):
            position = self.data["yellow"]["position"][i]
            block = ItemBlock(self.settings, self.screen, position)
            blocks.add(block)
        # Bricks
        for i in range(self.data["brick"]["count"]):
            position = self.data["brick"]["position"][i]
            block = Brick(self.settings, self.screen, position)
            blocks.add(block)
        # Dead blocks
        for i in range(self.data["block"]["count"]):
            position = self.data["block"]["position"][i]
            block = DeadBlock(self.settings, self.screen, position)
            blocks.add(block)
        return blocks

    def update(self, scrolling):
        """Scrolls all objects in the level, excluding Mario."""
        if scrolling:
            self.background.update()
            for terrain in self.terrain.sprites():
                terrain.update()
        self.enemies.update(self, scrolling)

    def draw(self):
        """Draws all objects in the level, excluding Mario."""
        self.background.draw()
        for terrain in self.terrain.sprites():
            terrain.draw()
        for enemy in self.enemies.sprites():
            enemy.draw()
