import os
import sys
import pygame


class Tile(pygame.sprite.Sprite):
    spisok = []

    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'wall':
            Tile.spisok += [(pos_x, pos_y)]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x + 15
        self.rect.y = tile_height * pos_y + 5

    def update(self, mod):
        if mod == 1:
            i = get_cell((self.rect.x, self.rect.y - 50))
            if i not in Tile.spisok:
                self.rect.y -= 50
        elif mod == 2:
            i = get_cell((self.rect.x, self.rect.y + 50))
            if i not in Tile.spisok:
                self.rect.y += 50
        elif mod == 3:
            i = get_cell((self.rect.x + 50, self.rect.y))
            if i not in Tile.spisok:
                self.rect.x += 50
        elif mod == 4:
            i = get_cell((self.rect.x - 50, self.rect.y))
            if i not in Tile.spisok:
                self.rect.x -= 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    if os.path.isfile(filename) is False:
        print('Nevernui format vvoda')
        terminate()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def get_cell(pos):
    x, y = pos
    x = x // 50
    y = y // 50
    return (x, y)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    FPS = 50
    clock = pygame.time.Clock()
    start_screen()
    tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
    player_image = load_image('mar.png')
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player, level_x, level_y = generate_level(load_level(input()))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_UP]:
                    player_group.update(1)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    player_group.update(2)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    player_group.update(3)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    player_group.update(4)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
