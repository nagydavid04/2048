
import os
import random
import pygame
pygame.init()


class Game:
    def __init__(self, size):
        self.size = size

        self.letters = "abcdefghijklmnopqrstuvwxyz123456789~!@#$%^&*()_+}{|?><:/*-"
        self.coordinates_matrix = []
        self.coordinates = []

        self.map_table = {}
        self.map_modified = {}
        for letter in self.letters[:self.size]:
            row = []
            for num in range(1, self.size + 1):
                self.map_table[f"{letter}{num}"] = False
                self.map_modified[f"{letter}{num}"] = False
                row.append(f"{letter}{num}")
                self.coordinates.append(f"{letter}{num}")
            self.coordinates_matrix.append(row)

        ## GRAFIKA
        self.rect_restart_button = pygame.Rect(0, 0, WIDTH // 8, HEIGHT // 8)

        self.rect_change_button = pygame.Rect(0, HEIGHT - 2 * HALF_HEIGHT_CHANGE_BUTTON, 2 * HALF_WIDTH_CHANGE_BUTTON, 2 * HALF_HEIGHT_CHANGE_BUTTON)

        self.rendered_texts_halfwidth_halfheight = {}

        SCORE_TEXT = FONT_BIG_TEXT.render("PONTSZÁM", True, [0, 0, 0])
        self.rendered_texts_halfwidth_halfheight["SCORE"] = [SCORE_TEXT, SCORE_TEXT.get_width() // 2,
                                                             SCORE_TEXT.get_height() // 2]

        RESTART_TEXT = FONT_SMALL_TEXT.render("ÚJRAINDÍTÁS", True, [0, 0, 0])
        self.rendered_texts_halfwidth_halfheight["RESTART"] = [RESTART_TEXT, RESTART_TEXT.get_width() // 2,
                                                               RESTART_TEXT.get_height() // 2]

        LOST_TEXT = FONT_BIG_TEXT.render("Vesztettél :(", True, [150, 20, 20])
        self.rendered_texts_halfwidth_halfheight["LOST"] = [LOST_TEXT, LOST_TEXT.get_width() // 2,
                                                               LOST_TEXT.get_height() // 2]

    def reset_map_modified(self):
        for key in list(self.map_modified.keys()):
            self.map_modified[key] = False

    def rotate_90(self, datas):
        new_datas = []
        for index in range(len(datas[0])):
            inner = []
            for row in self.coordinates_matrix[::-1]:
                inner.append(row[index])
            new_datas.append(inner)
        return new_datas

    def move_value(self, pos1, pos2):
        if self.map_table[pos1] and not self.map_table[pos2]:
            self.map_table[pos2] = self.map_table[pos1]
            self.map_table[pos1] = False
            return True
        return False

    def insert_random_num(self, nums):
        table = list(self.map_table.values())
        empty_coordinates = []

        for index, element in enumerate(table):
            if not element:
                empty_coordinates.append(self.coordinates[index])

        self.map_table[random.choice(empty_coordinates)] = random.choice(nums)

    def move_value_left(self, coord, left_coordinates):
        if len(left_coordinates) == 0:
            return True

        coord2 = left_coordinates[-1]

        if not self.move_value(coord, coord2):
            if self.map_table[coord] == self.map_table[coord2] and not self.map_modified[coord2]:
                self.map_table[coord2] = self.map_table[coord2] * 2
                self.map_table[coord] = False
                self.map_modified[coord2] = True
        else:
            self.move_value_left(coord2, left_coordinates[:-1])

    def left(self):
        map_table_copy = self.map_table.copy()
        for row in self.coordinates_matrix:
            for index, coord in enumerate(row):
                if self.map_table[coord]:
                    self.move_value_left(coord, row[:index])

        return not self.map_table == map_table_copy

    def right(self):
        map_table_copy = self.map_table.copy()
        for row in self.coordinates_matrix:
            row = row[::-1]
            for index, coord in enumerate(row):
                if self.map_table[coord]:
                    self.move_value_left(coord, row[:index])

        return not self.map_table == map_table_copy

    def up(self):
        map_table_copy = self.map_table.copy()
        for row in self.rotate_90(self.coordinates_matrix):
            row = row[::-1]
            for index, coord in enumerate(row):
                if self.map_table[coord]:
                    self.move_value_left(coord, row[:index])

        return not self.map_table == map_table_copy

    def down(self):
        map_table_copy = self.map_table.copy()
        for row in self.rotate_90(self.coordinates_matrix):
            for index, coord in enumerate(row):
                if self.map_table[coord]:
                    self.move_value_left(coord, row[:index])

        return not self.map_table == map_table_copy

    def check_loss(self):
        if False not in list(self.map_table.values()):
            for row_index, row in enumerate(self.coordinates_matrix):
                for coord_index, coord in enumerate(row):
                    val = self.map_table[coord]
                    val_next = None
                    val_down = None

                    if coord_index != self.size - 1:
                        val_next = self.map_table[row[coord_index + 1]]

                    if row_index != self.size - 1:
                        val_down = self.map_table[self.coordinates_matrix[row_index + 1][coord_index]]

                    if val_next == val or val_down == val:
                        return False

            return True

        return False

    def draw_table(self, change):
        for row_index, row in enumerate(self.coordinates_matrix, start=1):
            for coord_index, coord in enumerate(row, start=1):
                value = self.map_table[coord] if self.map_table[coord] else ""
                if value not in self.rendered_texts_halfwidth_halfheight.keys():
                    rendered_text = FONT_NUMS.render(str(value), True, [0, 0, 0])
                    half_width = rendered_text.get_width() // 2
                    half_height = rendered_text.get_height() // 2
                    self.rendered_texts_halfwidth_halfheight[value] = [rendered_text, half_width, half_height]

                if value != "":
                    if change == 1:
                        text, half_width, half_height = self.rendered_texts_halfwidth_halfheight[value]
                        screen.blit(text, (WIDTH // 2 + coord_index * WIDTH // (2 * self.size) - half_width - WIDTH // (4 * self.size), row_index * HEIGHT // self.size - half_height - HEIGHT // (2 * self.size)))
                    else:
                        screen.blit(IMAGES_WEASELS[value], (WIDTH // 2 + coord_index * WIDTH // (2 * self.size) - IMAGES_WEASELS_HALF_WIDTH - WIDTH // (4 * self.size), row_index * HEIGHT // self.size - IMAGES_WEASELS_HALF_HEIGHT - HEIGHT // (2 * self.size)))

    def draw_boxes(self):
        for col_index in range(self.size + 1):
            pygame.draw.line(screen, [0, 0, 0], [WIDTH // 2 + col_index * WIDTH // (2 * self.size), 0], [WIDTH // 2 + col_index * WIDTH // (2 * self.size), HEIGHT], 5)

        for row_index in range(self.size + 1):
            pygame.draw.line(screen, [0, 0, 0], [WIDTH // 2, row_index * HEIGHT // self.size], [WIDTH, row_index * HEIGHT // self.size], 5)

    def draw_score(self):
        text, half_width, half_height = self.rendered_texts_halfwidth_halfheight["SCORE"]
        screen.blit(text, (WIDTH // 4 - half_width, HEIGHT // 4 - half_height))

        score = 0
        for val in self.map_table.values():
            if val:
                score += val

        score_text = FONT_BIG_TEXT.render(str(score), True, [150, 20, 20])
        screen.blit(score_text, (WIDTH // 4 - score_text.get_width() // 2, HEIGHT // 2.5 - score_text.get_height()))

    def draw_restart_button(self):
        pygame.draw.rect(screen, [200, 200, 200], self.rect_restart_button)
        text, half_width, half_height = self.rendered_texts_halfwidth_halfheight["RESTART"]
        screen.blit(text, (WIDTH // 16 - half_width, HEIGHT // 16 - half_height))

    def draw_change_button(self):
        screen.blit(CHANGE_BUTTON_IMAGE, (0, HEIGHT - 2 * HALF_HEIGHT_CHANGE_BUTTON))

    def draw_motivation(self, motivation):
        text = FONT_MEDIUM_TEXT.render(motivation[1], True, [0, 0, 0])
        screen.blit(text, (WIDTH // 4 - text.get_width() // 2, HEIGHT * 0.65 - text.get_height() // 2))
        screen.blit(motivation[0], (WIDTH // 4 - IMAGES_ANIMALS_HALF_WIDTH, HEIGHT * 0.8 - IMAGES_ANIMALS_HALF_HEIGHT))

    def show_game(self, motivation, change):
        screen.fill([3, 236, 252])
        self.draw_boxes()
        self.draw_table(change)
        self.draw_score()
        self.draw_restart_button()
        self.draw_change_button()
        if motivation is not None:
            self.draw_motivation(motivation)
        pygame.display.update()

    def show_end(self):
        screen.fill([3, 236, 252])

        text, half_width, half_height = self.rendered_texts_halfwidth_halfheight["LOST"]
        screen.blit(text, (WIDTH // 2 - half_width, HEIGHT // 2 - half_height))

        pygame.display.update()

    def loop(self, change=1):
        self.insert_random_num([2, 4])
        self.insert_random_num([2])

        restart = False
        end = False

        mouse_pos = None
        mouse_pressed = False
        motivation = None
        counter = 0
        change = change
        change_pressed = False
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

            counter += 1
            if counter > FPS * 10 and motivation is None:
                animal = random.choice(ANIMALS)
                motivation = [IMAGES_ANIMALS[animal], random.choice(ANIMALS_TEXTS[animal])]
                counter = 0

            if counter > 5 * FPS and motivation is not None:
                motivation = None
                counter = 0

            is_mouse_pressed = pygame.mouse.get_pressed()[0]
            mouse_x, mouse_y = None, None
            if is_mouse_pressed:
                mouse_x, mouse_y = pygame.mouse.get_pos()

            if is_mouse_pressed and self.rect_restart_button.collidepoint(mouse_x, mouse_y):
                restart = True
                break

            if is_mouse_pressed and self.rect_change_button.collidepoint(mouse_x, mouse_y) and not change_pressed:
                change *= -1
                change_pressed = True
            elif not is_mouse_pressed and change_pressed:
                change_pressed = False

            if is_mouse_pressed and not mouse_pressed:
                mouse_pressed = True
                mouse_pos = [mouse_x, mouse_y]

            if not is_mouse_pressed and mouse_pressed:
                mouse_pressed = False
                mouse_pos2 = pygame.mouse.get_pos()

                is_vertical = abs(mouse_pos2[1] - mouse_pos[1]) > abs(mouse_pos2[0] - mouse_pos[0])

                done = False
                if mouse_pos2[1] - mouse_pos[1] < -HEIGHT // 8 and is_vertical:
                    if self.up():
                        done = True

                elif mouse_pos2[1] - mouse_pos[1] > HEIGHT // 8 and is_vertical:
                    if self.down():
                        done = True

                elif mouse_pos2[0] - mouse_pos[0] < -WIDTH // 8 and not is_vertical:
                    if self.left():
                        done = True

                elif mouse_pos2[0] - mouse_pos[0] > WIDTH // 8 and not is_vertical:
                    if self.right():
                        done = True

                mouse_pos = None

                if done:
                    self.insert_random_num([2])

                    self.reset_map_modified()

            self.show_game(motivation, change)

            if self.check_loss():
                end = True
                break

        if restart:
            pygame.time.wait(100)
            game = Game(self.size)
            game.loop(change)

        elif end:
            pygame.time.wait(3000)
            self.show_end()
            pygame.time.wait(3000)
            game = Game(self.size)
            game.loop(change)


DISPLAY_INFO = pygame.display.Info()
WIDTH, HEIGHT = DISPLAY_INFO.current_w, DISPLAY_INFO.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FPS = 60

MATRIX_SIZE = 4

FONT_NUMS = pygame.font.SysFont("couriernew", int(WIDTH // (MATRIX_SIZE * 5)), bold=True)
FONT_SMALL_TEXT = pygame.font.SysFont("couriernew", WIDTH // 60, bold=True)
FONT_MEDIUM_TEXT = pygame.font.SysFont("couriernew", WIDTH // 35, bold=True)
FONT_BIG_TEXT = pygame.font.SysFont("couriernew", WIDTH // 17, bold=True)

IMAGES_ANIMALS_HALF_WIDTH = WIDTH // 16 - WIDTH // 200
IMAGES_ANIMALS_HALF_HEIGHT = HEIGHT // 8 - HEIGHT // 200

IMAGES_WEASELS_HALF_WIDTH = WIDTH // (4 * MATRIX_SIZE) - WIDTH // 200
IMAGES_WEASELS_HALF_HEIGHT = HEIGHT // (2 * MATRIX_SIZE) - HEIGHT // 200

HALF_WIDTH_CHANGE_BUTTON = WIDTH // 20
HALF_HEIGHT_CHANGE_BUTTON = HEIGHT // 20
CHANGE_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "zsizsi.png")).convert_alpha(), (2 * HALF_WIDTH_CHANGE_BUTTON, 2 * HALF_HEIGHT_CHANGE_BUTTON))

ANIMALS_TEXTS = {"daisy": ["Juhúú", "Csak így tovább!", "Mnyau", "Morr morr"], "fifi": ["Vaff ügyes vagy!", "Kaphatok hamit?"], "boby": ["Nyaff nyaff megharaplak", "Szia!"]}
IMAGES_ANIMALS = {}
ANIMALS = ["daisy", "fifi", "boby"]
for animal in ANIMALS:
    image = pygame.image.load(os.path.join("images", f"{animal}.png")).convert_alpha()
    IMAGES_ANIMALS[animal] = pygame.transform.scale(image, (2 * IMAGES_ANIMALS_HALF_WIDTH, 2 * IMAGES_ANIMALS_HALF_HEIGHT))

IMAGES_WEASELS = {}
for i in range(1, 12):
    image = pygame.image.load(os.path.join("images", f"menyet{2**i}.png")).convert_alpha()
    IMAGES_WEASELS[2**i] = pygame.transform.scale(image, (2 * IMAGES_WEASELS_HALF_WIDTH, 2 * IMAGES_WEASELS_HALF_HEIGHT))

game = Game(MATRIX_SIZE)
game.loop()


