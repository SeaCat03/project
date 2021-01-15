import pygame
from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576


def main():
    # Инициализировать все импортированные модули pygame
    pygame.init()
    # Установиливаем ширину и высоту экрана [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-Man")
    # Окно открыто до тех пор, пока пользователь не нажмет кнопку закрытия.
    done = False
    clock = pygame.time.Clock()
    # Создание игрового объекта
    game = Game()

    # --- Основной Цикл Программы ---
    while not done:
        # События процесса (нажатия клавиш, щелчки мыши и т.д.)
        done = game.process_events()
        # Игровая логика
        game.run_logic()
        # Текущий экран
        game.display_frame(screen)
        # Ограничение до 30 кадров
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
