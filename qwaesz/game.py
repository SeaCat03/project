import pygame
from player import Player
from enemies import Block, Ellipse, Slime, enviroment, draw_enviroment

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Game(object):
    def __init__(self):
        self.about = False
        self.game_over = True
        # Создаём переменную для счета
        self.score = 0
        # Создаём шрифт
        self.font = pygame.font.Font(None, 35)
        # Создаём меню игры
        self.menu = Menu(("Начать игру", "Об игре", "Выход"), font_color=WHITE, font_size=60)
        # Создаём Пакмaна
        self.player = Player(30, 120, "player.png")
        # Создаём блоки, которые будут задавать путь, по которым двигается Пакмaн
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        self.dots_group = pygame.sprite.Group()

        # Рисуем окружвющую среду:
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j * 32 + 8, i * 32 + 8, BLACK, 16, 16))

        # Создаём врагов
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(160, 32, 2, 0))  # 1
        self.enemies.add(Slime(320, 96, 0, 2))  # 2
        self.enemies.add(Slime(448, 32, -2, 0))  # 3
        self.enemies.add(Slime(544, 128, 0, 2))  # 4
        self.enemies.add(Slime(32, 224, 0, 2))  # 5
        self.enemies.add(Slime(320, 320, 0, -2))  # 6
        self.enemies.add(Slime(448, 320, 2, 0))  # 7
        self.enemies.add(Slime(640, 480, 2, 0))  # 8

        # Добавляем еду
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j * 32 + 12, i * 32 + 12, WHITE, 8, 8))

        # Загружаем звуковые эффекты
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.pacman_death_sound = pygame.mixer.Sound("pacman_death.ogg")

    def process_events(self):
        for event in pygame.event.get():  # Инициализируем действия пользователя
            if event.type == pygame.QUIT:  # Если пользователь нажал закрыть
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:

                            # Начать игру
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:

                            #  О игре
                            self.about = True
                        elif self.menu.state == 2:

                            # Пользователь нажал кнопку Выход
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True

        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks, self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)

            # Когда block_hit_list содержит один спрайт, это означает, что игрок попал в точку
            if len(block_hit_list) > 0:
                # Звуковой эффект
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.pacman_death_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

    def display_frame(self, screen):

        # Код рисования окружающей среды меню
        if self.game_over:
            fon = pygame.transform.scale(load_image('fon.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(fon, (0, 0))
            if self.about:
                # Правила
                self.display_message(screen, ["ЧАВО:", "", "Экран игры занимает собой лабиринт,",
                                              "коридоры которого заполнены точками.",
                                              " Задача игрока — управляя Пакманом,", "съесть все точки в лабиринте,",
                                              "избегая встречи с привидениями,",
                                              "которые гоняются за героем."])
            else:
                self.menu.display_frame(screen)
        else:
            # --- Начало игры ---
            fon = pygame.transform.scale(load_image('empty.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(fon, (0, 0))
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            if self.score < 156:
                # Текст счета очков
                text = self.font.render("Очков: " + str(self.score), True, WHITE)
                screen.blit(text, [600, 545])
            if self.score > 155:
                # Текст при наборе макс.балла
                text1 = self.font.render("Вы победили, открыт режим хождения просто так", True, WHITE)
                screen.blit(text1, [100, 545])

        pygame.display.flip()

    def display_message(self, screen, message, color=(255, 255, 255)):
        hei = 50
        for x in message:
            label = self.font.render(x, True, color)
            # Получаем ширину и высоту
            width = label.get_width()
            height = label.get_height()
            # Определяем положение текста
            posX = (SCREEN_WIDTH / 2) - (width / 2)
            posY = ((SCREEN_HEIGHT - hei) / len(message)) * (message.index(x) + 1) - (height / 2)
            # Рисуем положение текста
            screen.blit(label, (posX, posY))


class Menu(object):
    state = 0

    def __init__(self, items, font_color=(0, 0, 0), select_color=(255, 0, 0), ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            # Получаем положение персонажа
            width = label.get_width()
            height = label.get_height()
            posX = (SCREEN_WIDTH / 2) - (width / 2)
            # Общая высота текстового блока
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            screen.blit(label, (posX, posY))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
